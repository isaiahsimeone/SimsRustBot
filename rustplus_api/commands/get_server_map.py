import base64
from util.tools import Tools

async def get_server_map(socket):
    #server_info = await socket.get_info()
    map_image = await socket.get_map()
    
    pixel_data = list(map_image.getdata())

    image_dict = {
        'width': map_image.width,
        'height': map_image.height,
        'pixels': pixel_data
    }
    
    return image_dict