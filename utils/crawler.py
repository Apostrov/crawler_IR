import urllib.request
from bs4 import BeautifulSoup

class Song:
    def __init__(self):
        self.get_random_song()

    def get_random_song(self):
        url = "https://www.lyrics.com/random.php"
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        self.title = soup.find(id="lyric-title-text").get_text()
        self.artist = soup.find('h3', class_='lyric-artist').find('a').get_text()
        self.text = soup.find(id="lyric-body-text").get_text()