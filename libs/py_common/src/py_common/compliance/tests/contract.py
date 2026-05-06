import pytest

from py_common.compliance.mock import MockComplianceProvider


@pytest.mark.asyncio
async def test_mock_compliance_contract_get_report() -> None:
    provider = MockComplianceProvider()
    report = await provider.get_report("AAPL")
    assert report.instrument_symbol == "AAPL"
