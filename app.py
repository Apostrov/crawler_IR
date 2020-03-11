from flask import Flask, request, render_template
from utils.load_songs import add_song, get_collection, get_song
from search_engine.search import make_invindex, search_song
from search_engine.spelling_correction import make_soundex_index
from search_engine.wildcard_query import make_bigram_index 

app = Flask(__name__)

@app.route('/')
def index():
    collection = get_collection()
    return render_template('songs.html', songs=collection) 

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
        songs = search_song(query, collection, invertedIndex, soundexIndex, bigramIndex)
        return render_template('songs.html', songs=songs) 

@app.route('/update', methods=['POST'])
def upadate():
    song = add_song(request.json)
    return "Added"

def init():
    collection = get_collection()
    invertedIndex = make_invindex(collection)
    soundexIndex = make_soundex_index(collection)
    bigramIndex = make_bigram_index(collection)
    return invertedIndex, soundexIndex, bigramIndex

if __name__ == "__main__":
    invertedIndex, soundexIndex, bigramIndex = init()
    app.run(debug=True)