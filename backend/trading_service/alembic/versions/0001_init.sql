-- phase 1 baseline for trading-service
CREATE TABLE IF NOT EXISTS orders (
  id UUID PRIMARY KEY,
  idempotency_key TEXT UNIQUE NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
