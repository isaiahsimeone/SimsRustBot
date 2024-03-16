import asyncio
import threading

import loguru

from commands.command_executor_service import CommandExecutorService
from config.config_manager_service import ConfigManagerService
from database.database_service import DatabaseService
from discord_bot.discord_bot_service import DiscordBotService
from ipc.bus_subscriber import BusSubscriber
from ipc.message_bus import MessageBus
from ipc.rust_socket_manager import RustSocketManager
from log.log_config import setup_logger
from rustplus_api.rust_plus_api_service import RustPlusAPIService
from rustplus_api.services.chat_manager_service import ChatManagerService
from rustplus_api.services.event_listener_service import EventListenerService
from rustplus_api.services.fcm_listener_service import FCMListenerService
from rustplus_api.services.map_poller_service import MapPollerService
from rustplus_api.services.rust_time_manager_service import RustTimeManagerService
from rustplus_api.services.storage_monitor_manager_service import StorageMonitorManagerService
from rustplus_api.services.team_poller_service import TeamPollerService
from util.printer import Printer
from web.web_server_service import WebServerService


def start_service_threaded(service: BusSubscriber) -> None:
    """Starts a service's execute coroutine in a new thread with its own event loop.

    :param service: A BusSubscriber service
    :type service: :class:`ipc.bus_service.BusSubscriber`
    """
    def thread_target() -> None:
        asyncio.run(service.execute())

    thread = threading.Thread(target=thread_target)
    thread.start()

@loguru.logger.catch
async def main() -> None:
    Printer.print_banner()
    setup_logger()

    bus = MessageBus()

    RustSocketManager.initialise()

    # Initialise services with the bus
    services = [
        ConfigManagerService(bus),
        DatabaseService(bus),
        RustPlusAPIService(bus),
        MapPollerService(bus),
        TeamPollerService(bus),
        EventListenerService(bus),
        RustTimeManagerService(bus),
        FCMListenerService(bus),
        StorageMonitorManagerService(bus),
        CommandExecutorService(bus),
        DiscordBotService(bus),
        WebServerService(bus),
        ChatManagerService(bus)
    ]

    tasks = [asyncio.create_task(service.execute()) for service in services]

    # Run all services concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
