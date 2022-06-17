from bs4 import BeautifulSoup
import json
import pandas as pd
import csv
import time
import re

async def quantityGames(s, url):
    res=await s.get(url)
    amountGames=dict(res.json())["total_count"]
    return int(amountGames)

async def totalGames(s, amountGames):
    allGames=[]
    for i in range(0, amountGames, 50):
        url=f'https://store.steampowered.com/search/results/?query&start={i}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_230_7&infinite=1'
        res=await s.get(url)
        data=dict(res.json())["results_html"]

        soup=BeautifulSoup(data, "html.parser")

        games=soup.find_all("a")
        for game in games:
            
            name=game.find("div", class_='col search_name ellipsis').find("span").text
            price=game.find("div", {"class": "search_price"}).text.strip().split("$")[0].replace("ARS", "").replace(",", ".").replace(" ", "")
            try:
                discountPrice=game.find("div", {"class": "search_price"}).text.strip().split("$")[1].replace("ARS", "").replace(",", ".").replace(" ", "")
                price=discountPrice
            except:
                price=price

                if price.count(".")>1:
                    price=price.replace(".", "", 1)

            if price!='Free To Play' and price!='Free to Play' and price!="FreetoPlay" and price!='FreeToPlay':
                gamePrice={
                    'name':name,
                    'price':price
                }
                allGames.append(gamePrice)
    return allGames

async def saveGames(allGames):
    allGamesdf= pd.DataFrame(allGames)
    allGamesdf.to_csv("gamespricesSteam.csv", index=False)

def searchedGameSteam(game):
    
    with open("gamespricesSteam.csv", "r", encoding='utf-8') as csv_file:
        csv_reader=csv.reader(csv_file, delimiter=",")
        gamePriceSteam="The game doesn't exists in STEAM"
        for line in csv_reader:
            gameSteam=re.sub('[^0-9a-zA-Z :]+', '', line[0])
            if game.lower() in gameSteam.lower():
                gamePriceSteam=[re.sub('[^0-9a-zA-Z : . ,]+', '', line[0]).replace(",", ".").replace("Rs", ""), re.sub('[^0-9a-zA-Z : . ,]+', '', line[1]).replace(",", ".").replace("Rs", "")]
                break
    return gamePriceSteam

async def dbSteam(s):
    url='https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&os=win&snr=1_7_7_7000_7&filter=topsellers&infinite=1'
    header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.64"}

    print("Scraping Steam...")

    start_time=time.time()

    amountGames= await quantityGames(s, url)

    allGames=await totalGames(s, amountGames)

    await saveGames(allGames)

    print("Steam scraped!")
    print("it takes Steam: ",time.time()-start_time, "secs to scrape all games")

