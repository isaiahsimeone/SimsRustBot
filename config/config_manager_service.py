
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

import loguru

from ipc.data_models import Test
from util.tools import Tools
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

import os 

# The path containing the .json config files ("." by default (same level as run.py))
CONFIG_PATH = "."


class ConfigManagerService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        
        self.config = {}
        
        self.load_config()
        self.load_fcm_credentials()
        self.load_server_details()

            
    @loguru.logger.catch
    async def execute(self):
        await self.publish("global", Message(Test(content="theresponse")))
        
    
    def load_config(self):
        if not Tools.file_exists(f"{CONFIG_PATH}/config.jfson"):
            self.warning(f"Could not find {CONFIG_PATH}/config.json. I am creating a default one")
            self.generate_default_config()
        pass
    
    def load_fcm_credentials(self):
        pass
    
    def load_server_details(self):
        pass
    
    def validate_server_details(self):
        pass

    def generate_default_config(self):
        pass
    
    async def on_message(self, topic: str, message: Message):
        self.debug(f"Bus message ({topic}):", message)
