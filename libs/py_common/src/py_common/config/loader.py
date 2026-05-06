from __future__ import annotations

import json
from pathlib import Path

from jsonschema import validate
from pydantic import BaseModel


class GeneralConfig(BaseModel):
    bot_enabled: bool
    environment: str
    account_type: str
    base_currency: str
    timezone: str


class BotConfig(BaseModel):
    general: GeneralConfig
    risk: dict
    compliance: dict
    execution: dict


def load_bot_config(config_path: str = "config/bot.json", schema_path: str = "config/bot.schema.json") -> BotConfig:
    config_raw = json.loads(Path(config_path).read_text())
    schema_raw = json.loads(Path(schema_path).read_text())
    validate(instance=config_raw, schema=schema_raw)
    return BotConfig.model_validate(config_raw)
