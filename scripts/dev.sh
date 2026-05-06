#!/usr/bin/env bash
# Hybrid dev runner: docker for postgres+redis, local processes for everything else.
#
#   ./scripts/dev.sh             # start everything; Ctrl-C stops the foreground processes
#   ./scripts/dev.sh --down      # also stop the docker postgres/redis on exit
#   ./scripts/dev.sh --no-infra  # skip docker entirely (assume postgres/redis are already up)
#   ./scripts/dev.sh --no-fe     # skip the Next.js frontend (backend-only loop)
#   ./scripts/dev.sh --help      # show this help
#
# Logs from each child process are prefixed with a tag and a colour so you can
# eyeball which service is talking. Ctrl-C cleanly shuts down all children.

set -euo pipefail

# Enable job control so background pipelines belong to this shell's job table.
# Without this, Ctrl-C cleanup often kills only the `sed` side of `cmd | sed` and
# leaves uvicorn / next dev running.
set -m 2>/dev/null || true

# --- locate repo root -------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT}"

# --- parse args -------------------------------------------------------------
DOWN_ON_EXIT=0
SKIP_INFRA=0
SKIP_FRONTEND=0
for arg in "$@"; do
  case "${arg}" in
    --down)      DOWN_ON_EXIT=1 ;;
    --no-infra)  SKIP_INFRA=1 ;;
    --no-fe|--no-frontend) SKIP_FRONTEND=1 ;;
    -h|--help)
      sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *)
      echo "Unknown flag: ${arg}" >&2
      exit 2 ;;
  esac
done

# --- colours / logging helpers ---------------------------------------------
if [ -t 1 ]; then
  RESET=$'\033[0m'; BOLD=$'\033[1m'; DIM=$'\033[2m'
  RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'
  BLUE=$'\033[34m'; MAGENTA=$'\033[35m'; CYAN=$'\033[36m'
else
  RESET=''; BOLD=''; DIM=''; RED=''; GREEN=''; YELLOW=''; BLUE=''; MAGENTA=''; CYAN=''
fi

log()  { printf '%s[dev]%s %s\n' "${BOLD}${CYAN}" "${RESET}" "$*"; }
warn() { printf '%s[dev]%s %s\n' "${BOLD}${YELLOW}" "${RESET}" "$*"; }
err()  { printf '%s[dev]%s %s\n' "${BOLD}${RED}" "${RESET}" "$*" >&2; }

# --- prereq checks ---------------------------------------------------------
need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "missing required tool: $1"
    case "$1" in
      uv)     err "  install: curl -LsSf https://astral.sh/uv/install.sh | sh" ;;
      docker) err "  install Docker Desktop or run with --no-infra after starting postgres/redis manually" ;;
      node)   err "  install Node 20 (https://nodejs.org or 'nvm install 20')" ;;
    esac
    return 1
  fi
}

MISSING=0
need uv || MISSING=1
[ "${SKIP_INFRA}" -eq 1 ] || need docker || MISSING=1
[ "${SKIP_FRONTEND}" -eq 1 ] || need node || MISSING=1
[ "${MISSING}" -eq 0 ] || exit 1

# --- bootstrap .env --------------------------------------------------------
if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
  log "created .env from .env.example"
fi

# --- start postgres + redis (unless --no-infra) ----------------------------
if [ "${SKIP_INFRA}" -eq 0 ]; then
  log "starting postgres + redis via docker compose"
  docker compose -f infra/docker-compose.yml --profile dev up -d postgres redis >/dev/null
fi

# --- sync python deps ------------------------------------------------------
log "uv sync (workspace)"
uv sync --all-extras

# --- frontend deps ---------------------------------------------------------
if [ "${SKIP_FRONTEND}" -eq 0 ]; then
  if [ ! -d frontend/node_modules ]; then
    log "installing frontend deps"
    if [ -f frontend/package-lock.json ]; then
      (cd frontend && npm ci --silent)
    else
      (cd frontend && npm install --silent)
    fi
  fi
