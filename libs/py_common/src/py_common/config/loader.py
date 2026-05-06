from __future__ import annotations

import json
import os
from functools import lru_cache
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


def _walk_up_for(start: Path, target: str) -> Path | None:
    for candidate in [start, *start.parents]:
        path = candidate / target
        if path.is_file():
            return path
    return None


def _resolve_config_paths(
    config_path: str | None,
    schema_path: str | None,
) -> tuple[Path, Path]:
    if config_path is None:
        env_path = os.getenv("BOT_CONFIG_PATH")
        if env_path:
            config_path = env_path

    if config_path is not None:
        config_file = Path(config_path)
        if not config_file.is_absolute():
            cwd_candidate = Path.cwd() / config_file
            config_file = cwd_candidate if cwd_candidate.is_file() else config_file
    else:
        config_file = (
            _walk_up_for(Path.cwd(), "config/bot.json")
            or _walk_up_for(Path(__file__).resolve().parent, "config/bot.json")
        )
        if config_file is None:
            raise FileNotFoundError(
                "Could not locate config/bot.json. Set BOT_CONFIG_PATH or run from the repo root."
            )

    if schema_path is not None:
        schema_file = Path(schema_path)
    else:
        schema_file = config_file.parent / "bot.schema.json"
        if not schema_file.is_file():
            schema_file = (
                _walk_up_for(config_file.parent, "config/bot.schema.json")
                or schema_file
            )

    return config_file, schema_file


@lru_cache(maxsize=4)
def _load_bot_config_cached(config_path: str | None, schema_path: str | None) -> BotConfig:
    config_file, schema_file = _resolve_config_paths(config_path, schema_path)
    config_raw = json.loads(config_file.read_text())
    schema_raw = json.loads(schema_file.read_text())
    validate(instance=config_raw, schema=schema_raw)
    return BotConfig.model_validate(config_raw)


def load_bot_config(
    config_path: str | None = None,
    schema_path: str | None = None,
) -> BotConfig:
    """Load and validate the bot config.

    Resolution order for the config file:
    1. Explicit ``config_path`` argument.
    2. ``BOT_CONFIG_PATH`` environment variable.
    3. ``config/bot.json`` walking up from CWD.
    4. ``config/bot.json`` walking up from this module's location.

    Result is cached, so repeated calls are free. Pass ``reload_bot_config()``
    to drop the cache (e.g. after a config-on-disk change).
    """
    return _load_bot_config_cached(config_path, schema_path)


def reload_bot_config() -> None:
    _load_bot_config_cached.cache_clear()
