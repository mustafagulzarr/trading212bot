from __future__ import annotations

from app.domain.models import OrderResponse


class InMemoryTradingRepo:
    def __init__(self) -> None:
        self.orders: dict[str, OrderResponse] = {}
        self.daily_loss_triggered: bool = False
        self.bot_enabled: bool = True

    def save_order(self, order: OrderResponse) -> None:
        self.orders[order.id] = order

    def get_order(self, order_id: str) -> OrderResponse | None:
        return self.orders.get(order_id)

    def list_orders(self) -> list[OrderResponse]:
        return list(self.orders.values())
