from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.services.cash_and_dca_v1 import CashAndDcaV1
from app.services.defensive_quality_v1 import DefensiveQualityV1
from app.services.trim_and_hedge_v1 import TrimAndHedgeV1
from py_common.domain.strategy import Regime, StrategyContext


@pytest.mark.asyncio
async def test_defensive_quality_emits_signals() -> None:
    strategy = DefensiveQualityV1()
    ctx = StrategyContext(as_of=datetime.now(UTC), regime=Regime.BEAR, universe_symbols=["AAPL", "MSFT"], momentum_scores={}, parameters={})
    signals = await strategy.generate_signals(ctx)
    assert len(signals) == 2


@pytest.mark.asyncio
async def test_cash_and_dca_emits_buy_signal() -> None:
    strategy = CashAndDcaV1()
    ctx = StrategyContext(as_of=datetime.now(UTC), regime=Regime.CRASH, universe_symbols=["SPUS"], momentum_scores={}, parameters={})
    signals = await strategy.generate_signals(ctx)
    assert signals[0].direction == "BUY"


@pytest.mark.asyncio
async def test_trim_and_hedge_emits_sell_signal() -> None:
    strategy = TrimAndHedgeV1()
    ctx = StrategyContext(as_of=datetime.now(UTC), regime=Regime.EUPHORIA, universe_symbols=["AAPL", "MSFT"], momentum_scores={}, parameters={})
    signals = await strategy.generate_signals(ctx)
    assert all(signal.direction == "SELL" for signal in signals)
