from collections import defaultdict
from search_engine.text_processing import preprocess
from search_engine.wildcard_query import wildcard_query
from search_engine.spelling_correction import correction

def make_invindex(collection):
    invertedIndex = defaultdict(set)
    index = 0
    for song in collection:
        clean = preprocess(song.text)
        for word in clean:
            invertedIndex[word].add(index)
        index += 1
    return invertedIndex

def add_to_invindex(invertedIndex):
    pass

def search(index, query):
    query = query.strip()
    relevant_documents = []
    for word in query.split(' '):
        relevant_documents.append(index[word])
    return list(set.intersection(*relevant_documents))

def addToQueries(queries, query):
    for index in range(len(queries)):
        queries[index] += ' ' + query
    return queries

def search_song(text, collection, invertedIndex, soundexIndex, bigramIndex):
    clean = preprocess(text, True)
    queries = []
    for token in clean:
        if '*' in token:
            wildcard = wildcard_query(token, bigramIndex)
            if len(wildcard) > 0:
                queries.append(wildcard)
        elif token not in invertedIndex:
            corrected = correction(token, soundexIndex)
            if len(corrected) > 0:
                queries.append(corrected)
        else:
            queries.append(token)

    processedQueries = ['']
    for query in queries:
        if type(query) is str:
            addToQueries(processedQueries, query)
        else:
            newQueries = []
            for subQuery in query:
                newQueries += addToQueries(processedQueries[:], subQuery)
            processedQueries = newQueries

    relevantsIndex = set()
    for query in processedQueries:
        relevantsIndex.update(search(invertedIndex, query))
   
    return [collection[index] for index in relevantsIndex]