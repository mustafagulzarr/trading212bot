from decimal import Decimal

from app.services.regime_detector import RegimeDetector
from py_common.domain.strategy import Regime


def test_regime_detector_crash() -> None:
    detector = RegimeDetector()
    result = detector.detect(Decimal("0.25"), Decimal("0.40"), Decimal("0.30"), Decimal("0.5"))
    assert result.regime == Regime.CRASH


def test_regime_detector_bull_default() -> None:
    detector = RegimeDetector()
    result = detector.detect(Decimal("0.02"), Decimal("0.10"), Decimal("0.60"), Decimal("0.4"))
    assert result.regime == Regime.BULL
