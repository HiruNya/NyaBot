async def run(client, message):
    msg = message.content.lower()
    dest = message.channel
    if "fuck you" in msg:
        await client.send_message(dest, "No, Fuck You!")
    elif msg.startswith("boice"):
        await client.send_message(dest, "nice")