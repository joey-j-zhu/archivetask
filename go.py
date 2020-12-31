from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys
import wget
from bs4 import BeautifulSoup
import keyword_search as ks
import html5lib

regex = re.compile(
    "(youtu\.be/|youtube\.com/(watch\?(.*\&)?v=|(embed|v)/))([^?&\"'>]+)"
)

entries = 0
matching_entries = 0
hits = 0

file_name = "http://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-30/segments/1563195523840.34/warc/CC-MAIN-20190715175205-20190715200159-00000.warc.gz"

if len(sys.argv) > 1:
    file_name = sys.argv[1]

stream = None
print("test")
if file_name.startswith("http://") or file_name.startswith(
    "https://"
):
    stream = requests.get(file_name, stream=True).raw
else:
    stream = open(file_name, "rb")


#Main loop
# The stream object could be a file on disk or a remote network stream.
# The ArchiveIterator reads the WARC content in a single pass. The record
# is represented by an ArcWarcRecord object which contains the format
# (ARC or WARC), record type, the record headers, http headers (if any),
# and raw stream for reading the payload.

for record in ArchiveIterator(stream):
    if record.rec_type == "warcinfo":
        continue

    if not ".com/" in record.rec_headers.get_header(
        "WARC-Target-URI"
    ):
        continue

    entries = entries + 1
    #Processing happens right here

    contents = (
        record.content_stream()
        .read()
        .decode("utf-8", "replace")
    )
    soup = BeautifulSoup(contents, "html5lib")
    #print(soup.find_all('body'))

    score = 0
    covid_keywords = ["COVID-19", "coronavirus", "<"]
    econ_keywords = ["IRS", "economy"]

    # Improve this search to a trie-based search if/when needed
    # Do a pre-processing to clean out of very common words and delimiters if/when needed
    body = soup.find_all('b')
    for keyword in covid_keywords + econ_keywords:
        if keyword in body:
            score += 1
    print(score)

    #print(soup)

    # Contents are the HTML file itself. We can parse out all the delimiters and CSS and extract the actual data

    m = regex.search(contents)
    if m:
        matching_entries = matching_entries + 1
        hits = hits + 1
        m = regex.search(contents, m.end())
    while m:
        m = regex.search(contents, m.end())
        hits = hits + 1

print(
    "Python: "
    + str(hits)
    + " matches in "
    + str(matching_entries)
    + "/"
    + str(entries)
)