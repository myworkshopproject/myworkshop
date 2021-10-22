"""
Django logging settings.
"""

from logging.config import dictConfig

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        # root logger:
        "": {
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}

# Disables Django’s logging configuration and then manually configures logging:
LOGGING_CONFIG = None


dictConfig(LOGGING)
