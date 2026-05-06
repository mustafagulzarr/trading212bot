from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Protocol

from pydantic import BaseModel


class Regime(StrEnum):
    BEAR = "BEAR"
    CRASH = "CRASH"
    EUPHORIA = "EUPHORIA"
    BULL = "BULL"


class Signal(BaseModel):
    id: str
    symbol: str
    direction: str
    strength: Decimal
    target_quantity: Decimal
    rationale: dict[str, Any]


class StrategyContext(BaseModel):
    as_of: datetime
    regime: Regime
    universe_symbols: list[str]
    momentum_scores: dict[str, Decimal]
    parameters: dict[str, Any]


class Strategy(Protocol):
    name: str
    version: str
    applicable_regimes: list[Regime]

    async def generate_signals(self, ctx: StrategyContext) -> list[Signal]: ...
