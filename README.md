# trading212bot

Shariah-compliant trading bot scaffold. Three FastAPI microservices (`market-data`, `trading`, `strategy`) backed by Postgres + Redis, with a Next.js dashboard.

## Quick start (recommended: hybrid dev)

One command, hot reload, prefixed logs, Ctrl-C stops everything.

```bash
./scripts/dev.sh
# or
make dev
```

What it does:

1. Creates `.env` from `.env.example` if missing.
2. Starts Postgres + Redis via `docker compose` (only if Docker is available).
3. Runs `uv sync --all-extras` to install Python deps for the workspace.
4. Installs frontend deps (only if `frontend/node_modules` is absent).
5. Boots the three services with `uvicorn --reload` and the frontend with `next dev`, with coloured per-service log prefixes.

URLs once it's up:

- Market data: <http://localhost:8001/health>
- Trading: <http://localhost:8002/health>
- Strategy: <http://localhost:8003/health>
- Frontend: <http://localhost:3000>

Useful flags:

```bash
./scripts/dev.sh --no-fe      # backend-only loop
./scripts/dev.sh --no-infra   # don't touch docker (postgres/redis already running)
./scripts/dev.sh --down       # also stop postgres/redis on Ctrl-C
./scripts/dev.sh --help
```

## Alternative: full docker

Slower iteration, but everything runs in containers (useful for CI parity / first run on a clean machine):

```bash
make up        # docker compose up -d --build (dev profile)
make down      # tear down + delete volumes
```

The compose file builds each backend image from the repo root so `libs/py_common` and `config/` are included.

## Tests

```bash
make test      # pytest -q across libs/py_common + the three backends
```

`pyproject.toml` configures `asyncio_mode = "auto"`, so `async def test_…` functions are detected automatically.

## Prerequisites

- Python **3.12+** and [`uv`](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Node **20+** (`nvm install 20`)
- Docker (only for `make up` and the postgres/redis side of `make dev`)
- `ripgrep` (only for `make lint`)

## Environment

`.env.example` is the source of truth. Copy to `.env` (or let `scripts/dev.sh` do it). Notable variables:

| Var | Default | Used by |
|---|---|---|
| `BOT_CONFIG_PATH` | auto-discovered | Python services — overrides `config/bot.json` lookup |
| `LIVE_TRADING` | `false` | trading-service — must also be `true` along with `I_UNDERSTAND_REAL_MONEY` to start in `environment=live` |
| `I_UNDERSTAND_REAL_MONEY` | `false` | trading-service — see above |
| `NEXT_PUBLIC_*_API` | `http://localhost:800{1,2,3}` | frontend — point the dashboard at non-default backends |

`config/bot.json` ships with safe defaults: `broker=mock` and `compliance.provider=mock`. Swap these once the real implementations land — `Trading212Broker` will give you a clear error message if you point at it before then.

## Repo layout

```
backend/
  market_data_service/    instrument master, OHLCV, compliance lookup
  trading_service/        orders, positions, broker boundary, kill-switch + live-mode guard
  strategy_service/       regime detection, strategies, backtests
libs/
  py_common/              shared protocols (broker, compliance), config loader, logging, decimal utils
frontend/                 Next.js 14 dashboard (App Router + react-query)
infra/                    docker-compose, postgres init.sql
config/                   bot.json + bot.schema.json
scripts/
  dev.sh                  hybrid dev runner (this is the one you want)
  logging_lint.sh         no-print() lint
  run_backtest.py         CLI entry to backtest service
docs/                     ARCHITECTURE.md, IMPLEMENTATION_PLAN.md, RUNBOOK.md, LIVE_READINESS.md
retrospective-main.md     code retrospective for the current `main` branch
```

## Running just one service in isolation

```bash
uv run uvicorn app.main:app --reload --app-dir backend/market_data_service --port 8001
```

The config loader walks up from CWD to find `config/bot.json`, so this works from any directory.
