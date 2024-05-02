
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, List

import loguru

from ipc.data_models import DevicePaired, SmartSwitchStates
from rust_socket.rust_socket_manager import RustSocketManager

if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

ENTITY_TYPE_SMART_SWITCH = "1"

class SmartSwitchManagerService(BusSubscriber, Loggable):
    
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocketManager
        
        self.paired_smart_switches: List[dict] = []
        self.switch_states: dict[str, bool] = {} # True == switch on
    
    @loguru.logger.catch
    async def execute(self: SmartSwitchManagerService) -> None:
        await self.subscribe("device_paired")
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        
        # Get the currently paired devices
        paired_devices = (await self.last_topic_message_or_wait("paired_devices")).data["devices"]
        for device in paired_devices:
            print("********Checking device", device)
            if device.get("entityType", "") == ENTITY_TYPE_SMART_SWITCH:
                self.paired_smart_switches.append(device)
        
            
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = await RustSocketManager.get_instance()

        # Fetch the state of the switches
        for switch in self.paired_smart_switches:
            switch_status = await self.is_switch_enabled_in_game(switch["entityId"], switch["steam_id"])
            self.switch_states[switch["entityId"]] = switch_status
        
        await self.publish("smart_switch_states", SmartSwitchStates(switches=self.switch_states))
        
        self.warning("************************************************")
        print("SWITCH STATES", self.switch_states.items())
        self.warning("************************************************")

        # We just polled all the switches. That'll be good for a bit. Save some tokens
        await asyncio.sleep(10)

        # Smart Switch Polling loop
        switch_index = 0
        total_switches = len(self.paired_smart_switches)
        while True:
            if not self.paired_smart_switches:
                await asyncio.sleep(5)
                self.debug("paired_smart_switches is empty")
                continue
            
            current_number_switches = len(self.paired_smart_switches)
            if total_switches != current_number_switches:
                total_switches = current_number_switches
            
            # Ensure index is valid, adjust for changes in list size
            switch_index %= total_switches
            
            switch_eid = self.paired_smart_switches[switch_index].get("entityId")
            switch_owner_steam_id = self.paired_smart_switches[switch_index].get("steam_id")
            
            if switch_eid:
                is_switch_enabled = await self.is_switch_enabled_in_game(switch_eid, switch_owner_steam_id)
                self.switch_states[switch_eid] = is_switch_enabled
            
            if switch_index == total_switches - 1:
                self.debug("Checked all switches. Going to start of list")
                await self.publish("smart_switch_states", SmartSwitchStates(switches=self.switch_states))
                await asyncio.sleep(9) # Wait 9 seconds
                switch_index = 0
            else:
                switch_index += 1
        
    async def is_switch_enabled_in_game(self, eid: str, switch_owner_steam_id) -> bool:
        self.debug("Checking: ", eid)
        entity_info = await self.socket.get_entity_info(eid, switch_owner_steam_id)
        if not entity_info:
            self.error("Entity info is none? entityId is", eid, "steam_id is", switch_owner_steam_id)
            return False
        print("entity info val:", entity_info.value)
        return entity_info.value
        
    # Someone requests status of a smart switch (on or off) or a list of smart switches
    async def on_message(self: SmartSwitchManagerService, topic: str, message: Message):
        match topic:
            case "device_paired": # Message is of type DevicePaired
                if message.data["entityType"] == ENTITY_TYPE_SMART_SWITCH:
                    self.paired_smart_switches.append(message.data)
            case _:
                self.error(f"Encountered topic {topic} that I don't have a case for")
        """            pairing_message = DevicePaired(
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
        """