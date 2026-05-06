from app.services.cash_and_dca_v1 import CashAndDcaV1
from app.services.defensive_quality_v1 import DefensiveQualityV1
from app.services.momentum_breakout_v1 import MomentumBreakoutV1
from app.services.trim_and_hedge_v1 import TrimAndHedgeV1


def get_strategy(name: str):
    registry = {
        "momentum_breakout_v1": MomentumBreakoutV1,
        "defensive_quality_v1": DefensiveQualityV1,
        "cash_and_dca_v1": CashAndDcaV1,
        "trim_and_hedge_v1": TrimAndHedgeV1,
    }
    if name not in registry:
        raise ValueError(f"Unsupported strategy: {name}")
    return registry[name]()
