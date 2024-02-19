from rustplus import RustSocket, ChatEvent, CommandOptions, FCMListener
import asyncio
import json

def hexdump(src: bytes, bytesPerLine: int = 16, bytesPerGroup: int = 4, sep: str = '.'):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
    lines = []
    maxAddrLen = len(hex(len(src)))
    if 8 > maxAddrLen:
        maxAddrLen = 8

    for addr in range(0, len(src), bytesPerLine):
        hexString = ""
        printable = ""

        # The chars we need to process for this line
        chars = src[addr : addr + bytesPerLine]

        # Create hex string
        tmp = ''.join(['{:02X}'.format(x) for x in chars])
        idx = 0
        for c in tmp:
            hexString += c
            idx += 1
            # 2 hex digits per byte.
            if idx % bytesPerGroup * 2 == 0 and idx < bytesPerLine * 2:
                hexString += " "
        # Pad out the line to fill up the line to take up the right amount of space to line up with a full line.
        hexString = hexString.ljust(bytesPerLine * 2 + int(bytesPerLine * 2 / bytesPerGroup) - 1)

        # create printable string
        tmp = ''.join(['{}'.format((x <= 127 and FILTER[x]) or sep) for x in chars])
        # insert space every bytesPerGroup
        idx = 0
        for c in tmp:
            printable += c
            idx += 1
            # Need to check idx because strip() would also delete genuine spaces that are in the data.
            if idx % bytesPerGroup == 0 and idx < len(chars):
                printable += " "

        lines.append(f'{addr:0{maxAddrLen}X}  {hexString}  |{printable}|')
    return lines

with open("test/rustplus.py.config.json", "r") as input_file:
    fcm_details = json.load(input_file)

class FCM(FCMListener):
    
    def on_notification(self, obj, notification, data_message):
        print(notification)
        
FCM(fcm_details).start()

async def chat_event_handler(event: ChatEvent):
    print(f"{event.message.name}: {event.message.message}")

async def proto_event_handler(data: bytes):
    for line in hexdump(data.byte_data):
        print(line)
    
async def main():
    socket = RustSocket("49.2.177.161", "28083", 76561198032291162, -1746662161)
    await socket.connect()

    # Register event handlers
    socket.chat_event(chat_event_handler)
    socket.protobuf_received(proto_event_handler)

    print(f"It is {(await socket.get_time()).time}")

    # Keep the script running to listen to events
    await asyncio.Future()  # This will keep the script running indefinitely

    await socket.disconnect()

asyncio.run(main())
