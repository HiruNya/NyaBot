from random import randint

MILKTEA = (
    "Original",
    "Jasmine",
    "Green Tea",
    "Coconut",
    "Papaya",
    "Sesame",
    "Coffee",
    "Barley",
    "Lavender",
    "Mung Bean",
    "Red Bean",
    "Lychee",
    "Osmanthus Flower",
    "Juice Ginger Brown Sugar",
    "Caramel",
    "Pudding",
    "Hazelnut",
    "Vanilla",
    "Taro",
    "Almond",
    "Chocolate",
    "Chrysanthemum",
    "Strawberry",
    "Green Apple",
    "Peach",
    "White Chocolate",
    "Watermelon",
    "Rose",
    "Mango"
    )

async def help(client, message):
    output = "Here are all the commands you can do:\n"
    output += "Music Features - **NO LONGER WORKS**\n```\n"
    output += "!start - Starts the bot on the voice channel you are in\n"
    output += "!play - Plays the music from a video from youtube\n"
    output += "!stop - The bot leaves the channel\n"
    output += "!pause - Pauses the music\n"
    output += "!volume - Changes to the volume (in % and max is 200%)\n"
    output += "!skip - Skips the current song\n"
    output += "```\n"
    output += "Searches Anime Image Sites:\n```\n"
    output += "!nyandere [tag] - Searches yande.re for a specific tag\n"
    output += "!nyandere reset - Resets the counter for the posts in yande.re\n"
    output += "!konyachan [tag] - Searches konachan for a specific tag\n"
    output += "!konychan reset - Resets the counter for the posts in konachan"
    output += "```\n Other Cool Stuff:\n```\n"
    output += "!ping - Checks if the bot is running\n"
    output += "!lol [Summoner Name] - Gives the profile for a specific summoner in League of Legends\n"
    output += "!osu [Name] - Gives the profile for a person in the game OSU!\n"
    output += "!yt [Search Term] - Searches Youtube and gives the link to it\n"
    output += "!roll dice - Rolls a metaphorical dice\n"
    output += "!flip coin - Flips a metaphorical coin\n"
    output += "!milk tea - Suggest a flavour of milk tea\n"
    output += "```"
    await client.send_message(message.channel, output)

async def probability(dice):
    if dice == 0:
        num = randint(0, 1)
        output = "Coin Flip: "
        if num == 0:
            output += "Heads"
        else:
            output += "Tails"
    else:
        output = "Dice Roll: "+str(randint(1, 6))
    return output

async def fund(client, message):
    await client.send_message(message.channel, "Not available until you FUCKING FUND MY RASPBERRY PI!")

async def run(client, message):
    msg = message.content.lower()
    dest = message.channel
    if msg.startswith("fuck you") or msg.startswith("fuk u"):
        await client.send_message(dest, "No, Fuck You!")
    elif msg.startswith("boice"):
        await client.send_message(dest, "nice")
    elif msg.startswith("hi ") or msg == "hi":
        await client.send_message(dest, "hooyaa")
    elif "whelan" in msg:
        await client.send_message(dest, await probability(1))
    elif msg.startswith("!milk tea"):
        num = randint(0, len(MILKTEA)-1)
        await client.send_message(dest, "You should get the {0} Milk Tea!".format(MILKTEA[num]))
    elif msg.startswith("!flip coin"):
        await client.send_message(dest, await probability(0))
    elif msg.startswith("!roll dice"):
        await client.send_message(dest, await probability(1))
