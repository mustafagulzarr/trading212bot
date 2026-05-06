-- phase 1 baseline for market-data-service
CREATE TABLE IF NOT EXISTS instruments (
  id UUID PRIMARY KEY,
  symbol TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
