# A quick trie and keyword-search module to be used in the main file

_end = '_end_'

def make_trie(*words):
    root = dict()
    for word in words:
        curr = root
        for letter in word:
            curr = curr.setdefault(letter, {})
        curr[_end] = _end
    return root

def add_to_trie(root, *words):
    for word in words:
        curr = root
        for letter in word:
            curr = curr.setdefault(letter, {})
        curr[_end] = _end
    return root

def in_trie(trie, word):
    curr = trie
    for letter in word:
        if letter not in curr:
            return False
        curr = curr[letter]
    return _end in curr

def scan(body, trie):
    curr = trie
    counter = 0
    for i, letter in enumerate(body):
        if letter not in curr:
            curr = trie
        else:
            curr = curr[letter]
        if _end in curr:
            counter += 1
            curr = trie
    return counter

print(scan("the quick fox jumps over the lazy dog", make_trie("fox", "og", "o")))

print(scan("dadadadadadadadadadad", make_trie("ad", "da")))


