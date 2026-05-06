from __future__ import annotations

from datetime import UTC, datetime

from py_common.compliance.registry import get_provider
from py_common.config.loader import BotConfig

from app.domain.models import JobAccepted
from app.repositories.in_memory_repo import InMemoryMarketDataRepo


class MarketDataService:
    def __init__(self, repo: InMemoryMarketDataRepo, config: BotConfig) -> None:
        self._repo = repo
        self._config = config

    async def recompute_compliance_for_instrument(self, instrument_id: str) -> JobAccepted:
        instrument = self._repo.get_instrument(instrument_id)
        if instrument is None:
            raise ValueError("instrument not found")
        provider = get_provider(self._config.compliance["provider"])
        report = await provider.get_report(instrument.symbol)
        self._repo.set_compliance(instrument_id, report)
        return JobAccepted(job="recompute-compliance", accepted_at=datetime.now(UTC))

    async def sync_universe(self) -> JobAccepted:
        for instrument in self._repo.list_instruments():
            provider = get_provider(self._config.compliance["provider"])
            report = await provider.get_report(instrument.symbol)
            self._repo.set_compliance(instrument.id, report)
        return JobAccepted(job="sync-universe", accepted_at=datetime.now(UTC))
