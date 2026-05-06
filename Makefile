.PHONY: help dev up down test typecheck lint migrate seed backtest clean

help:
	@echo "Targets:"
	@echo "  make dev        Hybrid dev: docker postgres+redis, local uvicorn --reload x3, next dev (one Ctrl-C stops all)"
	@echo "  make up         Full docker compose (everything containerized)"
	@echo "  make down       Stop docker compose"
	@echo "  make test       Run pytest across backends + py_common"
	@echo "  make typecheck  (TODO)"
	@echo "  make lint       Logging lint (no print() in non-test code)"
	@echo "  make migrate    (TODO Phase 2: Alembic)"
	@echo "  make seed       (TODO Phase 2)"
	@echo "  make backtest   (TODO Phase 4)"
	@echo "  make clean      Remove __pycache__ artifacts"

dev:
	./scripts/dev.sh

up:
	docker compose -f infra/docker-compose.yml --profile dev up -d --build

down:
	docker compose -f infra/docker-compose.yml down -v

test:
	@./scripts/test.sh

typecheck:
	@echo "TODO Phase 2: wire mypy --strict"

lint:
	./scripts/logging_lint.sh

migrate:
	@echo "TODO Phase 2: wire Alembic"

seed:
	@echo "TODO Phase 2: seed baseline taxonomy"

backtest:
	@echo "TODO Phase 4: run backtest harness"

clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
