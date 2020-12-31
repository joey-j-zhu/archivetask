# archivetask

The given code essentially gives us the HTML, CSS, and JavaScript of raw pages, which include a lot of boilerplate and delimiters that we can parse out. Some quick searching shows that BeautifulSoup (bs4) and HTML5Lib appear to be the libraries I'm looking for in order to do this. 

After this, we've distilled the problem into matching up sequences of strings. I do have brute-force methods like keyword searches at my disposal; a straightforward solution would just be to give each page a score based on how well it matched a list of keywords, and sort them and take the best ones.

Step 1: Hardcode the keywords, and brute-force count their occurrences in each page. 

To make it faster, we can switch to trie-based keyword searching. The stuff inside HTML and CSS delimiters will have no relevance with our keywords so we can also get rid of them when detecting.


However, it would be very helpful to learn a list of keywords rather than hardcode them in. This would be prone to picking up articles that just happen to have keywords like "Vaccine" and "IRS" in totally irrelevant contexts. NLP and unsupervised ML may have to be leveraged to efficiently solve such problems. I haven't formally learned the go-to algorithms, but I can at least imitate the approaches. 



Subproblem: How can we appropriately expand our set of new keywords?

Solution: Look for words that show up in high-scoring sites but not in low-scoring sites and add them to the list of keywords

Caveat: new keywords might deviate from the original set, to the point where we are high-scoring irrelevant articles about other viruses or something.


Subproblem: How can we make use of speech patterns to filter out pages with keywords that aren't actually correlated?

This subproblem also led me to consider categorizing the keywords themselves, probably on whether they're relevant to COVID-19, the economy, or neither. This greatly simplifies the dimensions and gives us more tools to work with.

Viterbi Algorithm: we can look for keyword-dense sections and boil those down to Markov chains 
so we can run Viterbi on occurrences of these keywords to see 







