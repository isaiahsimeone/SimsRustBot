
async def get_team_chat(socket):
    try:
        return await socket.get_team_chat()
    except:
        return None