import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import asyncio
import re

async def quantityPagesPS4(s ,url):
    res= await s.get(url)
    soup= BeautifulSoup(res.text, "html.parser")
    totalPages=int(soup.find("ol", class_="psw-l-space-x-1 psw-l-line-center psw-list-style-none").find_all("li")[-1].find("span").text)
    return totalPages

async def quantityGamesPS4(s ,url, totalPages):
    res=await s.get(f"https://store.playstation.com/en-in/category/85448d87-aa7b-4318-9997-7d25f4d275a4/{totalPages}")
    soup=BeautifulSoup(res.text, "html.parser")
    quantityGamesLastPage=len(soup.find_all("ul", class_="psw-grid-list psw-l-grid"))
    totalGames=((totalPages-1)*24)+(quantityGamesLastPage)
    return totalGames

async def pricesGamesPS4(s, url, totalPages):
    gamesPrice=[]
    for i in range(1, totalPages+1):
        await asyncio.sleep(0.8)
        res=await s.get(f"https://store.playstation.com/en-in/category/85448d87-aa7b-4318-9997-7d25f4d275a4/{i}")
        soup=BeautifulSoup(res.text, "html.parser")
        quantityGamesPage=soup.find("ul", class_="psw-grid-list psw-l-grid")

        for game in quantityGamesPage:
            name=game.find("span", class_="psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2").text
            price=(game.find("span", class_="psw-m-r-3").text).replace(",", "")
            gamePrice={
                'name':name,
                'price':price
            }
            gamesPrice.append(gamePrice)
    return gamesPrice

async def saveGamesPS4(gamesPrice):
    allGamesPS4df= pd.DataFrame(gamesPrice)
    allGamesPS4df.to_csv("gamespricesPS4.csv", index=False)

def searchedGamePS(game):
    try:
        with open("gamespricesPS4.csv", "r", encoding='utf-8') as csv_file:
            csv_reader=csv.reader(csv_file, delimiter=",")
            gamePricePS="The game doesn't exists in PLAYSTATION STORE"
            for line in csv_reader:
                gameps4=re.sub('[^0-9a-zA-Z :]+', '', line[0])
                if game.lower() in gameps4.lower():
                    gamePricePS=[re.sub('[^0-9a-zA-Z : . ,]+', '', line[0]).replace(",", ".").replace("Rs", ""), re.sub('[^0-9a-zA-Z : . ,]+', '', line[1]).replace(",", ".").replace("Rs", "")]
                    break  
    except Exception as e:
        print(e)
        print('There was an error in Play Station search')
    return gamePricePS

async def dbPlayStation(s):
    url='https://store.playstation.com/en-in/category/85448d87-aa7b-4318-9997-7d25f4d275a4/1'
    header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.64"}

    print("Scraping PS...")

    start_time=time.time()

    totalPages= await quantityPagesPS4(s, url,)

    gamesPrice= await pricesGamesPS4(s, url, totalPages)

    await saveGamesPS4(gamesPrice)

    print("PS Scraped")
    print("it takes PS: ",time.time()-start_time, "secs to scrape all games")
