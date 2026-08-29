# TradePulse — Instance Overlay

> TradePulse-specific load-context. The framework spine (`docs/framework.md`, `docs/workflow.md`, `docs/standards.md`) is project-agnostic. This file is the **project-specific overlay** that says "here is what is wired in TradePulse, today".

---

## 1. What TradePulse is

TradePulse is a solo day-trader's short-bias small-cap trading assistant. The user is the only trader; the system exists to give that one person an institutional-grade edge. When G1–G6 are complete, the daily experience is:

1. A ticker starts moving. Within seconds TradePulse has it: from scanners (RVOL, big mover, microstructure) or from the Slack community feed — whichever fires first.
2. TradePulse answers "what is moving and why" — for every candidate it assembles catalyst truth, extension metrics, borrow reality, price levels, community read.
3. TradePulse renders a verdict: **WATCH / STALK / IGNORE**, with a single **Fade Card** for STALK-grade: thesis, entry zone, stop, invalidation, size — computed from the actual account risk budget.
4. Everything arrives on the frontend (port 3000) via WebSocket with audio priority for A-grade setups.
5. Every card is graded afterwards against realized price action and (later) IBKR fills. The system learns which setups pay *for this trader* and recalibrates.

**Test of success (plain English):** On a day like 2026-07-06, when Slack says "INLF pop" at 20:46 and INLF is +82% with 223k shortable shares, halt history, 4 rejections at $6.63 — the trader's screen shows a ranked Fade Card within a minute, with the borrow, the catalyst verdict, the level, and the risk plan.

## 2. Architecture at a glance

```
                       ┌─────────────────────────────────────┐
                       │  Frontend (Vega, separate repo)    │
                       │  port 3000, WebSocket consumer     │
                       └─────────────┬───────────────────────┘
                                     │ WebSocket / REST
                       ┌─────────────▼───────────────────────┐
                       │  FastAPI monolith  (port 8000)      │
                       │  app/main.py  · 70+ routers         │
                       │  · Slack ingest (slack_processor)   │
                       │  · Scanner engine (50-symbol watch) │
                       │  · Comprehensive ticker profile     │
                       │    (14-source fan-out)              │
                       │  · Realtime processor + WS delivery │
                       └────┬──────────────┬─────────────┬────┘
                            │              │             │
                  ┌─────────▼──────┐ ┌──────▼──────┐ ┌───▼─────────┐
                  │  IBKR (TWS)    │ │  Alpaca REST │ │  Polygon    │
                  │  PRIMARY       │ │  + WS        │ │  (needs     │
                  │  quotes/bars   │ │  fallback    │ │  API key)   │
                  └────────────────┘ └──────────────┘ └─────────────┘
                            │
                  ┌─────────▼──────────────────────────────┐
                  │  Fundamentals (Yahoo → Finnhub →       │
                  │  AlphaVantage → FMP → Benzinga)        │
                  │  News (Tavily + SEC EDGAR + Benzinga)   │
                  │  Borrow (IBKR shortable)               │
                  └────────────────────────────────────────┘
                            │
                  ┌─────────▼──────────────────────────────┐
                  │  PostgreSQL (asyncpg) + pgvector       │
                  │  Redis (dedup + cache)                 │
                  │  Temporal worker (background jobs)     │
                  └────────────────────────────────────────┘
```

To discover the live scale of any layer, do not use hardcoded numbers from any doc. Run:

```bash
# How many routers?
grep -r "@router\." app/api app/routers -l | wc -l

# How many models?
grep -r "^class .*Base" app/models/*.py | wc -l

# How many Prometheus counters?
grep -c "^Counter\|^Gauge\|^Histogram" app/core/prometheus_metrics.py
```

## 3. The 9-stage data flow

```
1. Ingestion        — slack_client WS / cron / REST
2. Parsing          — message_quality_filter, symbol_extractor
3. Analysis         — experts/react_engine.py, unified_market_data_client
4. Dedup/Filter     — core/cache + DedupService (Redis SETNX)
5. Scoring          — stock_selection_scoring_service
6. Storage          — app/models/database.py (AsyncSession)
7. Aggregation      — advisory/morning_briefing_service, eod_report_service
8. API Serving      — FastAPI Depends(ServiceContainer)
9. Reporting        — slack_adapter, eod_report_*, csv writers
```

## 4. Key files to know

| File | Why |
|---|---|
| `app/main.py` | Lifespan, all router mounts, the system in one file |
| `app/services/unified_market_data_client.py` | 7-tier quote fallback; top comment defines priority |
| `app/services/fundamentals_provider.py` | Yahoo → Finnhub → AV → FMP fallback |
| `app/services/ibkr_client.py` | IBKRClient + client-ID range allocation |
| `app/services/comprehensive_ticker_profile_service.py` | The 14-source fan-out for ticker profile |
| `app/core/safe_provider_call.py` | Provider-call helper (mandatory) |
| `app/core/prometheus_metrics.py` | Where new counters go |
| `app/core/circuit_breaker.py` | Circuit breaker for external APIs |
| `app/core/database.py` | `get_db()` (sync), `get_async_db()` (async) |
| `app/models/database.py` | SQLAlchemy `Base` subclasses |
| `app/services/scanner_engine.py` | 50-symbol watchlist scanner |
| `app/services/slack_processor.py` | Slack message ingest |

## 5. The product roadmap (master plan)

`docs/implementation_plans/g0_ultimate_assistant_master_plan_2026_07.md` defines the target state. The G-series ships in this order:

