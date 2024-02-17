
async def send_message(socket, message, sender=None):
    author = ""
    if sender:
        author = f"[{sender}]"
    await socket.send_team_message("[BOT] " + str(author) + " " + str(message))