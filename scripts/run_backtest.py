from __future__ import annotations

import argparse
import asyncio
from decimal import Decimal

from backend.strategy_service.app.domain.models import BacktestRequest
from backend.strategy_service.app.services.backtest_service import BacktestService


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run backtest")
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--from", dest="start", required=True)
    parser.add_argument("--to", dest="end", required=True)
    parser.add_argument("--initial-capital", dest="initial_capital", default="100000")
    args = parser.parse_args()

    service = BacktestService()
    result = await service.run(
        BacktestRequest(
            strategy=args.strategy,
            start=args.start,
            end=args.end,
            initial_capital=Decimal(args.initial_capital),
            params={"top_n": 3, "min_score": "0.7"},
        )
    )
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
