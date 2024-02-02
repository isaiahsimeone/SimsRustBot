
async def send_message(socket, message):
    await socket.send_team_message(message)
    print(f"It is {(await socket.get_time()).time}")