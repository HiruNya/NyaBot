import socket
import json

s = socket.socket()
s.connect(("api.vndb.org",19534))

is_connected = 0

def Connect():
    global is_connected
    if is_connected == 0:
        y = 'login {"protocol":1,"client":"NyaBot","clientver":1}\x04'.encode('utf-8')
        #print(y)
        s.send(y)
        r = s.recv(1024)
        print("Connected - ",r)
        is_connected = 1
    
def closeConnection():
    s.close()
    print("VNDB Connection Closed")

def parse(string):
    string = string.replace('results ','')
    string = string.replace("b","")
    string = string.replace("'","")
    string = string.replace("\\x04","")
    string = string.replace("\\","")
    return string

def getDBStats():
    Connect()
    y = 'dbstats\x04'.encode('utf-8')
    s.send(y)
    r = str(s.recv(1024))
    r = r.replace("'","")
    r = r.replace("bdbstats ","")
    r = r.replace('\\x04',"")
    #print(r)
    p = json.loads(r)
    #print(p)
    output = "Users: "+str(p['users'])+"\n"
    output += "Threads: "+str(p['threads'])+"\n"
    output += "Tags: "+str(p['tags'])+"\n"
    output += "Releases: "+str(p['releases'])+"\n"
    output += "Producers: "+str(p['producers'])+"\n"
    output += "Chars: "+str(p['chars'])+"\n"
    output += "Posts: "+str(p['posts'])+"\n"
    output += "Visual Novels: "+str(p['vn'])+"\n"
    output += "Traits: "+str(p['traits'])+"\n"
    return output

def getVN(search):
    Connect()
    search = search.replace(" ","")
    #print(search)
    #tags = tags.replace(" ","")
    #tags = tags.replace(",",'and')
    #print(tags)
    #if search != "" and tags != "":
    #    term = ' ((search~"'+search+'")and(tags=("'+tags+'")))'
    #elif search == "" and tags != "":
    #    term = ' (tags="'+tags+'")'
    #elif search != "" and tags == "":
    #    term = ' (title~("'+search+'"))'
    if search != "":
        term = ' ((search~"'+search+'"))'
    else:
        term = ''
    #print(term)
    y = ('get vn basic,stats'+term+'{"results":1,"sort":"rating","reverse":true}\x04').encode('utf-8') 
    #print(y)
    x = s.send(y)
    #print(x)
    r = str(s.recv(1024))
    #print(r)
    if "error" in r:
        print(r)
        return "Error"
    else:
        r = parse(r)
        #print(r)
        p = json.loads(r)
        #print(p)
        output = "Title: "+p["items"][0]["title"]+"\n"
        #output += "Description: "+p["items"][0]["description"]+"\n"
        #output += "Length: "+str(p["items"][0]["length"])+"/5 \n"
        output += "Rating: "+str(p["items"][0]["rating"])+"/10 \n"
        output += "https://vndb.org/v"+str(p["items"][0]["id"])
        return output

def getVNId(idnum):
    Connect()
    idnum = idnum.replace(" ","")
    try:
        num = int(idnum)
    except ValueError:
        return "Not a Valid Number"
    y = ('get vn basic,stats (id='+str(num)+') {"results":1,"sort":"rating","reverse":true}\x04').encode('utf-8') 
    s.send(y)
    r = str(s.recv(1024))
    if "error" in r:
        return "Error"
    else:
        r = parse(r)
        p = json.loads(r)
        output = "Title: "+p["items"][0]["title"]+"\n"
        output += "Rating: "+str(p["items"][0]["rating"])+"/10 \n"
        output += "https://vndb.org/v"+str(p["items"][0]["id"])
        return output
        
