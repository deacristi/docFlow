---
inclusion: always
---

# docFlow v3.1 - AI Context Monitoring Protocol

> This steering rule ensures consistent context health monitoring throughout development sessions.

## 🔄 Self-Monitoring Protocol

### Message Tracking
At the START of every response involving code changes, mentally track:
- Current message number in this session (estimate)
- Files viewed (count)
- Files modified (count)

### Automatic Health Checks (Every 10-15 Messages)
Perform a mental context health check:

1. **Architecture Check**: Do I remember the project's architecture?
2. **Pattern Check**: Do I remember forbidden patterns and required patterns?
3. **Standards Check**: Do I remember to use configuration for all tunable values?

If ANY answer is "uncertain":
1. Inform user: "📊 Context refresh recommended - reloading project standards"
2. Re-read the project's context documentation

### Proactive Refresh Triggers
Automatically suggest context refresh when:
- 40+ messages exchanged in session
- 10+ files viewed
- Switching to a different feature/module
- User corrects an assumption
- Uncertain about a pattern or standard

## 📋 Phase Gate Reminders

Before implementing ANY code changes, verify:
1. ✅ Investigation complete (examined relevant code)
2. ✅ Understand current implementation
3. ✅ Solution follows project standards
4. ✅ No breaking changes to existing functionality

## ⚠️ Critical Constraints (Customize for Your Project)

### Database Access
```python
# ✅ CORRECT - Use context managers
async with get_db() as session:
    result = await session.execute(query)

# ✅ CORRECT - FastAPI dependency injection
def endpoint(db: Session = Depends(get_db_session)):
    pass

# ❌ FORBIDDEN - Direct instantiation
SessionLocal()  # WRONG!
```

### Configuration
```python
# ✅ CORRECT - Use settings/config
timeout = settings.API_TIMEOUT
url = settings.API_BASE_URL

# ❌ FORBIDDEN - Magic numbers
timeout = 30  # Magic number!
url = "https://..."  # Hardcoded!
```

### Error Handling
```python
# ✅ CORRECT - Specific exceptions
except ValueError as e:
    logger.error(f"Validation failed: {e}")
    raise

# ❌ FORBIDDEN - Bare except
except:  # WRONG!
    pass
```

## 🎯 Platform Requirements

Customize these for your environment:
- **Environment**: [Your OS]
- **Shell Commands**: [Your shell syntax]
- **API Testing**: Always check API spec before assuming endpoints
- **Health Check**: Verify services are running before claiming they're down
