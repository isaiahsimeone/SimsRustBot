
import logging
import loguru

class LogInterceptor(logging.Handler):
    
    intercept = [("rustplus", "RustPlus.py")]
    
    def emit(self, record) -> None:
        try:
            class_name = record.name.split(".")[0]
        except:
            class_name = record.name
        # rustplus.py puts out these messages that we don't want, discard them
        if class_name == "rustplus" and record.msg.strip() == "[RustPlus.py]":
            return None
        
        for _, (first, second) in enumerate(LogInterceptor.intercept):
            if class_name == first:
                class_name = second
                break
        else:
            return None
        
        # map logging levels to Loguru levels
        level_map = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR",
            logging.CRITICAL: "CRITICAL"
        }
        loguru_level = level_map.get(record.levelno, "INFO")

        # Log the message using Loguru with the formatted message
        loguru.logger.bind(class_name=class_name).log(loguru_level, record.msg)