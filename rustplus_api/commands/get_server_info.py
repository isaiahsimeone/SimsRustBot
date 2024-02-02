
async def get_server_info(socket):
    server_info = await socket.get_info()
    print(f"It is {(await socket.get_time()).time}")