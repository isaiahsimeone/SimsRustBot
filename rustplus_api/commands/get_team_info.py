from ipc.serialiser import serialise_API_object

async def get_team_info(socket):
    return (await socket.get_team_info())