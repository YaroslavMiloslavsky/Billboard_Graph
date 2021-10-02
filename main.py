from bs4 import BeautifulSoup as bs
from pandas.core.frame import DataFrame
import requests
from idsecret import Token, URLS
import lyricsgenius as lg
import os
import matplotlib.pyplot as plt
import pandas as pd

token = Token()
urls = URLS()

skip_non_songs = True
exclude_terms = ['(Remix)', '(Live)']
remove_section_headers = True
genius = lg.Genius(token.get_access_token(), skip_non_songs=skip_non_songs, excluded_terms=exclude_terms, remove_section_headers=remove_section_headers)
    

def get_songs() -> dict:
    hot_page = requests.get(urls.get_top_url())
    hot_page_content = hot_page.content
    soup = bs(hot_page_content, 'html.parser')
    chart_list_container = soup.find('div', class_= 'chart-list container')
    chart_table = chart_list_container.find_all('li')
    chart_map = {}
    for i in chart_table:
        artist = i.find_next('span',class_= 'chart-element__information').find_next('span', class_ = 'chart-element__information__song text--truncate color--primary').contents
        song = i.find_next('span',class_= 'chart-element__information').find_next('span', class_ = 'chart-element__information__artist text--truncate color--secondary').contents
        chart_map[artist.pop(0)] = song.pop(0)

    return chart_map

# Recives a map of [artist]song type and finds lyrics for all available songs in the genius API
def write_lyrics(chart_map):
    for artist in chart_map:
        if artist is None:
            break
        with open(os.path.join(urls.get_lyrics_folder(), str(artist + '.txt')), 'w') as f:
            song = genius.search_song(title= chart_map[artist], artist=artist).lyrics
            f.write(song)
        f.close()

# Recives a folder with the lyrics text files (Test needed) and maps the number of occurrences in these files 
# And then
# Recives a map of type [word]occurrences and plots the data via bar diagram
# tol is how many words to display on the graph
def print_data_bar(tol = 100, print_data = True)-> DataFrame:
    words = {}
    lyrics_files = os.listdir(urls.get_lyrics_folder())
    unwanted_chars = '.,-()"'
    for song in lyrics_files:
        with open(os.path.join(urls.get_lyrics_folder(),song), 'r') as f:
            data = f.read()
            text = data.split()
            for raw_word in text:
                word = raw_word.strip(unwanted_chars).lower()
                if word.isalnum() and len(word)>2 and word is not None and word not in urls.to_ignore():
                    if word not in words:
                        words[word] = 0
                    else:
                        words[word] += 1
        f.close()
    df = pd.Series(words).to_frame('count')
    df = df.sort_values(by=['count'], ascending=False)
    df = df[df['count']>10]
    pd.set_option('display.max_rows', df.shape[0]+1)
    if print_data is True:
        df = df[:tol]
        df.plot(kind = 'bar')
        plt.show()
    else:
        print(df)

    return df

if __name__ == "__main__":
    songs = get_songs() # Gets the song
    write_lyrics(songs) # Gets the lyrics for each song
    print_data_bar() # Prints the bar graph
    print_data_bar(print_data=False) # Prints the DataFrame


