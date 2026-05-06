from __future__ import annotations

from datetime import date, UTC, datetime

from fastapi import APIRouter, HTTPException, Query

from app.repositories.in_memory_repo import InMemoryMarketDataRepo
from app.services.market_data_service import MarketDataService
from py_common.config.loader import load_bot_config

router = APIRouter()
repo = InMemoryMarketDataRepo()
service = MarketDataService(repo=repo, config=load_bot_config())


@router.get("/instruments")
async def list_instruments(compliant_only: bool = Query(default=False)) -> list[dict]:
    instruments = repo.list_universe() if compliant_only else repo.list_instruments()
    return [i.model_dump() for i in instruments]


@router.get("/instruments/{instrument_id}/ohlcv")
async def get_ohlcv(instrument_id: str, from_date: date | None = Query(default=None, alias="from"), to: date | None = None) -> list[dict]:
    return [b.model_dump() for b in repo.get_ohlcv(instrument_id, from_date, to)]


@router.get("/instruments/{instrument_id}/compliance")
async def get_compliance(instrument_id: str) -> dict:
    report = repo.get_compliance(instrument_id)
    if report is None:
        raise HTTPException(status_code=404, detail="compliance report not found")
    return report.model_dump(mode="json")


@router.post("/instruments/{instrument_id}/compliance/recompute")
async def recompute_compliance(instrument_id: str) -> dict:
    try:
        accepted = await service.recompute_compliance_for_instrument(instrument_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return accepted.model_dump(mode="json")


@router.post("/instruments/{instrument_id}/refresh")
async def refresh_instrument(instrument_id: str) -> dict:
    if repo.get_instrument(instrument_id) is None:
        raise HTTPException(status_code=404, detail="instrument not found")
    return {"job": "refresh-instrument", "instrument_id": instrument_id, "accepted_at": datetime.now(UTC).isoformat()}


@router.get("/universe")
async def get_universe() -> list[dict]:
    return [i.model_dump() for i in repo.list_universe()]


@router.post("/jobs/sync-universe")
async def sync_universe() -> dict:
    accepted = await service.sync_universe()
    return accepted.model_dump(mode="json")


@router.post("/jobs/recompute-compliance")
async def recompute_compliance_bulk() -> dict:
    accepted = await service.sync_universe()
    return {"job": accepted.job, "accepted_at": accepted.accepted_at, "scope": "all"}


@router.get("/taxonomy")
async def get_taxonomy() -> list[dict]:
    return [{"id": "rule-1", "pattern": "alcohol", "default_classification": "HARAM", "category": "ALCOHOL"}]


@router.put("/taxonomy/{taxonomy_id}")
async def update_taxonomy(taxonomy_id: str, payload: dict) -> dict:
    return {"id": taxonomy_id, "updated": True, "payload": payload}
