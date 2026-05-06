from enum import StrEnum


class LogEvent(StrEnum):
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_CONFIG_LOADED = "system.config.loaded"
    SYSTEM_CONFIG_RELOADED = "system.config.reloaded"
    SYSTEM_SHUTDOWN = "system.shutdown"
    ORDER_REQUESTED = "order.requested"
    ORDER_FAILED = "order.failed"
