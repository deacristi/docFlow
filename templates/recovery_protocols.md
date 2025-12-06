# docFlow v3.1 - Recovery Protocols

**Version**: 3.1.0  
**Purpose**: Standardized procedures for recovering from common development issues

---

## Overview

These protocols provide step-by-step recovery procedures for common failure scenarios in AI-assisted development.

---

## Protocol 1: Context Degradation Recovery

### Symptoms
- AI suggests forbidden patterns
- AI forgets project architecture
- AI makes incorrect assumptions about existing code
- AI asks questions already answered in this session

### Recovery Steps

1. **STOP** current task immediately
2. **Save** any work in progress:
   ```bash
   git diff > scratch_changes.patch
   ```
3. **Reload** project context documentation
4. **Verify** understanding with quick checks:
   - "What's the project architecture?"
   - "What's the correct database access pattern?"
   - "Where should config values be stored?"
5. **Resume** task with fresh context

### Prevention
- Check context health every 30-40 messages
- Use steering rules for automatic reminders
- Start new session for major feature changes

---

## Protocol 2: Bad Implementation Rollback

### Symptoms
- Tests failing after changes
- Runtime errors in new code
- Import errors
- Type errors

### Recovery Steps

1. **STOP** making more changes
2. **Identify** scope of bad changes:
   ```bash
   git status
   git diff HEAD --name-only
   ```
3. **Assess** damage:
   ```bash
   # Check for syntax errors
   python -m py_compile path/to/file.py
   
   # Run tests
   pytest tests/ -v --tb=short
   ```
4. **Choose** recovery approach:

   **Option A: Small changes (< 5 files)**
   ```bash
   git checkout HEAD -- path/to/file.py
   ```

   **Option B: Large changes**
   ```bash
   git checkout -- .
   ```

   **Option C: Already committed**
   ```bash
   git reset --soft HEAD~1
   ```

5. **Document** what went wrong
6. **Restart** with proper 6-phase workflow

### Prevention
- Validate after each phase
- Make small, incremental commits
- Test changes before moving to next phase

---

## Protocol 3: Breaking Change Recovery

### Symptoms
- Existing tests failing (that were passing before)
- Other features broken
- Import errors in unmodified files
- API consumers reporting errors

### Recovery Steps

1. **STOP** and assess damage:
   ```bash
   pytest tests/ -v --tb=short
   ```

2. **Identify** breaking change:
   ```bash
   git diff HEAD~1 -- src/
   ```

3. **Check** downstream dependencies:
   - Search for usages of modified functions/classes
   - Review import statements

4. **Choose** recovery approach:

   **Option A: Fix Forward**
   - Update all downstream code to use new interface

   **Option B: Rollback**
   ```bash
   git revert HEAD
   ```

   **Option C: Deprecate**
   - Keep old API working
   - Add new API alongside
   - Mark old as deprecated

5. **Document** in issue analysis if significant

### Prevention
- Always check downstream before modifying public interfaces
- Use search to find all usages before changing function signatures
- Add deprecation period for breaking changes

---

## Protocol 4: Scope Creep Recovery

### Symptoms
- Implementation taking much longer than planned
- Adding features not in original requirements
- Code complexity increasing without clear benefit
- Lost track of original goal

### Recovery Steps

1. **STOP** and review original requirements
2. **Compare** current implementation to original request
3. **Identify** scope additions:
   - List features added beyond original request
   - Assess value of each addition

4. **Decide** for each addition:
   - **Keep**: If nearly complete AND valuable
   - **Remove**: If not in requirements
   - **Defer**: If valuable but not urgent

5. **Refocus** on original goal
6. **Communicate** with user:
   ```
   I noticed I was adding [X] which wasn't in the original request.
   I've refocused on [original goal]. Would you like me to add [X] 
   as a separate change after this is complete?
   ```

### Prevention
- Review original request before each implementation step
- Ask before adding "nice to have" features
- Keep changes minimal and focused

---

## Protocol 5: Database/Migration Issues

### Symptoms
- Migration errors
- Database schema mismatch
- Foreign key constraint violations

### Recovery Steps

1. **STOP** and check current state:
   ```bash
   # For Alembic
   alembic current
   alembic history
   ```

2. **Identify** the issue:
   ```bash
   alembic upgrade head 2>&1
   ```

3. **Choose** recovery approach:

   **Option A: Fix migration script**
   - Edit the migration script
   - Test with `alembic upgrade head`

   **Option B: Rollback migration**
   ```bash
   alembic downgrade -1
   ```

   **Option C: Reset (dev only)**
   ```bash
   # WARNING: This drops all data!
   alembic downgrade base
   alembic upgrade head
   ```

4. **Verify** database state

### Prevention
- Always test migrations on dev database first
- Create backup before running migrations in production
- Review migration scripts before running

---

## Quick Reference Card

| Scenario | First Action | Recovery Command |
|----------|--------------|------------------|
| AI forgot patterns | Reload context | Load project docs |
| Code doesn't work | Check diff | `git diff HEAD` |
| Revert file | Checkout | `git checkout HEAD -- <file>` |
| Revert all | Reset | `git checkout -- .` |
| Undo commit | Reset soft | `git reset --soft HEAD~1` |
| Tests failing | Run tests | `pytest tests/ -v` |
| Import error | Check syntax | `python -m py_compile <file>` |
| Migration error | Check status | `alembic current` |

---

## Emergency Escalation

### When to Escalate
- Data loss or corruption
- Security vulnerability introduced
- Production system affected
- Unable to recover with protocols above

### Escalation Steps
1. **STOP** all changes immediately
2. **Document** current state and what happened
3. **Create** detailed issue analysis
4. **Notify** stakeholders
5. **Wait** for guidance before proceeding

---

**Version**: 3.1.0  
**Last Updated**: December 2025
