from __future__ import annotations
from typing import TYPE_CHECKING
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
        data = notification['data']
        body = json.loads(data['body'])
        
        if data['channelId'] == "pairing":
            self.log("Paring request", body['entityName'], "ID", body['entityId'])
            msg = {'id': body['entityId'], 'name': body['entityName'], 'dev_type': body['entityType']}
            if not await self.valid_device(body['entityId'], body['entityType']):
                print(f"Ignoring device {body['entityId']} that isn't present on the server")
            else:
                self.api.BUS.db_insert("device", msg)
        elif data['channelId'] == "alarm":
            self.log(f"An Alarm said: {data['title']} : {data['message']}")
            
    # TODO: Smart alarms have a state associated with them ,we should capture that in the DB
            
    async def valid_device(self, eid, etype):
        match etype:
            case DeviceType.SWITCH:
                # hopefully this is all good - dont want to turn shit on, which seems to be the only way to check
                return True
            case DeviceType.ALARM:
                # We just listen to these, so it doesn't matter
                return True
            case DeviceType.STORAGE_MONITOR:
                try:
                    await self.api.socket.get_contents(eid)
                except:
                    return False
            case _:
                print(f"Big fuckup: Somehow got a device with ID {eid}?")
        return True