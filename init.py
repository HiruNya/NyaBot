# NekoBot v2

# Importing external modules
import discord
import asyncio

# Importing my scripts
import settings
import audio
import API

# Setting up the discord client
client = discord.Client()
global client

# Loading the opus library
discord.opus.load_opus("libopus-0.dll")

# Events


@client.event
async def on_ready():
    print("Ready!")


@client.event
async def on_server_join(server):
    print("Joined the server", server)


@client.event
async def on_server_leave(server):
    print("Left the server", server)


@client.event
async def on_message(message):
    msg = message.content.lower()
    if msg.startswith("!ping"):
        await client.send_message(message.channel, "Pong!")
    elif msg.startswith("!start") or msg.startswith("!summon") or msg.startswith("!init"):
        await audio.start(client, message)
    elif msg.startswith("!play"):
        await audio.play(client, message)
    elif msg.startswith("!stop"):
        await audio.stop(client, message)
    elif msg.startswith("!pause"):
        await audio.pause(client, message,mode=True)
    elif msg.startswith("!resume"):
        await audio.pause(client, message,mode=False)
    elif msg.startswith("!volume") or msg.startswith("!vol"):
        await audio.volume(client, message)
    elif msg.startswith("!skip"):
        await audio.skip(client, message)
    elif msg.startswith("!nyandere "):
        await API.YandereGet(client, message, 0)
    elif msg.startswith("!nyandere reset"):
        await API.YandereReset(client, message, 0)
    elif msg.startswith("!konyachan "):
        await API.YandereGet(client, message, 1)
    elif msg.startswith("!konyachan reset"):
        await API.YandereReset(client, message, 1)
    elif msg.startswith("!lol "):
        await API.LOLProfile(client, message)

# Run the bot
client.run(settings.DiscordToken)
