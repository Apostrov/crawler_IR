from multiprocessing import Pool
from flask import Flask
from utils.crawler import Song
from utils.search import make_index, search_song
from utils.spelling_correction import make_soundex_index
from utils.wildcard_query import make_bigram_index 

app = Flask(__name__)


def get_song(num):
    while(True):
        try:
            song = Song()
        except:
            continue
        else:
            return song

def get_collection(size=1000):
    with Pool(100) as p:
        return p.map(get_song, range(size))

@app.route('/')
def index():
    collection = get_collection(25)
    invertedIndex = make_index(collection)
    soundexIndex = make_soundex_index(collection)
    bigramIndex = make_bigram_index(collection)
    songs = search_song('es', collection, invertedIndex, soundexIndex, bigramIndex)
    song = songs[0]
    return f"""
    Found {len(songs)} song\n
    First song: {song.artist} - {song.title}\n
    {song.text}
    """

if __name__ == "__main__":
    app.run(debug=True)