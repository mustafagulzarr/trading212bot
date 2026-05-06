import pytest
from decimal import Decimal

from py_common.brokers.base import OrderRequest, OrderSide, OrderType
from py_common.brokers.mock import MockBrokerProvider


@pytest.mark.asyncio
async def test_mock_broker_contract_place_order() -> None:
    broker = MockBrokerProvider()
    order = await broker.place_order(
        OrderRequest(
            idempotency_key="k1",
            broker_symbol="AAPL_US_EQ",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=Decimal("1"),
        )
    )
    assert order.idempotency_key == "k1"
