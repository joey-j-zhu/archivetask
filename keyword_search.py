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

# Count the number of times a word in the trie is found in a body text
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

# Iterate through a body text word by word, separated by spaces
def parse(body, delimiter=''):
    string = ""
    i = 0
    for i, letter in enumerate(body):
        if letter == delimiter:
            yield string
            string = ""
        else:
            string += letter
        i += 1


def remove_delimiters(body, left, right):
    counter = 0
    new_string = ""
    for letter in body:
        if letter == left:
            counter += 1
        elif letter == right:
            counter -= 1
        elif counter == 0:
            new_string += letter
    return new_string

# print(scan("the quick fox jumps over the lazy dog", make_trie("fox", "og", "o")))
# print(scan("dadadadadadadadadadad", make_trie("ad", "da")))

# print(remove_delimiters("the quick <brown> fox jumps <\over> the la<z<y>> dog", "<", ">"))



