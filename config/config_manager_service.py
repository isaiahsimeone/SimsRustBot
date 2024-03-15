
from __future__ import annotations

import asyncio
import json
import threading
from pathlib import Path
from typing import TYPE_CHECKING

from watchdog.observers import Observer

from ipc.bus_subscriber import BusSubscriber
from ipc.data_models import Config
from ipc.message import Message
from log.loggable import Loggable
from util.file_watchdog import FileWatchdog
from util.tools import Tools

if TYPE_CHECKING:
    from ipc.message_bus import MessageBus

class ConfigManagerService(BusSubscriber, Loggable):
    def __init__(self: ConfigManagerService, bus: MessageBus) -> None:
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config_filepath = "./config.json"

        self.initial_config = {}
        self.config = {}

    async def execute(self: ConfigManagerService) -> None:
        await self.subscribe("get_config")
        await self.load_config()

        # Watch for changes to config files
        await self.watch_configs_for_change()

        # Run forever
        await asyncio.Future()

    async def publish_config(self: ConfigManagerService) -> None:
        config = Config(config=self.config)
        await self.publish("config", Message(config))

    async def watch_configs_for_change(self: ConfigManagerService) -> None:
        config_file_watcher = FileWatchdog(self.config_filepath, callback=self.load_config)

        observer = Observer()
        observer.schedule(config_file_watcher, path=Path(self.config_filepath).parent, recursive=False)
        observer_thread = threading.Thread(target=observer.start, daemon=True)
        observer_thread.start()

    async def load_config(self: ConfigManagerService) -> None:
        self.debug(f"Loading config {self.config_filepath}")

        if not Tools.file_exists(self.config_filepath):
            self.warning(f"Could not find {self.config_filepath}. I am creating a default one")
            self.generate_default_config()

        # Load JSON config into dictionary
        try:
            with open(self.config_filepath, mode="r") as config_file:
                self.config = json.load(config_file)
        except json.JSONDecodeError:
            self.critical(f"Failed to read JSON from {self.config_filepath}")

        # Save initial config before updating with fcm and server keys
        self.initial_config = self.config

        # Load the FCM credentials file into the dictionary
        fcm_filepath = self.config["servers"]["fcm_filepath"]
        if not fcm_filepath:
            self.critical("Cannot find fcm_filepath in JSON. Check your config.json")
        if not Tools.file_exists(fcm_filepath):
            self.critical(f"There is no file: {fcm_filepath}")
        self.debug(f"fcm_credentials are at {fcm_filepath}")

        try:
            with open(fcm_filepath, mode="r") as fcm_file:
                self.config["fcm_credentials"] = json.load(fcm_file)
        except json.JSONDecodeError:
            self.critical(f"Failed to read JSON from {fcm_filepath}")

        # Load the server details file into the dictionary
        servers_path = self.config["servers"]["server_configs_path"]
        selected_server = self.config["servers"]["selected_server"]
        selected_server_filepath = f"{servers_path}/{selected_server}"

        if not selected_server_filepath:
            self.critical(f"Cannot find selected server JSON file ({selected_server_filepath}). Check your config.json")
        if not Tools.file_exists(selected_server_filepath):
            self.critical(f"There is no file: {selected_server_filepath}")
        self.debug(f"Config for selected server is at {selected_server_filepath}")

        try:
            with open(selected_server_filepath, mode="r") as selected_server_file:
                self.config["server_details"] = json.load(selected_server_file)
        except json.JSONDecodeError:
            self.critical(f"Failed to read JSON from {selected_server_filepath}")

        self.info(f"Config has been loaded - {self.config_filepath}, {fcm_filepath}, {selected_server_filepath}")
        await self.publish_config()

    def generate_default_config(self: ConfigManagerService) -> None:
        with open("./config/_default_config.json", mode="r") as default, open(self.config_filepath, "w") as config:
            config.write(default.read())

        self.debug(f"Created default config {self.config_filepath}")

    """
    async def change_server(self: ConfigManagerService, new_server_file: str):
        self.info("Changing server. The new server file is ", new_server_file)
        self.initial_config["servers"]["selected_server"] = new_server_file
        await self.update_config()
    """

    async def update_config(self: ConfigManagerService) -> None:
        with open(self.config_filepath, mode="w") as config_file:
            json.dump(self.initial_config, config_file, indent=4)
        self.info(f"Updated {self.config_filepath}")
        # Then reload it
        await self.load_config()

    async def on_message(self: ConfigManagerService, topic: str, message: Message) -> None:
        self.debug(f"Bus message ({topic}):", message)

        # A service is requesting the config
        if topic == "get_config":
            config = Config(config=self.config)
            await self.publish("config", Message(config))
            # We should update our socket here
