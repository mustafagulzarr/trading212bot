from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel


class Instrument(BaseModel):
    id: str
    symbol: str
    isin: str | None = None
    name: str
    currency: str
    exchange: str
    is_active: bool = True


class OHLCVBar(BaseModel):
    instrument_id: str
    bar_date: date
    open: str
    high: str
    low: str
    close: str
    volume: str
    source: str = "eodhd"


class JobAccepted(BaseModel):
    job: str
    accepted_at: datetime
