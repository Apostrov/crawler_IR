import pickle
from os import listdir
from os.path import isfile, join
from collections import defaultdict
from search_engine.text_processing import preprocess

INDEXFOLDER = "inverted_index"

def make_invertedIndex(collection):
    invertedIndex = defaultdict(set)
    index = 0
    for song in collection:
        clean = preprocess(song.text)
        for word in clean:
            invertedIndex[word].add(index)
        index += 1
    
    for word in invertedIndex:
        path = join(INDEXFOLDER, word)
        pickle.dump(invertedIndex[word], open(path, "wb"))

def add_to_invertedIndex(invertedIndex):
    pass

def get_invertedIndex():
    files = [f for f in listdir(INDEXFOLDER) if isfile(join(INDEXFOLDER, f))]
    invertedIndex = defaultdict(set)
    for word in files:
        path = join(INDEXFOLDER, word)
        indexes = pickle.load(open(path, "rb"))
        invertedIndex[word] = indexes
    return invertedIndex

def search(invertedIndex, query):
    query = query.strip()
    relevant_documents = []
    for word in query.split(' '):
        relevant_documents.append(invertedIndex[word])
    return list(set.intersection(*relevant_documents))