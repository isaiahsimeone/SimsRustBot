
from __future__ import annotations
import asyncio
import difflib
from typing import TYPE_CHECKING, List

from commands.command_registry import CommandRegistry
from ipc.data_models import RustTeamChatMessage, SendChatMessage
from rust_socket.rust_socket_manager import RustSocketManager
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

class CommandExecutorService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocketManager
        
        self.prefix = "-" # TODO: get from config
        
    
    async def execute(self):
        await self.subscribe("team_message")
        # Get config
        self.config = await self.last_topic_message_or_wait("config")
        # Get socket
        await self.last_topic_message_or_wait("socket_ready")
        self.socket = await RustSocketManager.get_instance()
        
        #self.command_executor = CommandExecutor(self.socket, self.publish, "/") #TODO: get from config
        
        await asyncio.Future()
        
    async def parse_and_execute_command(self, message, sender_steam_id):
        if not message.startswith(self.prefix):
            return "" # Not a command

        # Remove the leader and split the input into components
        components = message[len(self.prefix):].split()
        if not components:
            return "" # not a command

        # The first component is the command name, the rest are arguments
        command_name, *args = components
        
        # Find and execute the command
        command = CommandRegistry.commands.get(command_name.lower())
        if command:
            self.debug(f"Executing command '{command}' with args {args}")
            topic, output = await command.execute(self.socket, self.publish, sender_steam_id, args)
            if output:
                await self.publish(topic, output)
        else:
            msg = f"Unknown command '{command_name}'. Did you mean '{self.suggest_closest_match(command_name)}'?"
            self.info(msg)
            await self.publish("send_chat_message", SendChatMessage(prefix="bot", message=msg))
            return "?:" + str(command_name) + ":" + str(self.suggest_closest_match(command_name))
        
        return ""
        
        # levenshtein distance
    def suggest_closest_match(self, command_name):
        """
        Levenshtein distance to determine which command is closest
        to a provided one (excluding itself)
        """
        # Get a list of all possible names and aliases
        all_names = list(CommandRegistry.commands.keys())
        self.debug("allnames=", all_names)
        # Use difflib to find the closest match(es)
        closest_matches = difflib.get_close_matches(command_name.lower(), all_names, n=1, cutoff=0.3)
        if closest_matches:
            return closest_matches[0]  # Return the closest match
        return "idk"  # No close match found

    async def on_message(self, topic: str, message: Message) -> None:
        match topic:
            case "team_message":
                self.debug("execute", message.data["message"])
                await self.parse_and_execute_command(message.data["message"], message.data["steam_id"])
            case _:
                self.error(f"I don't have a case for {topic}")
