from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter

from app.domain.models import BacktestRequest
from app.services.backtest_service import BacktestService
from app.services.regime_detector import RegimeDetector
from app.services.strategy_registry import get_strategy

router = APIRouter()
regime_detector = RegimeDetector()
backtest_service = BacktestService()


@router.get('/regime/current')
async def current_regime() -> dict:
    snapshot = regime_detector.detect(Decimal("0.05"), Decimal("0.20"), Decimal("0.55"), Decimal("1.10"))
    return snapshot.model_dump(mode="json")


@router.post('/regime/recompute')
async def recompute_regime() -> dict:
    snapshot = regime_detector.detect(Decimal("0.12"), Decimal("0.29"), Decimal("0.47"), Decimal("0.50"))
    return snapshot.model_dump(mode="json")


@router.get('/strategies')
async def list_strategies() -> list[dict]:
    strategy = get_strategy("momentum_breakout_v1")
    return [{"name": strategy.name, "version": strategy.version, "applicable_regimes": [r.value for r in strategy.applicable_regimes]}]


@router.get('/strategies/{strategy_name}')
async def get_strategy_by_name(strategy_name: str) -> dict:
    strategy = get_strategy(strategy_name)
    return {"name": strategy.name, "version": strategy.version, "applicable_regimes": [r.value for r in strategy.applicable_regimes]}


@router.post('/signals/generate')
async def generate_signals() -> dict:
    result = await backtest_service.run(
        BacktestRequest(strategy="momentum_breakout_v1", start="2020-01-01", end="2020-12-31", initial_capital=Decimal("100000"), params={"top_n": 2, "min_score": "0.7"})
    )
    return {"signals": [s.model_dump(mode="json") for s in result.signals]}


@router.post('/backtest')
async def run_backtest(request: BacktestRequest) -> dict:
    result = await backtest_service.run(request)
    return result.model_dump(mode="json")


@router.get('/backtest/{run_id}')
async def get_backtest(run_id: str) -> dict:
    return {"run_id": run_id, "status": "completed"}
