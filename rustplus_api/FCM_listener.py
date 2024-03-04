from rustplus import FCMListener
import json
from enum import Enum

class DeviceType(Enum):
    SWITCH = 1
    ALARM = 2
    STORAGE_MONITOR = 3

class FCM(FCMListener):
    def __init__(self, fcm_details, rustAPI):
        super().__init__(fcm_details)
        self.rustAPI = rustAPI
        
    def on_notification(self, obj, notification, d):
        #print("Got notification from server:", notification)
        data = notification['data']
        body = json.loads(data['body'])
        
        if data['channelId'] == "pairing":
            print("**Paring request", body['entityName'], "ID", body['entityId'])
            msg = {'id': body['entityId'], 'name': body['entityName'], 'dev_type': body['entityType']}
            self.rustAPI.BUS.db_insert("device", msg)
        elif data['channelId'] == "alarm":
            print(f"An Alarm said: {data['title']} : {data['message']}")
            