```
G1 (evidence) → G2 (IBKR bars) → G3 (WS delivery)
                                        │
        G5 (Slack intel) ────────────────┤
                                        ▼
                                  G4 (Fade Engine)
                                        │
                                        ▼
                                  G6 (outcome loop)
```

Plan-family letters: `g` (product), `h` (short-bias inputs), `i` (Benzinga), `j` (data integrity substrate). Legacy families: `a/b/c/d/e/f`.

## 6. What's shipped (do not redo)

- **F1** — IBKR cancelMktData hygiene
- **F2** — typed-exception helper (`safe_provider_call`) for all provider calls
- **F4** — FMP `CircuitBreaker.is_open()` rename
- **F5** — async/sync cleanup in `comprehensive_ticker_profile_service`
- **F6** — provider-drift counter (`tradepulse_provider_drift_total{provider,method,kind}`)
- **G1** — evidence-chain repair
- **Polygon `get_historical_data`** fix (the old `get_bars` doesn't exist; the rename is canonical)

## 7. Live status — discover, don't trust the docs

Run these to know what is currently wired:

```powershell
# Backend alive?
Invoke-RestMethod http://localhost:8000/health

# Providers up/down + last success
(Invoke-WebRequest http://localhost:8000/api/trust/source-health -UseBasicParsing).Content

# Today's log lines, by logger (what was actually called)
Get-Content logs\tradepulse.log | Select-String '"logger":' | ForEach-Object {
  ($_ | ConvertFrom-Json).logger
} | Group-Object | Sort-Object Count -Descending | Select-Object -First 15

# Today's errors, by logger
Get-Content logs\tradepulse_errors.log | ForEach-Object {
  try { ($_ | ConvertFrom-Json).logger } catch {}
} | Group-Object | Sort-Object Count -Descending | Select-Object -First 10
```

## 8. Live hazards — known operational risks

These have produced real incidents and are tracked in `docs/issues/`:

- **IBKR port unreachable at startup** — first 30-90 min of each market day, no IBKR quotes. The codebase assumes the user starts TWS before uvicorn.
- **Polygon `not_configured` without `POLYGON_API_KEY`** — historical bars then rely on IBKR + Alpaca free tier; single failure = no history. Get a paid tier to enable the third-party arbiter.
- **Alpaca `[FORBIDDEN]` after key rotation** — fixed in past sessions; if it reappears, it's a regression in `alpaca_client.py`.
- **FMP `'CircuitBreaker' object has no attribute 'is_open'`** — fixed in F4; if it reappears, the rename was reverted.
- **Tavily `[QUOTA_EXCEEDED]`** — Tavily's circuit breaker opens when quota is exhausted; degrades to no news rather than crashing.
- **Slack `messages_processed: 0`** — the room is connected but no traffic; usually means the user isn't in the watched channels.
- **Provider drift** — every counter renaming / method signature change produces `tradepulse_provider_drift_total{kind="code_drift"}` increments; if it spikes, a recent PR renamed a method.

## 9. Operational gotchas

- **Pre-existing anti-pattern findings (~383 in unrelated files)** — `scripts/check_anti_patterns.py` produces noise. Run it scoped to your files (`2>&1 | Select-String "<my_file>"`). Don't try to clear pre-existing findings in this PR — they belong to a separate cleanup plan.
- **The pre-push hook is not currently installed at `.git/hooks/`.** It is documented in `docs/framework.md` §5.2 but not wired. Until it is, multi-agent safety is convention only — be diligent.
- **`unified_quote_source_total`, `market_data_polygon_historical_total`, `tradepulse_provider_drift_total`, `tradepulse_fmp_request_errors_total`** all exist. New plans add new counters following the same `prometheus_metrics.py` pattern.
- **`alembic upgrade head`** is required before any service that touches new schema columns starts.

## 10. Known doc staleness

The framework docs that point at the following files should be treated with caution — they are the F-series findings that the framework itself documented as risks:

- **`docs/ai_context/MASTER_CONTEXT_LOADER.md`** — referenced by `bootstrap.md` history; does not currently exist on disk. `docs/prompts/load_context.md` is the substitute.
- **`docs/reports/data_source_strategy_benzinga_bloomberg_2026-07-08.md`** — referenced by old bootstrap; archived in chat salvage; the strategy decisions (Benzinga over Bloomberg, Ortex for borrow) are reflected in the I/H/J plans.
- **`docs/HANDOFF_PROMPT.md`** — superseded by `docs/prompts/bootstrap.md` + this overlay.

If you find a doc staleness not listed here, note it in the PR description and update this overlay.

## 11. What NOT to do

- Don't rename `PolygonClient.get_historical_data` back to `get_bars`. The old name doesn't exist.
- Don't write a new `unified_market_data_client = UnifiedMarketDataClient()` at module scope. Use the lazy factory.
- Don't add new `except Exception as e:` blocks around provider calls. Use `safe_provider_call`.
- Don't skip Phase F1. Line numbers in plans drift; the verification is the only thing that catches silent breakage.
- Don't push with `--no-verify` without asking the user.
- Don't open a PR that bundles multiple plans.
- Don't hardcode counts in any doc. Use "scan to discover".

## 12. When you ship a plan

1. Run the full test suite: `pytest tests/ -q -p no:warnings --tb=short`.
2. Run the anti-pattern checker scoped to your files.
3. Stage exactly the files you authored (use `git status`).
4. Commit with conventional-commits (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `test:`).
5. Push the branch.
6. Open a PR against `main` with: what was implemented, what was tested, deviations from plan, known limitations, next-phase dependencies.
7. Update the implementation report in `docs/implementation_reports/<plan>_implementation_report_<YYYY_MM>.md`.