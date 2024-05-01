from typing import Any
from loguru import logger
import logging
import sys

from log.log_interceptor import LogInterceptor

""" Specifies whether debug prints should be written to stdout (True), or silenced"""
PRINT_DEBUG = True

color_map = {
    "ConfigManagerService": "#C70039",
    "DatabaseService": "#DAF7A6",
    "RustPlusAPIService": "#FF5733",
    "MapPollerService": "#9C27B0",
    "TeamPollerService": "#FFEB3B",
    "EventListenerService": "#00BCD4",
    "RustTimeManagerService": "#FF9800",
    "FCMListenerService": "#E91E63",
    "StorageMonitorManagerService": "#4CAF50",
    "CommandExecutorService": "#00E676",
    "DiscordBotService": "#2196F3",
    "WebServerService": "#FF4081",
    "MessageBus": "#7C4DFF",
    "ChatManagerService": "#8BD34A",
    "WebRoutes": "#00BFA5",
    "BattleMetricsService": "#669101",
    "RustPlus.py": "#E040FB",
    "FCMWorker": "#B71C1C",
    "RustSocketManager": "#00C853",
    "placeholder1": "#2962FF",
    "placeholder2": "#FFD600",
    "placeholder3": "#3E2723",
    "placeholder4": "#AA00FF",
    "placeholder5": "#64DD17",
    "default": "#FFFFFF",
}

def custom_formatter(record) -> str:
    """
    The custom formatting used by loguru
    """
    if record["exception"]:
        # For exceptions, return the original message format
        return "{message}\n{exception}\n".format(
            message=record["message"],
            exception=record["exception"]
        )
    if not PRINT_DEBUG and record["level"].name == "DEBUG":
        return ""
    
    class_name = record["extra"].get("class_name", "default")

    # Maximum class name length for alignment
    max_class_name_length = 25
    
    shortened_name = class_name[0:max_class_name_length - 3] + "..." if len(class_name) > max_class_name_length else class_name

    padded_class_name = shortened_name.rjust(max_class_name_length)

    color = color_map.get(class_name, "#FFFFFF")

    time = record["time"].strftime("%H:%M:%S")
    level = record["level"].name
    
    coloured_class_name = f"<fg {color}>{padded_class_name} | </fg {color}>"
    
    message = ""
    if level == "ERROR":
        message = f"<red>{time} [ERR!]</red> {coloured_class_name}<red>{record['message']}</red>"
    if level == "WARNING":
        message = f"<yellow>{time} [WARN]</yellow> {coloured_class_name}<yellow>{record['message']}</yellow>"
    if level == "DEBUG":
        message = f"<fg #567fff>{time} [DEBG]</fg #567fff> {coloured_class_name}{record['message']}"
    if level == "INFO":
        message = f"<fg #fff>{time} [INFO]</fg #fff> {coloured_class_name}{record['message']}"
    if level == "CRITICAL":
        message = f"<v><red>{time} [CRIT]</red></v> {coloured_class_name}<red>{record['message']}</red>"

    return f"{message}\n"

def get_colour(service_name) -> str:
    return color_map.get(service_name, "#FFFFFF")

def get_colourised_name(service_name) -> str:
    return f"<fg {get_colour(service_name)}>{service_name}</fg {get_colour(service_name)}>"

def exception_only(record) -> Any:
    return record["exception"] != None

def setup_logger() -> None:
    """Setup the loguru logger
    """
    logger.remove()

    logging.basicConfig(handlers=[LogInterceptor()], level=logging.DEBUG)

    logger.add(sys.stderr, backtrace=True, diagnose=True, filter=exception_only)
    logger.add(sys.stdout, format=custom_formatter, colorize=True)
