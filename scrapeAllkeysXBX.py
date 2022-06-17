from bs4 import BeautifulSoup
import json
import pandas as pd
import csv
import time
import re
from requests_html import AsyncHTMLSession
import asyncio

async def pricesAllkeysXBX(s, totalPages):
    header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.64"}
    gamesPrice=[]
    for i in range(1, totalPages+1):
        print(i)
        await asyncio.sleep(1.5)
        res=await s.get(f"https://cheapdigitaldownload.com/catalog/category-xbox-games-all/page-{i}/")
        soup=BeautifulSoup(res.text, "html.parser")
        GamesPage=soup.find_all("li", class_="search-results-row")

        for game in GamesPage:
            name=game.find("h2", class_="search-results-row-game-title").text
            try:
                price=game.find("div", class_="search-results-row-price").text.strip()
            except:
                price="No register"

            gamePrice={
                "name":name,
                "price":price
            }

            gamesPrice.append(gamePrice)
    return gamesPrice

async def saveGamesAllkeysXBX(gamesPrices):
    allGamesAllkeysXBXdf= pd.DataFrame(gamesPrices)
    allGamesAllkeysXBXdf.to_csv("gamespricesAllkeysXBX.csv", index=False)

def searchedGameAllkeysXBX(game):
    try:
        with open("gamespricesAllkeysXBX.csv", "r", encoding='utf-8') as csv_file:
            csv_reader=csv.reader(csv_file, delimiter=",")
            gamePriceAllkeysXBX="The game doesn't exists in ALLKEYS"
            for line in csv_reader:
                gameAllkeysXBX=re.sub('[^0-9a-zA-Z :]+', '', line[0])
                if game.lower() in gameAllkeysXBX.lower():
                    gamePriceAllkeysXBX=[re.sub('[^0-9a-zA-Z : . ,]+', '', line[0]).replace(",", ".").replace("Rs", ""), re.sub('[^0-9a-zA-Z : . ,]+', '', line[1]).replace(",", ".").replace("Rs", "")]
                    break  
    except Exception as e:
        print(e)
        print('There was an error in Allkeys XBX search')
    return gamePriceAllkeysXBX

async def dbAllkeysXBX(s):

    print("Scraping Allkeys XBX...")

    start_time=time.time()

    gamesPricesAllkeysXBX=await pricesAllkeysXBX(s, 250)

    await saveGamesAllkeysXBX(gamesPricesAllkeysXBX)

    print("Allkeys XBX Scraped")
    print("it takes Allkeys XBX: ",time.time()-start_time, "secs to scrape all games")