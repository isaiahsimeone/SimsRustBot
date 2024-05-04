from typing import Coroutine
from ipc.data_models import CommandTime
from log.loggable import Loggable
from rust_socket.rust_socket_manager import RustSocketManager
from .command import Command
from .command_registry import command

@command
class GetPopulationCommand(Command, Loggable):
    def get_aliases(self):
        return ["pop", "playercount", "getplayercount", "howmanyplayers", "population", "popcount", "playerpopulation", "playerpop"]

    async def execute(self, socket: RustSocketManager, publish, sender_steam_id: str, args=[]):
        try:
            response = await socket.get_info()
            player_count = response.players
            max_players = response.max_players
            queued_players = response.queued_players
            
            msg = f"There are {player_count}/{max_players} online"
            
            if queued_players != 0:
                msg += f". There are {queued_players} in queue"
            
            await publish("command_result", CommandTime(command="get_population", message=msg))

        except Exception as e:
            self.error(f"Failed to execute GetPopulationCommand: {e}")
    
    def help(self):
        pass
