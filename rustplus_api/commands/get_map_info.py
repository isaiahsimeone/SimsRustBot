from ipc.serialiser import serialise_API_object

async def get_map_info(socket):
    return (await socket.get_raw_map_data())
    
     