# API

# Import external modules
import aiohttp
import asyncio
import json

# Import my scripts
import settings

counter = {"yandere":1,"konachan":1}
global counter

async def YoutubeGet(search):
    search = search.replace(" ", "+")
    while "++" in search:
        search = search.replace("++", "+")
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1&q="+search+"&type=video&key="+settings.YoutubeToken) as resp:
            r = await resp.text()
            output = json.loads(r)["items"][0]["id"]["videoId"]
            return "https://www.youtube.com/watch?v="+output   

async def YandereGet(client, message, site):
    # Site 0 = yande.re
    # Site 1 = konachan.com
    if site == 0:
        num = counter["yandere"]
        counter["yandere"] += 1
        tag = message.content.replace("!nyandere ", "")
        tag = tag.replace(" ", "+")
        URL = "https://yande.re/post.json?limit=1&page="
    elif site == 1:
        num = counter["konachan"]
        counter["konachan"] += 1
        tag = message.content.replace("!konyachan ", "")
        tag = tag.replace(" ", "+")
        URL = "http://konachan.com/post.json?limit=1&page="
    URL += str(num)
    if tag.replace(" ", "") != "":
        tag = tag.replace("nsfw", "rating:explicit")
        tag = tag.replace("sfw" or "safe", "rating:safe")
        tag = tag.replace("?" or "q", "rating:questionable")
        URL += "&tags="+tag
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            r = await resp.json()
            try:
                output = r[0]['file_url']
            except:
                output = "Invalid Tag"
    await client.send_message(message.channel, output)

async def YandereReset(client, message,site):
    if site == 0:
        counter["yandere"] = 1
    elif site == 1:
        counter["konachan"] = 1
    await client.send_message(message.channel, "Counter Reset!")

async def LOLIDFind(message, API):
    username = message.content.replace("!lol ", "")
    username = username.replace(" ", "%20")
    URL = "https://oce.api.pvp.net/api/lol/oce/v1.4/summoner/by-name/{1}?api_key={0}".format(API, username)
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            r = await resp.json()
            if "status" not in r:
                ID = list(r.values())[0]["id"];
                LVL = list(r.values())[0]["summonerLevel"];
                NAME = list(r.values())[0]["name"];
            else:
                ID = 0
                LVL = ""
                NAME = ""
    return {"id": ID, "lvl": LVL, "name": NAME}

async def getLOLSummary(API, Summoner):
    ID = Summoner["id"]
    URL = "https://oce.api.pvp.net/api/lol/oce/v1.3/stats/by-summoner/{1}/summary?api_key={0}".format(API, ID)
    async with aiohttp.ClientSession() as session, session.get(URL) as resp:
        r = await resp.json()
        # if "status" not in r:
        try:
            for i in range(0, len(r["playerStatSummaries"])):
                if r["playerStatSummaries"][i]["playerStatSummaryType"] == "Unranked":
                    won = r["playerStatSummaries"][i]["wins"]
                    x = r["playerStatSummaries"][i]["aggregatedStats"]
                    ck = x["totalChampionKills"]
                    nmk = x["totalMinionKills"]
                    tk = x["totalTurretsKilled"]
                    nmk = x["totalNeutralMinionsKilled"]
                    ta = x["totalAssists"]
                    output = "Summoner Name: {0}\r\nLvl: {1}\r\nWins: {2}\r\nTotal Champions Killed: {3}\r\n"
                    output += "Total Turrets Killed: {4}\r\nTotal Neutral Minions Killed: {5}\r\nTotal Assists: {6}"
                    output = output.format(Summoner["name"], Summoner["lvl"], won, ck, tk, nmk, ta)
                    return output
        except:
            return 0

async def LOLProfile(client, message):
    API = settings.LOLAPIKEY
    Summoner = await LOLIDFind(message, API)
    if Summoner["id"] != 0:
        output = await getLOLSummary(API, Summoner)
        if output == 0:
            output = "ERROR"
    else:
        output = "Invalid name"
    await client.send_message(message.channel, output)
