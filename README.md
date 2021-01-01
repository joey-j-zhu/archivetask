# archivetask

So for this project I'm only going to be concerning articles of the English alphabet.


Planning naive, functioning solution

The given code essentially gives us the HTML, CSS, and JavaScript of raw pages, which include a lot of boilerplate and delimiters that we can parse out. Some quick searching shows that BeautifulSoup (bs4) and HTML5Lib appear to be the libraries I'm looking for in order to do this. 

After this, we've distilled the problem into matching up sequences of strings. I do have brute-force methods like keyword searches at my disposal; a straightforward solution would just be to give each page a score based on how well it matched a list of keywords, and sort them and take the best ones.

Step 1: Hardcode the keywords, and brute-force count their occurrences in each page. 

To make it faster, we can switch to trie-based keyword searching. The stuff inside HTML and CSS delimiters will have no relevance with our keywords so we can also get rid of them when detecting.

I've opted to just directly read the raw webpages rather than pass them into BeautifulSoup just so I have more direct leverage over what's actually going on in the file.


Planning keyword updating scheme

It would be very helpful to learn a list of keywords rather than hardcode them in. This would be prone to picking up articles that just happen to have keywords like "Vaccine" and "IRS" in totally irrelevant contexts. NLP and unsupervised ML may have to be leveraged to efficiently solve such problems. I haven't formally learned the go-to algorithms of ML, but I can at least imitate the approaches.

Stick with handpicked keywords:
  Put a heuristic on more central keywords. We can attach a number on each leaf of the trie, such that lower numbers indicate words with less relevance. 
  If we have a fixed group of handpicked keywords, we can run multiplicative weight update and seeing what words appeared in high or low-scoring pages.

The computer learns new keywords:
  Find two high-scoring URLs and cross-reference them to find new keywords. This can possibly be done by loading words from one document onto a trie (and possibly   filter out common words to keep the trie small), and comparing that trie against the other document, which is still roughly linear provided the words don't get
  horribly long.  
  Actually, this can be used in tandem with the idea above; just initialize new words with a low number


Planning correlation/pattern detecting scheme

So another way to simplify such a problem would be boil each word into one of three states: a coronavirus-related keyword, an economy-related keyword, or neither. Then we can find keyword-heavy areas within the page and create a corresponding hidden Markov chain using the Viterbi Algorithm. This way, we can classify which passages are actually talking about coronavirus and economics in tandem (larger weights between the first two states), versus which passages just mention them in separate contexts.


So I didn't get the time to implement everything or fix all my bugs, but I've laid out adequate structure and helper functions that executing my plans should be straightforward.



