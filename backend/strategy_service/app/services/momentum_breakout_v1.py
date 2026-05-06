from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from py_common.domain.strategy import Regime, Signal, StrategyContext


class MomentumBreakoutV1:
    name = "momentum_breakout_v1"
    version = "1.0.0"
    applicable_regimes = [Regime.BULL]

    async def generate_signals(self, ctx: StrategyContext) -> list[Signal]:
        top_n = int(ctx.parameters.get("top_n", 3))
        min_score = Decimal(str(ctx.parameters.get("min_score", "0.0")))

        ranked = sorted(ctx.momentum_scores.items(), key=lambda item: item[1], reverse=True)
        selected = [(symbol, score) for symbol, score in ranked if score >= min_score and symbol in ctx.universe_symbols][:top_n]

        signals: list[Signal] = []
        for symbol, score in selected:
            signals.append(
                Signal(
                    id=str(uuid4()),
                    symbol=symbol,
                    direction="BUY",
                    strength=score,
                    target_quantity=Decimal("1"),
                    rationale={"strategy": self.name, "score": str(score)},
                )
            )
        return signals
