"""The ConfigManagerService class is  designed to manage application configuration.
It handles loading, updating, and distributing configuration settings to various components.

The ConfigManagerService acts as both a subscriber and publisher on the message bus, enabling
it to respond to configuration requests and propagate configuration changes across the system.
It also monitors the configuration file for changes, reloading the configuration dynamically
and notifying subscribers of updates.
"""

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
    """A service for managing application configuration within an asynchronous message-driven architecture.

    The ConfigManagerService is responsible for loading the initial application configuration from a JSON
    file, monitoring the configuration file for changes, and dynamically updating the in-memory configuration.
    It publishes the current configuration to the message bus upon request and when changes are detected.

    Attributes
    ----------
        - bus (MessageBus): The message bus instance for publishing and subscribing to messages.
        - config_filepath (str): The file path to the main configuration file.
        - initial_config (dict): A dictionary representing the initial loaded configuration.
        - config (dict): A dictionary representing the current active configuration, including
                       dynamically loaded components such as FCM credentials and server details.

    The :class:`ipc.bus_subscriber.BusSubscriber` base class provides bus communication methods
    The :class:`logging_abc.Loggable` base class provides structured logging methods

    """

    def __init__(self: ConfigManagerService, bus: MessageBus) -> None:
        """Initialises the ConfigManagerService with a reference to the message bus.
        """
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config_filepath = "./config.json"

        self.initial_config = {}
        self.config = {}

    async def execute(self: ConfigManagerService) -> None:
        """The main point of execution for the service.

        :param self: This instance
        :type self: :class:`ConfigManagerService`
        """
        await self.subscribe("get_config")
        await self.load_config()

        # Watch for changes to config files
        await self.watch_configs_for_change()

        # Run forever
        await asyncio.Future()

    async def publish_config(self: ConfigManagerService) -> None:
        """Publish the contents of the config to the bus (:class:`ipc.message_bus.MessageBus`).

        :param self: This instance
        :type self: :class:`ConfigManagerService`
        """
        config = Config(config=self.config)
        await self.publish("config", Message(config))

    async def watch_configs_for_change(self: ConfigManagerService) -> None:
        """Watches the config file for changes.

        When the file specified by `self.config_filepath` changes, this method
        will call the `self.load_config` callback, indicating that the config
        file has changed, and thus reloading the config file.

        :param self: This instance
        :type self: :class:`ConfigManagerService`
        """
        config_file_watcher = FileWatchdog(self.config_filepath, callback=self.load_config)

        observer = Observer()
        observer.schedule(config_file_watcher, path=Path(self.config_filepath).parent, recursive=False)
        observer_thread = threading.Thread(target=observer.start, daemon=True)
        observer_thread.start()

    async def load_config(self: ConfigManagerService) -> None:
        """Load the config.json file.

        This method loads the config.json file from `self.config_filepath`. If
        a config file does not exist, this method will create a default one. Once
        the config file is loaded, the filepath of both fcm_credentials, and the selected
        server details will be loaded into `self.config`.

        :param self: This instance
        :type self: :class:`ConfigManagerService`
        """
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
        """Generate a default config.json file from the template file.

        :param self: This instance
        :type self: :class:`ConfigManagerService`
        """
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
        """Update the config file.

        Updates the config.json file from the dictionary `self.config`
        in this class.

        :param self: This instance
        :type self: :class:`ConfigManagerService`
        """
        with open(self.config_filepath, mode="w") as config_file:
            json.dump(self.initial_config, config_file, indent=4)
        self.info(f"Updated {self.config_filepath}")
        # Then reload it
        await self.load_config()

    async def on_message(self: ConfigManagerService, topic: str, message: Message) -> None:
        """Receive a message, under a subscribed topic, from the bus.

        :param self: This instance
        :type self: :class:`ConfigManagerService`
        :param topic: The topic of the message being received
        :type topic: str
        :param message: The message being received
        :type message: Message
        """
        self.debug(f"Bus message ({topic}):", message)

        # A service is requesting the config
        if topic == "get_config":
            config = Config(config=self.config)
            await self.publish("config", Message(config))
