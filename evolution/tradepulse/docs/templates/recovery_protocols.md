# Recovery Protocols

> Use when a change is in production and something is broken. The goal is to restore the previous working state quickly, then diagnose the cause.

---

## Decision tree: roll back vs. fix forward

| Question | If yes | If no |
|---|---|---|
| Is the change isolated? Can it be reverted without affecting other in-flight work? | Roll back | Fix forward |
| Is the change fully merged to `main`? | Hotfix or revert | Push a fix branch |
| Is the system serving users right now? | Roll back first, fix later | Take time to fix forward |
| Has the change been running > 24h and only now broken? | Diagnose first; rollback only if cause is the change | Diagnose first |

When in doubt: **roll back first, diagnose later.** A broken system is worse than a temporarily-reverted feature.

---

## Protocol 1 — Roll back a single PR

1. `git log --oneline -20` to find the offending merge commit.
2. `git revert <commit>` to create a revert commit.
3. `pytest tests/fast/unit/ -q -p no:warnings --tb=short` — confirm tests pass on the revert.
4. `scripts/check_anti_patterns.py 2>&1 | grep <file>` — confirm no new findings.
5. Push the revert branch and open a PR labeled `revert: <title>`.
6. After merge: open a follow-up issue to diagnose the root cause.

## Protocol 2 — Disable a feature flag

If the change is behind a settings flag, the fastest rollback is flipping the flag.

1. Find the flag in `app/core/config.py` or `config_specification.yaml`.
2. `git revert` the change to the default value, OR set the env var override.
3. Restart the service: `.\restart_development.bat`.
4. Confirm via `curl http://localhost:8000/health` and the relevant endpoint.
5. Open a follow-up issue to fix the flag-on path.

## Protocol 3 — Stop a runaway process

If a background job is consuming too many resources:

1. Identify the process: `tasklist | grep python`.
2. For a specific worker: `.\stop_development.bat`.
3. For a specific background task: kill the relevant asyncio task via the service's stop method.
4. Verify cleanup: `curl http://localhost:8000/health`.
5. Investigate the cause before re-enabling.

## Protocol 4 — Recover from a bad Alembic migration

1. Identify the bad migration: `ls alembic/versions/ | tail -5`.
2. **Do not** run `alembic downgrade -1` in production without testing. The downgrade may fail or cause data loss.
3. If the migration is in production and broken: `alembic stamp head` to a known-good revision, then write a corrective migration.
4. If the migration is in staging only: `alembic downgrade <good_revision>`, fix the migration file, regenerate.
5. Always have a `down_revision` that actually works. Test it.

## Protocol 5 — Recover from a settings drift in production

When `settings.<NAME>` is missing and a service is throwing `AttributeError` at every call:

1. Identify the missing setting from the error trace.
2. Add the field to `Settings` with a sensible default.
3. Add the YAML key.
4. Add the `_apply()` mapping.
5. Deploy — the production factory catches the `AttributeError` and the next call succeeds.
6. Open a follow-up issue: why was the 3-step lifecycle skipped?

## Protocol 6 — Recover from a duplicate-path bug

When the system is doing the same work twice (e.g. realtime processor + direct callback):

1. Identify the duplicate path by reading the code.
2. Decide which path is the "primary" and which is the legacy.
3. Disable the legacy path with a settings flag (default off).
4. Deploy the flag-off.
5. Open a follow-up issue to remove the legacy path entirely.

**Don't just remove the legacy code.** The setting flag gives you a quick rollback. Removal is a separate change.

---

## Post-incident checklist

After a recovery:

- [ ] System is serving requests normally.
- [ ] No errors in `logs/tradepulse.log` for the relevant service.
- [ ] `curl http://localhost:8000/health` is green.
- [ ] Affected users notified (if user-facing).
- [ ] Follow-up issue filed for root-cause analysis.
- [ ] If the recovery revealed a gap in the framework (e.g. a missing anti-pattern check), file an issue to add it.