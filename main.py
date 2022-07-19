import asyncio
import requests
from bs4 import BeautifulSoup
kanji_url = "https://www.romajidesu.com/kanji/"
file_name = "song-name.txt" 

all_lines = []
with open(file_name) as file:
    all_lines = [line.rstrip() for line in file]

# Remove duplicates
lines = []
[lines.append(x) for x in all_lines if x not in lines]
print("Wait around", len(lines) + 5, "seconds")

formatted_kanji = {}


def minify_kanji_detail(kanji):
    formatted = {"symbol": "", "meaning": "", "onyomi": "", 'kunyomi': ""}

    formatted["symbol"] = kanji.find("a", class_="joujou").text[0]
    formatted["meaning"] = kanji.find("div", class_="kanji_meaning").div.p.text

    # .ruby.rt.text for pronunciation
    formatted["onyomi"] = kanji.find("div", class_="on_yomi").ruby.text

    # .ruby.rt.text for pronunciation
    formatted["kunyomi"] = kanji.find("div", class_="kun_yomi").ruby.text

    return formatted


async def get_kanji_from_line(line):
    full_url = kanji_url + line.replace(" ", "%20")
    r = requests.get(full_url)

    if r.status_code == 200:
        kanji_list = []
        soup = BeautifulSoup(r.content, "html.parser")
        soup.prettify()
        kanji_detail = soup.find_all("div", class_="kanji_detail")
        for kanji in kanji_detail:
            kanji_list.append(minify_kanji_detail(kanji))

        for kanji in kanji_list:
            if(kanji["symbol"] not in formatted_kanji.keys()):
                formatted_kanji[kanji["symbol"]] = kanji
    await asyncio.sleep(.5)

loop = asyncio.get_event_loop()
tasks = []
for line in lines:
    tasks.append(get_kanji_from_line(line=line))

loop.run_until_complete(asyncio.wait(tasks))
loop.close()

print(formatted_kanji)