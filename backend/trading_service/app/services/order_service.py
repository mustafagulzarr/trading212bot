from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from py_common.brokers.base import OrderRequest, OrderSide, OrderType
from py_common.brokers.registry import get_broker
from py_common.compliance.base import ComplianceStatus
from py_common.compliance.registry import get_provider
from py_common.config.loader import BotConfig

from app.domain.models import OrderCreateRequest, OrderResponse
from app.repositories.in_memory_repo import InMemoryTradingRepo


class OrderService:
    def __init__(self, repo: InMemoryTradingRepo, config: BotConfig) -> None:
        self._repo = repo
        self._config = config

    async def _guard_chain(self, req: OrderCreateRequest) -> tuple[bool, str | None]:
        # 1) kill switch
        if not self._repo.bot_enabled or not self._config.general.bot_enabled:
            return False, "KILL_SWITCH"

        # 2) compliance
        provider = get_provider(self._config.compliance["provider"])
        report = await provider.get_report(req.symbol)
        if report.status != ComplianceStatus.COMPLIANT:
            return False, "NOT_SHARIAH_COMPLIANT"

        # 3) capability check
        broker = get_broker(self._config.execution["broker"])
        order_type = req.order_type.upper()
        if order_type == "LIMIT" and not broker.capabilities.supports_limit_orders:
            return False, "BROKER_CAPABILITY_UNSUPPORTED"

        # 4) daily loss limit
        if self._repo.daily_loss_triggered:
            return False, "DAILY_LOSS_LIMIT"

        # 5) idempotency (simplified v1: reject duplicate signal id)
        if req.signal_id and any(o.id.startswith(req.signal_id) for o in self._repo.list_orders()):
            return False, "IDEMPOTENCY_HIT"

        # 6) rate limit placeholder
        return True, None

    async def place_order(self, req: OrderCreateRequest) -> OrderResponse:
        allowed, reason = await self._guard_chain(req)
        order_id = f"{req.signal_id or 'ord'}-{uuid4()}"
        if not allowed:
            order = OrderResponse(id=order_id, status="REJECTED", rejection_reason=reason, created_at=datetime.now(UTC))
            self._repo.save_order(order)
            return order

        broker = get_broker(self._config.execution["broker"])
        await broker.place_order(
            OrderRequest(
                idempotency_key=order_id,
                broker_symbol=req.symbol,
                side=OrderSide(req.side.upper()),
                order_type=OrderType(req.order_type.upper()),
                quantity=Decimal(req.quantity),
            )
        )
        order = OrderResponse(id=order_id, status="SUBMITTED", created_at=datetime.now(UTC))
        self._repo.save_order(order)
        return order
