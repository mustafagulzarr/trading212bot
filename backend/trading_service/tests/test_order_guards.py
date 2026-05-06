from decimal import Decimal

from app.domain.models import OrderCreateRequest
from app.repositories.in_memory_repo import InMemoryTradingRepo
from app.services.order_service import OrderService
from py_common.config.loader import load_bot_config


async def test_kill_switch_guard_blocks_order() -> None:
    repo = InMemoryTradingRepo()
    repo.bot_enabled = False
    service = OrderService(repo=repo, config=load_bot_config())
    result = await service.place_order(OrderCreateRequest(symbol="AAPL", side="BUY", order_type="MARKET", quantity=Decimal("1")))
    assert result.status == "REJECTED"
    assert result.rejection_reason == "KILL_SWITCH"
