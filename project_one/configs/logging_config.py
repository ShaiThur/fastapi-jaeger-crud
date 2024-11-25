import logging
import sys
from logging.config import dictConfig

from opentelemetry import trace

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "opentelemetry": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        }
    },
    "loggers": {
        "": {
            "handlers": ["default", "opentelemetry"],
            "level": "INFO"
        },
        "uvicorn.error": {
            "handlers": ["default", "opentelemetry"],
            "level": "INFO"
        },
    }
}


class OpenTelemetryHandler(logging.Handler):
    def emit(self, record):
        span = trace.get_current_span()
        if span.is_recording():
            span.add_event(
                record.getMessage(),
                {
                    "log.level": record.levelname,
                    "log.name": record.name,
                    "log.filename": record.pathname,
                    "log.funcName": record.funcName,
                    "log.lineno": record.lineno
                }
            )


dictConfig(LOGGING_CONFIG)
logging.getLogger(__name__).addHandler(OpenTelemetryHandler())

logger = logging.getLogger(__name__)
