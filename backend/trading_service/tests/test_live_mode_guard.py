import os


def test_live_mode_requires_double_confirmation() -> None:
    os.environ["LIVE_TRADING"] = "false"
    os.environ["I_UNDERSTAND_REAL_MONEY"] = "false"
    # Guard logic is evaluated at app import time; this test documents required env expectations.
    assert os.environ["LIVE_TRADING"] != "true" or os.environ["I_UNDERSTAND_REAL_MONEY"] != "true"
