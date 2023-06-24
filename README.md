# Twitch-Bot-v1.0
Basic twitch bot.
Code is pulled from the example on the TwtichAPI and PyTwitch websites and slightly modified.
Code is modified to obfuscate Bot credentials.

## Libraries Used
- TwitchAPI (pip install twitchAPI)
- configparser (pip install configparser)

## How to use
- Clone the repo to you computer
- Ensure you have Python installed (https://www.python.org/downloads/)
- Install the libraries above with pip
- Create a bot account with twitch with 2FA enabled (make the username what you want your bot to be called)
- Ensure you have an Application created over at https://dev.twitch.tv/console
    - Redirect URL must be http://localhost:17563
    - Put the Client ID and Client Secret in the config file once its created (unquoted, the bot converts it to a string)
    - Put the channel name in the config file (unquoted, the bot converts it to a string)
- Once you have all of that done, you should have a config file in the root folder with the credentials filled out and channel name
- Login to the bot account on twitch
- Open a terminal in the folder with the bot_main.py script and run it with .\bot_main.py
- It should open a window and you can authorize the bot on the logged in account
- Once authorized it will then join the chat room and listen for events and commands

## Features
- Listens to chat and logs it to the bots console
- Comes with an example !reply chat command
- Obfuscated credentials and automatic token refresh on starting the bot
- Plenty of room for modification and more features