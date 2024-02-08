from ipc.serialiser import serialise_API_object

async def get_monuments(socket):
    monuments = (await socket.get_raw_map_data())
    
    return monuments