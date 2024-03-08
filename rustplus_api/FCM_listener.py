from __future__ import annotations
from typing import TYPE_CHECKING


from ipc.data_models import RustDeviceAlarmMessage, RustDevicePaired

from ipc.message import Message, MessageType


if TYPE_CHECKING:
    from rust_plus_api import RustPlusAPI
    from ipc.bus import BUS
    from rustplus import RustSocket
    
from rustplus import FCMListener
import json
from enum import Enum
import asyncio
class DeviceType(Enum):
    SWITCH = 1
    ALARM = 2
    STORAGE_MONITOR = 3

class FCM(FCMListener):
    def __init__(self, fcm_details, rust_api: RustPlusAPI):
        super().__init__(fcm_details)
        self.api = rust_api
        self.log = rust_api.log
        
    def on_notification(self, obj, notification, data_message):
        asyncio.run(self.handle_notification(obj, notification, data_message))
        
    async def handle_notification(self, obj, notification, data_message):
        print(notification)
        data = notification['data']
        body = json.loads(data['body'])
        
        if data['channelId'] == "pairing" and 'entityType' in body: # Discard server pairing message
            self.log("Paring request", body['entityName'], "ID", body['entityId'])
            if not await self.valid_device(body['entityId'], body['entityType']):
                print(f"Ignoring device {body['entityId']} that isn't present on the server")
            else:
                await self.add_device(data)
        elif data['channelId'] == "alarm":
            await self.process_alarm_message(data)
            self.log(f"An Alarm said: {data['title']} : {data['message']}")
            
    async def valid_device(self, eid, etype):
        match etype:
            case DeviceType.SWITCH.value:
                # hopefully this is all good - dont want to turn shit on, which seems to be the only way to check
                return True
            case DeviceType.ALARM.value:
                # We just listen to these, so it doesn't matter
                return True
            case DeviceType.STORAGE_MONITOR.value:
                try:
                    await self.api.socket.get_contents(eid)
                    return True
                except:
                    return False
            case _:
                print(f"Big fuckup: Somehow got a device with ID {eid}?")
        return True
    
    async def add_device(self, data):
        self.log(f"Adding device- :", data)
        body = json.loads(data['body'])
        self.log(body['entityType'], " =?= ", DeviceType.SWITCH.value)

        msg = {'id': body['entityId'], 'name': body['entityName'], 
               'dev_type': body['entityType'], 'state': '0'}
        self.api.BUS.db_insert("device", msg)
        if int(body['entityType']) == DeviceType.SWITCH.value:
            print("ITS A SWITCH")
            self.api.event_listener.update_smart_switch_handlers() #type:ignore
            
        msg = RustDevicePaired(
            id=body['EntityId'],
            name=body['entityName'],
            dev_type=body['entityType'],
            state=False
        )
        
        await self.api.send_message(Message(MessageType.DEVICE_PAIRED, msg))
        
    async def process_alarm_message(self, data):
        msg = RustDeviceAlarmMessage(title=data['title'], message=data['message'])
        await self.api.send_message(Message(MessageType.DEVICE_ALARM_MSG, msg))