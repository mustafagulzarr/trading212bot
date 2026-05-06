"""Tests for the live-mode startup guard in trading_service.app.main.

The guard reads `general.environment` from config plus the `LIVE_TRADING` and
`I_UNDERSTAND_REAL_MONEY` env vars, and refuses to start unless both env vars
are set to "true" when the config is in live mode.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest


def _write_live_config(tmp_path: Path) -> Path:
    config = {
        "general": {
            "bot_enabled": True,
            "environment": "live",
            "account_type": "INVEST",
            "base_currency": "GBP",
            "timezone": "Europe/London",
        },
        "risk": {"daily_loss_limit_pct": 0.02},
        "compliance": {"provider": "mock", "max_report_age_days": 30, "block_on_compliance_unknown": True},
        "execution": {"broker": "mock", "rate_limit_per_minute": 30},
    }
    config_path = tmp_path / "bot.json"
    config_path.write_text(json.dumps(config))

    schema_src = Path(__file__).resolve().parents[3] / "config" / "bot.schema.json"
    (tmp_path / "bot.schema.json").write_text(schema_src.read_text())
    return config_path


def _reimport_main() -> None:
    for mod in [m for m in sys.modules if m == "app.main" or m.startswith("app.main.")]:
        del sys.modules[mod]
    from py_common.config.loader import reload_bot_config
    reload_bot_config()
    importlib.import_module("app.main")


def test_live_mode_refuses_to_start_without_double_confirmation(monkeypatch, tmp_path) -> None:
    config_path = _write_live_config(tmp_path)
    monkeypatch.setenv("BOT_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("LIVE_TRADING", "false")
    monkeypatch.setenv("I_UNDERSTAND_REAL_MONEY", "false")

    with pytest.raises(RuntimeError, match="Refusing to start in live mode"):
        _reimport_main()


def test_live_mode_starts_with_double_confirmation(monkeypatch, tmp_path) -> None:
    config_path = _write_live_config(tmp_path)
    monkeypatch.setenv("BOT_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("LIVE_TRADING", "true")
    monkeypatch.setenv("I_UNDERSTAND_REAL_MONEY", "true")

    _reimport_main()
    assert "app.main" in sys.modules


def test_demo_mode_ignores_live_flags(monkeypatch) -> None:
    monkeypatch.delenv("BOT_CONFIG_PATH", raising=False)
    monkeypatch.setenv("LIVE_TRADING", "false")
    monkeypatch.setenv("I_UNDERSTAND_REAL_MONEY", "false")

    _reimport_main()
    assert "app.main" in sys.modules
