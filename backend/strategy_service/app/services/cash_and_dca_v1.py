from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from py_common.domain.strategy import Regime, Signal, StrategyContext


class CashAndDcaV1:
    name = "cash_and_dca_v1"
    version = "1.0.0"
    applicable_regimes = [Regime.CRASH]

    async def generate_signals(self, ctx: StrategyContext) -> list[Signal]:
        picks = ctx.universe_symbols[:1]
        return [
            Signal(
                id=str(uuid4()),
                symbol=s,
                direction="BUY",
                strength=Decimal("0.4"),
                target_quantity=Decimal("1"),
                rationale={"strategy": self.name, "reason": "DCA in crash"},
            )
            for s in picks
        ]
