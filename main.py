import requests
from bs4 import BeautifulSoup


def minify_kanji_detail(kanji):
    formatted = {"symbol": "", "meaning": "", "onyomi": "", 'kunyomi': ""}

    formatted["symbol"] = kanji.find("a", class_="joujou").text[0]
    formatted["meaning"] = kanji.find("div", class_="kanji_meaning").div.p.text

    # .ruby.rt.text for pronunciation
    formatted["onyomi"] = kanji.find("div", class_="on_yomi").ruby.text

    # .ruby.rt.text for pronunciation
    formatted["kunyomi"] = kanji.find("div", class_="kun_yomi").ruby.text

    return formatted


# First line from Band-Maid song "Choose Me"
r = requests.get('https://www.romajidesu.com/kanji/愛こそはね%20目に見えない幻想')

if r.status_code == 200:
    formatted_kanji = []
    soup = BeautifulSoup(r.content, "html.parser")
    soup.prettify()
    kanji_list = soup.find_all("div", class_="kanji_detail")
    for kanji in kanji_list:
        formatted_kanji.append(minify_kanji_detail(kanji))

    for kanji in formatted_kanji: 
        print(kanji)

# RomajiDesu Html Template
#   .kanji_detail
#       .kanji_left,         contains: kanji, radicals
#       .kanji_right,        contains: meanings
#       .kanji_strokes_order contains: rect(s) inside of svg
