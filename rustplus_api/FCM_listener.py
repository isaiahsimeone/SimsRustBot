from rustplus import FCMListener
import json


class FCM(FCMListener):
    
    def on_notification(self, obj, notification, data):
        print("Got notification from server:", notification)
        
        