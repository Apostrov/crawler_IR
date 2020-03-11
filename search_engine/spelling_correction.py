from collections import defaultdict
from search_engine.text_processing import preprocess

def soundex(word):
    removed = ['a', 'e', 'i', 'o', 'u', 'y']
    replaced = {
        '1': ['b', 'f', 'p', 'v'],
        '2': ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z'],
        '3': ['d', 't'],
        '4': ['l'],
        '5': ['m', 'n'],
        '6': ['r']
    }
    firstChar = word[0].upper()
    removedHandW = word[1:].replace('h', '').replace('w', '')
    
    replacedWord = ''
    for char in removedHandW:
        for num, group in replaced.items():
            if char in group:
                replacedWord += num
                break
        else:
            replacedWord += char

    withoutRepetition = ''
    lastChar = ''
    for char in replacedWord:
        if lastChar == char:
            continue
        lastChar = char
        withoutRepetition += char

    removedWord = ''
    for char in withoutRepetition:
        if char not in removed:
            removedWord += char

    soundexed = firstChar + removedWord
    while len(soundexed) < 4:
        soundexed += '0'
    return soundexed[:4]

def make_soundex_index(collection):
    soundexCollection = defaultdict(set)
    for song in collection:
        text = preprocess(song.text, True)
        for word in text:
            soundexCollection[soundex(word)].add(word)
    return soundexCollection

def levenshtein_distance(word1, word2):
    distanceMatrix = [[0 for i in range(len(word2) + 1)] for j in range(len(word1) + 1)]
    for i in range(1, len(word1) + 1):
        distanceMatrix[i][0] = i
    for i in range(1, len(word2) + 1):
        distanceMatrix[0][i] = i
    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            if word1[i - 1] == word2[j - 1]:
                distanceMatrix[i][j] = distanceMatrix[i - 1][j - 1]
            else:
                insertion = distanceMatrix[i][j - 1] + 1
                deletion = distanceMatrix[i - 1][j] + 1
                replacement = distanceMatrix[i - 1][j - 1] + 1

                distanceMatrix[i][j] = min(insertion, deletion, replacement)
    
    return distanceMatrix[len(word1)][len(word2)]

def correction(word, soundexIndex):
    soundexed = soundex(word)
    if soundexed not in soundexIndex:
        return []
    soundexWords = soundexIndex[soundexed]
    closest = []
    minDistance = 1e10
    for sWord in soundexWords:
        distance = levenshtein_distance(word, sWord)
        if distance < minDistance:
            closest = [sWord]
            minDistance = distance
        elif distance == minDistance:
            closest.append(sWord)
    return closest