from typing import Final
from bs4 import BeautifulSoup as bs
import requests
from idsecret import Token, URLS
import lyricsgenius as lg
import os
import matplotlib.pyplot as plt
from matplotlib import pyplot
import pandas as np

token = Token()
urls = URLS()

skip_non_songs = True
exclude_terms = ['(Remix)', '(Live)']
remove_section_headers = True
genius = lg.Genius(token.getAccessToken(), skip_non_songs=skip_non_songs, excluded_terms=exclude_terms, remove_section_headers=remove_section_headers)
    

def writeLyrics(chart_map):
    for artist in chart_map:
        if artist is None:
            break
        with open(os.path.join(urls.getLyricsFolder(), str(artist + '.txt')), 'w') as f:
            song = genius.search_song(title= chart_map[artist], artist=artist).lyrics
            f.write(song)
        f.close()

def getSongs():
    hot_page = requests.get(urls.getTopUrl())
    hot_page_content = hot_page.content
    soup = bs(hot_page_content, 'html.parser')
    chart_list_container = soup.find('div', class_= 'chart-list container')
    chart_table = chart_list_container.find_all('li')
    chart_map = {}
    for i in chart_table:
        artist = i.find_next('span',class_= 'chart-element__information').find_next('span', class_ = 'chart-element__information__song text--truncate color--primary').contents
        song = i.find_next('span',class_= 'chart-element__information').find_next('span', class_ = 'chart-element__information__artist text--truncate color--secondary').contents
        # print(artist, song)
        chart_map[artist.pop(0)] = song.pop(0)

    # for entry in chart_map:
    #     print(chart_map[entry],':' ,entry)

    return chart_map

words = {}
count = 0
some_list = os.listdir(urls.getLyricsFolder())
unwanted_cahrs = '.,-()"'
for song in some_list:
    with open(os.path.join(urls.getLyricsFolder(),song), 'r') as f:
        data = f.read()
        text = data.split()
        for raw_word in text:
            word = raw_word.strip(unwanted_cahrs).lower()
            if word.isalnum() and len(word)>2 and word is not None:
                if word not in words:
                    words[word] = 0
                else:
                    words[word] += 1
    f.close()

names = list(words.keys())
values = list(words.values())


df = np.Series(words).to_frame('count')
df = df.sort_values(by=['count'], ascending=False)
df = df[df['count']>10]
np.set_option('display.max_rows', df.shape[0]+1)

print(df)

df = df[:100]
df.plot(kind = 'bar')
plt.show()

