-- phase 1 baseline for strategy-service
CREATE TABLE IF NOT EXISTS market_regimes (
  id UUID PRIMARY KEY,
  regime TEXT NOT NULL,
  detected_at TIMESTAMPTZ NOT NULL
);
