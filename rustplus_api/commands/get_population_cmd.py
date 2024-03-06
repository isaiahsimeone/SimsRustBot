from .command import Command
from .command_registry import command

@command
class GetPopulationCommand(Command):
    def get_aliases(self):
        return ["pop", "playercount", "getplayercount", "howmanyplayers", "population", "popcount", "playerpopulation", "playerpop"]

    async def execute(self, rust_api, sender_steam_id, args=[]):
        try:
            response = await rust_api.get_socket().get_info()
            player_count = response.players
            max_players = response.max_players
            queued_players = response.queued_players
            
            msg = f"There are {player_count}/{max_players} online"
            
            if queued_players != 0:
                msg += f". There are {queued_players} in queue"
            
            await rust_api.send_game_message(msg)

        except Exception as e:
            rust_api.log(f"Failed to execute GetPopulationCommand: {e}", type="error")
    
    def help(self):
        pass
