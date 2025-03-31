
import logging
import logging.config
from colorama import init as init_colorama
from colorama import Fore, Back, Style


init_colorama(wrap=False)


class LevelBaseFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        self.default_format = "%(asctime)s:%(levelname)s %(message)s"

    def get_format(self, record: logging.LogRecord) -> str:
        dt_fmt = f"{Style.DIM + Fore.GREEN}%(asctime)s{Fore.RESET}"
        trace_stack_fmt = f"{Fore.BLUE}%(name)s{Fore.RESET}:[%(filename)s:%(module)s:{Fore.BLUE}%(lineno)s{Fore.RESET}]"
        debug_level_fmt = f"{Style.NORMAL + Fore.CYAN}{record.levelname} {Fore.RESET}"
        info_level_fmt = f"{Style.NORMAL + Fore.GREEN}{record.levelname} {Fore.RESET}"
        error_level_fmt = f"{Style.NORMAL + Fore.RED}{record.levelname} {Fore.RESET}"

        formats = {
            logging.DEBUG: f"{dt_fmt}: {debug_level_fmt} {trace_stack_fmt} %(message)s",
            logging.INFO: f"{dt_fmt}: {info_level_fmt} %(message)s",
            logging.ERROR: f"{dt_fmt}: {error_level_fmt} {trace_stack_fmt} %(message)s"
        }        
        return formats.get(record.levelno, self.default_format)     

    def format(self, record: logging.LogRecord):
        log_format = self.get_format(record)
        formatter = logging.Formatter(log_format, self.datefmt)
        return formatter.format(record)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "level_based": {"()": LevelBaseFormatter},
        "default": {
            "format": "%(asctime)s: %(levelname)s %(name)s:[%(filename)s:%(module)s:%(lineno)s] %(message)s" 
        },
        "db_formatter": {
            "format": "%(asctime)s: %(levelname)s %(name)s:[%(filename)s:%(module)s:%(lineno)s]\n%(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "level_based",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        },
        "api_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "src/logs/api.log",
            "mode": "a",
            "maxBytes": 10_000,
            "backupCount": 5, # Roll over log files :: api.log.1 to api.log.5
            "formatter": "default"
        },
        "db_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "src/logs/db.log",
            "mode": "a",
            "maxBytes": 100_000,
            "backupCount": 5, # Roll over log files :: api.log.1 to api.log.5
            "formatter": "db_formatter"
        }
    },
    "loggers": {
        "fastapi": {
            "level": "DEBUG",
            "handlers": ["console", "api_file_handler"],
            "propagate": False,
        },
        # "pymongo": {
        #     "level": "DEBUG",
        #     "handlers": ["db_file_handler"],
        #     "propagate": False,
        # },        
        "pymongo.command": {
            "level": "DEBUG",
            "handlers": ["db_file_handler"],
            "propagate": False,
        },
        # "pymongo.server": {
        #     "level": "INFO",
        #     "handlers": ["db_file_handler"],
        #     "propagate": False,
        # },
        # "pymongo.pool": {
        #     "level": "INFO",
        #     "handlers": ["db_file_handler"],
        #     "propagate": False,
        # },
        # "pymongo.cursor": {
        #     "level": "DEBUG",
        #     "handlers": ["db_file_handler"],
        #     "propagate": False,
        # }
    }
}

if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)

    logger = logging.getLogger("fastapi")

    logger.info("INFO")
    logger.debug("DEBUG")
    logger.error("ERROR")