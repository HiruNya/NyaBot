#NekoBot

#importing the discord API
import discord
import asyncio
import time
import ast
#Importing my scripts
import API
import TimeFunc
#Counter for Yandere Page Number
yc = 1
#Time Counters
#-!nya introduce
tni = 0
#-!nya help
tnh = 0
#-!nya facts
tnf = 0
#-!nya pics
tncp = 0
#-!nya yandere
tny = 0
#-!nya konachan
tnkc = 0
#-!nya add
tna = 0
#-!nya ping
tnp = 0

#Setting up credentials
token = ''

#Setting up the object
client = discord.Client()

#Events
@client.event
async def on_ready():
    print("Ready!")
    
@client.event
async def on_server_join(server):
    print("Joined the server",server)

@client.event
async def on_message(message):
    destination = message.channel
    msg = message.content.lower()
    if msg.startswith("!nya"):
        #NEW - TEST NEEDED-------------#
        if msg.startswith("!nya hello"):
            #Introduces itself
            global tni
            if TimeFunc.deltaTimeTrue(tni,time.time(),3):
                await client.send_message(destination,"Hello My Name is Nya! I was created by Hiruna Jayamanne")
                tni = int(time.time())
        elif msg.startswith("!nya help"):
            #Shows help
            global tnh
            if TimeFunc.deltaTimeTrue(tnh,time.time(),3):
                await client.send_message(destination,"I can only do 5 things:\n'!nya help': Tells you what you can do with me *wink* *wink*\n'!nya introduce': Introduce my self\n'!nya cat facts [How many facts to produce(up to 10)]': Tells you an interesting fact about cats\n'!nya cat pic': Gives you a picture of a cat\n'!nyandere [tag]': Gives a picture from yande.re\nEnjoy!")
                tnh = int(time.time())
        elif msg.startswith("!nya cat facts"):
            #Gives Cat Facts
            global tnf
            if TimeFunc.deltaTimeTrue(tnf,time.time(),3):
                argument = msg.replace("!nya cat facts","")
                argument = argument.replace(" ","")
                if argument == "":
                    await client.send_message(destination,str(API.getCatFacts(1)))
                else:
                    sent = 0
                    for i in range(0,10,1):
                        if str(i) in argument:
                            await client.send_message(destination,API.getCatFacts(i))
                            sent = 1
                            break
                    if sent == 0:
                        await client.send_message(destination,API.getCatFacts(1))
                tnf = int(time.time())
        elif msg.startswith("!nya cat pic"):
            #Gets a pic of a cat
            global tncp
            if Time.FuncdeltaTimeTrue(tnp,time.time(),3):
                await client.send_message(destination,API.getCatPic())
                tnp = int(time.time())
        elif msg.startswith("!nyandere"):
            global tny
            if TimeFunc.deltaTimeTrue(tny,time.time(),3):
                global yc
                argument = msg.replace("!nyandere","")
                if argument.replace(" ","")=="reset":
                    yc = 1
                else:
                    if not "rating:" in argument:
                        if ("?" in argument) or("questionable" in argument):
                            argument = argument.replace("?","rating:q")
                            argument = argument.replace("questionable","rating:q")
                        elif ("explicit" in argument) or ("nsfw" in argument):
                            argument = argument.replace("nsfw","rating:e")
                            argument = argument.replace("explicit","rating:e")
                        elif ("safe" in argument) or ("sfw" in argument):
                            argument = argument.replace("safe","rating:s")
                            argument = argument.replace("sfw","rating:s")
                    text = API.YandereGET(argument,yc,0)
                    await client.send_message(destination,text)
                    yc += 1
                tny = int(time.time())
        elif msg.startswith("!nya add"):
            global tna
            if TimeFunc.deltaTimeTrue(tny,time.time(),3):
                argument = msg.replace("!nya add","")
                argument = argument.replace(" ","")
                result = "Please enter some values"
                try:
                    #if "*" in argument:
                    #    argument = argument.split("*")
                    #    for i in range (0,len(argument),1):
                    #        argument[i] = ast.literal_eval(argument)
                    result = ast.literal_eval(argument)
                except ValueError:
                    result = "Value Error"
                except ZeroDivisionError:
                    result = "Cannot Divide By Zero"
                except SyntaxError:
                    result = "Doesn't make sense"
                await client.send_message(destination,result)
        elif msg.startswith("!nya ping"):
            global tnp
            if TimeFunc.deltaTimeTrue(tnp,time.time(),3):
                await client.send_message(destination,"Pong!")
    elif msg.startswith("!konyachan"):
        global tnkc
        if TimeFunc.deltaTimeTrue(tny,time.time(),3):
            argument = msg.replace("!konyachan","")
            if not "rating:" in argument:
                if ("?" in argument) or("questionable" in argument):
                    argument = argument.replace("?","rating:q")
                    argument = argument.replace("questionable","rating:q")
                elif ("explicit" in argument) or ("nsfw" in argument):
                    argument = argument.replace("nsfw","rating:e")
                    argument = argument.replace("explicit","rating:e")
                elif ("safe" in argument) or ("sfw" in argument):
                    argument = argument.replace("safe","rating:s")
                    argument = argument.replace("sfw","rating:s")
                msg = API.YandereGET(argument,yc,1)
                await client.send_message(destination,msg)
                yc += 1
                tny = int(time.time())
        
                
            
client.run(token)
