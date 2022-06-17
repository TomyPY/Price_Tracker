import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import jellyfish
import asyncio
from datetime import datetime
from requests_html import AsyncHTMLSession
from scrapePsStore import dbPlayStation, searchedGamePS
from scrapeSteam import dbSteam, searchedGameSteam
from scrapeXbxStore import dbXBX, searchedGameXBX
from scrapeAllkeysPC import dbAllkeysPC, searchedGameAllkeysPC
from scrapeAllkeysXBX import dbAllkeysXBX, searchedGameAllkeysXBX

async def scrape(message):
        s=AsyncHTMLSession()
        start_time=time.time()
        task1=asyncio.create_task(dbPlayStation(s))
        task2=asyncio.create_task(dbSteam(s))
        task3=asyncio.create_task(dbXBX(s))
        task4=asyncio.create_task(dbAllkeysPC(s))
        task5=asyncio.create_task(dbAllkeysXBX(s))

        resPS=await task1
        resSTEAM=await task2
        resXBX=await task3
        resAllkeysPC=await task4
        resAllkeysXBX=await task5
       