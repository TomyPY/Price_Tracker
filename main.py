import aiogram
import asyncio
import time
from scrapePsStore import dbPlayStation, searchedGamePS
from scrapeSteam import dbSteam, searchedGameSteam
from scrapeXbxStore import dbXBX, searchedGameXBX
from scrapeAllkeysPC import dbAllkeysPC, searchedGameAllkeysPC
from scrapeAllkeysXBX import dbAllkeysXBX, searchedGameAllkeysXBX
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from scrapeAll import scrape
import csv
from csv import writer
import os

API_KEY=""
chat={}

storage = MemoryStorage()
bot = Bot(token=API_KEY,parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    game=State()
    condition=State()
    conditionRemove=State()
    gameRemove=State()
    gamePrice=State()

@dp.message_handler(commands=['start', 'START', 'Start', 'sTART'])
async def start(message: types.Message):
    # ************************ START COMMAND ************************
    await message.reply('''
Hello, This is a price tracker bot! ✅

You will be able to track prices in:

⚡️Xbox store
⚡️Playstation Store
⚡️Steam
⚡️AllKeysgames
    
Type /help to see all the commands :)
        ''')

@dp.message_handler(commands=['help', 'Help', 'HELP', 'hELP'])
async def help_commands(message: types.Message):
    # ************************ HELP COMMAND ************************
    await message.reply( 
    '''
This are all the commands:

✅/start  ❓ Start the bot
✅/help   ❓ See all commands

✅/scrape ❓ Refresh prices of all games. (It takes 15 minutes)
✅/track_list ❓ See all games in your tracklist

✅/track_list_add ❓ Add a game into tracklist
✅/track_list_remove ❓ Remove a game from tracklist
✅/track_list_check ❓ Compare actual prices and tracklist prices

✅/game_price ❓ Checkout a game price

⚠️YOU NEED TO PUT ONLY THE COMMAND DOESN'T NEED ANY PARAMETER⚠️

''')

@dp.message_handler(commands=['scrape'])
async def scrape_it(message: types.Message):
    # ************************ SCRAPE COMMAND ************************
    print("SCRAPE COMMAND EXECUTED")
    await message.reply("Scraping🔨🔧...")
    await scrape(message)
    await message.reply("Finish! All games are updated ✅")


@dp.message_handler(commands=['track_list'])
async def track_list(message: types.Message):
    print("TRACK_LIST COMMAND EXECUTED")
    try:
        arr=read_tracking_file()
        
        txt=arr[1]

        await message.answer(txt)

    except:
        await message.answer("You don't have a track list yet, or an error has occured")


@dp.message_handler(commands=['track_list_add'])
async def track_list_add(message: types.Message):
    print("TRACK_LIST_ADD COMMAND EXECUTED")
    await Form.game.set()
    await message.answer("Please, write the name of the game")


@dp.message_handler(state=Form.game)
async def process_name(message: types.Message, state: FSMContext):
    print("PROCESSING NAME ADD")
    """Process game name"""
    # Finish our conversation
    await state.finish()

    chat['gameName']=message.text

    gamePS=searchedGamePS(message.text)
    gameSteam=searchedGameSteam(message.text)
    gameXBX=searchedGameXBX(message.text)
    gameAllkeysPC=searchedGameAllkeysPC(message.text)
    gameAllkeysXBX=searchedGameAllkeysXBX(message.text)

    if type(gamePS)==list:
        await message.answer(f'Game: <b>{str(gamePS[0])}</b> price: <b>{str(gamePS[1])}</b> IN PS')
        chat['gamePS']=gamePS
    else:
        await message.answer(gamePS)
    if type(gameSteam)==list:
        await message.answer(f'Game: <b>{str(gameSteam[0])}</b> price: <b>{str(gameSteam[1])}</b> IN STEAM')
        chat['gameSteam']=gameSteam
    else:
        await message.answer(gameSteam)
    if type(gameXBX)==list:
        await message.answer(f'Game: <b>{str(gameXBX[0])}</b> price: <b>{str(gameXBX[1])}</b> IN XBX')
        chat['gameXBX']=gameXBX
    else:
        await message.answer(gameXBX)
    if type(gameAllkeysPC)==list:
        await message.answer(f'Game: <b>{str(gameAllkeysPC[0])}</b> price: <b>{str(gameAllkeysPC[1])}</b> IN PC ALLKEYS')
        chat['gameAllkeysPC']=gameAllkeysPC
    else:
        await message.answer(gameAllkeysPC)
    if type(gameAllkeysXBX)==list:
        await message.answer(f'Game: <b>{str(gameAllkeysXBX[0])}</b> price: <b>{str(gameAllkeysXBX[1])}</b> IN XBX ALLKEYS')
        chat['gameAllkeysXBX']=gameAllkeysXBX
    else:
        await message.answer(gameAllkeysXBX)

    await Form.condition.set()
    await message.answer('Do you want to add it to the track list? <b>yes/no</b>')


@dp.message_handler(state=Form.condition)
async def process_name_condition(message: types.Message, state: FSMContext):
    print("PROCESSING CONDITION TO ADD")
    """Process condition """
    # Finish our conversation
    await state.finish()

    condition=message.text

    fileName = (r".\games_tracking.csv")
    if os.path.isfile(fileName):
        pass
    else:
        with open("games_tracking.csv", 'w') as s:
            print("File created")
            s.close()
    
    if condition.lower()=='yes':
        try:
            with open("games_tracking.csv", 'a', newline="") as s:
                csv_writer=csv.writer(s)
                csv_writer.writerow([f"*{chat['gameName']}*{chat['gamePS'][1] if chat['gamePS']!='empty' else 'empty'}*{chat['gameSteam'][1] if chat['gameSteam']!='empty' else 'empty'}*{chat['gameXBX'][1] if chat['gameXBX']!='empty' else 'empty'}*{chat['gameAllkeysPC'][1] if chat['gameAllkeysPC']!='empty' else 'empty'}*{chat['gameAllkeysXBX'][1] if chat['gameAllkeysXBX']!='empty' else 'empty'}"])
                s.close()
            await message.answer("The game was store it ✔️")
        except Exception as e:
            print(e)
            await message.answer("⚠️The game wasn't store it because an error has occurred⚠️")
    else:
        await message.answer("The game wasn't store it ✔️")


@dp.message_handler(commands=['track_list_remove'])
async def track_list_remove(message: types.Message):
    print("TRACK_LIST_REMOVE COMMAND EXECUTED")
    await Form.gameRemove.set()
    await message.answer("Please, write the name of the game")


@dp.message_handler(state=Form.gameRemove)
async def process_gameRemove(message:types.Message, state: FSMContext):
    print("PROCESSING GAME REMOVED NAME")
    await state.finish()
    gamesArr=[]

    arr=read_tracking_file()
    for game in arr[0]:
        gamesArr+=[(game.split("*")[1]).lower()]

    if (message.text).lower() in gamesArr:
        chat['gameRemove']=(message.text).lower()
        await Form.conditionRemove.set()
        await message.answer("Your game is "+message.text+". Do you want to remove it?")
    else:
        await message.answer("Your game was not found in track list")
    

@dp.message_handler(state=Form.conditionRemove)
async def process_gameRemove_condition(message: types.Message, state: FSMContext):
    print("PROCESSING CONDITION REMOVED NAME")
    await state.finish()
    conditionRemove=message.text

    if (conditionRemove).lower() == 'yes':
        remove_game_tracking_file()
        await message.answer("The game was removed")
    else:
        await message.answer("The game was not removed")


@dp.message_handler(commands=['track_list_check'])
async def track_list_price_day(message: types.Message):
    print("TRACK LIST CHECK COMMAND EXECUTED")
    arr_track_list=[]
    with open('games_tracking.csv', 'r', encoding='utf-8') as s:
        for line in s:
            arr_track_list+=[line]
        s.close()
    
    for game in arr_track_list:
        game=game.split('*')
        gameName=game[1]
        gamePricePS=float(game[2].strip())
        gamePriceSteam=float(game[3].strip())
        gamePriceXBX=float(game[4].strip())
        gamePriceAllkeysPC=float(game[5].strip())
        gamePriceAllkeysXBX=float(game[6].strip())
        
        gameNewPS=searchedGamePS(gameName)
        gameNewSteam=searchedGameSteam(gameName)
        gameNewXBX=searchedGameXBX(gameName)
        gameNewAllkeysPC=searchedGameAllkeysPC(gameName)
        gameNewAllkeysXBX=searchedGameAllkeysXBX(gameName)

        gameNewPSPrice=float(gameNewPS[1].strip())
        gameNewSteamPrice=float(gameNewSteam[1].strip())
        gameNewXBXPrice=float(gameNewXBX[1].strip())
        gameNewPriceAllkeysPC=float(gameNewAllkeysPC[1].strip())
        gameNewPriceAllkeysXBX=float(gameNewAllkeysXBX[1].strip())

        print(gameNewPSPrice)
        print(gameNewSteamPrice)
        print(gameNewXBXPrice)
        print(gameNewPSPrice)

        if type(gameNewPS)==list:
            if float(gameNewPSPrice)==float(gamePricePS):
                await message.answer(f"🕔The game <b>{gameNewPS[0]}</b> has no changes in his price🕔")
                dataPS=gameNewPS

            if float(gameNewPSPrice)<float(gamePricePS):
                price=100/(gamePricePS/(gamePricePS-gameNewPSPrice))
                await message.answer(f"💫The game <b>{gameNewPS[0]}</b> is <b>%{round(price, 2)}</b> cheapest!💫\n in: Play Station | old price: <b><u>{gamePricePS}</u></b> | new price: <b>{gameNewPSPrice}</b>")
                dataPS=gameNewPS

            if float(gameNewPSPrice)>float(gamePricePS):
                price=((gameNewPSPrice-gamePricePS)/gamePricePS)*100
                await message.answer(f"💸The game <b>{gameNewPS[0]}</b> is <b>%{round(price, 2)}</b> more expensive!💸\n in: Play Station | Old price: <b><u>{gamePricePS}</u></b> | New price: <b>{gameNewPSPrice}</b>")
                dataPS=gameNewPS

        if type(gameNewSteam)==list:

            if float(gameNewSteamPrice)==float(gamePriceSteam):
                await message.answer(f"🕔The game <b>{gameNewSteam[0]}</b> has no changes in his price🕔")
                dataSteam=gameNewSteam

            if float(gameNewSteamPrice)<float(gamePriceSteam):
                price=100/(gamePriceSteam/(gamePriceSteam-gameNewSteamPrice))
                await message.answer(f"💫The game <b>{gameNewSteam[0]}</b> is <b>%{round(price, 2)}</b> cheapest!💫\n in: Steam | old price: <b><u>{gamePriceSteam}</u></b> | new price: <b>{gameNewSteamPrice}</b>")
                dataSteam=gameNewSteam

            if float(gameNewSteamPrice)>float(gamePriceSteam):
                price=((gameNewSteamPrice-gamePriceSteam)/gamePriceSteam)*100
                await message.answer(f"💸The game <b>{gameNewSteam[0]}</b> is <b>%{round(price, 2)}</b> more expensive!💸\n in: Steam | old price: <b><u>{gamePriceSteam}</u></b> | new price: <b>{gameNewSteamPrice}</b>")
                dataSteam=gameNewSteam

        if type(gameNewXBX)==list:
            if float(gameNewXBXPrice)==float(gamePriceXBX):
                await message.answer(f"🕔The game <b>{gameNewXBX[0]}</b> has no changes in his price🕔")
                dataXBX=gameNewXBX

            if float(gameNewXBXPrice)<float(gamePriceXBX):
                price=100/(gamePriceXBX/(gamePriceXBX-gameNewXBXPrice))
                await message.answer(f"💫The game <b>{gameNewXBX[0]}</b> is <b>%{round(price, 2)}</b> cheapest!💫\n in: Steam | old price: <b><u>{gamePriceXBX}</u></b> | new price: <b>{gameNewXBXPrice}</b>")
                dataXBX=gameNewXBX

            if float(gameNewXBXPrice)>float(gamePriceXBX):
                price=((gameNewXBXPrice-gamePriceXBX)/gamePriceXBX)*100
                await message.answer(f"💸The game <b>{gameNewXBX[0]}</b> is <b>%{round(price, 2)}</b> more expensive!💸\n in: Steam | old price: <b><u>{gamePriceXBX}</u></b> | new price: <b>{gameNewXBXPrice}</b>")
                dataXBX=gameNewXBX

        if type(gameNewAllkeysPC)==list:

            if float(gameNewPriceAllkeysPC)==float(gamePriceAllkeysPC):
                await message.answer(f"🕔The game <b>{gameNewAllkeysPC[0]}</b> has no changes in his price🕔")
                
            if float(gameNewPriceAllkeysPC)<float(gamePriceAllkeysPC):
                price=100/(gamePriceAllkeysPC/(gamePriceAllkeysPC-gameNewPriceAllkeysPC))
                await message.answer(f"💫The game <b>{gameNewAllkeysPC[0]}</b> is <b>%{round(price, 2)}</b> cheapest!💫\n in: Steam | old price: <b><u>{gamePriceAllkeysPC}</u></b> | new price: <b>{gamePriceAllkeysPC}</b>")

            if float(gameNewPriceAllkeysPC)>float(gamePriceAllkeysPC):
                price=((gameNewPriceAllkeysPC-gamePriceAllkeysPC)/gamePriceAllkeysPC)*100
                await message.answer(f"💸The game <b>{gameNewAllkeysPC[0]}</b> is <b>%{round(price, 2)}</b> more expensive!💸\n in: Steam | old price: <b><u>{gamePriceAllkeysPC}</u></b>| new price: <b>{gamePriceAllkeysPC}</b>")

        if type(gameNewAllkeysXBX)==list:

            if float(gameNewPriceAllkeysXBX)==float(gamePriceAllkeysXBX):
                await message.answer(f"🕔The game <b>{gameNewAllkeysXBX[0]}</b> has no changes in his price🕔")

            if float(gameNewPriceAllkeysXBX)<float(gamePriceAllkeysXBX):
                price=100/(gamePriceAllkeysXBX/(gamePriceAllkeysXBX-gameNewPriceAllkeysXBX))
                await message.answer(f"💫The game <b>{gameNewAllkeysXBX[0]}</b> is <b>%{round(price, 2)}</b> cheapest!💫\n in: Steam | old price: <b><u>{gamePriceAllkeysXBX}</u></b> | new price: <b>{gamePriceAllkeysXBX}</b>")

            if float(gameNewPriceAllkeysXBX)>float(gamePriceAllkeysXBX):
                price=((gameNewPriceAllkeysXBX-gamePriceAllkeysXBX)/gamePriceAllkeysXBX)*100
                await message.answer(f"💸The game <b>{gameNewAllkeysXBX[0]}</b> is <b>%{round(price, 2)}</b> more expensive!💸\n in: Steam | old price: <b><u>{gamePriceAllkeysXBX}</u></b> | new price: <b>{gamePriceAllkeysXBX}</b>")

@dp.message_handler(commands=['game_price'])
async def game_price_check(message: types.Message):

    await Form.gamePrice.set()
    await message.answer("What game are you looking for?")

@dp.message_handler(state=Form.gamePrice)
async def process_gamePrice(message: types.Message, state: FSMContext):
    await state.finish()
    game=message.text

    gamePS=searchedGamePS(game)
    gameSteam=searchedGameSteam(game)
    gameXBX=searchedGameXBX(game)
    gameAllkeysPC=searchedGameAllkeysPC(game)
    gameAllkeysXBX=searchedGameAllkeysXBX(game)

    if type(gamePS)==list:
        await message.answer(f'Game: <b>{str(gamePS[0])}</b> price: <b>₹ {str(gamePS[1])}</b> IN PS')
    else:
        await message.answer(gamePS)
    if type(gameSteam)==list:
        await message.answer(f'Game: <b>{str(gameSteam[0])}</b> price: <b>₹ {str(gameSteam[1])}</b> IN STEAM')
    else:
        await message.answer(gameSteam)
    if type(gameXBX)==list:
        await message.answer(f'Game: <b>{str(gameXBX[0])}</b> price: <b>₹ {str(gameXBX[1])}</b> IN XBX')
    else:
        await message.answer(gameXBX)
    if type(gameAllkeysPC)==list:
        await message.answer(f'Game: <b>{str(gameAllkeysPC[0])}</b> price: <b>$ {str(gameAllkeysPC[1])}</b> IN PC ALLKEYS')
    else:
        await message.answer(gameAllkeysPC)
    if type(gameAllkeysXBX)==list:
        await message.answer(f'Game: <b>{str(gameAllkeysXBX[0])}</b> price: <b>$ {str(gameAllkeysXBX[1])}</b> IN XBX ALLKEYS')
    else:
        await message.answer(gameAllkeysXBX)

def read_tracking_file():
    print("READING GAMES TRACKING FILE")
    gamesARR=[]
    txt='You have the next games in the tracking list:\n\n'
    with open("games_tracking.csv", 'r') as s:
        for line in s:
            gamesARR.append(line)
        s.close()
    
    for game in gamesARR:
        txt+=f"⭐️{game.split('*')[1]}\n    Price PS: <b>{game.split('*')[2] if game.split('*')[2].strip() != 'm' else 'Empty'}</b>\n    Price Steam: <b>{game.split('*')[3] if game.split('*')[3].strip() != 'm' else 'Empty'}</b>\n    Price XBX: <b>{game.split('*')[4] if game.split('*')[4].strip() != 'm' else 'Empty'}</b>\n\n"

    return [gamesARR, txt]

def remove_game_tracking_file():
    gamesArr=[]
    with open('games_tracking.csv', 'r', newline='', encoding='utf-8') as s:
        for line in s:
            gamesArr.append([line.strip()])
        s.close()

    for game in gamesArr:
        if chat['gameRemove'] in game[0].lower():
            gamesArr.pop(gamesArr.index(game))

    with open("games_tracking.csv", 'w', newline='') as s:
        csv_writer=csv.writer(s)
        for game in gamesArr:
            csv_writer.writerow(game)
        s.close()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)