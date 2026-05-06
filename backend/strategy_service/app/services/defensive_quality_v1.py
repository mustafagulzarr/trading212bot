from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from py_common.domain.strategy import Regime, Signal, StrategyContext


class DefensiveQualityV1:
    name = "defensive_quality_v1"
    version = "1.0.0"
    applicable_regimes = [Regime.BEAR]

    async def generate_signals(self, ctx: StrategyContext) -> list[Signal]:
        return [
            Signal(
                id=str(uuid4()),
                symbol=symbol,
                direction="BUY",
                strength=Decimal("0.5"),
                target_quantity=Decimal("1"),
                rationale={"strategy": self.name, "reason": "defensive allocation"},
            )
            for symbol in ctx.universe_symbols[:2]
        ]
