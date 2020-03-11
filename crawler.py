import requests
import urllib.request
from bs4 import BeautifulSoup

MAXDOCKS = 5#1e6
ENGINGEURL = "http://127.0.0.1:5000/update"

def get_song(url=None):
    if url is None:
        url = "https://www.lyrics.com/random.php"
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp.read(), 'html.parser')
    song = {}
    song['url'] = resp.geturl()
    song['title'] = soup.find(id="lyric-title-text").get_text()
    song['artist'] = soup.find('h3', class_='lyric-artist').find('a').get_text()
    song['text'] = soup.find(id="lyric-body-text").get_text()
    return song

def send_song(song):
    requests.post(url=ENGINGEURL, json=song)

def ping_url(urls):
    print(f'Checking if the songs alive')
    deadUrl = []
    aliveUrl = []
    for url in urls:
        code = urllib.request.urlopen(url).getcode()
        if code != 200:
            deadUrl.append(url)
        else:
            aliveUrl.append(url)
    return aliveUrl, deadUrl

def main(docksNumber):
    docNumber = 0
    urls = []
    while(docNumber < docksNumber):
        try:
            song = get_song()
        except KeyboardInterrupt:
            break
        except:
            continue
        else:
            print(f"Sending song [{song['artist']}:{song['title']}]")
            send_song(song)
            docNumber += 1
            urls.append(song['url'])
            if docNumber % 4 == 0:
                aliveUrl, deadUrl = ping_url(urls)
                print(aliveUrl, deadUrl)

if __name__ == "__main__":
    main(MAXDOCKS)
