# Workflow — Phases, Gate Phrases, Recovery

> Companion to `framework.md`. This file is the operational reference: phases in order, gate phrases verbatim, recovery protocols.

The workflow is a forcing function. The phases ensure every change — bug fix, feature, refactor — passes through the same checks. **Skipping a phase is what makes changes break.** No phase is skippable unless the change qualifies for fast-track.

---

## Workflow selection

| Change type | Workflow | When |
|---|---|---|
| Typo, config, < 20 lines, single file, no API change, no new dep, no schema change | **Fast-track** | One step: read the file, follow the standards, run the tests, ship |
| Bug fix | **Bug-fix workflow** (B1–B7) | Root cause unknown |
| Feature | **Feature workflow** (F1–F5) | Plan exists |

---

## Feature workflow (F1–F5)

### F1 — Pre-implementation verification

Before writing any code, verify the plan against the live codebase.

1. **Line-number re-verification**: every file the plan references — read it. Confirm insertion points, function signatures, class structures.
2. **Dependency check**: every import, factory, service — confirm it exists.
3. **Config check**: `config_specification.yaml` has the sections the plan references (or the plan adds them).
4. **Schema check**: Pydantic and DB models referenced — confirm current definitions.
5. **Counter check**: if plan declares counters, confirm `<domain>_<noun>_total{labels}` and registry import.
6. Run `scripts/verify_plan_f1.py <plan.md>` — must exit 0.

Gate: `✅ Plan verified against codebase. All insertion points confirmed. Proceeding to implementation.`

### F2 — Implementation

1. Follow the plan in order. Don't deviate unless a plan error surfaces.
2. Match existing file patterns (DB access, imports, error handling) — see `standards.md` §"File Consistency Rule".
3. **Tests alongside code**, not after. For each new function or class, write its test before moving on.
4. Provider calls use `safe_provider_call`.
5. After each logical unit: `pytest tests/fast/unit/test_<component>.py -v`.

Gate: `✅ Implementation complete. All component tests pass. Proceeding to regression testing.`

### F3 — Regression testing (mandatory)

1. **Run the full suite**: `pytest tests/ -q -p no:warnings --tb=short`. If anything fails, fix it.
2. **Run the anti-pattern checker scoped to your files**: `check_anti_patterns.py 2>&1 | Select-String "<my_file>"` — no new findings.
3. **Manual smoke test**: start the server, hit key endpoints, watch the logs.
4. **Cross-reference downstream**: if the change touches the signal pipeline (detector → FSM → trade calc → confidence → risk → persist → event), verify each downstream step still receives correct inputs.

Gate: `✅ All tests pass (N total, M new). No regressions detected. Proceeding to ship.`

### F4+F5 — Ship (report, commit, push, PR)

1. **Implementation report**: Create `docs/implementation_reports/<plan>_implementation_report_<YYYY_MM>.md` for every shipped plan. Update `IMPLEMENTATION_TRACKER.md` and refresh `HANDOFF_PROMPT.md`. The PR body serves as a concise implementation report covering: what was implemented, what was tested, deviations from plan, known limitations, and next-phase dependencies.
2. **Alembic migration check**: if any `app/models/*.py` was modified, run:

   ```shell
   alembic revision --autogenerate -m "<description>"
   alembic upgrade head
   pytest tests/ -q -p no:warnings --tb=short
   ```
