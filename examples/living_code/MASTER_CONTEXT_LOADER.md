# Master Context Loader

> Entry point for AI context loading. Read this file first.

**Last Updated:** [DATE]  
**Version:** 1.0

---

## Quick Start for AI Assistants

### Load Order
1. **This file** - Critical constraints and overview
2. **`patterns/forbidden_patterns.md`** - What NOT to do
3. **`architecture/system_overview.md`** - How the system works
4. **Task-specific docs** - Based on what you're working on

### Critical Constraints (Never Violate)

```python
# ❌ FORBIDDEN
except:                          # Bare except
timeout = 30                     # Magic numbers
url = "https://api.example.com"  # Hardcoded URLs
client = APIClient()             # Global instances

# ✅ REQUIRED
except SpecificException:        # Specific exceptions
timeout = settings.API_TIMEOUT   # Config values
url = settings.API_BASE_URL      # Config values
container.get_client()           # Dependency injection
```

---

## Project Overview

### Architecture
- **Type:** [Monolith/Microservices/Modular Monolith]
- **Framework:** [FastAPI/Django/Flask/etc.]
- **Database:** [PostgreSQL/MySQL/MongoDB/etc.]
- **Cache:** [Redis/Memcached/etc.]

### Key Components
| Component | Purpose | Location |
|-----------|---------|----------|
| API Layer | HTTP endpoints | `app/api/` |
| Services | Business logic | `app/services/` |
| Models | Data structures | `app/models/` |
| Core | Shared utilities | `app/core/` |

---

## Current State

### Features
| Feature | Status | Notes |
|---------|--------|-------|
| Feature A | ✅ Complete | Production ready |
| Feature B | 🚧 In Progress | 80% complete |
| Feature C | 📋 Planned | Q2 2025 |

### Known Issues
- Issue 1: [Description] - Workaround: [Solution]
- Issue 2: [Description] - Workaround: [Solution]

---

## Development Standards

### Database Access
```python
# FastAPI routes - use dependency injection
@router.get("/items/{id}")
async def get_item(id: str, db: Session = Depends(get_db_session)):
    return await db.execute(query)

# Async operations - use context manager
async with get_db() as session:
    result = await session.execute(query)
```

### Configuration
```python
# All config via settings object
from app.core.config import settings

timeout = settings.API_TIMEOUT
base_url = settings.API_BASE_URL
debug = settings.DEBUG_MODE
```

### Error Handling
```python
# Specific exceptions with context
try:
    result = await external_api.call()
except APITimeoutError as e:
    logger.error("API timeout", extra={"endpoint": e.endpoint})
    raise ServiceUnavailableError("External service timeout")
except APIError as e:
    logger.error("API error", extra={"code": e.code})
    raise
```

---

## File Reference

### Must-Read Files
| File | Purpose | When to Read |
|------|---------|--------------|
| `patterns/forbidden_patterns.md` | Anti-patterns | Always |
| `patterns/approved_patterns.md` | Best practices | When implementing |
| `architecture/system_overview.md` | System design | New features |
| `architecture/data_flow.md` | Data movement | Data changes |

### Service Documentation
| Service | File | Purpose |
|---------|------|---------|
| Auth | `services/auth.md` | Authentication/Authorization |
| Data | `services/data.md` | Data processing |
| API | `services/api.md` | External API integration |

---

## Refresh Protocol

If context seems stale or uncertain:

1. **Check freshness**: `python scripts/check_freshness.py`
2. **Re-read this file**: May have been updated
3. **Verify patterns**: Check `forbidden_patterns.md`
4. **Ask user**: If still uncertain, ask for clarification

---

## Contact

- **Maintainer:** [Name/Team]
- **Documentation:** [Link to full docs]
- **Issues:** [Link to issue tracker]
