# Engineering Workflow — TradePulse

> **The code is the source of truth. These docs are a guide, not a contract.** Verified by `scripts/verify_plan_f1.py`.

This is the operating procedure for every change. It is **specific to this codebase** (FastAPI monolith, asyncpg, multi-provider market data, OpenAI ReAct, Slack ingest), but the spine is project-agnostic — copy it to a new Python/FastAPI project and the rules still apply.

---

## What this is not

- Not a single-AI scratchpad. Multiple AI sessions may work concurrently on the same branch.
- Not a "best practices" essay. Each rule has a violation mode and a known fix.
- Not aspirational. Every mandatory rule has either a hook, a checker, or is explicitly labeled "reviewer-enforced".

---

## 1. Phase 0 — Load context (every thread, no exceptions)

You are starting work. Before you write a single line:

| # | Read | Why |
|---|---|---|
| 1 | `docs/framework.md` (this file) | Operating procedure — phases, gates, Council of Agents |
| 2 | `docs/workflow.md` | Feature (F1–F5) + bug-fix (B1–B7) workflows + Council constraints + recovery |
| 3 | `docs/prompts/load_context.md` | Minimum-viable context loader (one-page summary, links standards & instance overlay) |

> **⚠️ Pre-push hook status**: The pre-push hook is **not installed** in this repository. Multi-agent safety relies on convention (§5.1 contamination guard) and manual `git status` checks before staging. Do not assume automated protection.
>
> **Full context loading**: This framework applies to **ANY** change in TradePulse — from a one-line typo fix to a G-series feature. All context documents are loaded at Phase 0 to maintain systemic coherence. There is no conditional loading based on plan family or subsystem.

Then read the **codebase shape** — focused, not exhaustive:

| File | Why |
|---|---|
| `app/main.py` (lifespan, router mounts) | The picture of the whole system |
| The 7-tier provider fallback (top of `app/services/unified_market_data_client.py`) | Quote path |
| The provider-call helper `app/core/safe_provider_call.py` | Every provider call must use it |
| The counter file `app/core/prometheus_metrics.py` (existing counter block) | Where new counters land |

### Verify the live state

```bash
git status                                  # clean branch + no untracked contamination
git log --oneline -10                       # who's working on what
curl -s http://localhost:8000/health | head -c 500   # backend alive
```

If `git status` shows files modified or untracked that you didn't author — **another agent is working in this tree**. Stop. Decide: take it or yield it (see §5.1).

---

## 2. The Workflow

### 2.1 Feature Implementation (use for any new code)

Four phases (five logical steps). Each phase has a named gate phrase (verbatim, end the phase with it).

| Phase | What you produce | Gate phrase |
|---|---|---|
| **F1 — Pre-implementation verification** | Read the plan. Confirm every `file:line` reference matches live code. Confirm every import target exists. Confirm `config_specification.yaml` has the sections you need. Run `./venv/Scripts/python.exe scripts/verify_plan_f1.py <plan.md>` — must exit 0. | `✅ Plan verified against codebase. All insertion points confirmed. Proceeding to implementation.` |
| **F2 — Implementation** | Write code in plan order. Tests alongside. Follow `standards.md`. Provider calls go through `safe_provider_call`. New Prometheus counters declared in plan's §Configuration. | `✅ Implementation complete. All component tests pass. Proceeding to regression testing.` |
| **F3 — Regression testing** | Full test suite passes. `scripts/check_anti_patterns.py --paths <your_files>` shows **no new findings** on files you modified. Manual smoke test if API-affecting. | `✅ All tests pass (N total, M new). No regressions detected. Proceeding to ship.` |
| **F4+F5 — Ship it** | If SQLAlchemy `Base` subclass added → Alembic migration. Verify git identity: `git config user.name` returns `deacristi` and `git config user.email` returns `dea.cristi@gmail.com` — reject gate unless both match exactly. Stage only the files you authored. Conventional-commits. Push. Open PR against `main`. **PR body serves as concise implementation report**. A separate `docs/implementation_reports/<plan>_implementation_report_<YYYY_MM>.md` artifact is still mandatory for every shipped plan, along with updates to `IMPLEMENTATION_TRACKER.md` and `HANDOFF_PROMPT.md`. Reviewer validates standards checklist before Verifier sign-off. | `✅ Branch pushed. PR opened. Ready for review.` |

### 2.2 Bug Fix Workflow (use when root cause is unknown)

Seven phases: **B1 → B2 → B3 → B4 → B5 → B6 → B7**. Same structure, deeper root-cause discipline.

