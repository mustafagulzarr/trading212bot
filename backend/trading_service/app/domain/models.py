from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class OrderCreateRequest(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: Decimal
    signal_id: str | None = None


class OrderResponse(BaseModel):
    id: str
    status: str
    rejection_reason: str | None = None
    created_at: datetime
