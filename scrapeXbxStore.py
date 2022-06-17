import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import re
import asyncio
from requests_html import AsyncHTMLSession

async def pricesGamesXBX(s, totalPages):
    gamesPrice=[]
    for i in range(1, totalPages+1):
        res=await s.get(f"https://xbdeals.net/in-store/all-games/{i}?platforms=xboxone&sort=rating-desc")
        soup=BeautifulSoup(res.text, "html.parser")
        GamesPage=soup.find_all("a", class_="game-collection-item-link")

        for game in GamesPage:
            name=game.find("p", class_="game-collection-item-details-title").text
            try:
                price=(game.find("span", class_="game-collection-item-regular-price").text).replace(",", "")

            except:
                price="No register"
            try:
                discountPrice=(game.find("span", class_="game-collection-item-discount-price").text).replace(",", "")
                price=discountPrice
            except:
                price=price

            gamePrice={
                "name":name,
                "price":price
            }

            gamesPrice.append(gamePrice)
    return gamesPrice

async def saveGamesXBX(gamesPrice):
    allGamesXBXdf= pd.DataFrame(gamesPrice)
    allGamesXBXdf.to_csv("gamespricesXBX.csv", index=False)

def searchedGameXBX(game):

    try:
        with open("gamespricesXBX.csv", "r", encoding='utf-8') as csv_file:
            csv_reader=csv.reader(csv_file, delimiter=",")
            gamePriceXBX="The game doesn't exists in XBOX"
            for line in csv_reader:
                gameXBX=re.sub('[^0-9a-zA-Z :]+', '', line[0])
                if gameXBX!='name':
                    if game.lower() in gameXBX.lower():
                        gamePriceXBX=[re.sub('[^0-9a-zA-Z : . ,]+', '', line[0]).replace(",", ".").replace("Rs", ""), re.sub('[^0-9a-zA-Z : . ,]+', '', line[1]).replace(",", ".").replace("Rs", "")]
                        break        
    except Exception as e:
        print(e)
        print('There was an error in Xbox search')
    return gamePriceXBX

async def dbXBX(s):

    print('Scraping XBX...')

    start_time=time.time()

    gamesPrice=await pricesGamesXBX(s, 226)

    await saveGamesXBX(gamesPrice)

    print("XBX Scraped!")
    print("it takes XBX: ",time.time()-start_time, "secs to scrape all games")