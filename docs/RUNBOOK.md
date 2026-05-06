# RUNBOOK

## Emergency halt
- Set `BOT_ENABLED=false` in config and reload services.
- If running live, revoke Trading 212 API key immediately.

## Live mode safety
- Live mode requires both:
  - `LIVE_TRADING=true`
  - `I_UNDERSTAND_REAL_MONEY=true`

## Partial fill recovery
- Call `POST /reconcile` in trading-service.
- Validate positions and open orders manually.

## DB outage
- Stop order placement.
- Restore database from latest backup.
- Reconcile broker state before re-enable.
