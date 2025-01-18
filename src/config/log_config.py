"""The module responsible for logging configuration."""

from .app_config import Config

config: Config = Config()
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "[%(levelname)s] [%(asctime)s] | %(funcName)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG" if config.debug else "INFO",
            "formatter": "base",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": "logfile.log",
            "backupCount": 3,
            "when": "d",
            "interval": 10,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "main_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "propagate": False,
        },
    },
}
