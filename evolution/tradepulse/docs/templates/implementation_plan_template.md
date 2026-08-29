# [<PLAN-ID>] — [<Short Description>] — Implementation Plan

**Plan Family**: `<g|h|i|j|a|b|c|d|e|f>` · **Plan ID**: `<family><n>` (e.g. `g4`, `h1`, `i2`)
**Branch**: `feat/<family><n>-<short-desc>` (per v4 §3)
**Priority**: `High / Medium / Low` (per architecture assessment severity)
**Estimated Effort**: `X-Y days` (per master plan §3 sequencing)
**Standards reference**: `docs/development_standards_compressed.md`
**Workflow reference**: `docs/workflow_guide.md` (Phases F1–F5; Bug Fix Phases B1–B7)
**Master doc**: `docs/implementation_plans/g0_ultimate_assistant_master_plan_2026_07.md` (G-series plans)
**Issue doc** (for bug fixes): `docs/issues/<ID>_<short>_root_cause_<YYYY_MM>.md`

> **All `file:line` references below will be verified at F1** by `scripts/verify_plan_f1.py`. Drift between plan and live code is the #1 cause of broken PRs.

---

## Objective

[What this plan accomplishes in 2-3 sentences. Cite the user-experience gap from `g0_ultimate_assistant_master_plan_2026_07.md` §1 or `data_source_strategy_benzinga_bloomberg_2026-07-08.md` if applicable. No hardcoded numbers — link to existing docs.]

## Success Criteria

- [Measurable outcome 1 — what the trader/user can do after this is done]
- [Measurable outcome 2]
- [Performance target with a specific metric, e.g. "p95 latency < N ms"]
- [User experience improvement, e.g. "Fade card now displays squeeze_risk"]
- [Backward compatibility: existing API responses not broken; `provider_drift_total` increments on code drift]

## Value Proposition for the Day Trader

[One paragraph. Specific to short-selling day-trading on small caps, not generic.]

---

## Plain-Language Summary

| Aspect | Description |
|---|---|
| **What's being built** | [One sentence a non-engineer can understand] |
| **Where in the pipeline** | [Which stage(s) of the TradePulse 9-stage flow, with file paths] |
| **What type of change** | `feature / bug fix / refactor / data migration / docs / performance optimization` |
| **The fix in plain English** | [One sentence] |

---

## Architecture Overview

### System Integration Points (NEW: must be exhaustive)

| File | Line | Role |
|---|---|---|
| `<new file>` | `<loc>` | [what it does] |
| `<existing file>` | `<line of integration>` | [what part] |

### New vs. Modified vs. Untouched

- **New**: files this plan adds (with their reason).
- **Modified**: files this plan edits, with the specific lines/ranges.
- **Untouched but dependent**: files whose behavior shifts because this plan changes their input/contract.

### Data Flow Diagram

Only when non-obvious. Use ASCII or Mermaid. Cite file:line on the edges. Don't restate code.

---

## Configuration (NEW in v4)

### `.env` (live values)

```dotenv
# Add here
NEW_KEY=value
```

### `config_specification.yaml` (defaults)

```yaml
<plan_family>:
  <plan_section>:
    <key>: <value>
    defaults:
      <key>: <default>    # class-level fallback in app/core/config.py
```

### `app/core/config.py` (typed access)

```python
class Settings(BaseSettings):
    NEW_KEY: <type> = <default>
```

### New Prometheus Counters (NEW in v4 — required if plan adds metrics)

| Counter | Labels | Emitted when |
|---|---|---|
| `tradepulse_<domain>_<noun>_total` | `["label_a", "label_b"]` | [when the metric ticks] |
| `tradepulse_<domain>_<state>_gauge` | `["label_a"]` | [when the gauge updates] |

Use `provider_drift_total{provider, method, kind}` from F6 if you add a new provider. Existing counter pattern is at `app/core/prometheus_metrics.py:898-935` (F2/F4/F6 counter declarations).

---

## Implementation Phases

### Phase 1: Foundation

**Tasks**

1. Configuration — 3-step lifecycle (`.env` + `config_specification.yaml` + `app/core/config.py`).
2. Database schema (Alembic migration if any).
3. Base classes / models.

**Deliverables**

- [ ] Configuration externalized
- [ ] Database schema migrated (if applicable)
- [ ] Base classes implemented

