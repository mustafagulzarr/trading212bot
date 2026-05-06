from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from py_common.domain.strategy import Regime, Signal, StrategyContext


class TrimAndHedgeV1:
    name = "trim_and_hedge_v1"
    version = "1.0.0"
    applicable_regimes = [Regime.EUPHORIA]

    async def generate_signals(self, ctx: StrategyContext) -> list[Signal]:
        return [
            Signal(
                id=str(uuid4()),
                symbol=symbol,
                direction="SELL",
                strength=Decimal("0.6"),
                target_quantity=Decimal("1"),
                rationale={"strategy": self.name, "reason": "trim winners / raise cash"},
            )
            for symbol in ctx.universe_symbols[:2]
        ]
