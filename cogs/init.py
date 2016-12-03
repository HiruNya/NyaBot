# NekoBot v2

# Importing external modules
import discord
import sys
from time import sleep
from os import startfile
from colorama import init,Fore
init(autoreset=True)

# Importing my scripts
import settings
import audio
import API
import talk
import quiz


print(Fore.LIGHTCYAN_EX + 'NyaBot v2 - Multipurpose Discord Bot!\nCreated by Hiruna Jayamanne (AKA "HirunaV2")\nCode may be freely duplicated and/or changed!')

# Setting up the discord client
client = discord.Client()
# global client

# Loading the opus library
discord.opus.load_opus("libopus-0.dll")

# Events


@client.event
async def on_ready():
    print(Fore.LIGHTGREEN_EX + "Ready!")
    global client
    servers = list(client.servers)
    serverList = []
    for i in range(len(servers)-1):
        serverList.append(servers[i].name)
    print(Fore.GREEN + "Currently on Server(s): {0}".format(', '.join(serverList)))
    await client.change_presence(game=discord.Game(name='with myself'))


@client.event
async def on_server_join(server):
    print(Fore.LIGHTYELLOW_EX + "Joined the server", server)


@client.event
async def on_server_leave(server):
    print(Fore.LIGHTYELLOW_EX + "Left the server", server)

@client.event
async def on_member_join(member):
    await client.send_message(member.server.default_channel, "Welcome to the server, {0}!".format(member.mention))

@client.event
async def on_member_ban(member):
    await client.send_message(member.server.default_channel, "{0} has been exiled to the Shadow Dimension!".format(member.name))


@client.event
async def on_message(message):
    global client
    msg = message.content.lower()
    if msg.startswith("!ping"):
        await client.send_message(message.channel, "Pong!")
    elif msg.startswith("!help"):
        await talk.help(client, message)
    elif msg.startswith("!start") or msg.startswith("!summon") or msg.startswith("!init"):
        # await audio.start(client, message)
        await talk.fund(client, message)
    elif msg.startswith("!play"):
        # await audio.play(client, message)
        await talk.fund(client, message)
    elif msg.startswith("!stop"):
        # await audio.stop(client, message)
        await talk.fund(client, message)
    elif msg.startswith("!pause"):
        # await audio.pause(client, message,mode=True)
        await talk.fund(client, message)
    elif msg.startswith("!resume"):
        # await audio.pause(client, message,mode=False)
        await talk.fund(client, message)
    elif msg.startswith("!volume") or msg.startswith("!vol"):
        # await audio.volume(client, message)
        await talk.fund(client, message)
    elif msg.startswith("!skip"):
        # await audio.skip(client, message)
        await talk.fund(client, message)
    elif msg.startswith("!nyandere reset"):
        await API.YandereReset(client, message, 0)
    elif msg.startswith("!nyandere "):
        await API.YandereGet(client, message, 0)
    elif msg.startswith("!konyachan reset"):
        await API.YandereReset(client, message, 1)
    elif msg.startswith("!konyachan "):
        await API.YandereGet(client, message, 1)
    elif msg.startswith("!lol "):
        await API.LOLProfile(client, message)
    elif msg.startswith("!osu "):
        await API.getOSUProfile(client, message)
    elif msg.startswith("!yt "):
        await API.YoutubeSearch(client, message)
    elif msg.startswith("!quiz start "):
        await quiz.quizStart(client, message)
    elif msg.startswith("!quiz stop"):
        await quiz.quizStop(client, message)
    elif msg.startswith("!quiz list") or msg.startswith('!quiz start') or msg.startswith("!quiz help"):
        await quiz.quizList(client, message)
    else:
        await talk.run(client, message)

# Run the bot
# try:
#     client.run(settings.DiscordToken)
# except:
#     print(Fore.RED + "Error: Restaring...")
#     sleep(60)
#     sys.exit(startfile("NB.bat"))

client.run(settings.DiscordToken)