### Phase 2: Core Implementation

**Tasks**

1. Main logic — follow dev-standards §10 "File Consistency Rule": match existing patterns in each file you modify.
2. API integration (FastAPI route, Pydantic request/response models).
3. Caching layer (if needed).
4. **Provider calls must use `safe_provider_call`** (F6).
5. **Prometheus counters must be declared in §"New Prometheus Counters" above.**

**Deliverables**

- [ ] Core logic implemented
- [ ] API endpoints functional
- [ ] Tests written alongside code

### Phase 3: Testing

**Tasks**

1. Unit tests covering every public method of every new/modified class.
2. Integration tests for API endpoints.
3. Live integration tests (gated on live API keys).

**Deliverables**

- [ ] Tests pass: `pytest tests/fast/unit/<plan>.py -v`
- [ ] Anti-pattern checker shows **no new findings** in files you modified.
- [ ] `scripts/verify_plan_f1.py docs/implementation_plans/<this-plan>.md` exits 0 at the moment of commit.

---

## F1 — Pre-Implementation Verification (mandatory)

Before writing code, run `scripts/verify_plan_f1.py` against this plan; if it fails, the plan is stale. Fix or note the drift in this section.

In phase F1, also confirm:

- [ ] Every `file:line` reference in this plan points at live code.
- [ ] Every `from app.X import Y` has been re-checked.
- [ ] `config_specification.yaml` has the sections this plan declares (added in §"Configuration").
- [ ] If plan creates a `Base` subclass, no Alembic migration conflicts.
- [ ] If plan adds a Prometheus counter, name follows `tradepulse_<domain>_<noun>_total` pattern.

---

## Risk and Mitigation Matrix (NEW in v4)

| Risk | Likelihood | Mitigation |
|---|---|---|
| Plan-line drift | High | F1 verifier script gates the commit |
| Multi-agent working-tree contamination | High | §6 protocol: pre-stage `git status` check |
| Silent counter-name collision | Medium | §7.1 naming convention; reviewer checks |
| Working tree has untracked files you didn't author | Medium | §6.1 stop-or-yield protocol |
| Bare `except Exception` regression | Low | F2 fix: only `safe_provider_call` is permitted |

---

## Pre-Implementation Checklist (mandatory before F2 starts)

- [ ] DB access: `get_db()` for sync ORM or `get_async_db()` for async — never mixed (`dev-standards_compressed.md` §1).
- [ ] Magic numbers: all thresholds use `settings.spec.get("key", DEFAULT_CONSTANT)` (`dev-standards_compressed.md` §2).
- [ ] Singleton factories: simple `if None: create` (parameterless) or parameter-update for parameterized.
- [ ] Provider calls: use `safe_provider_call` from `app/core/safe_provider_call.py`. Do not write `except Exception as e:` blocks (`dev-standards_compressed.md` §5).
- [ ] Telemetry: Prometheus counters on all success/error exit paths. Failure paths must update metrics before returning.
- [ ] Lazy imports: inside methods when cross-service circular dependencies exist.
- [ ] Timing: `time.monotonic()` for elapsed; `now_utc()` for wall-clock.
- [ ] Backward compatibility: new dataclass/model fields have defaults; new config sections have `DEFAULT_*` class constants.
- [ ] File consistency: match existing patterns within each file.
- [ ] DB schema / Alembic: if `app/models/` was modified, generate + apply migration.

---

## Expected Outcomes

### For the Day Trader

- **Immediate benefits**
- **Time savings** (quantified)
- **Performance improvement**
- **Risk reduction**

### Technical Metrics

- **Response time**: target p95
- **Throughput**: target req/s
- **Reliability**: error rate target
- **Observability**: counter increments per plan's path

---

## Implementation Checklist

- [ ] Plan created from this template
- [ ] F1 verification passed (`scripts/verify_plan_f1.py`)
- [ ] Plan-family + branch name confirmed per v4 §3
- [ ] Implementation complete (F2)
- [ ] Tests pass (F3)
- [ ] Anti-pattern checker clean on modified files
- [ ] Implementation report written (F4)
- [ ] PR opened (F5) with conventional-commits body

---

## Open Questions

[Anything the plan does not yet resolve. Flag here, not in code.]
