from __future__ import annotations

from datetime import date

from py_common.compliance.base import ComplianceReport

from app.domain.models import Instrument, OHLCVBar


class InMemoryMarketDataRepo:
    def __init__(self) -> None:
        self.instruments: dict[str, Instrument] = {
            "1": Instrument(id="1", symbol="AAPL", name="Apple Inc.", currency="USD", exchange="NASDAQ"),
            "2": Instrument(id="2", symbol="MSFT", name="Microsoft Corp.", currency="USD", exchange="NASDAQ"),
        }
        self.compliance_by_instrument: dict[str, ComplianceReport] = {}
        self.ohlcv_by_instrument: dict[str, list[OHLCVBar]] = {}

    def list_instruments(self) -> list[Instrument]:
        return list(self.instruments.values())

    def get_instrument(self, instrument_id: str) -> Instrument | None:
        return self.instruments.get(instrument_id)

    def set_compliance(self, instrument_id: str, report: ComplianceReport) -> None:
        self.compliance_by_instrument[instrument_id] = report

    def get_compliance(self, instrument_id: str) -> ComplianceReport | None:
        return self.compliance_by_instrument.get(instrument_id)

    def list_universe(self) -> list[Instrument]:
        compliant = []
        for instrument in self.instruments.values():
            report = self.compliance_by_instrument.get(instrument.id)
            if report and report.status.value == "COMPLIANT":
                compliant.append(instrument)
        return compliant

    def get_ohlcv(self, instrument_id: str, start: date | None, end: date | None) -> list[OHLCVBar]:
        bars = self.ohlcv_by_instrument.get(instrument_id, [])
        if start:
            bars = [b for b in bars if b.bar_date >= start]
        if end:
            bars = [b for b in bars if b.bar_date <= end]
        return bars
