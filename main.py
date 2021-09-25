from typing import Final
from bs4 import BeautifulSoup as bs
import requests
HOT_URL : Final[str] = 'https://www.billboard.com/charts/hot-100'


hot_page = requests.get(HOT_URL)
hot_page_content = hot_page.content
soup = bs(hot_page_content, 'html.parser')
chart_list_container = soup.find('div', class_= 'chart-list container')
# print(chart_list_container.children)
chart_table = chart_list_container.find_all('li')
chart_map = {}
for i in chart_table:
    artist = i.find_next('span',class_= 'chart-element__information').find_next('span', class_ = 'chart-element__information__song text--truncate color--primary').contents
    song = i.find_next('span',class_= 'chart-element__information').find_next('span', class_ = 'chart-element__information__artist text--truncate color--secondary').contents
    # print(artist, song)
    chart_map[artist.pop(0)] = song.pop(0)

for entry in chart_map:
    print(chart_map[entry],':' ,entry)

#Next step is to find every lyrics