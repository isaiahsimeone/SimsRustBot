from ipc.serialiser import serialise_API_object
import asyncio

class StorageMonitorManager:
    def __init__(self, BUS):
        self.BUS = BUS
        self.should_poll = BUS.get_config().get("rust").get("storage_monitor_should_poll")
        self.poll_rate = int(BUS.get_config().get("rust").get("storage_monitor_polling_frequency_seconds"))
        
        self.monitor_ids = []
    
    
    async def start_storage_polling(self):
        self.get_monitor_ids()
        while self.should_poll:
            print("poll monitors")
            await self.poll_storage()
            await asyncio.sleep(self.poll_rate)
            
    async def poll_storage(self):
        pass
        
    def get_items(self, monitor_id):
        pass
    
    def get_all_items(self):
        pass
    
    def get_monitor_ids(self):
        monitors = self.BUS.db_query("id", "Devices", "dev_type=3")
        self.monitor_ids = [monitor[0] for monitor in monitors]
        print("Monitors:", self.monitor_ids)
        
    # Called from outside when there's a new monitor, or one is gone 
    def update_monitor_ids(self):
        self.get_monitor_ids()
        