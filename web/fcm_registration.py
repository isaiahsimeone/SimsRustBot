from push_receiver import register, listen
import json
import requests
import uuid
from messenger import Messenger, Service
from flask import Flask, render_template, request
import threading

FCM_SENDER_ID = 976529667804

class FCMRegistration:
    def __init__(self, messenger):
        self.messenger = messenger
        self.messenger.subscribe(Service.FCMREGISTRAR, self.process_message)
        self.messenger.print(Service.FCMREGISTRAR, "FCM Registrar subscribed for messages")
        

    def register_with_fcm(self):
        self.messenger.print(Service.FCMREGISTRAR,"Registering with FCM")
        fcm_token = register(str(FCM_SENDER_ID))
        
        self.messenger.print(Service.FCMREGISTRAR,"Fetching expo push token")
        expo_token = self.get_expo_token(fcm_token)
        
        self.messenger.print(Service.FCMREGISTRAR, "Expo Token:", expo_token)
        
        self.messenger.print(Service.FCMREGISTRAR, "Launching web server for callback")
        rust_auth_token = self.link_steam_with_rust_plus()
        
        self.messenger.print(Service.FCMREGISTRAR, "Got rust_auth token:", rust_auth_token)
        
    def get_expo_token(self, fcm_token):
        response = requests.post('https://exp.host/--/api/v2/push/getExpoPushToken', json={
            'deviceId': str(uuid.uuid4()),
            'experienceId': '@facepunch/RustCompanion',
            'appId': 'com.facepunch.rust.companion',
            'deviceToken': fcm_token,
            'type': 'fcm',
            'development': False
        })
        return response.json()['data']['expoPushToken']


    
    def link_steam_with_rust_plus(self):
        token = None
        
        @app.route('/')
        def index():
            return render_template("pair.html")

        @app.route('/callback')
        def callback():
            nonlocal token
            token = request.args.get('token')
            if token:
                return 'Steam Account successfully linked with rustplus.py'
            else:
                return 'Token missing from request!'
            
        def run():
            app.run(port=3000)

        threading.Thread(target=run).start()
        
        # busy wait until token populated
        while token is None:
            pass
        
        return token
    
    def process_message(self):
        pass