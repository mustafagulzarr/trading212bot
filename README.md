# trading212bot

## 5-minute quick start

1. Copy environment defaults:
   ```bash
   cp .env.example .env
   ```
2. Start services:
   ```bash
   make up
   ```
3. Verify health checks:
   ```bash
   curl http://localhost:8001/health
   curl http://localhost:8002/health
   curl http://localhost:8003/health
   ```
4. Open frontend placeholder:
   - http://localhost:3000

## Phase 0 status
- Monorepo scaffolding created.
- Backend service stubs expose `/health`.
- Docker Compose profile scaffolding included.
