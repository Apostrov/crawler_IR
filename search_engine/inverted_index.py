import pickle
from os import listdir, remove
from os.path import isfile, join, exists
from collections import defaultdict
from search_engine.text_processing import preprocess

INDEXFOLDER = "inverted_index"

def make_invertedIndex(collection):
    invertedIndex = defaultdict(set)
    for url in collection:
        clean = preprocess(collection[url].text)
        for word in clean:
            invertedIndex[word].add(url)
    save_invertedIndex(invertedIndex)
    
def save_invertedIndex(invertedIndex):
    for word in invertedIndex:
        path = join(INDEXFOLDER, word)
        pickle.dump(invertedIndex[word], open(path, "wb"))

def add_to_invertedIndex(song):
    invertedIndex = defaultdict(set)
    clean = preprocess(song.text)
    for word in clean:
        invertedIndex[word].add(song.url)
    
    for word in invertedIndex:
        path = join(INDEXFOLDER, word)
        if exists(path):
            indexes = pickle.load(open(path, "rb"))
            indexes.update(invertedIndex[word])
            pickle.dump(indexes, open(path, "wb"))
        else:
            pickle.dump(invertedIndex[word], open(path, "wb"))

def delete_from_invertedIndex(url):
    invertedIndex = get_invertedIndex()
    removeFiles = []
    for word in invertedIndex:
        if url in invertedIndex[word]:
            invertedIndex[word].remove(word)
            if len(invertedIndex[word]) < 1:
                removeFiles.append(word)
    
    for word in removeFiles:
        path = join(INDEXFOLDER, word)
        remove(path)
    
    save_invertedIndex(invertedIndex)

def get_invertedIndex(word):
    if len(word.strip()) == 0:
        return set()
    path = join(INDEXFOLDER, word)
    if exists(path):
        return pickle.load(open(path, "rb"))
    return set()

def search(query):
    query = query.strip()
    relevant_documents = []
    for word in query.split(' '):
        relevant_documents.append(get_invertedIndex(word))
    return list(set.intersection(*relevant_documents))