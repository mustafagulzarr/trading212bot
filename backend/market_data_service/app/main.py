from fastapi import FastAPI

from app.api.routes import router as market_data_router
from py_common.config.loader import load_bot_config
from py_common.logging import configure_logging, get_logger
from py_common.logging.events import LogEvent
from py_common.logging.middleware import CorrelationIdMiddleware

configure_logging()
logger = get_logger(__name__)
config = load_bot_config()

app = FastAPI(title="market-data-service")
app.add_middleware(CorrelationIdMiddleware)
app.include_router(market_data_router)

logger.info(
    "service startup",
    extra={
        "event": LogEvent.SYSTEM_STARTUP.value,
        "service": "market-data-service",
        "context": {"environment": config.general.environment},
    },
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "market-data-service"}
