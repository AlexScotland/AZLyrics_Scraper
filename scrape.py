import sys
import urllib.request as urllib2
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class htmlStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
        
    def handle_data(self, d):
        self.fed.append(d)
        
    def get_data(self):
        return ''.join(self.fed)

def stripTags(html):
    s = htmlStripper()
    s.feed(html)
    return s.get_data()

def getSongList(url):
    song_list = []
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,"html.parser")    
    for song in soup.find_all('div',{'id':'listAlbum'}):
        for link in song.find_all('a'):
            song_link=link.get('href')
            song_name=link.get_text()
            song_link=SongLink[3:]
            generated_link='http://www.azlyrics.com/'+song_link
            song_list.append((song_name,generated_link))
    return song_list

def getLyrics(song_url):
    try:
        page=urllib2.urlopen(song[1])
    except Exception as msg:
        print("[ERR ] Cannot Navigate to link:  "+str(msg))
        print("[Cont] Skipping Song.")
    else:
        soup=BeautifulSoup(page,'lxml')
        soup=soup.find_all('div', class_="")
        text=soup[1]
        text=str(text)
        text=stripTags(text)
        text=text.replace("<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->","")
        return text

def writeTextFile(songText, songName):
    with open("dataset.txt", "a") as txtFile:
        txtFile.write(songName)
        txtFile.write(songText)
        txtFile.close()

def concatURL(artistName):
    artistName=artistName.lower()
    first_letter = artistName[0]
    url = "http://www.azlyrics.com/"+first_letter+"/"+artistName.replace(" ", "")+".html"
    return url

#############################################################################################
artist_names = ['Lil Pump']
proxies = {
    'http': '141.176.60.201:3128',
    'http': '209.97.131.118:8080',
           }
proxy=urllib2.ProxyHandler(proxies)
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
for name in artist_names:
    artist_url = concatURL(name)
    print(artist_url)
    song_list=getSongList(artist_url)
    counter = 0
    for song in songList:
        songLyrics=getLyrics(song)
        if songLyrics == None:
            pass
        else:
            writeTextFile(songLyrics,str(songList[counter][0]))
        counter +=1
