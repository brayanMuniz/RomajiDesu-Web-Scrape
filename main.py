import requests
from bs4 import BeautifulSoup

# First line from Band-Maid song "Choose Me"
r = requests.get('https://www.romajidesu.com/kanji/愛こそはね%20目に見えない幻想')
content = ""

if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    soup.prettify()
    content = soup.find_all("div", class_="kanji_detail")

print(content)

# RomajiDesu Html Template
#   .kanji_detail
#       .kanji_left,         contains: kanji, radicals
#       .kanji_right,        contains: meanings
#       .kanji_strokes_order contains: rect(s) inside of svg
