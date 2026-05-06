from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.domain.models import OrderCreateRequest
from app.repositories.in_memory_repo import InMemoryTradingRepo
from app.services.order_service import OrderService
from py_common.brokers.registry import get_broker
from py_common.config.loader import load_bot_config

router = APIRouter()
config = load_bot_config()
repo = InMemoryTradingRepo()
service = OrderService(repo=repo, config=config)


def _broker():
    return get_broker(config.execution["broker"])


@router.get('/account/summary')
async def account_summary() -> dict:
    summary = await _broker().get_account_summary()
    return summary.model_dump(mode="json")


@router.get('/positions')
async def positions() -> list[dict]:
    values = await _broker().get_positions()
    return [v.model_dump(mode="json") for v in values]


@router.post('/orders')
async def create_order(request: OrderCreateRequest) -> dict:
    result = await service.place_order(request)
    return result.model_dump(mode="json")


@router.get('/orders/{order_id}')
async def get_order(order_id: str) -> dict:
    order = repo.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail='order not found')
    return order.model_dump(mode="json")


@router.get('/orders')
async def list_orders() -> list[dict]:
    return [o.model_dump(mode="json") for o in repo.list_orders()]


@router.delete('/orders/{order_id}')
async def cancel_order(order_id: str) -> dict:
    order = repo.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail='order not found')
    order.status = "CANCELLED"
    return order.model_dump(mode="json")


@router.post('/reconcile')
async def reconcile() -> dict:
    return {"reconciled": True, "open_orders": len(repo.list_orders())}


@router.get('/broker/info')
async def broker_info() -> dict:
    broker = _broker()
    return {"name": broker.name, "capabilities": broker.capabilities.model_dump(mode="json")}
