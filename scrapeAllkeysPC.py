from bs4 import BeautifulSoup
import json
import pandas as pd
import csv
import time
import re
from requests_html import AsyncHTMLSession
import asyncio

async def pricesAllkeysPC(s, totalPages):
    header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.64"}
    gamesPrice=[]
    for i in range(1, totalPages+1):
        print(i)
        await asyncio.sleep(1.5)
        res=await s.get(f"https://cheapdigitaldownload.com/catalog/category-pc-games-all/page-{i}/", headers=header)
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

async def saveGamesAllkeysPC(gamesPrices):
    allGamesAllkeysPCdf= pd.DataFrame(gamesPrices)
    allGamesAllkeysPCdf.to_csv("gamespricesAllkeysPC.csv", index=False)

def searchedGameAllkeysPC(game):
    try:
        with open("gamespricesAllkeysPC.csv", "r", encoding='utf-8') as csv_file:
            csv_reader=csv.reader(csv_file, delimiter=",")
            gamePriceAllkeysPC="The game doesn't exists in ALLKEYS"
            for line in csv_reader:
                gameAllkeysPC=re.sub('[^0-9a-zA-Z :]+', '', line[0])
                if game.lower() in gameAllkeysPC.lower():
                    gamePriceAllkeysPC=[re.sub('[^0-9a-zA-Z : . ,]+', '', line[0]).replace(",", ".").replace("Rs", ""), re.sub('[^0-9a-zA-Z : . ,]+', '', line[1]).replace(",", ".").replace("Rs", "")]
                    break  
    except Exception as e:
        print(e)
        print('There was an error in Allkeys PC search')
    return gamePriceAllkeysPC

async def dbAllkeysPC(s):

    print("Scraping Allkeys PC...")

    start_time=time.time()

    gamesPricesAllkeysPC=await pricesAllkeysPC(s, 250)

    await saveGamesAllkeysPC(gamesPricesAllkeysPC)

    print("Allkeys PC Scraped")
    print("it takes Allkeys PC: ",time.time()-start_time, "secs to scrape all games")