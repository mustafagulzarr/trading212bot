from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from py_common.domain.strategy import Regime, Signal


class RegimeSnapshot(BaseModel):
    regime: Regime
    confidence: Decimal
    detected_at: datetime
    inputs_snapshot: dict
    model_version: str


class BacktestRequest(BaseModel):
    strategy: str
    start: str
    end: str
    initial_capital: Decimal
    params: dict


class BacktestResult(BaseModel):
    run_id: str
    strategy: str
    metrics: dict
    signals: list[Signal]
