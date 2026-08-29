# docFlow v4 — Phase Gate Checklist

**Version**: 4.0.0  · **Last Updated**: 2026-07-09

Used as a single-page reference for the F1–F5 / B1–B7 gate phrases, deliverables, and verification steps. Each phase has **one** named gate phrase (verbatim) that ends the phase and signals the next.

---

## F-series — Feature Implementation

### Phase F1 — Pre-Implementation Verification

**Deliverables**

- [ ] Read `g0_ultimate_assistant_master_plan_2026_07.md` (target state) and this plan's lineage in `g0` §3.
- [ ] Read every `file:line` reference in the plan.
- [ ] For each `file:line`, run the live codebase search and confirm the line still matches.
- [ ] Confirmed every `from app.X import Y` target exists in `app/` matching the path.
- [ ] Confirmed `config_specification.yaml` has (or plan creates) the sections referenced.
- [ ] Run `python scripts/verify_plan_f1.py docs/implementation_plans/<plan>.md` — must exit 0.
- [ ] `git status` is clean (you've claimed the working tree; see v4 §6).
- [ ] Plan follows v4 §3 family + plan-id convention; branch name is `feat/<family><n>-<short>`.

**Gate phrase**: `✅ Plan verified against codebase. All insertion points confirmed. Proceeding to implementation.`

---

### Phase F2 — Implementation

**Deliverables**

- [ ] Code written in the order specified by the plan.
- [ ] Tests written alongside code, before next method.
- [ ] Provider calls use `safe_provider_call`.
- [ ] New Prometheus counters declared in the plan's §"Configuration" (per v4 §7.1).
- [ ] No magic numbers — every threshold goes through `settings.spec.get()` or class constants.
- [ ] No bare `except:` statements — specific exceptions only.
- [ ] No deleted code — old paths marked deprecated instead.
- [ ] Async vs sync DB chosen correctly per `dev-standards_compressed.md` §1.

**Gate phrase**: `✅ Implementation complete. All component tests pass. Proceeding to regression testing.`

---

### Phase F3 — Regression Testing

**Deliverables**

- [ ] Full test suite passes:
  ```powershell
  $env:PYTHONPATH = "."
  .\venv\Scripts\python.exe -m pytest tests/ -q -p no:warnings --tb=short
  ```
- [ ] Anti-pattern checker shows **no new findings** in files you modified:
  ```powershell
  .\venv\Scripts\python.exe scripts/check_anti_patterns.py 2>&1 | Select-String "<my_file>"
  ```
- [ ] `scripts/verify_plan_f1.py docs/implementation_plans/<plan>.md` still exits 0 (line drift post-edit).
- [ ] Live smoke test if the change affects API behavior.
- [ ] No regressions in existing functionality.

**Gate phrase**: `✅ All tests pass (N total, M new). No regressions detected. Proceeding to ship.`

---

### Phase F4+F5 — Ship (report, commit, push, PR)

**Deliverables**

- [ ] Create `docs/implementation_reports/<plan>_implementation_report_<YYYY_MM>.md` for every shipped plan. PR body serves as concise summary covering: what was implemented, what was tested, deviations from plan, known limitations, next-phase deps.
- [ ] If SQLAlchemy `Base` subclass added/modified, generated Alembic migration:

  ```shell
  ./venv/Scripts/python.exe -m alembic revision --autogenerate -m "<plan-id>:<short-desc>"
  ./venv/Scripts/python.exe -m alembic upgrade head
  ./venv/Scripts/python.exe -m pytest tests/ -q -p no:warnings --tb=short
  ```
- [ ] Verify git identity: `git config user.name` returns `deacristi` and `git config user.email` returns `dea.cristi@gmail.com`.
- [ ] Working tree clean except for files you authored (`git status`).
- [ ] Branch named per v4 §3 (`feat/<family><n>-<short>`).
- [ ] Commit message follows conventional-commits (`feat:`, `fix:`, `refactor:`, `chore:`, `docs:`).
- [ ] Push branch.
- [ ] Open PR against `main`. PR body serves as concise implementation report.
- [ ] Update `IMPLEMENTATION_TRACKER.md` and refresh `HANDOFF_PROMPT.md`.
- [ ] Reviewer validates standards checklist before Verifier sign-off.

**Gate phrase**: `✅ Branch pushed. PR opened. Ready for review.`

---

## B-series — Bug Fix

| Phase | Gate phrase |
|---|---|
| B1 — Root cause investigation | `✅ Root cause identified. Proceeding to documentation.` |
| B2 — Documentation (issue + RCA in `docs/issues/`) | `✅ Documentation complete. Proceeding to solution design.` |
| B3 — Solution design | `✅ Solution design complete. Proceeding to implementation planning.` |
| B4 — Implementation | `✅ Implementation complete. Tests pass. Proceeding to validation.` |
| B5 — Regression testing | Same as F3. |
| B6 — Code review & validation | `✅ Validation complete. Proceeding to ship.` |
| B7 — Ship It | Same as F4+F5. |

---

## Fast-Track (< 20 lines, single file, no API change, no new dependency)

**Deliverables**

- [ ] Verified current implementation.
- [ ] Change is backward compatible.
- [ ] No forbidden patterns (no bare `except:`, no `SessionLocal()` outside scripts, no `datetime.now()` outside timezone-aware ctx).
- [ ] Provider call uses `safe_provider_call`.
- [ ] No new Prom counter.
- [ ] Anti-pattern checker shows no new findings on the modified file.
- [ ] All existing unit tests pass.
- [ ] `scripts/verify_plan_f1.py` not strictly required for Fast-Track, but recommended when the file change touches a shared module.

**Gate phrase**: `✅ Simple change verified (fast-track). Risk: Low. Implementing with validation.`

---

## Failure Phrases

If a phase can't complete, emit a failure phrase with a brief reason. Example:

```
❌ F2 blocked: tests/test_<plan>.py fails on edge case where X.
  Continuing in [fix] branch; re-running F2.
```
