import re
from search_engine.text_processing import preprocess

def word_to_bigrams(word, begining=True, ending=True):
    bigrams = []
    bigram = '$' if begining else ''

    for char in word:
        bigram += char
        if len(bigram) == 2:
            bigrams.append(bigram)
        bigram = char

    if ending:
        bigrams.append(bigram + '$')

    return bigrams

def make_bigram_index(collection):
    bigramIndex = {}

    for url in collection:
        bigramIndex = add_to_bigram(collection[url], bigramIndex)
    
    return bigramIndex

def add_to_bigram(song, bigramIndex):
    text = preprocess(song.text, False)
    for word in text:
        for bigram in word_to_bigrams(word):
            if bigram not in bigramIndex:
                bigramIndex[bigram] = [word]
            else:
                bigramIndex[bigram].append(word)
    
    return bigramIndex

def wildcard_query(pattern, bigramIndex):
    parts = pattern.strip().split('*')
    begin, end = parts.pop(0), parts.pop(-1)
    
    bigrams = set()
    if len(begin) != 0:
        bigrams.update(word_to_bigrams(begin, ending=False))
    if len(end) != 0:
        bigrams.update(word_to_bigrams(end, begining=False))
    for part in parts:
        bigrams.update(word_to_bigrams(part, begining=False, ending=False))
    
    if len(bigrams) == 0 and pattern.strip() == '*':
        return [value for values in bigramIndex.values() for value in values]
    
    words = set(bigramIndex[bigrams.pop()])
    for bigram in bigrams:
        words.intersection_update(bigramIndex[bigram])
        
    regex = pattern.replace('*', '.*?')
    findWords = []
    for word in words:
        if re.fullmatch(regex, word):
            findWords.append(word)
    return findWords