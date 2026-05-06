#!/usr/bin/env bash
# Run pytest across the workspace.
#
# Why one invocation per backend service: each service ships its source under
# the package name `app/`. Three different `app/` packages cannot coexist in
# the same Python process; we therefore run a separate pytest for each, with
# only that service's directory on PYTHONPATH.

set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

EXIT=0

run_in() {
  local label="$1" tests_dir="$2" service_dir="${3:-}"
  if [ ! -d "${tests_dir}" ]; then
    return 0
  fi
  echo
  echo "==> ${label}"
  if [ -n "${service_dir}" ]; then
    PYTHONPATH="${service_dir}${PYTHONPATH:+:${PYTHONPATH}}" \
      uv run pytest -q "${tests_dir}" || EXIT=$?
  else
    uv run pytest -q "${tests_dir}" || EXIT=$?
  fi
}

run_in "libs/py_common"            "libs/py_common/tests"
run_in "market_data_service"       "backend/market_data_service/tests"  "backend/market_data_service"
run_in "trading_service"           "backend/trading_service/tests"      "backend/trading_service"
run_in "strategy_service"          "backend/strategy_service/tests"     "backend/strategy_service"

exit "${EXIT}"