| Phase | What you produce | Gate phrase |
|---|---|---|
| B1 | Root cause investigation — 100% certainty before proceeding. | `✅ Root cause identified. Proceeding to documentation.` |
| B2 | RCA in `docs/issues/<ID>_*.md` with ASCII data-flow trace. | `✅ Documentation complete. Proceeding to solution design.` |
| B3 | Solution design following standards. | `✅ Solution design complete. Proceeding to implementation planning.` |
| B4 | Fix code + tests that reproduce the bug AND verify the fix. | `✅ Fix implemented and tested. Proceeding to validation.` |
| B5 | Full regression — same as F3. | `✅ All tests pass. No regressions detected. Proceeding to validation.` |
| B6 | Code review + validation against standards checklist. | `✅ Validation complete. Proceeding to ship.` |
| B7 | Alembic (if schema changed) + commit + push + PR. | `✅ Branch pushed. PR opened. Ready for review.` |

### 2.3 Fast-Track (rare — precise criteria below)

Fast-track applies ONLY when ALL of the following are true:
- ≤ 20 lines changed
- Single file modified
- No API endpoint changes
- No new dependencies
- No schema changes (no Alembic migration required)
- No provider client changes (`app/services/*_client.py`)
- No signal pipeline changes (detector → promoter → validator path)

```
✅ Simple change verified (fast-track).
- Current state: [one-line]
- Change: [one-line]
- Risk: Low
Implementing with validation.
```

Fast-track is **not** a waiver. Provider calls still use `safe_provider_call`. Modified file still passes `check_anti_patterns.py`. The change is still tested.

### 2.4 Council of Agents (mandatory for non-fast-track work)

Six roles enforce phase-gate separation. Production gates confirm work is done; validation gates confirm work is correct. No agent may emit a validation gate phrase for output it produced.

| Role | Owns | Verifies | Gate phrases emitted |
|---|---|---|---|
| **Architect** | Plan drafting, insertion-point confirmation | — | — |
| **F1 Verifier** | Runs `verify_plan_f1.py` on Architect's plan | Architect's plan | F1 |
| **Implementer** | Code + tests (F2/B4), regression suite (F3/B5) | Architect's plan (F1) | F2, F3, B4, B5 (production gates) |
| **Reviewer** | Solution design validation, anti-pattern scan, standards checklist, counter naming | Implementer's code & solution design | B3, B6 |
| **Verifier** | Independent test reproduction, PR readiness check | Reviewer's findings | F4+F5, B7 |
| **Root Cause Analyst** | B1 investigation, B2 RCA documentation | — | B1, B2 |

**Production vs Validation gates**: F2, F3, B4, B5 are *production* gates — the Implementer emits them after completing the work. F1, B3, B6, F4+F5, B7 are *validation* gates — they require a different role or session because they confirm correctness, not completion.

**Separation rule**: The Implementer produces F2/F3/B4/B5 output and emits those production gate phrases. Validation gates require separation: F1 requires a separate F1 Verifier session; B3 requires the Reviewer (not the Implementer who drafted the design); F4+F5/B7 require Verifier sign-off on a separate agent session or spawned `claude` agent.

**Single-session protocol**: When operating alone in one Claude Code session, declare role transitions explicitly (e.g., `[ROLE: Implementer]`, `[ROLE: Reviewer]`). Spawned agents are required for F1 verification, B3 solution design validation, and F4+F5/B7 PR readiness checks. For production gates (F2, F3, B4, B5) and B6 review, inline role transitions with explicit declaration are permitted — the same-agent identity check applies only to validation gates requiring separate sessions (F1, B3, F4+F5, B7).

**Bug-fix mapping**: B1/B2 are owned by the Root Cause Analyst (may be the same agent as Implementer, but the RCA document must be verified by a separate read-through before B3 proceeds). B3 (Solution Design validation) is owned by the Reviewer, following the same separation principle as F1.

---

## 3. Plan-Family + Plan-Id Convention

Every implementation plan follows the existing series-letter convention. The plan-id is the file name; the family letter denotes the **pipeline phase** it lands in.

| Family | Pipeline phase | Examples |
|---|---|---|
| `g` | G-series product work (master plan) | `g0` master, `g1` evidence, `g2` IBKR bars, `g3` WS delivery, `g4` fade engine, `g5` Slack intel, `g6` outcome loop, `g7` fade integration |
| `h` | Short-bias inputs | `h1` borrow aggregator, `h2` squeeze engine |
| `i` | Benzinga wire | `i1` Benzinga Tier 1, `i2` Benzinga Tier 2 |
| `j` | Data integrity substrate | `j1` source-disagreement, `j2` EDGAR substrate, `j3` dark pool |
| `a`–`f` | Legacy families | Pre-G-series cleanup, hygiene, microstructure, FMP, Slack recovery, calibration, TradeZero |

**Do not** invent new families. **Do not** number above the highest existing number in a family — if `h2` exists, the next `h` plan is `h3`.

