# Forbidden Patterns

> These patterns are NEVER allowed in production code. AI assistants must flag and refuse to implement these.

**Last Updated:** [DATE]

---

## Database Access

### ❌ Direct SessionLocal Usage
```python
# FORBIDDEN - No cleanup, connection leaks
session = SessionLocal()
result = session.query(User).all()
```

### ✅ Correct Pattern
```python
# Use dependency injection in routes
@router.get("/users")
async def get_users(db: Session = Depends(get_db_session)):
    return await db.execute(select(User))

# Use context manager in async code
async with get_db() as session:
    result = await session.execute(query)
```

---

## Exception Handling

### ❌ Bare Except
```python
# FORBIDDEN - Catches everything including KeyboardInterrupt
try:
    do_something()
except:
    pass
```

### ❌ Silent Failures
```python
# FORBIDDEN - Hides errors
try:
    do_something()
except Exception:
    pass
```

### ✅ Correct Pattern
```python
# Specific exceptions with logging
try:
    do_something()
except SpecificError as e:
    logger.error("Operation failed", extra={"error": str(e)})
    raise
except AnotherError as e:
    logger.warning("Recoverable error", extra={"error": str(e)})
    return fallback_value
```

---

## Configuration

### ❌ Magic Numbers
```python
# FORBIDDEN - Hardcoded values
timeout = 30
max_retries = 3
threshold = 0.75
```

### ❌ Hardcoded URLs
```python
# FORBIDDEN - Environment-specific
api_url = "https://api.example.com/v1"
```

### ✅ Correct Pattern
```python
# All config via settings
from app.core.config import settings

timeout = settings.API_TIMEOUT
max_retries = settings.MAX_RETRIES
threshold = settings.CONFIDENCE_THRESHOLD
api_url = settings.API_BASE_URL
```

---

## Global State

### ❌ Module-Level Instances
```python
# FORBIDDEN - Created at import time
client = APIClient()
cache = {}
lock = Lock()
```

### ✅ Correct Pattern
```python
# Lazy initialization via dependency injection
class ServiceContainer:
    def __init__(self):
        self._client: Optional[APIClient] = None
    
    async def get_client(self) -> APIClient:
        if self._client is None:
            self._client = APIClient()
            await self._client.connect()
        return self._client
```

---

## Async Operations

### ❌ Blocking Calls in Async
```python
# FORBIDDEN - Blocks event loop
async def get_data():
    response = requests.get(url)  # Blocking!
    return response.json()
```

### ✅ Correct Pattern
```python
# Use async HTTP client
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

---

## Enforcement

These patterns are checked by:
1. **Pre-commit hooks** - Block commits with violations
2. **CI/CD pipeline** - Fail builds with violations
3. **Code review** - Mandatory checklist item
4. **AI steering rules** - AI refuses to implement

See `scripts/check_anti_patterns.py` for automated checking.
