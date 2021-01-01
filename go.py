from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys
import wget
from bs4 import BeautifulSoup
import keyword_search as ks
import html5lib

prefix = "s3://commoncrawl/crawl-data/CC-MAIN-2020-05"

entries = 0
matching_entries = 0
hits = 0

file_name = "http://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-30/segments/1563195523840.34/warc/CC-MAIN-20190715175205-20190715200159-00000.warc.gz"

covid_keywords = ks.make_trie("COVID-19", "coronavirus", "pandemic", "WHO", "CDC")
econ_keywords = ks.make_trie("IRS", "economy", "recession", "stocks")

# I entered these paths the way CommonCrawl instructed, but for some reason they are simply not working
paths = [
    "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-16/segment.paths.gz"
    # Other paths for other months below this
]

# January and February are last because coronavirus began spiking in March and we want to search that first
months = [
    "March/April",
    "May/June",
    "July",
    "August",
    "September",
    "October",
    "November/December",
    "Jan",
    "Feb",
]

def make_stream(path):
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    stream = None
    if path.startswith("http://") or path.startswith(
        "https://"
    ):
        stream = requests.get(path, stream=True).raw
    else:
        stream = open(path, "rb")
    return stream

def clean(body):
    return ks.remove_delimiters(ks.remove_delimiters(body, "{", "}"), "<", ">")

# Return from an ArchiveIterator stream
def scrape(stream, bailout=-1):
    candidates = []
    i = 0
    for record in ArchiveIterator(stream):
        if i == bailout:
            break
        if record.rec_type == "warcinfo":
            continue

        if not ".com/" in record.rec_headers.get_header(
            "WARC-Target-URI"
        ):
            continue

        # Data is read and decoded
        contents = (
            record.content_stream()
            .read()
            .decode("utf-8", "replace")
        )
        # Data is cleaned
        soup = BeautifulSoup(contents, "html5lib")
        body = clean(contents)
        # print(body)

        if body != "":
            # Data is read and scored
            covid_score = ks.scan(body, covid_keywords)
            econ_score = ks.scan(body, econ_keywords)
            correlation_score = 0

            # This is where we decide whether the page is good or not. Right now it's just a simple count of
            # how many times covid and econ keywords popped up
            if covid_score > 1 and econ_score > 1:
                candidates.append(record)
                print(record.rec_headers.get_header("WARC-Target-URI"))
                # print(covid_score, econ_score)
    return candidates


#for i, path in enumerate(paths):
 #   print(months[i] + ":")
  #  sites = scrape(make_stream(path))
   # print(sites)


# Just to show that this program works, you can run the code below instead. Also throw in keywords that would have
# popped up in 2019 rather than 2020 (and uncomment lines 92 and 93)
# sites = scrape(make_stream(file_name))