# Load Context — minimum-viable context loader

> Single-page summary for a fresh thread. Read in 5 minutes; brings an AI up to Phase 0.

## 1. What this codebase is

TradePulse: a solo day-trader's short-bias small-cap trading assistant. FastAPI monolith on Windows 11 + PowerShell. Python 3.11, asyncpg + pgvector, IBKR (primary provider), Alpaca, Yahoo, Finnhub, FMP, Polygon, TwelveData, OpenAI ReAct, Slack ingest, Temporal workers. Companion frontend in a separate repo (Vega).

## 2. What to read (in order)

| # | Doc | Lines | Why |
|---|---|---|---|
| 1 | `docs/framework.md` | all | Operating procedure — phases, gate phrases, multi-agent rules, counter naming, F1 verifier |
| 2 | `docs/workflow.md` | all | 6-phase feature workflow + 7-phase bug-fix workflow + recovery protocols |
| 3 | `docs/standards.md` | all | Mandatory constraints, code-review checklist, patterns |
| 4 | `docs/instance/load_context.md` | all | Project-specific overlay (master plan, key files, current state) |

Then read the codebase shape:

| File | Why |
|---|---|
| `app/main.py` | Lifespan, router mounts, the picture of the whole system |
| `app/services/unified_market_data_client.py` (top comment) | 7-tier fallback chain priority |
| `app/core/safe_provider_call.py` | Every provider call must use it |
| `app/core/prometheus_metrics.py` | Where new counters go |

## 3. The 5 hard rules

1. **Code is the source of truth.** Docs are a guide. `scripts/verify_plan_f1.py` proves it.
2. **No deleted code.** Deprecate with a comment, leave the file.
3. **One plan → one branch → one PR.** Bundling is forbidden.
4. **Settings 3-step lifecycle.** Field + YAML + `_apply` mapping + test, all in one change.
5. **`safe_provider_call` for every provider call.** No `except Exception: errors.append(...)` patterns.

## 4. Common commands (Windows / venv)

```powershell
# Activate venv
.\venv\Scripts\activate

# Health check
Invoke-RestMethod http://localhost:8000/health

# Provider health
Invoke-RestMethod http://localhost:8000/api/trust/source-health

# Run unit tests
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m pytest tests/fast/unit/ -q -p no:warnings --tb=short

# Run a single test file
.\venv\Scripts\python.exe -m pytest tests/fast/unit/test_<name>.py -v -p no:warnings

# Anti-pattern checker
.\venv\Scripts\python.exe scripts/check_anti_patterns.py

# F1 verifier
.\venv\Scripts\python.exe scripts\verify_plan_f1.py docs\implementation_plans\<plan>.md

# Generate / apply Alembic migration
.\venv\Scripts\python.exe -m alembic revision --autogenerate -m "<description>"
.\venv\Scripts\python.exe -m alembic upgrade head

# Start / stop / restart / status
.\start_development.bat
.\stop_development.bat
.\restart_development.bat
.\status_development.bat
```

## 5. Multi-agent guard

Before staging, run `git status`. If you see files modified or untracked that you didn't author — another agent is working in this tree. Decide: take it or yield it. Never push with another agent's uncommitted or unstaged changes in your tree.

## 6. The phase gate phrases (verbatim, end each phase with one)

```
✅ Plan verified against codebase. All insertion points confirmed. Proceeding to implementation.   (F1)
✅ Implementation complete. All component tests pass. Proceeding to regression testing.              (F2)
✅ All tests pass (N total, M new). No regressions detected. Proceeding to ship.                    (F3)
✅ Branch pushed. PR opened. Ready for review.                                                      (F4+F5)
✅ Root cause identified. Proceeding to documentation.                                              (B1)
✅ Simple change verified. Implementing with validation.                                            (Fast-track)
```

## 7. The 4 templates you need

| Use when | Template |
|---|---|
| Adding code (feature) | `docs/templates/implementation_plan_template.md` |
| Adding `docs/issues/<ID>_*.md` | `docs/templates/issue_root_cause_analysis_template.md` |
| F1 / phase reference | `docs/templates/phase_gate_checklist.md` |
| ASCII data-flow trace (required in every RCA) | `docs/templates/root_cause_dataflow_trace_guide.md` |
| Rollback / recovery | `docs/workflow.md` §"Recovery Protocols" |

That's it. 5 minutes, you're at Phase 0.