from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Literal, Protocol

from pydantic import BaseModel


class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderStatus(StrEnum):
    PENDING_SUBMIT = "PENDING_SUBMIT"
    SUBMITTED = "SUBMITTED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class BrokerCapabilities(BaseModel):
    supports_market_orders: bool
    supports_limit_orders: bool
    supports_stop_orders: bool
    supports_stop_limit_orders: bool
    supports_extended_hours: bool
    supports_fractional_shares: bool
    supports_short_selling: bool
    supports_options: bool
    min_order_value: Decimal | None
    base_currency: str
    rate_limit_per_minute: int
    is_paper: bool


class AccountSummary(BaseModel):
    broker: str
    account_id: str
    account_type: Literal["ISA", "INVEST", "DEMO", "PAPER", "OTHER"]
    currency: str
    cash_available: Decimal
    cash_reserved: Decimal
    investments_value: Decimal
    total_value: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    fetched_at: datetime


class BrokerPosition(BaseModel):
    broker_symbol: str
    quantity: Decimal
    average_price: Decimal
    current_price: Decimal | None
    market_value: Decimal
    unrealized_pnl: Decimal
    currency: str


class OrderRequest(BaseModel):
    idempotency_key: str
    broker_symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal
    limit_price: Decimal | None = None
    stop_price: Decimal | None = None
    time_in_force: Literal["DAY", "GTC"] = "DAY"
    extended_hours: bool = False


class BrokerOrder(BaseModel):
    broker: str
    broker_order_id: str | None
    idempotency_key: str
    status: OrderStatus
    submitted_at: datetime | None
    filled_at: datetime | None
    filled_quantity: Decimal
    filled_value: Decimal
    avg_fill_price: Decimal | None
    raw_response: dict[str, Any]


class BrokerProvider(Protocol):
    name: str
    capabilities: BrokerCapabilities

    async def health_check(self) -> bool: ...
    async def resolve_symbol(self, internal_symbol: str) -> str: ...
    async def get_account_summary(self) -> AccountSummary: ...
    async def get_positions(self) -> list[BrokerPosition]: ...
    async def place_order(self, req: OrderRequest) -> BrokerOrder: ...
    async def get_order(self, broker_order_id: str) -> BrokerOrder: ...
    async def cancel_order(self, broker_order_id: str) -> BrokerOrder: ...
    async def list_open_orders(self) -> list[BrokerOrder]: ...
    async def get_order_history(self, since: datetime) -> list[BrokerOrder]: ...
