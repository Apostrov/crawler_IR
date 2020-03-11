import os
from flask import Flask, request, render_template
from utils.load_songs import add_song, get_collection, get_song, delete_song
from search_engine.search import search_song
from search_engine.inverted_index import make_invertedIndex, get_invertedIndex, add_to_invertedIndex, delete_from_invertedIndex
from search_engine.spelling_correction import make_soundex_index, add_to_soundex
from search_engine.wildcard_query import make_bigram_index , add_to_bigram

app = Flask(__name__)

@app.route('/')
def index():
    collection = get_collection()
    return render_template('songs.html', songs=collection.values()) 

@app.route('/song')
def song():
    url = request.args.get('url')
    id = url.replace('/', '_')
    song = get_song(id)
    return render_template('song.html', song=song)

@app.route('/query')
def query():
    query = request.args.get('query')
    if query is None:
        return render_template('query.html')
    else:
        collection = get_collection()
        invertedIndex = get_invertedIndex()
        songs = search_song(query, collection, invertedIndex, soundexIndex, bigramIndex)
        return render_template('songs.html', songs=songs) 

@app.route('/update', methods=['POST', 'DELETE'])
def upadate():
    if request.method == 'POST':
        song = add_song(request.json)
        add_to_invertedIndex(song)
        add_to_soundex(song, soundexIndex)
        add_to_bigram(song, bigramIndex)
        return "OK"
    else:
        url = request.json.url
        delete_song(url)
        delete_from_invertedIndex(url)
        return "OK"

def init():
    if not os.path.exists('inverted_index'):
        os.makedirs('inverted_index')

    if not os.path.exists('songs'):
        os.makedirs('songs')
    
    collection = get_collection()
    make_invertedIndex(collection)
    soundexIndex = make_soundex_index(collection)
    bigramIndex = make_bigram_index(collection)
    return soundexIndex, bigramIndex

if __name__ == "__main__":
    soundexIndex, bigramIndex = init()
    app.run(debug=True)