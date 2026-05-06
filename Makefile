.PHONY: up down test typecheck lint migrate seed backtest clean

up:
	docker compose -f infra/docker-compose.yml --profile dev up -d --build

down:
	docker compose -f infra/docker-compose.yml down -v

test:
	pytest -q libs/py_common/tests

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
