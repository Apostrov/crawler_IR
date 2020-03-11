import requests
import urllib.request
from bs4 import BeautifulSoup

MAXDOCKS = 1e6
ENGINGEURL = "http://127.0.0.1:80/update"

def get_song(url=None):
    if url is None:
        url = "https://www.lyrics.com/random.php"
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp.read(), 'html.parser')
    song = {}
    song['url'] = resp.geturl()
    if song['url'] == 'https://www.lyrics.com/no-lyrics.php' or '+' in song['url'] or '%' in song['url']:
        raise Exception('Wrong link')
    song['title'] = soup.find(id="lyric-title-text").get_text()
    song['artist'] = soup.find('h3', class_='lyric-artist').find('a').get_text()
    song['text'] = soup.find(id="lyric-body-text").get_text()
    return song

def send_song(song):
    print(f"Sending song [{song['artist']}:{song['title']}]")
    requests.post(url=ENGINGEURL, json=song)

def delete_song(url):
    print(f'Delete song: {url}')
    requests.delete(url=ENGINGEURL, json={'url': url})

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
    urls = []
    while(True):
        try:
            if(len(urls) <= MAXDOCKS):
                song = get_song()
        except KeyboardInterrupt:
            break
        except:
            continue
        else:
            if(len(urls) <= MAXDOCKS):
                send_song(song)
                urls.append(song['url'])

            if len(urls) % 10 == 0:
                urls, deadUrl = ping_url(urls)
                for url in deadUrl:
                    delete_song(url)

if __name__ == "__main__":
    main(MAXDOCKS)
