import asyncio

import loguru

from commands.command_executor_service import CommandExecutorService
from config.config_manager_service import ConfigManagerService
from database.database_service import DatabaseService
from discord_bot.discord_bot_service import DiscordBotService
from ipc.message_bus import MessageBus
from rust_socket.rust_socket_manager import RustSocketManager
from log.log_config import setup_logger
from rust.rust_plus_api_service import RustPlusAPIService
from services.battle_metrics_service import BattleMetricsService
from services.chat_manager_service import ChatManagerService
from services.event_listener_service import EventListenerService
from services.fcm_listener_service import FCMListenerService
from services.map_poller_service import MapPollerService
from services.rust_time_manager_service import RustTimeManagerService
from services.storage_monitor_manager_service import StorageMonitorManagerService
from services.team_poller_service import TeamPollerService
from util.printer import Printer
from web.web_server_service import WebServerService

@loguru.logger.catch
async def main() -> None:
    Printer.print_banner()
    setup_logger()

    bus = MessageBus()

    RustSocketManager.prepare()

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
        ChatManagerService(bus),
        BattleMetricsService(bus)
    ]

    tasks = [asyncio.create_task(service.execute()) for service in services]

    # Run all services concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
