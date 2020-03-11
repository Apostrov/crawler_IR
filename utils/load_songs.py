import os
import pickle
from os import listdir
from os.path import isfile, join

DOCFOLDER = "songs"

class Song:
    def __init__(self, url, title, artist, text):
        self.url = url
        self.title = title
        self.artist = artist
        self.text = text

def add_song(jsonSong):
    song = Song(jsonSong['url'], jsonSong['title'], 
                jsonSong['artist'], jsonSong['text'])
    save_song(song)
    return song

def delete_song(url):
    path = get_path(url)
    os.remove(path)

def get_path(url):
    id = url.replace('/', '_')
    return f"{DOCFOLDER}/{id}"

def save_song(song):
    path = get_path(song.url)
    pickle.dump(song, open(path, "wb"))

def get_song(path):
    path = join(DOCFOLDER, path)
    if os.path.exists(path) and os.path.isfile(path):
        song = pickle.load(open(path, "rb"))
        return song
    return None

def get_collection():
    files =  [f for f in listdir(DOCFOLDER) if isfile(join(DOCFOLDER, f))]
    collection = {}
    for path in files:
        url = path.replace('_', '/')
        song = get_song(path)
        if not song is None:
            collection[url] = song
    return collection