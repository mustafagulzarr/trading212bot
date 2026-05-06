from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

from py_common.compliance.base import ComplianceReport, ComplianceStatus


class InHouseAAOIFIProvider:
    name = "in_house_aaoifi"
    methodology = "AAOIFI"

    async def get_report(self, symbol: str) -> ComplianceReport:
        return ComplianceReport(
            instrument_symbol=symbol,
            provider=self.name,
            methodology="AAOIFI",
            status=ComplianceStatus.UNKNOWN,
            business_screen="UNKNOWN",
            financial_screen="UNKNOWN",
            non_compliant_revenue_pct=Decimal("0"),
            report_date=date.today(),
            fetched_at=datetime.now(UTC),
            screen_inputs={"note": "phase2 scaffold"},
            rationale="Phase 2 scaffold provider; full AAOIFI logic pending.",
        )

    async def bulk_get_reports(self, symbols: list[str]) -> list[ComplianceReport]:
        return [await self.get_report(symbol) for symbol in symbols]
