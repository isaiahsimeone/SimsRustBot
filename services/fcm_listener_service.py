
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, List

import loguru

from rustplus import FCMListener

from ipc.data_models import DevicePaired, Empty, FCMMessage, PairedDevices, SmartAlarmMessage
from rust_socket.rust_socket_manager import RustSocketManager

if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable
import json
from rustplus import RustSocket

class FCMListenerService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        
        self.fcm_listeners: dict[int, FCMWorker]
        
        self.encountered_fcm_messages: set[str] = set()
        self.paired_devices: list[DevicePaired] = []
        self.paired_device_entity_ids: set[str] = set()
    
    
    @loguru.logger.catch
    async def execute(self):
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        
        # Create an FCM listener for the leader socket
        leader_fcm_credentials = self.config["fcm_credentials"]
        leader_steam_id = self.config["server_details"]["playerId"]
        server_ip_addr = self.config["server_details"]["ip"]
        
        # Get a list of encountered FCM message Ids. Some duplicated messages
        # Will arrive as soon as the FCM workers start, we need to check that they haven't 
        # been encountered, so we don't transmit them again
        self.encountered_fcm_messages = (await self.last_topic_message_or_wait("database_encountered_fcm_messages")).data["encountered_messages"]
        
        # Publish the devices that are paired
        self.paired_devices = (await self.last_topic_message_or_wait("database_paired_devices")).data["devices"]
        for device in self.paired_devices:
            self.paired_device_entity_ids.add(device["entityId"])
            
        print("entity ids paired is=", self.paired_device_entity_ids)

        await self.publish("paired_devices", PairedDevices(devices=self.paired_devices))
        
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        
        FCMWorker(leader_fcm_credentials, leader_steam_id, server_ip_addr, self).start()
        
        await asyncio.Future()
        
    

    @loguru.logger.catch
    async def on_message(self: FCMListenerService, topic: str, message: Message):
        pass


# Wrap one of these for each socket
class FCMWorker(FCMListener, Loggable):
    def __init__(self, fcm_credentials: dict, steam_id: str, only_from_ip: str, fcm_listener_service: FCMListenerService):
        self.steam_id: str = steam_id
        self.fcm_listener_service = fcm_listener_service
        self.only_from_ip = only_from_ip
        super().__init__(fcm_credentials)
        self.info("Started FCM listener worker for", steam_id)

    def on_notification(self, obj, notification, data_message) -> None:
        asyncio.run(self.handle_notification(obj, notification, data_message))
        
    async def device_exists_in_game(self, eid, device_type):
        pass
    
    async def handle_notification(self, obj, notification, data_message) -> None:
        data = ""
        body = ""
        try:
             data = notification["data"]
             body = json.loads(data["body"])
        except Exception as e:
            self.error("Failed to parse FCM message. Ignoring")
            print(notification)
            return None
        
        if body.get("ip", "") != self.only_from_ip:
            self.debug("Dropping FCM message intended for a different rust server")
        
        fcm_message = FCMMessage(entityType=body.get("entityType", "alarm"), # If entityType is not there, it's a smart alarm
                           ip=body["ip"],
                           steam_id=body.get("playerToken", ""),
                           entityId=body.get("entityId", ""),
                           entityName=body.get("entityName", "alarm"),
                           server_id=body["id"],
                           message=data["message"],
                           title=data["title"],
                           channelId=data["channelId"],
                           fcm_message_id=notification["fcmMessageId"])
        
        # Don't publish if it's been encountered already
        if fcm_message.fcm_message_id in self.fcm_listener_service.encountered_fcm_messages:
            self.debug("Discarding FCM message that has already been encountered")
            return None
        
        # Primarily for database service to record
        await self.fcm_listener_service.publish("fcm_message", fcm_message)
        
        # Smart alarm message
        if data.get("channelId", "") == "alarm":
            model = SmartAlarmMessage(title=data["title"], message=data["message"], steam_id=self.steam_id)
            await self.fcm_listener_service.publish("smart_alarm_message", model)
            return None
        
        # Pairing message
        if data.get("channelId", "") == "pairing": # TODO: ensure entity id not in paired devices
            if fcm_message.entityId in self.fcm_listener_service.paired_device_entity_ids:
                self.debug("Not sending pair message about device we've already encountered (entityId in database)")
                return None

            pairing_message = DevicePaired(
                            entityType=body.get("entityType", ""),
                            ip=body["ip"],
                            entityId=body.get("entityId", ""),
                            steam_id=body.get("playerToken", ""),
                            entityName=body.get("entityName", ""),
                            server_id=body["id"],
                            message=data["message"],
                            title=data["title"],
                            channelId=data["channelId"],
                            fcm_message_id=notification["fcmMessageId"])
            
            await self.fcm_listener_service.publish("device_paired", pairing_message)
            
            # Add this device to the list of paired devices, then publish that list
            self.fcm_listener_service.paired_devices.append(pairing_message)
            # This device has been seen
            self.fcm_listener_service.paired_device_entity_ids.add(fcm_message.entityId)
            await self.fcm_listener_service.publish("paired_devices", PairedDevices(devices=self.fcm_listener_service.paired_devices))

    
    
    