### Branch naming

```
<family><number>-<short-description>
```

```
feat/g4-fade-thesis-engine
fix/h1-borrow-aggregator
docs/i1-benzinga-tier1-wire
chore/g0-master-plan
```

### Plan-id field (every plan begins with)

```markdown
**Plan Family**: `g`  · **Plan ID**: `g4`  · **Branch**: `feat/g4-fade-thesis-engine`
```

---

## 4. Pre-Implementation Verification (F1) — Mechanized

### 4.1 The script

`scripts/verify_plan_f1.py` greps every `file:line` reference in a plan and confirms it points at live code.

```bash
python scripts/verify_plan_f1.py docs/implementation_plans/<plan>.md
# exit 0 = pass
# exit 1 = some refs drifted; script prints which lines of which files moved
```

For each reference the script:

1. Reads the referenced file.
2. Confirms the line number is within range.
3. Reads the planned code snippet (if quoted in a ```python block); confirms it appears within ±5 lines of the cited line.

### 4.2 What F1 must also verify (manual, but mandatory)

- **Imports target exists.** Re-verify every `from app.X import Y` after the diff.
- **Config has the section.** `config_specification.yaml` has the keys (added in plan's §Configuration if missing).
- **DB models match.** If plan creates a `Base` subclass, scan `alembic/versions/` for conflicts.
- **Counter-naming.** If plan declares Prometheus counters, confirm `<domain>_<noun>_total{labels}` and registry import.
- **`check_anti_patterns.py` baseline.** Run it on the planned set before editing to baseline pre-existing findings.

### 4.3 Anti-pattern checker scope

Run `scripts/check_anti_patterns.py 2>&1 | grep` against **only the files you modified**. Confirm **no new findings** you introduced. Pre-existing findings in unrelated files are out of scope (separate cleanup plan).

---

## 5. Multi-Agent Working in Parallel

### 5.1 Council coordination & contamination guard

Before staging:

```bash
git status
```

If you see untracked or modified files you did **not** author — another agent is working in this tree. Two responses:

1. **You take it**: read their in-flight work, fold it into your plan's Implementation section.
2. **You yield it**: stash your uncommitted changes to your own branch path, let them finish.

Never push with another agent's uncommitted or unstaged changes in your tree.

When operating as a council, each role must confirm the previous role's gate phrase exists in the conversation transcript before proceeding. **Exception**: F1 and B1 are first gates in their workflows and have no preceding gate phrase; for these, verify the Architect's plan artifact or Root Cause Analyst's investigation notes exist instead. The same-agent identity check applies **only** to gates requiring separate sessions (F1, F4+F5, B7). For gates that permit inline transitions (F2, F3, B3, B4, B5, B6), a single session may emit the gate phrase after an explicit `[ROLE: ...]` declaration — see §2.4 Single-session protocol. This applies to both single-session role-switching and multi-session councils.

### 5.2 Pre-commit hook (recommended)

```bash
#!/usr/bin/env bash
# Refuse commit if `git status --porcelain` shows files outside the staged set.
python -c "
import subprocess, sys
staged = set(subprocess.check_output(['git','diff','--cached','--name-only']).decode().split())
porcelain = subprocess.check_output(['git','status','--porcelain']).decode().splitlines()
extra = set()
for line in porcelain:
    if not line: continue
    code, path = line[0:2], line[3:].strip()
    if code.strip() in ('M','A','D','R','C','U') and path not in staged:
        extra.add(path)
if extra:
    print(f'REFUSED: unstaged files present: {sorted(extra)}', file=sys.stderr)
    sys.exit(1)
"
```

### 5.3 Counter file safety

`app/core/prometheus_metrics.py` is edited by every new plan. When you add a counter, place the `Counter(...)` block immediately **above** the `# ====` separator that closes the existing section. In the commit message list the counter name. If a merge conflict surfaces on `prometheus_metrics.py`, resolve by family letter (e.g. `h1` counters first, then `h2`).

### 5.4 Shared provider-client files

| File | Conflict rate | Mitigation |
|---|---|---|
| `app/services/unified_market_data_client.py` | High (5+ plans/quarter) | Branch from latest `main`; rebase often |
| `app/core/prometheus_metrics.py` | High (every plan adds a counter) | See §5.3 |
| `app/services/comprehensive_ticker_profile_service.py` | High | Add new fan-out keys; don't edit existing keys |
| `app/core/config.py` | Medium | Settings blocks at the bottom per family-letter section |
| `config_specification.yaml` | Medium | New top-level keys per family |

---

## 6. Standards — codified patterns

The full `docs/standards.md` is mandatory. These rules are enforced:

| Rule | Enforced by |
|---|---|
| DB access (`get_db()` sync, `get_async_db()` async — never mixed) | `check_anti_patterns.py` |
| Settings 3-step lifecycle (field + YAML + `_apply` mapping + test) | reviewer (F5/B7) — checker does not yet AST-detect this |
| No magic numbers in business logic | reviewer |
| Singleton factory pattern (no module-level `Client()`) | `check_anti_patterns.py` |
| Specific exceptions first; no bare `except:` | `check_anti_patterns.py` |
| Prometheus counters on every exit path | reviewer |
| `time.monotonic()` for elapsed; `now_utc()` for wall-clock | reviewer |
| Absolute imports only; no `try/except ImportError` workarounds | `check_anti_patterns.py` |
| New fields have defaults; Alembic for every DB model change | reviewer + Alembic migration |
| `safe_provider_call` for every provider call | reviewer + F6 finding as canonical example |
| Counter naming `<tradepulse_><domain>_<noun>_total{labels}` | reviewer + F6 counter as canonical example |
| No deleted code — deprecate with comment | reviewer + master plan §4 |
| Tests alongside code | pytest in CI |
| One plan → one branch → one PR | convention |

### 6.1 `safe_provider_call` — use everywhere

`app/core/safe_provider_call.py` exists. Every provider call goes through it:

```python
data = await safe_provider_call(
    provider="benzinga", method="get_news",
    coro=benzinga.get_news(symbol),
    errors_list=errors,
)
```

### 6.2 Counter naming (codified)

Format: `<tradepulse_><domain>_<noun>_total{labels}`. Examples:

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

### 6.3 No deleted code

Never delete a provider client, a fallback path, or a configuration key. Mark deprecated with a comment. Other agents may still be working in that area.

### 6.4 Alembic for every DB model change

If your plan adds or modifies a `Base` subclass in `app/models/`:

```powershell
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m alembic revision --autogenerate -m "<feature_id>:<short desc>"
.\venv\Scripts\python.exe -m alembic upgrade head
.\venv\Scripts\python.exe -m pytest tests/ -q -p no:warnings --tb=short
```

Review the autogenerated migration before committing — autogenerate misses complex index changes.

---

## 7. Templates — cross-reference

| Document | Use when |
|---|---|
| `docs/templates/implementation_plan_template.md` | Adding code (feature) |
| `docs/templates/issue_root_cause_analysis_template.md` | Adding `docs/issues/<ID>_*.md` |
| `docs/templates/phase_gate_checklist.md` | Disambiguating gate phases; F1 reference |
| `docs/templates/root_cause_dataflow_trace_guide.md` | Required inside every issue RCA — ASCII data-flow trace |
| `docs/templates/recovery_protocols.md` | Decision tree + 5 protocols for rollback, flag-off, runaway, alembic, settings drift |

---

## 8. Testing — Three Layers, One Cycle

```powershell
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m pytest tests/fast/unit/ -q -p no:warnings --tb=short   # unit
.\venv\Scripts\python.exe -m pytest tests/ -q -p no:warnings --tb=short              # full
.\venv\Scripts\python.exe scripts/check_anti_patterns.py 2>&1 | Select-String "<file_or_glob>"
```

Manual smoke test if the change affects API behavior. `Invoke-RestMethod http://localhost:8000/health` is the cheapest live probe; surface-level fields (status, version) tell you the right backend is serving.

Coverage target: 70% on new code. Don't over-test getters/setters.

---

## 9. Shipping

One plan → one branch → one PR. Bundling is not allowed.

```bash
git checkout -b <type>/<family><n>-<short>
git add <only the files I authored>
git commit -m "<type>(<family><n>): <one-line summary>

<what> + <why> + <issue/link>
Co-Authored-By: ..."

git push -u origin <type>/<family><n>-<short>
gh pr create --base main --title "..."
```

If push is blocked by a hook, **fix the new findings** — don't `--no-verify` without explicit user approval.

---

## 10. Quick Reference

```powershell
# Health
Invoke-RestMethod http://localhost:8000/health

# Tests
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m pytest tests/fast/unit/<plan>.py -v

# Anti-patterns (scoped to your files)
.\venv\Scripts\python.exe scripts/check_anti_patterns.py 2>&1 | Select-String "my_file"

# Verify plan F1
.\venv\Scripts\python.exe scripts\verify_plan_f1.py docs\implementation_plans\<plan>.md

# Pull from main
git fetch origin main && git rebase origin/main
```

```bash
# Same in bash
cd '/f/Docs/Dev/AI Scripts/TradePulse/TradePulse_final_augment/backend_v4'
PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe -m pytest tests/fast/unit/ -q --tb=line -p no:cacheprovider -W ignore
PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe scripts/check_anti_patterns.py 2>&1 | grep my_file
```