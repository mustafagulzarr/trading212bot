from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from app.domain.models import RegimeSnapshot
from py_common.domain.strategy import Regime


class RegimeDetector:
    def detect(self, drawdown_pct: Decimal, realized_vol_pct: Decimal, breadth_pct: Decimal, zscore_200sma: Decimal) -> RegimeSnapshot:
        if drawdown_pct > Decimal("0.20") and realized_vol_pct > Decimal("0.35"):
            regime = Regime.CRASH
            confidence = Decimal("0.9")
        elif drawdown_pct > Decimal("0.10"):
            regime = Regime.BEAR
            confidence = Decimal("0.75")
        elif zscore_200sma > Decimal("2.0") and breadth_pct > Decimal("0.80"):
            regime = Regime.EUPHORIA
            confidence = Decimal("0.8")
        else:
            regime = Regime.BULL
            confidence = Decimal("0.7")

        return RegimeSnapshot(
            regime=regime,
            confidence=confidence,
            detected_at=datetime.now(UTC),
            inputs_snapshot={
                "drawdown_pct": str(drawdown_pct),
                "realized_vol_pct": str(realized_vol_pct),
                "breadth_pct": str(breadth_pct),
                "zscore_200sma": str(zscore_200sma),
            },
            model_version="v1",
        )
