# docFlow v3.1 - Development Standards

**Philosophy:** Production-grade quality without over-engineering  
**Enforcement:** Automated checks + code review

---

## Core Principles

1. **Configuration Over Code:** All tunable values in config
2. **Fail Gracefully:** Degrade features, don't crash
3. **Async First:** Non-blocking operations by default
4. **Test What Matters:** Focus on business logic and integrations
5. **Document Decisions:** ADRs for architectural choices

---

## MANDATORY CONSTRAINTS (Never Violate)

### Database Access

| Pattern | ❌ FORBIDDEN | ✅ REQUIRED |
|---------|-------------|-------------|
| **Async DB** | `SessionLocal()` directly | `async with get_db()` |
| **FastAPI Routes** | Manual session management | `db: Session = Depends(get_db_session)` |
| **Scripts** | No cleanup | Context manager with try/finally |

### Configuration Management

| Pattern | ❌ FORBIDDEN | ✅ REQUIRED |
|---------|-------------|-------------|
| **Magic Numbers** | `timeout = 30` | `timeout = settings.API_TIMEOUT` |
| **Hardcoded URLs** | `url = "https://..."` | `url = settings.API_BASE_URL` |
| **Environment Checks** | `if os.getenv("DEBUG")` | `if settings.DEBUG_MODE` |
| **Thresholds** | `if score > 0.7` | `if score > settings.CONFIDENCE_THRESHOLD` |

### Exception Handling

| Pattern | ❌ FORBIDDEN | ✅ REQUIRED |
|---------|-------------|-------------|
| **Bare Except** | `except:` | `except SpecificException:` |
| **Silent Failures** | `except: pass` | `except Exception as e: logger.error(...); raise` |
| **Generic Exceptions** | `raise Exception("error")` | `raise CustomException("error", context={...})` |

### Global State

| Pattern | ❌ FORBIDDEN | ✅ REQUIRED |
|---------|-------------|-------------|
| **Module-level Instances** | `client = APIClient()` | Lazy initialization function |
| **Mutable Globals** | `_cache = {}` | Dependency injection or app.state |
| **Global Locks** | `_lock = Lock()` | Instance-level locks |

---

## IMPLEMENTATION PATTERNS

### 1. Dependency Injection

**Problem:** Global singletons create testing nightmares and race conditions

**Solution:** Dependency injection container

```python
from typing import Annotated
from fastapi import Depends

class ServiceContainer:
    """Centralized dependency injection"""
    
    def __init__(self):
        self._client: Optional[APIClient] = None
        self._cache: Optional[CacheManager] = None
    
    async def get_client(self) -> APIClient:
        """Get or create client (lazy singleton)"""
        if self._client is None:
            self._client = APIClient()
            await self._client.connect()
        return self._client

# Global container (single instance)
_container = ServiceContainer()

async def get_container() -> ServiceContainer:
    return _container

Container = Annotated[ServiceContainer, Depends(get_container)]

# Usage in routes
@router.get("/data/{id}")
async def get_data(id: str, container: Container):
    client = await container.get_client()
    return await client.fetch(id)
```

### 2. Circuit Breakers for External APIs

**Problem:** Repeated calls to failing services waste resources

**Solution:** Circuit breaker pattern with automatic fallback

```python
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing - reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        timeout_seconds: int = 60
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)
        self.state = CircuitState.CLOSED
        self.failure_count = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpen(f"Circuit '{self.name}' is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
```

### 3. Structured Logging with Context

**Problem:** Difficult to trace requests across async operations

**Solution:** Context-aware structured logging

```python
import logging
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar('request_id', default=None)

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
        }
        if request_id := request_id_var.get():
            log_data['request_id'] = request_id
        return json.dumps(log_data)
```

---

## AUTOMATED ENFORCEMENT

### Pre-Commit Hooks

```powershell
# PowerShell pre-commit hook
Write-Host "Running code quality checks..."

# Check for bare except
$bareExcepts = Select-String -Path "**/*.py" -Pattern "except:" | 
    Where-Object { $_ -notmatch "except Exception" }
if ($bareExcepts) {
    Write-Host "❌ BLOCKED: Bare except statements found"
    exit 1
}

# Run tests
pytest tests/ -q --tb=no
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ BLOCKED: Tests failing"
    exit 1
}

Write-Host "✅ All checks passed"
```

