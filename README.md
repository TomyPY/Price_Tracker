# Price_Tracker
Telegram Bot to track games prices

#Introduction:

Hello world! This is a game price tracker for STEAM, XBOX STORE and PLAYSTATION STORE.
With this bot you can have a database with allgames of STEAM, XBOX STORE and PLAYSTATION STORE whis his prices.
Track the games that you want and check if they are cheapest or more expensive!

To install all dependencies:
```
$ pip install pyTelegramBotAPI -r requeriments.txt
```

#How to use it:

To use it you have to create a bot through BotFather https://t.me/botfather. Get the API_ID and replace it in the API_ID variable in the code, then just turn on the bot!

#Commands:
- `/start` - Start the bot
- `/help` - See all commands
- `/scrape` - Refresh prices of all games. (It takes 15 minutes).
- `/track_list` -  See all games in your tracklist.
- `/track_list_add` -  Add a game into tracklist.
- `/track_list_remove` - Remove a game from tracklist.
- `/track_list_check` - Compare actual prices and tracklist prices.
- `/game_price` - Checkout a game price.

YOU NEED TO PUT ONLY THE COMMAND DOESN'T NEED ANY PARAMETER
