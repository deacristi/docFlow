# Approved Patterns

> These patterns are recommended for production code. AI assistants should use these as templates.

**Last Updated:** [DATE]

---

## Dependency Injection

### Service Container Pattern
```python
from typing import Annotated, Optional
from fastapi import Depends

class ServiceContainer:
    """Centralized dependency injection container"""
    
    def __init__(self):
        self._api_client: Optional[APIClient] = None
        self._cache: Optional[CacheManager] = None
    
    async def get_api_client(self) -> APIClient:
        """Lazy singleton with proper initialization"""
        if self._api_client is None:
            self._api_client = APIClient(
                base_url=settings.API_BASE_URL,
                timeout=settings.API_TIMEOUT
            )
            await self._api_client.connect()
        return self._api_client
    
    async def get_cache(self) -> CacheManager:
        """Lazy singleton for cache"""
        if self._cache is None:
            self._cache = CacheManager(
                redis_url=settings.REDIS_URL
            )
            await self._cache.initialize()
        return self._cache
    
    async def cleanup(self):
        """Cleanup all resources"""
        if self._api_client:
            await self._api_client.close()
        if self._cache:
            await self._cache.close()

# Global container instance
_container = ServiceContainer()

async def get_container() -> ServiceContainer:
    return _container

# Type alias for cleaner code
Container = Annotated[ServiceContainer, Depends(get_container)]

# Usage in routes
@router.get("/data/{id}")
async def get_data(id: str, container: Container):
    client = await container.get_api_client()
    return await client.fetch(id)
```

---

## Error Handling

### Custom Exception Hierarchy
```python
class AppError(Exception):
    """Base exception for application errors"""
    def __init__(self, message: str, context: dict = None):
        super().__init__(message)
        self.context = context or {}

class ValidationError(AppError):
    """Input validation failed"""
    pass

class ExternalServiceError(AppError):
    """External API call failed"""
    pass

class DataNotFoundError(AppError):
    """Requested data not found"""
    pass

# Usage
try:
    result = await external_api.call(params)
except TimeoutError as e:
    raise ExternalServiceError(
        "API timeout",
        context={"endpoint": endpoint, "timeout": timeout}
    )
```

### Graceful Degradation
```python
async def get_data_with_fallback(symbol: str) -> Data:
    """Try primary source, fall back to secondary"""
    try:
        return await primary_source.get(symbol)
    except ExternalServiceError as e:
        logger.warning(
            "Primary source failed, using fallback",
            extra={"symbol": symbol, "error": str(e)}
        )
        return await fallback_source.get(symbol)
```

---

## Configuration

### Settings Class Pattern
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings from environment"""
    
    # API Configuration
    API_BASE_URL: str = "https://api.example.com"
    API_TIMEOUT: int = 30
    API_MAX_RETRIES: int = 3
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    
    # Cache
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 300
    
    # Feature Flags
    DEBUG_MODE: bool = False
    ENABLE_FEATURE_X: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

---

## Logging

### Structured Logging Pattern
```python
import logging
import json
from contextvars import ContextVar
from datetime import datetime

# Context variables for request tracking
request_id_var: ContextVar[str] = ContextVar('request_id', default=None)

class StructuredFormatter(logging.Formatter):
    """JSON formatter with automatic context"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        # Add context
        if request_id := request_id_var.get():
            log_data['request_id'] = request_id
        
        # Add exception info
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Usage
logger = logging.getLogger(__name__)
logger.info("Processing request", extra={"user_id": user_id})
```

---

## Database Access

### Async Context Manager Pattern
```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

@asynccontextmanager
async def get_db():
    """Async database session context manager"""
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

# Usage
async def create_user(user_data: dict):
    async with get_db() as session:
        user = User(**user_data)
        session.add(user)
        # Commit happens automatically on context exit
        return user
```

### FastAPI Dependency Pattern
```python
async def get_db_session():
    """FastAPI dependency for database sessions"""
    async with get_db() as session:
        yield session

# Usage in routes
@router.post("/users")
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db_session)
):
    user = User(**user_data.dict())
    db.add(user)
    await db.commit()
    return user
```

---

## Testing

### Fixture Pattern
```python
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_api_client():
    """Mock API client for testing"""
    client = AsyncMock(spec=APIClient)
    client.fetch.return_value = {"data": "test"}
    return client

@pytest.fixture
def mock_container(mock_api_client):
    """Mock service container"""
    container = AsyncMock(spec=ServiceContainer)
    container.get_api_client.return_value = mock_api_client
    return container

async def test_get_data(mock_container):
    """Test with mocked dependencies"""
    result = await get_data("test_id", mock_container)
    assert result["data"] == "test"
    mock_container.get_api_client.assert_called_once()
```
