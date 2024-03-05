from .command import Command
from .command_registry import command


@command
class CountItemsCommand(Command):
    def get_aliases(self):
        return ["count", "itemcount", "howmany", "storage", "checkstorage", "checkitems"]

    async def execute(self, rust_api, sender_steam_id, args=[]):
        if len(args) != 1:
            await rust_api.send_game_message("Provide exactly one item name. For multi-word items, remove spaces")
            return
        if args[0] == "":
            await rust_api.send_game_message("Provide an item name")
        
        item = args[0]
        item_count = rust_api.storage_monitor_manager.get_item_count(item)
        
        if item_count == -1: # Unknown item name
            alternative = rust_api.rust_item_name_manager.suggest_closest_match(item)
            await rust_api.send_game_message(f"Unknown item '{item}'. Did you mean '{alternative}'?")
        elif item_count == 0:
            await rust_api.send_game_message(f"You have 0 {item}")
        else:
            await rust_api.send_game_message(f"{item}: {item_count}")

    def help(self):
        pass