### Anti-Pattern Checker Script

```python
# scripts/check_anti_patterns.py
import re
from pathlib import Path

def check_bare_excepts():
    """Check for bare except: statements"""
    issues = []
    for file in Path("app").rglob("*.py"):
        with open(file) as f:
            for i, line in enumerate(f, 1):
                if re.match(r'^\s*except:\s*(#.*)?$', line):
                    issues.append(f"{file}:{i}: Bare except statement")
    return issues

def check_magic_numbers():
    """Check for hardcoded numbers"""
    issues = []
    allowed = {0, 1, 100, 1000}
    
    for file in Path("app").rglob("*.py"):
        if "test_" in file.name:
            continue
        with open(file) as f:
            for i, line in enumerate(f, 1):
                if "settings." in line:
                    continue
                for match in re.finditer(r'\b(\d+)\b', line):
                    num = int(match.group(1))
                    if num not in allowed and num > 1:
                        issues.append(f"{file}:{i}: Magic number {num}")
    return issues[:10]

if __name__ == "__main__":
    all_issues = check_bare_excepts() + check_magic_numbers()
    if all_issues:
        print("❌ Anti-patterns detected:")
        for issue in all_issues:
            print(f"  - {issue}")
        exit(1)
    print("✅ No anti-patterns detected")
```

---

## CODE REVIEW CHECKLIST

### For Reviewer

**Architecture (P0 - Must Check):**
- [ ] Uses dependency injection, not global instances
- [ ] Async operations non-blocking
- [ ] Proper exception hierarchy (no bare except)
- [ ] Configuration-driven (no magic numbers)

**Quality (P1 - Should Check):**
- [ ] Has unit tests for business logic
- [ ] Logging includes context
- [ ] Error messages are actionable
- [ ] Database sessions properly managed

**Production (P2 - Nice to Have):**
- [ ] Circuit breakers on external APIs
- [ ] Graceful degradation if services unavailable
- [ ] Performance considerations documented

### For Author

**Before Creating PR:**
- [ ] Pre-commit hooks pass locally
- [ ] All tests pass
- [ ] Coverage >70% for new code
- [ ] No magic numbers (use config)
- [ ] Docstrings for public functions

---

## TESTING STRATEGY

### Test Pyramid

```
     /\
    /  \  E2E Tests (5%)
   /----\  - Critical user flows
  /      \
 /--------\ Integration Tests (25%)
/----------\ - API endpoints
/===========\ Unit Tests (70%)
              - Business logic
```

### What to Test

**Unit Tests (70%):**
- ✅ Business logic and calculations
- ✅ Edge cases and error handling
- ✅ Retry logic and fallbacks

**Integration Tests (25%):**
- ✅ API endpoints end-to-end
- ✅ Database operations
- ✅ Service interactions

**E2E Tests (5%):**
- ✅ Critical user flows only

**What NOT to Test:**
- ❌ Third-party library internals
- ❌ Framework behavior
- ❌ Simple getters/setters

---

## PRAGMATIC BALANCE

### Don't Over-Engineer

**❌ Too Much:**
- Writing tests for every line (aim for 70-80%, not 100%)
- Abstract factories for simple objects
- Complex inheritance hierarchies
- Perfect code before shipping

**✅ Right Amount:**
- Test business logic and integrations
- Simple dependency injection
- Composition over inheritance
- Ship, measure, improve

### When to Refactor

**Immediate (Red Alert):**
- Bare except: statements in production code
- Global mutable state in request handlers
- Unhandled exceptions crashing service
- Resource leaks (unclosed connections)

**Soon (Yellow Alert):**
- Code duplication (DRY violated >3 times)
- Functions >50 lines
- Cyclomatic complexity >10
- No tests for critical path

**Eventually (Green Alert):**
- Minor style inconsistencies
- Suboptimal performance (if not bottleneck)
- Missing docstrings (non-public functions)

---

## SUMMARY

**Key Components:**
1. ✅ Dependency Injection pattern
2. ✅ Circuit Breaker implementation
3. ✅ Structured Logging with context
4. ✅ Automated enforcement (pre-commit, CI/CD)
5. ✅ Anti-pattern checker scripts
6. ✅ Code review checklist
7. ✅ Testing strategy (70/25/5 pyramid)
8. ✅ Pragmatic balance guidance
