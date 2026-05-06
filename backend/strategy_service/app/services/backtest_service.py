from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from app.domain.models import BacktestRequest, BacktestResult
from app.services.strategy_registry import get_strategy
from py_common.domain.strategy import Regime, StrategyContext


class BacktestService:
    async def run(self, request: BacktestRequest) -> BacktestResult:
        strategy = get_strategy(request.strategy)

        ctx = StrategyContext(
            as_of=datetime.now(UTC),
            regime=Regime.BULL,
            universe_symbols=["AAPL", "MSFT", "NVDA", "AMZN"],
            momentum_scores={
                "AAPL": Decimal("0.81"),
                "MSFT": Decimal("0.75"),
                "NVDA": Decimal("0.93"),
                "AMZN": Decimal("0.68"),
            },
            parameters=request.params,
        )
        signals = await strategy.generate_signals(ctx)
        metrics = {
            "total_signals": len(signals),
            "start": request.start,
            "end": request.end,
            "initial_capital": str(request.initial_capital),
        }
        return BacktestResult(run_id=f"bt-{int(datetime.now(UTC).timestamp())}", strategy=request.strategy, metrics=metrics, signals=signals)
