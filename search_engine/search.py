from search_engine.inverted_index import search, get_invertedIndex
from search_engine.text_processing import preprocess
from search_engine.wildcard_query import wildcard_query
from search_engine.spelling_correction import correction

def addToQueries(queries, query):
    for index in range(len(queries)):
        queries[index] += ' ' + query
    return queries

def search_song(text, collection, soundexIndex, bigramIndex):
    clean = preprocess(text)
    queries = []
    for token in clean:
        if '*' in token:
            wildcard = wildcard_query(token, bigramIndex)
            if len(wildcard) > 0:
                queries.append(wildcard)
        elif len(get_invertedIndex(token)) == 0:
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
        relevantsIndex.update(search(query))
   
    return [collection[index] for index in relevantsIndex]