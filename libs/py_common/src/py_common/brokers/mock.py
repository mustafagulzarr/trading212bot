from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from py_common.brokers.base import AccountSummary, BrokerCapabilities, BrokerOrder, BrokerPosition, OrderRequest, OrderStatus


class MockBrokerProvider:
    name = "mock"
    capabilities = BrokerCapabilities(
        supports_market_orders=True,
        supports_limit_orders=True,
        supports_stop_orders=True,
        supports_stop_limit_orders=True,
        supports_extended_hours=False,
        supports_fractional_shares=True,
        supports_short_selling=False,
        supports_options=False,
        min_order_value=None,
        base_currency="GBP",
        rate_limit_per_minute=60,
        is_paper=True,
    )

    async def health_check(self) -> bool:
        return True

    async def resolve_symbol(self, internal_symbol: str) -> str:
        return internal_symbol

    async def get_account_summary(self) -> AccountSummary:
        return AccountSummary(
            broker=self.name,
            account_id="mock",
            account_type="PAPER",
            currency="GBP",
            cash_available=Decimal("10000"),
            cash_reserved=Decimal("0"),
            investments_value=Decimal("0"),
            total_value=Decimal("10000"),
            realized_pnl=Decimal("0"),
            unrealized_pnl=Decimal("0"),
            fetched_at=datetime.now(UTC),
        )

    async def get_positions(self) -> list[BrokerPosition]:
        return []

    async def place_order(self, req: OrderRequest) -> BrokerOrder:
        return BrokerOrder(
            broker=self.name,
            broker_order_id="mock-order-1",
            idempotency_key=req.idempotency_key,
            status=OrderStatus.SUBMITTED,
            submitted_at=datetime.now(UTC),
            filled_at=None,
            filled_quantity=Decimal("0"),
            filled_value=Decimal("0"),
            avg_fill_price=None,
            raw_response={"mock": True},
        )

    async def get_order(self, broker_order_id: str) -> BrokerOrder:
        req = OrderRequest(idempotency_key="id", broker_symbol="AAPL", side="BUY", order_type="MARKET", quantity=Decimal("1"))
        return await self.place_order(req)

    async def cancel_order(self, broker_order_id: str) -> BrokerOrder:
        order = await self.get_order(broker_order_id)
        order.status = OrderStatus.CANCELLED
        return order

    async def list_open_orders(self) -> list[BrokerOrder]:
        return []

    async def get_order_history(self, since: datetime) -> list[BrokerOrder]:
        return []
