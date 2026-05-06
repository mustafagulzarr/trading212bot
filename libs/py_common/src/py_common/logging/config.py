import json
import logging
from datetime import datetime, timezone
from typing import Any

from py_common.logging.context import get_correlation_id
from py_common.logging.redaction import redact_payload


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "event": getattr(record, "event", "system.log"),
            "service": getattr(record, "service", "unknown"),
            "correlation_id": get_correlation_id(),
            "context": redact_payload(getattr(record, "context", {})),
        }
        return json.dumps(payload, default=str)


def configure_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)
    root.setLevel(level)