fi

# --- launch services with prefixed/coloured output -------------------------
PIDS=()

run() {
  local tag="$1" colour="$2"; shift 2
  ( "$@" 2>&1 | sed -u "s|^|${BOLD}${colour}[${tag}]${RESET} |" ) &
  PIDS+=($!)
}

kill_pid_tree() {
  local root="$1"
  [ -n "${root}" ] || return 0
  local c
  for c in $(pgrep -P "${root}" 2>/dev/null || true); do
    kill_pid_tree "${c}"
  done
  kill "${root}" 2>/dev/null || true
}

cleanup() {
  local code=$?
  echo
  log "shutting down…"

  # Prefer killing known roots + their descendants (works with cmd | sed pipelines).
  for pid in "${PIDS[@]:-}"; do
    kill_pid_tree "${pid}"
  done

  # Fallback: any remaining background jobs started from this shell.
  jobp=$(jobs -p 2>/dev/null || true)
  if [ -n "${jobp}" ]; then
    for pid in ${jobp}; do
      kill_pid_tree "${pid}"
    done
  fi
  sleep 0.2
  jobp=$(jobs -p 2>/dev/null || true)
  if [ -n "${jobp}" ]; then
    for pid in ${jobp}; do
      kill -9 "${pid}" 2>/dev/null || true
    done
  fi

  for pid in "${PIDS[@]:-}"; do
    wait "${pid}" 2>/dev/null || true
  done
  if [ "${DOWN_ON_EXIT}" -eq 1 ] && [ "${SKIP_INFRA}" -eq 0 ]; then
    log "stopping postgres + redis (--down)"
    docker compose -f infra/docker-compose.yml down >/dev/null || true
  fi
  exit "${code}"
}
trap cleanup INT TERM EXIT

export BOT_CONFIG_PATH="${BOT_CONFIG_PATH:-${ROOT}/config/bot.json}"
export PYTHONUNBUFFERED=1

run market   "${GREEN}"  uv run uvicorn app.main:app --reload --app-dir backend/market_data_service --host 0.0.0.0 --port 8001
run trading  "${BLUE}"   uv run uvicorn app.main:app --reload --app-dir backend/trading_service     --host 0.0.0.0 --port 8002
run strategy "${MAGENTA}" uv run uvicorn app.main:app --reload --app-dir backend/strategy_service   --host 0.0.0.0 --port 8003

if [ "${SKIP_FRONTEND}" -eq 0 ]; then
  run frontend "${YELLOW}" npm --prefix frontend run dev
fi

# --- banner ---------------------------------------------------------------
sleep 1
echo
echo "${BOLD}  trading212bot — dev mode${RESET}"
echo "  ${DIM}market-data${RESET}     http://localhost:8001/health"
echo "  ${DIM}trading${RESET}         http://localhost:8002/health"
echo "  ${DIM}strategy${RESET}        http://localhost:8003/health"
[ "${SKIP_FRONTEND}" -eq 0 ] && echo "  ${DIM}frontend${RESET}        http://localhost:3000"
echo "  ${DIM}postgres${RESET}        localhost:5432  (user=postgres db=tradingbot)"
echo "  ${DIM}redis${RESET}           localhost:6379"
echo
echo "  ${BOLD}Ctrl-C${RESET} to stop. Pass ${BOLD}--down${RESET} to also stop postgres+redis."
echo "  ${DIM}If processes survive:${RESET} ${BOLD}pkill -f 'next dev'${RESET} · ${BOLD}pkill -f uvicorn${RESET} · or ${BOLD}Ctrl-\\\\${RESET} (SIGQUIT)"
echo

# Wait until any supervised child exits, then exit so the EXIT trap runs cleanup.
# macOS /bin/bash is 3.2 and does not support `wait -n` (bash 4.3+).
while true; do
  for pid in "${PIDS[@]:-}"; do
    if ! kill -0 "${pid}" 2>/dev/null; then
      exit 1
    fi
  done
  sleep 0.4
done