3. **Verify git identity**: Confirm `git config user.name` returns `deacristi` and `git config user.email` returns `dea.cristi@gmail.com` before staging.
4. Stage and commit (conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
5. Push branch: `git push -u origin <branch>`.
6. Open PR against `main`. **PR body serves as concise implementation report**.
7. **Create implementation report artifact**: `docs/implementation_reports/<plan>_implementation_report_<YYYY_MM>.md` is mandatory for every shipped plan. Update `IMPLEMENTATION_TRACKER.md` and refresh `HANDOFF_PROMPT.md`.
8. **Reviewer checkpoint**: Reviewer validates standards checklist and anti-pattern findings before Verifier sign-off.
9. **Verifier confirms PR readiness** after Reviewer sign-off.

Gate: `✅ Branch pushed. PR opened. Ready for review.`

---

## Bug-fix workflow (B1–B7)

### B1 — Root cause investigation

1. Re-read `standards.md` and the relevant template to confirm patterns are fresh.
2. **Use codebase search to load every file in the suspected data path.** Don't work from memory or docs alone.
3. Thorough analysis. Examine affected files, trace the data flow, reproduce the issue.
4. Root cause confirmed with high confidence. **Do not proceed until you understand the cause.**

Gate: `✅ Root cause identified. Proceeding to documentation.`

### B2 — Documentation

Create a root-cause analysis using `docs/templates/issue_root_cause_analysis_template.md`. Include a Visual Data-Flow Trace (ASCII diagram showing the runtime path from trigger to failure).

Gate: `✅ Documentation complete. Proceeding to solution design.`

### B3 — Solution design

Follow `standards.md`. Conservative — minimal surgical changes over comprehensive rewrites.

Gate: `✅ Solution design complete. Proceeding to implementation planning.`

### B4 — Implementation

1. Write the fix following the solution design.
2. Write tests that reproduce the bug AND verify the fix.
3. Run full suite: `pytest tests/ -q -p no:warnings --tb=short`.

Gate: `✅ Fix implemented and tested. Proceeding to validation.`

### B5 — Regression testing

Same as F3.

Gate: `✅ All tests pass. No regressions detected. Proceeding to validation.`

### B6 — Code review & validation

Review changes against the standards checklist. Final test that the root cause is resolved with no side effects.

Gate: `✅ Validation complete. Proceeding to ship.`

### B7 — Ship

Same as F4+F5.

Gate: `✅ Branch pushed. PR opened. Ready for review.`

---

## Fast-track

For changes < 20 lines, single file, no API change, no new dependency, no schema change.

1. Verify the change is truly simple.
2. Read the affected file. Match existing patterns (`standards.md` §"File Consistency Rule").
3. Make the change. Run existing unit tests: `pytest tests/fast/unit/ -q -p no:warnings --tb=short`.
4. If DB models were touched, generate the Alembic migration. Otherwise skip.
5. Commit, push, PR.
6. Say: `✅ Simple change verified. Implementing with validation.`

Fast-track is not a waiver of standards. Provider calls still use `safe_provider_call`. Modified file still passes `check_anti_patterns.py`. The change is still tested.

---

## Phase gate phrases (verbatim)

End every completed phase by emitting the exact phrase. The receiving thread uses these to know state.

```
✅ Plan verified against codebase. All insertion points confirmed. Proceeding to implementation.   (F1)
✅ Implementation complete. All component tests pass. Proceeding to regression testing.              (F2)
✅ All tests pass (N total, M new). No regressions detected. Proceeding to ship.                    (F3)
✅ Branch pushed. PR opened. Ready for review.                                                      (F4+F5)
✅ Root cause identified. Proceeding to documentation.                                              (B1)
✅ Documentation complete. Proceeding to solution design.                                           (B2)
✅ Solution design complete. Proceeding to implementation planning.                                 (B3)
✅ Fix implemented and tested. Proceeding to validation.                                           (B4)
✅ Validation complete. Proceeding to ship.                                                         (B6)
✅ Simple change verified. Implementing with validation.                                            (Fast-track)
```

If a phase can't complete, emit a failure phrase instead and link a brief reason.

---

## Recovery Protocols

> Use when a change is in production and something is broken. The goal is to restore the previous working state quickly, then diagnose the cause.

### Decision tree: roll back vs. fix forward

| Question | If yes | If no |
|---|---|---|
| Is the change isolated? Can it be reverted without affecting other in-flight work? | Roll back | Fix forward |
| Is the change fully merged to `main`? | Hotfix or revert | Push a fix branch |
| Is the system serving users right now? | Roll back first, fix later | Take time to fix forward |
| Has the change been running > 24h and only now broken? | Diagnose first; rollback only if cause is the change | Diagnose first |

When in doubt: **roll back first, diagnose later.** A broken system is worse than a temporarily-reverted feature.

### Protocol 1 — Roll back a single PR

1. `git log --oneline -20` to find the offending merge commit.
2. `git revert <commit>` to create a revert commit.
3. `pytest tests/fast/unit/ -q -p no:warnings --tb=short` — confirm tests pass on the revert.
4. `scripts/check_anti_patterns.py 2>&1 | grep <file>` — confirm no new findings.
5. Push the revert branch and open a PR labeled `revert: <title>`.
6. After merge: open a follow-up issue to diagnose the root cause.

### Protocol 2 — Disable a feature flag

If the change is behind a settings flag, the fastest rollback is flipping the flag.

1. Find the flag in `app/core/config.py` or `config_specification.yaml`.
2. `git revert` the change to the default value, OR set the env var override.
3. Restart the service: `.\restart_development.bat`.
4. Confirm via `curl http://localhost:8000/health` and the relevant endpoint.
5. Open a follow-up issue to fix the flag-on path.

### Protocol 3 — Stop a runaway process

If a background job is consuming too many resources:

1. Identify the process: `tasklist | grep python`.
2. For a specific worker: `.\stop_development.bat`.
3. For a specific background task: kill the relevant asyncio task via the service's stop method.
4. Verify cleanup: `curl http://localhost:8000/health`.
5. Investigate the cause before re-enabling.

### Protocol 4 — Recover from a bad Alembic migration

1. Identify the bad migration: `ls alembic/versions/ | tail -5`.
2. **Do not** run `alembic downgrade -1` in production without testing. The downgrade may fail or cause data loss.
3. If the migration is in production and broken: `alembic stamp head` to a known-good revision, then write a corrective migration.
4. If the migration is in staging only: `alembic downgrade <good_revision>`, fix the migration file, regenerate.
5. Always have a `down_revision` that actually works. Test it.

### Protocol 5 — Recover from a settings drift in production

When `settings.<NAME>` is missing and a service is throwing `AttributeError` at every call:

1. Identify the missing setting from the error trace.
2. Add the field to `Settings` with a sensible default.
3. Add the YAML key.
4. Add the `_apply()` mapping.
5. Deploy — the production factory catches the `AttributeError` and the next call succeeds.
6. Open a follow-up issue: why was the 3-step lifecycle skipped?

### Protocol 6 — Recover from a duplicate-path bug

When the system is doing the same work twice (e.g. realtime processor + direct callback):

1. Identify the duplicate path by reading the code.
2. Decide which path is the "primary" and which is the legacy.
3. Disable the legacy path with a settings flag (default off).
4. Deploy the flag-off.
5. Open a follow-up issue to remove the legacy path entirely.

**Don't just remove the legacy code.** The setting flag gives you a quick rollback. Removal is a separate change.

---

## Pre-implementation checklist (mandatory)

Run through this before writing any non-trivial change.

### DB access
- [ ] Using the right pattern for the file: `get_db()` for sync ORM, `get_async_db()` for true-async.
- [ ] Not mixing sync and async patterns in the same file.
- [ ] `get_db()` callers do NOT call `db.commit()` (auto-commits on clean exit).

### Magic numbers / config
- [ ] All numeric thresholds use `settings.spec.get(...)` or class constants.
- [ ] Confidence calculations use config parameters (base, increment, max).
- [ ] Time conversions use named constants.
- [ ] Retry limits come from config, not hardcoded.
- [ ] New config sections have `DEFAULT_*` class constants as fallback.

### Settings lifecycle (3-step add)
- [ ] **Step 1**: Field added to `Settings` class in `app/core/config.py` with a sensible default.
- [ ] **Step 2**: YAML key added to `config_specification.yaml` under the right section.
- [ ] **Step 3**: `_apply(...)` mapping added in `_sync_<vendor>_from_spec`.
- [ ] **Step 4**: Test asserting `settings.<NEW_NAME>` exists and has the expected default.
- [ ] **Step 5**: Run `pytest tests/fast/unit/` to confirm no regression.

This is the single most common drift pattern. The 3-step add is mandatory for every new `settings.<NAME>` reference.

### Singletons / factories
- [ ] Parameterless factories: simple `if None: create`.
- [ ] Parameterized factories: handle parameter updates for existing instances.
- [ ] Factory returns `None` when disabled; caller checks before using.

### Imports
- [ ] Cross-service imports that would cycle use lazy imports inside methods.
- [ ] Top-level imports limited to: stdlib, config, utilities, same-layer peers.
- [ ] No `try/except ImportError` workarounds.

### Exception handling
- [ ] Specific exceptions caught before generic `Exception`.
- [ ] No bare `except:` statements.

### Telemetry / timing
- [ ] All return paths have Prometheus counter updates (success and error).
- [ ] Elapsed time uses `time.monotonic()`; wall-clock uses `now_utc()` / `now_local()`.

### Backward compatibility
- [ ] New dataclass/model fields have defaults.
- [ ] New DB columns are `nullable=True` or have `server_default`.
- [ ] Existing API responses not broken by new fields.

### DB schema / Alembic
- [ ] If any `app/models/*.py` was modified, an Alembic migration is required.
- [ ] Run `alembic revision --autogenerate -m "<description>"` then `alembic upgrade head`.
- [ ] Review the generated migration — autogenerate can miss things.
- [ ] Re-run the full test suite after the migration.

---

## What to do when things go wrong

- **AI proposes a fix the user has already said NO to**: stop. Re-read the user's NO list. Do not re-propose.
- **AI adds a hardcoded count to a doc**: catch it in the F3 review. Replace with "scan to discover".
- **AI deletes code without being asked**: catch it in code review. The user said "code stays until I say it goes."
- **AI invents a new pattern instead of following an existing one**: catch in code review. Match the file's existing patterns.
- **Tests are passing but the change is wrong**: the live log or the next user interaction will tell you. The workflow is a forcing function, not a guarantee.

## The meta-rule

The workflow is small on purpose. The phases are minimal. The gate phrases are short. The standards are focused. **The AI's discipline is what makes this work, not the framework itself.** The framework gives the AI a structure; the AI's job is to follow it.