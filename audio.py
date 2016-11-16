#NekoBot v2 - Audio

#Importing external modules
import discord
import asyncio
import weakref
import threading

#Import my scripts
import API

#Load the opus library
discord.opus.load_opus("libopus-0.dll")

#Setting up variables
global players
players = weakref.WeakKeyDictionary() #Stores references to the stream players

async def start(client,message):
    msg = setUp(message)
    dest = msg["dest"]
    serv = msg["serv"]
    auth = msg["auth"]
    connection = client.voice_client_in(serv)
    if connection is None:
        channel = auth.voice.voice_channel
        if channel is not None:            
            await client.join_voice_channel(client.get_channel(auth.voice.voice_channel.id))
            await client.send_message(dest,"Joined the voice channel!")
        else:
            await client.send_message(dest,"Please join a voice channel first!")
    else:
        await client.send_message(dest,"I've already been summoned onto a server")

async def stop(client,message):
    msg = setUp(message)
    dest = msg["dest"]
    serv = msg["serv"]
    connection = client.voice_client_in(serv)
    if connection is not None:
        if connection in players:
            players[connection].stop()
            del players[connection]
        await connection.disconnect()
    else:
        await client.send_message(dest,"I'm not in a voice channel")

async def play(client,message):
    msg = setUp(message)
    dest = msg["dest"]
    serv = msg["serv"]
    auth = msg["auth"]
    arg = msg["msg"].replace("!play","")
    connection = client.voice_client_in(serv)
    if connection is not None:
        if connection in players:
            await players[connection].QueueAdd(arg)
        else:
            player = MusicPlayer()
            players[connection] = player
            await player.setup(client,connection,dest)
            await player.QueueAdd(arg)
            await player.start()
    else:
        await client.send_message(dest,"I haven't joined a voice channel yet!")

async def skip(client,message):
    msg = setUp(message)
    dest = msg["dest"]
    serv = msg["serv"]
    connection = client.voice_client_in(serv)
    if connection is not None:
        player = players[connection]
        if player is not None:
            player.skip()
        else:
            await client.send_message(dest,"I'm not playing anything")

async def pause(client,message,mode=True):
    msg = setUp(message)
    dest = msg["dest"]
    serv = msg["serv"]
    connection = client.voice_client_in(serv)
    if connection is not None:
        player = players[connection]
        if proc is None:
            await client.send_message(dest,"I'm not playing anything!")
        else:
            if pause:
                player.pause()
                await client.send_message(dest,"Music paused!")
            else:
                player.resume()
                await client.send_message(dest,"Music resumed!")
    else:
        await client.send_message(dest,"I haven't joined a channel yet")

async def volume(client,message):
    msg = setUp(message)
    dest = msg["dest"]
    serv = msg["serv"]
    connection = client.voice_client_in(serv)
    arg = msg["msg"].replace("!volume","")
    arg = arg.replace("!vol","")
    arg = arg.replace(" ","")
    try:
        volume = int(arg)
        if volume >= 0 and volume <= 200:
            if connection is not None:
                player = players[connection]
                if player is None:
                    await client.send_message(dest,"I'm not playing anything!")
                else:
                    player.volume(volume)
        else:
            await client.send_message(dest,"Must be between 1 and 200%")
    except ValueError:
        await client.send_message(dest,"Not a valid number")

def setUp(msg):
    output = {"dest":msg.channel,"serv":msg.server,"auth":msg.author,"msg":msg.content}
    return output

class MusicPlayer:
    async def setup(self,client,connection,destination):
        self.running = True
        self.q = asyncio.Queue()
        self.client = client
        self.connection = connection
        self.dest = destination
        self.vol = 1
    async def start(self):
        await self.loop()
    async def loop(self):
        self.running = True
        while not self.q.empty():
            if not self.running:
                break
            k = await self.q.get()
            self.player = await self.connection.create_ytdl_player(k)
            self.player.start()
            self.player.volume = self.vol
            await self.client.send_message(self.dest,"Playing: "+self.player.title)
            await asyncio.sleep(20)
            while True:
                if not self.player.is_playing():
                    break;
                else:
                    await asyncio.sleep(20)
        self.running = False
    def stop(self):
        self.running = False
        self.player.stop()
    def skip(self):
        self.player.stop()
    def pause(self):
        self.player.pause()
    def resume(self):
        self.player.resume()
    def volume(self,number):
        self.player.volume = number/100
        self.vol = self.player.volume
    async def QueueAdd(self,arg):
        await self.q.put(await API.YoutubeGet(arg))
        await self.client.send_message(self.dest,"Added to queue")
        if not self.running:
            await self.loop()
    
    
