# Development Standards

> **The code is the source of truth. Read it before relying on anything written here.**
>
> These standards exist so that:
> - An AI agent can write code that matches the rest of the codebase
> - A reviewer can spot drift quickly
> - A new contributor doesn't have to learn the codebase by reading hundreds of docs
>
> Every mandatory constraint is enforced by `scripts/check_anti_patterns.py` where possible. Run it before every commit. Treat its output as a hard gate.

---

## MANDATORY CONSTRAINTS (violating these blocks the PR)

### 1. DB access (mixed patterns break at runtime)

| Context | Forbidden | Correct |
|---|---|---|
| FastAPI route handlers (sync) | `async with get_db_session()` | `db: Session = Depends(get_db_session)` |
| FastAPI route handlers (true async) | `Depends(get_db_session)` | `session: AsyncSession = Depends(get_async_session)` OR `async with get_async_db() as db:` |
| Services / background tasks | `Depends(get_db_session)` | `async with get_db() as db:` (sync) OR `async with get_async_db() as db:` (true async) |
| Scripts, alembic | context manager | `SessionLocal()` acceptable |
| Anywhere outside `scripts/` | `SessionLocal()` | Use the context managers above |

**Never mix `get_db()` (sync) and `await session.execute()` (async) in the same file.** The sync session has no awaitable methods. The async session has no `.query()`. The anti-pattern checker flags this.

**`get_db()` auto-commits on clean context exit.** Do not call `db.commit()` inside the `with` block.

**`get_async_db()` does NOT auto-commit.** Call `await session.commit()` explicitly.

### 2. Settings — 3-step lifecycle (most common drift pattern)

When you add or change a `settings.<NAME>` reference, you must do **all three** in the same change:

1. **Field** in `Settings` class (`app/core/config.py`):
   ```python
   NEW_NAME: float = 80.0   # with sensible default
   ```
2. **YAML key** in `config_specification.yaml`:
   ```yaml
   <section>:
     <key>: <default>
   ```
3. **`_apply(...)` mapping** in `_sync_<vendor>_from_spec`:
   ```python
   _apply("<section>", "<key>", "NEW_NAME", transform=float)
   ```

Plus a test asserting `settings.<NEW_NAME>` exists with the expected default, and a full `pytest tests/` run to confirm no regression.

**Skip step 3 → `AttributeError` at every constructor call.** This is the PREMARKET-2026-07-06 bug class — two real incidents in 30 days. The anti-pattern checker does not yet AST-detect this; manual review is the enforcement until the checker grows it.

**Config reuse**: before adding a new setting, grep `app/core/config.py` for existing settings that cover the same concept. Reuse `ADVISORY_*`, `SCHEDULE_*`, or other existing settings rather than creating duplicates.

### 3. No magic numbers in business logic

**Forbidden: any literal in business logic.** All thresholds, timeouts, percentages, and other tunable values must come from `settings.*` (with a sensible default) or a named class constant.

```python
# ❌ WRONG
if confidence >= 0.7:
    return TRADE

# ✅ CORRECT
threshold = self.config.get("threshold", self.DEFAULT_THRESHOLD)
if confidence >= threshold:
    return TRADE
```

Class constants are preferred over config lookups when the value is truly invariant (e.g. `ABSOLUTE_MAX_WATCHLIST = 50`).

### 4. Singleton / factory patterns

| Pattern | Forbidden | Required |
|---|---|---|
| Module-level service instance | `client = APIClient()` at module top | Lazy factory `_client: Optional[...] = None; def get_client()` |
| Mutable global | `_cache = {}` at module top | DI or `app.state` |
| Global Lock | `_lock = Lock()` at module top | Instance-level |

The checker flags `name = CamelCaseClass()` at module scope for service-like names (suffixes: `Client`, `Service`, `Manager`, `Engine`, `Orchestrator`, `Tracker`, `Scheduler`, `Collector`, `Poller`, `Detector`, `Calculator`, `Aggregator`).

### 5. Exception handling

| Pattern | Forbidden | Required |
|---|---|---|
| Bare except | `except:` | `except SpecificException:` |
| Silent failure | `except: pass` | `except Exception as e: logger.error(...); raise` |
| Catch-all only | `except Exception` | Specific first, then catch-all |

