from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Literal, Protocol

from pydantic import BaseModel


class ComplianceStatus(StrEnum):
    COMPLIANT = "COMPLIANT"
    QUESTIONABLE = "QUESTIONABLE"
    NON_COMPLIANT = "NON_COMPLIANT"
    UNKNOWN = "UNKNOWN"


class ComplianceReport(BaseModel):
    instrument_symbol: str
    provider: str
    methodology: Literal["AAOIFI", "DJIM", "OTHER"]
    status: ComplianceStatus
    business_screen: Literal["PASS", "FAIL", "UNKNOWN"]
    financial_screen: Literal["PASS", "FAIL", "UNKNOWN"]
    compliant_revenue_pct: Decimal | None = None
    non_compliant_revenue_pct: Decimal | None = None
    debt_to_market_cap_ratio: Decimal | None = None
    securities_to_market_cap_ratio: Decimal | None = None
    interest_income_to_revenue_ratio: Decimal | None = None
    report_date: date
    fetched_at: datetime
    screen_inputs: dict[str, Any]
    rationale: str


class ComplianceProvider(Protocol):
    name: str
    methodology: str

    async def get_report(self, symbol: str) -> ComplianceReport: ...

    async def bulk_get_reports(self, symbols: list[str]) -> list[ComplianceReport]: ...
