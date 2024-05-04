from __future__ import annotations
from typing import TYPE_CHECKING

from rust_socket.rust_socket_manager import RustSocketManager

    
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def get_aliases(self):
        return []

    @abstractmethod
    async def execute(self, socket: RustSocketManager, publish, sender_steam_id: str, args=[]):
        pass
    
    """
    @abstractmethod
    async def execute_web(self, web_server, sender_steam_id, args=[])
        pass
    """
    
    @abstractmethod
    def help(self):
        pass