```python
# ✅ GOOD — specific exceptions first, then catch-all
try:
    result = await some_operation()
except (ValueError, TypeError, AttributeError) as e:
    logger.error(f"Data error: {e}")
    context.step_failed = "data_error"
except RuntimeError as e:
    logger.error(f"Runtime error: {e}")
    context.step_failed = "runtime_error"
except Exception as e:
    logger.error(f"Unexpected error: {type(e).__name__}: {e}")
    context.step_failed = "exception"
```

### 5a. Provider calls — `safe_provider_call` mandatory

Every provider call goes through `app/core/safe_provider_call.py`. Do not write `except Exception as e: errors.append(...)` blocks around provider calls.

```python
data = await safe_provider_call(
    provider="benzinga", method="get_news",
    coro=benzinga.get_news(symbol),
    errors_list=errors,
)
```

The helper classifies exceptions: `AttributeError`/`TypeError`/`ImportError` (code drift) are logged and re-raised; transport exceptions (`aiohttp.ClientError`, `asyncio.TimeoutError`, `asyncio.CancelledError`) are appended to `errors_list` and the chain proceeds to the next source.

This is the F6 finding as canonical example.

### 6. Telemetry on every exit path

Both success and failure paths must update Prometheus counters (or equivalent metrics). A failure that masks itself in a `logger.error` is a silent failure.

```python
# ✅ GOOD — both paths instrumented
try:
    async with get_db() as db:
        db.add(record)
    play_signal_persist_total.labels(status="success").inc()
except Exception as e:
    try:
        play_signal_persist_total.labels(status="error").inc()
    except Exception:
        pass  # counter failure must not mask the real error
    logger.error("Failed to persist signal: %s", e)
```

### 6a. Counter naming convention

Format: `<tradepulse_><domain>_<noun>_total{labels}`.

Examples in current code:
```python
market_data_polygon_historical_total = Counter('tradepulse_market_data_polygon_historical_total', ...)
unified_quote_source_total = Counter('tradepulse_unified_quote_source_total', ...)
tradepulse_provider_drift_total = Counter('tradepulse_provider_drift_total', ...)
tradepulse_fmp_requests_total = Counter('tradepulse_fmp_requests_total', ...)
```

Rules:
- Prefix `tradepulse_` always (older counters may lack it; new ones must not).
- `_total` suffix for monotonic counters; `_state` / `_gauge` for state gauges.
- Labels are mandatory for any counter that fans out by provider, status, source, method.
- Every plan that adds a counter declares it in the plan's §Configuration.
- Place new `Counter(...)` blocks immediately above the `# ====` separator that closes the existing section in `app/core/prometheus_metrics.py`.

### 7. Time and timezone

| Use case | Forbidden | Correct |
|---|---|---|
| Elapsed time | `time.time()` | `time.monotonic()` |
| Wall-clock timestamp | `datetime.now()` or `datetime.utcnow()` | `from app.core.timezone_utils import now_utc, now_local, now_et` |
| Timezone-aware comparison | naive `datetime.now()` | `now_utc()` (always timezone-aware) |

`time.monotonic()` is not affected by clock adjustments; use it for in-process age tracking. `time.time()` is for Unix epoch only.

### 8. Imports

- **Absolute imports only.** No `from .x import` / `from ..x import`. The checker flags this.
- **No `try/except ImportError` workarounds.** Use a lazy import inside the method if the import would create a cycle. The checker flags this as a warning.
- **Top-level imports**: stdlib, `app.core.config`, `app.core.timezone_utils`, same-layer peers. Cross-service imports must be lazy.

### 9. Backward compatibility

- New dataclass/model fields have defaults: `field: Optional[X] = None` or `field: bool = False`.
- New config sections have `DEFAULT_*` class constants so the service works without config.
- Factory functions returning `None` when disabled must be handled by callers.
- New DB columns: `nullable=True` or `server_default`. Alembic migration required.

### 10. No workarounds

Fix the root cause cleanly in one place. If a path changes, update every caller. **No temporary compatibility layers without a documented removal date.**

The 3-step settings lifecycle (§2) is a specific instance of this rule: a "compatibility" approach (silently catching `AttributeError` in the consumer) was the workaround that produced two real bugs. The rule is: fix it in the config layer, not in the consumer.

