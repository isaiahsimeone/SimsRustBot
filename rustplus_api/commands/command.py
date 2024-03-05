from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rust_plus_api import RustPlusAPI
    
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def get_aliases(self):
        return []

    @abstractmethod
    async def execute(self, rust_api: RustPlusAPI, sender_steam_id, args=[]):
        pass
    
    """
    @abstractmethod
    async def execute_web(self, web_server, sender_steam_id, args=[])
        pass
    """
    
    @abstractmethod
    def help(self):
        pass