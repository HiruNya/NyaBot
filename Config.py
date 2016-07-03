import configparser
config = configparser.ConfigParser()
config.read("config.ini")

def GET(section,key):
    return config[section][key]

def WRITE(section,key,value):
    #config[section][key]=value
    if CHECK(section,value)==0:
        config.add_section(section)
    config.set(section,key,str(value))
    with open('Config.ini','w') as file:
        config.write(file)

def CHECK(section,value):
    check = str(section) in config
    if check:
        check = str(value) in config[section]
        if check:
            return 2
        else: return 1
    else: return 0

def REMOVE(section,key):
    config.remove_option(section,key)
