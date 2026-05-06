import os

from fastapi import FastAPI

from app.api.routes import router as trading_router
from py_common.config.loader import load_bot_config
from py_common.logging import configure_logging, get_logger
from py_common.logging.events import LogEvent
from py_common.logging.middleware import CorrelationIdMiddleware

configure_logging()
logger = get_logger(__name__)
config = load_bot_config()

if config.general.environment == "live":
    live_flag = os.getenv("LIVE_TRADING", "false").lower() == "true"
    live_ack = os.getenv("I_UNDERSTAND_REAL_MONEY", "false").lower() == "true"
    if not (live_flag and live_ack):
        raise RuntimeError(
            "Refusing to start in live mode. Set LIVE_TRADING=true and I_UNDERSTAND_REAL_MONEY=true."
        )

app = FastAPI(title="trading-service")
app.add_middleware(CorrelationIdMiddleware)
app.include_router(trading_router)

logger.info(
    "service startup",
    extra={
        "event": LogEvent.SYSTEM_STARTUP.value,
        "service": "trading-service",
        "context": {"environment": config.general.environment},
    },
)


@app.get('/health')
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "trading-service"}
