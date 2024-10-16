import logging
import logging.config
from pathlib import Path

# Create logs directory if it doesn't exist
Path("logs").mkdir(parents=True, exist_ok=True)

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG"
        },
        "file_info": {
            "class": "logging.FileHandler",
            "filename": "logs/info.log",
            "formatter": "detailed",
            "level": "INFO"
        },
        "file_error": {
            "class": "logging.FileHandler",
            "filename": "logs/error.log",
            "formatter": "detailed",
            "level": "ERROR"
        }
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "file_info", "file_error"],
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file_info", "file_error"]
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

def get_db_logger():
    return logging.getLogger("db_logs")

def get_app_logger():
    return logging.getLogger("app_logs")

def get_llm_logger():
    return logging.getLogger("llm_logs")