### 11. No code deletion without explicit user instruction

The user said recently: "Rust code can help right? If it would work, what would it do? ... I do not want the code to be removed, I want it fixed and working." Treat as a hard rule: code stays until the user says it goes. Even dead code, even legacy code, even "I don't use it" code. The blast radius of deletion (lifespan wiring, conftest fixtures, imports) is rarely worth the cleanup.

### 12. No mock data, no placeholders, no TODOs in production code

- Real data from APIs and config.
- Real tests with real fakes (e.g. `mongomock`, `aioresponses`, in-memory SQLite).
- No `MagicMock()` returning `None` to "make the test pass."
- TODO comments are fine for documenting future work, but the comment must include a date and an owner.

### 13. File consistency

When modifying an existing file, **match the patterns already in that file**:
- DB pattern (`get_db()` vs `get_async_db()`)
- Import style (lazy vs eager)
- Config access style (`settings.spec.get()` vs `settings.<NAME>`)
- Log style (`logger.error("msg: %s", e)` vs `logger.error(f"msg: {e}")`)

**Exception**: if the existing pattern violates a MANDATORY constraint (e.g. bare except), fix it as part of the change.

### 14. Alembic for every DB model change

If your plan adds or modifies a `Base` subclass in `app/models/`:

```powershell
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m alembic revision --autogenerate -m "<feature_id>:<short desc>"
.\venv\Scripts\python.exe -m alembic upgrade head
.\venv\Scripts\python.exe -m pytest tests/ -q -p no:warnings --tb=short
```

Review the autogenerated migration before committing — autogenerate misses complex index changes.

---

## Implementation patterns (best practice, not blocking)

### Dependency injection

Use the `ServiceContainer` in `app/core/dependencies.py` for routes:

```python
from typing import Annotated
from fastapi import Depends
from app.core.dependencies import Container

@router.get("/quote/{symbol}")
async def get_quote(symbol: str, container: Container):
    ibkr = await container.get_ibkr_client()
    return await ibkr.get_quote(symbol)
```

### Circuit breakers for external APIs

Use `app/core/circuit_breaker.py`. Wrap external API calls. State transitions: CLOSED → OPEN (after `failure_threshold` consecutive failures) → HALF_OPEN (after `timeout_seconds`) → CLOSED (after `success_threshold` successes in HALF_OPEN).

### Structured logging with context

The framework's `app/core/logging_config.py` already provides JSON-formatted logs with `correlation_id`, `request_id`, `trading_session`, `market_hours`. Use them; don't add your own log format.

### No global state in request handlers

All state flows through DI or `app.state`. No module-level mutable globals.

---

## CODE REVIEW CHECKLIST (P0 = must check)

- [ ] Uses DI or factory pattern, not module-level globals.
- [ ] Async operations non-blocking.
- [ ] Proper exception hierarchy (no bare except).
- [ ] Provider calls routed through `safe_provider_call`.
- [ ] Configuration-driven (no magic numbers; settings 3-step lifecycle followed).
- [ ] Lazy imports where circular dependencies would occur.
- [ ] Correct DB pattern (no sync/async mix in the same file).
- [ ] Tests written alongside code, covering every public method.
- [ ] No mock data, no placeholders, no TODOs in production code.
- [ ] Backward compatible (new fields have defaults).
- [ ] Prometheus counters on every exit path; names follow `<tradepulse_><domain>_<noun>_total{labels}`.
- [ ] No code deleted without explicit user instruction.
- [ ] Alembic migration included if `app/models/` was modified.

---

## TESTING STRATEGY

70% unit / 25% integration / 5% E2E. Tests alongside code, not after. A test for every public method of every new or modified class. Tests must mock external dependencies — no live API calls in unit tests.

When fixing a bug in a service that has zero tests: write at least one test for each public method of that service, not just the one that exercises the bug. The bug surfaced because the service was untested; don't let that continue.

---

## DON'T OVER-ENGINEER

- Aim for 70-80% test coverage, not 100%.
- Simple DI over abstract factories.
- Composition over inheritance.
- Modular monolith over microservices.
- Ship, measure, improve.