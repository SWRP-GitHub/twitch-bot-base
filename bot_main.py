from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import configparser
import random
import json
path = "config.ini"
config = configparser.ConfigParser()
config.read(path)
jsonStartUser = '{"user":"bingo_Start_User","number":"0"}'
bingoArry = []
bingoToggle = [0]
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
# BINGO BASE COMMANDS
# bingoStart Command
### NOTES: Need to build a better detection system for bingoToggle and bingoArry.

async def bingo_start(cmd: ChatCommand):
    if cmd.user.name == 'super_lil_fist':
        bingoToggle.clear()
        bingoToggle.append(1)
        bingoArry.clear()
        bingoArry.append(jsonStartUser)
        print(f'Bingo Game started!')
        await cmd.send(f'Bingo Started! "!bingoChoose NUMBER" to pick a number for bingo!')
    else:
        cmd.reply('You are not authorized to do this command.')
# bingoStop


async def bingo_stop(cmd: ChatCommand):
    if cmd.user.name == 'super_lil_fist':
        bingoToggle.clear()
        bingoToggle.append(0)
        print(f'Bingo Game stopped!')
        await cmd.send(f'Bingo has Ended, Pending final results!')
    else:
        cmd.reply('You are not authorized to do this command.')
# bingoStatus


async def bingo_current(cmd: ChatCommand):
    if bingoToggle == [1]:
        print('There is a gaming currently going on!')
    else:
        print('No game is running! Start one with !bingoStart!')
# bingoChoose Command


async def bingo_command(cmd: ChatCommand):
    try:
        if bingoToggle == [0]:
            print('Bingo is not started! Run /bingoStart to start the bingo!')
        else:
            userInput = int(cmd.parameter)
    except ValueError:
        print(
            f'{cmd.user.name} submitted value {cmd.parameter} and it was not an integer')
        await cmd.reply(f'Selected value not an number {cmd.user.name}!')
    else:
        if userInput not in range(1, 501):
            print(
                f'{cmd.user.name} submitted value {cmd.parameter} and it was not an in specified range')
            await cmd.reply(f'Selected number not within range! Must be between 1 and 500! {cmd.user.name}!')
        else:
            playerRecord = str("{"+'"user":'+'"'+f'{str(cmd.user.name)}' +
                               '"'+","+'"number":'+'"'f'{cmd.parameter}'+'"'+"}")
            jsonPlayRecord = json.loads(playerRecord)
            for i in bingoArry:
                jsonArry = json.loads(i)
                if jsonPlayRecord["user"] in jsonArry["user"]:
                    print('user present in array, aborting')
                    await cmd.reply('You have already selected a number! Wait for a new round to begin!')
                    break
                if jsonPlayRecord["number"] in jsonArry["number"]:
                    print('number present in array, aborting')
                    await cmd.reply('Number selected by another user, try again!')
                    break
            else:
                print(f'{cmd.user.name} submitted {cmd.parameter} as their number')
                await cmd.send(f'{cmd.user.name} submitted {cmd.parameter} as their number in bingo!')
                bingoArry.append(playerRecord)
    finally:
        print('finishing selection')
        print(bingoArry)
# Bingo winner and clear Array


async def bingo_winner_command(cmd: ChatCommand):
    if cmd.user.name == 'super_lil_fist':
        randInt = random.randint(1, len(bingoArry))
        print(f'Array Length = {len(bingoArry)}')
        jsonWinner = json.loads(bingoArry[randInt])
        print(
            f'Winner is {jsonWinner["user"]} with number {jsonWinner["number"]}')
        await cmd.send(f'Winner is {jsonWinner["user"]} with number {jsonWinner["number"]}!')
        bingoArry.clear()
    else:
        cmd.reply('You are not Authorized to do this command.')
# this is where we set up the bot


async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_event(ChatEvent.SUB, on_sub)
    chat.register_command('reply', test_command)
    chat.register_command('bingoChoose', bingo_command)
    chat.register_command('bingoStart', bingo_start)
    chat.register_command('bingoStop', bingo_stop)
    chat.register_command('bingoStatus', bingo_current)
    chat.register_command('bingoWinner', bingo_winner_command)
    chat.start()
    try:
        input('press ENTER to end the bot')
    finally:
        chat.stop()
        await twitch.close()
asyncio.run(run())
