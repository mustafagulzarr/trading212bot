from __future__ import annotations

import asyncio
from typing import Any

import httpx


class EODHDClient:
    def __init__(self, api_key: str, base_url: str = "https://eodhd.com/api", timeout: float = 30.0) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def _get(self, path: str, params: dict[str, Any] | None = None, retries: int = 3) -> Any:
        merged = dict(params or {})
        merged["api_token"] = self._api_key
        for attempt in range(1, retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.get(f"{self._base_url}/{path.lstrip('/')}", params=merged)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError:
                if attempt == retries:
                    raise
                await asyncio.sleep(attempt)
        raise RuntimeError("unreachable")

    async def get_eod(self, symbol: str, period: str = "d") -> Any:
        return await self._get("eod", {"s": symbol, "period": period})
