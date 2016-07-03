import requests
import time
import Config
import TimeFunc
import json

def getCatFacts(num):
    #Thanks to CatFacts-API.apppot.com!
    r = requests.get("http://catfacts-api.appspot.com/api/facts?number="+str(num))
    print(r.text)
    x = json.loads(r.text)
    outputString = ""
    for i in range(0,num,1):
        outputString += "- "+str(x["facts"][i]) + "\n"
    return outputString

def getCatPic():
    #Thanks to TheCatAPI.com!
    r = requests.get("http://thecatapi.com/api/images/get?format=src")
    return r.url

def YandereGET(tag,num,site):
    #Thanks to Yande.re!
    #site 0 = yand.re
    #site 1 = konachan.com
    #site 2 = lolibooru.moe
    if site == 0:
        siteURL = "https://yande.re/post.json?limit=1&page="
    elif site == 1:
        siteURL = "http://konachan.com/post.json?limit=1&page="
    elif site == 2:
        siteURL = "https://lolibooru.moe/post.json?limit=1&page="
    if tag.replace(" ","") == "":
        r = requests.get(siteURL+str(num))
    else:
        r = requests.get(siteURL+str(num)+"&limit=1&tags="+tag)
    #print(r)
    p = r.text.replace("[{","")
    p = p.replace("}]","")
    p = p.replace(" ","%20")
    p2 = p.split(",")
    if len(p2) == 1:
    #    if tags.replace(" ","") != "":
    #        r = requests.get(siteURL+"1$tags="+tag)
    #        p = r.text.replace("[{","")
    #        p = r.text.replace("}]","")
    #        p2 = p.split(",")
    #        if len(p2) == 1:
    #            return "Invalid Tag"
    #    else:
         return "Invalid Tag"
    else:
        p3 = p2[10].replace('"file_url":"',"")
        p3 = p3.replace('"',"")
        return p3

def RedditGET(user):
    r = requests.get("https://www.reddit.com/user/"+str(user)+"/about.json")
    if "Too Many Requests" in r.text:
        return "Too Many Requests"
    else:
        print(r)
        p = r.text.replace('"link_karma": ','')
        p = p.replace('"comment_karma": ','')
        p = p.replace('"is_gold": ','')
        p = p.replace('"gold_expiration": ',"")
        p2 = p.split(",")
        print(p2)
        p3 = [p2[51],p2[59],p2[45],p2[41]]
        return p3

#Not Working RN
def AniListLogin():
    LastGenerated = Config.GET("AniList","Time")
    if TimeFunc.deltaTimeTrue(LastGenerated,time.time(),3600):
        r = requests.post("https://anilist.co/api/auth/access_token?grant_type=client_credentials&client_id=nightshadeneko-ulodg&client_secret=n2fwrgo05NxgSYX2gL2xsNn")
        print("AniList Token Requested")
        print(r.content)
        print("-----------------")
        p = json.loads(r.text)
        Config.WRITE("AniList","Token",p["access_token"])
        Config.WRITE("AniList","Time",str(int(time.time())))
    return Config.GET("AniList","Token")
def AniListGET(search):
    token = AniListLogin()
    r = requests.get("https://anilist.co/api/anime/search/"+search+"?access_token="+token)
   # print(r.content)
    if not "id" in r.text:
        #print(r.text)
        return "Incorrect Search Term"
    else:
        p = json.loads(r.text)
        output = "Title: "+p[0]["title_romaji"]+"\n"
        output += "Status: "+p[0]["airing_status"]+"\n"
        output += "Total Episodes: "+str(p[0]["total_episodes"])+"\n"
        output += "Score: "+p[0]["average_score"]+", Popularity: "+str(p[0]["popularity"])+"\n"
        output += p[0]["image_url_lge"]
        return output
def AniListAiringGET():
    token = AniListLogin()
    r = requests.get('https://anilist.co/api/browse/anime?sort=start_date-desc&status=Currently Airing&type=Tv&access_token='+token)
    #print(r.text)
    if not "id" in r.text:
        return "Incorrect Search Term"
    else:
        p = json.loads(r.text)
        output = ""
        num = len(p)
        if num > 30:
            num = 30
        for i in range(0,num,1):
            output += str(i+1) + "/ " + p[i]["title_romaji"]+"\n"
        return output
