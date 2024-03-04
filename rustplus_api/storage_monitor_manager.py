from ipc.serialiser import serialise_API_object
import asyncio
from .rust_item_collection import RustItemCollection

class StorageMonitorManager:
    def __init__(self, socket, BUS, item_name_manager):
        self.socket = socket
        self.BUS = BUS
        self.should_poll = BUS.get_config().get("rust").get("storage_monitor_should_poll")
        self.poll_rate = int(BUS.get_config().get("rust").get("storage_monitor_polling_frequency_seconds"))
        
        self.monitor_ids = []
        self.all_monitor_contents = None
        
        self.name_manager = item_name_manager
    
    
    async def start_storage_polling(self):
        self.get_monitor_ids()
        while self.should_poll:
            print("poll monitors")
            await self.poll_storage()
            await asyncio.sleep(self.poll_rate)
            
    async def poll_storage(self):
        await self.get_all_items()
        print("wire tool count:", self.get_item_count("-2139580305"))
        print("Did you mean:",self.name_manager.suggest_closest_match("rifle incendiary shots"))
        
    async def get_monitor_items(self, monitor_id):
        monitor_contents_raw = (await self.socket.get_contents(monitor_id)).contents
        item_collection = RustItemCollection(self.name_manager)
        for item in monitor_contents_raw:
            item_collection.insert((item.name, item.item_id, item.quantity))
        
        return item_collection
    
    async def get_all_items(self):
        self.all_monitor_contents = RustItemCollection(self.name_manager)
        
        for monitor in self.monitor_ids:
            self.all_monitor_contents.insert_collection(await self.get_monitor_items(monitor))
            
        #print(self.all_monitor_contents)
    
    def get_monitor_ids(self):
        """
        Get the IDs of all rust+ devices that are storage monitors
        """
        monitors = self.BUS.db_query("id", "Devices", "dev_type=3")
        self.monitor_ids = [monitor[0] for monitor in monitors]
        print("Monitors:", self.monitor_ids)
    
    def get_item_count(self, item_name):
        """
        Get the quantity of a specific item in the collection
        """
        return self.all_monitor_contents.quantity_by_name(item_name)

    # Called from outside when there's a new monitor, or one is gone 
    def update_monitor_ids(self):
        self.get_monitor_ids()

