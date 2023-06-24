from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import configparser
import random
import json
# Config loading
path = "config.ini"
config = configparser.ConfigParser()
config.read(path)

#Bingo Arry
bingoArry = []

# Build credentials based on config.ini
# Requires OAuth and RedirectURL to be 'http://localhost:17563' in the application settings.
APP_ID = f'{config.get("client_info","clientID")}'
APP_SECRET = f'{config.get("client_info","clientSecret")}'
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = f'{config.get("client_info","targetChannel")}'

# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print(' | Super_lil_Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)
    print(f"Joined {TARGET_CHANNEL}'s chat. ")
    await ready_event.chat.send_message(room=TARGET_CHANNEL, text='Hello, I am Online and ready to take Commands from Chat!')


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    print(f'{msg.user.name} said: {msg.text}')


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

# TESTING BINGO BASE COMMANDS
async def bingo_command(cmd: ChatCommand):
    try:
        userInput = int(cmd.parameter)
    except ValueError:
        print(f'{cmd.user.name} submitted value {cmd.parameter} and it was not an integer')
        await cmd.reply(f'Selected value not an number {cmd.user.name}!')
    else:
        if userInput not in range(1, 501):
            print(f'{cmd.user.name} submitted value {cmd.parameter} and it was not an in specified range')
            await cmd.reply(f'Selected number not within range! Must be between 1 and 500! {cmd.user.name}!')
        else:
            playerRecord = "{'User':" + f'{cmd.user.name}' + ", 'number':" + f'{cmd.parameter}'+'}'
            print(playerRecord)
            print(f'{cmd.user.name} submitted {cmd.parameter} as their number')
            await cmd.reply(f'{cmd.user.name} submitted {cmd.parameter} as their number in bingo!')
            bingoArry.append(playerRecord)
            jsonArry = json.loads(str(bingoArry))
            print(json.dumps(bingoArry))
    finally:
        print('finishing selection')

# Bingo winner and clear Array
async def bingo_winner_command(cmd: ChatCommand):
    if (cmd.parameter == 'winner' & cmd.user.name=='theSpaceVixen'):
        randInt = random.randint(1,501)
        print(f'Winner is {bingoArry[randInt]}')



# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
    
    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want
    #   listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    #   listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    #   listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    #   there are more events, you can view them all in this documentation

    #   you can directly register commands and their handlers, this will register the !reply command
    chat.register_command('reply', test_command)
    chat.register_command('bingoChoose', bingo_command)

    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to end the bot')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


# lets run our setup
asyncio.run(run())
