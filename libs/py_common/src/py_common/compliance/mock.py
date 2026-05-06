from __future__ import annotations

from datetime import UTC, date, datetime

from py_common.compliance.base import ComplianceReport, ComplianceStatus


class MockComplianceProvider:
    name = "mock"
    methodology = "AAOIFI"

    async def get_report(self, symbol: str) -> ComplianceReport:
        return ComplianceReport(
            instrument_symbol=symbol,
            provider=self.name,
            methodology="AAOIFI",
            status=ComplianceStatus.COMPLIANT,
            business_screen="PASS",
            financial_screen="PASS",
            report_date=date.today(),
            fetched_at=datetime.now(UTC),
            screen_inputs={"source": "mock"},
            rationale="Mock compliant report",
        )

    async def bulk_get_reports(self, symbols: list[str]) -> list[ComplianceReport]:
        return [await self.get_report(symbol) for symbol in symbols]
