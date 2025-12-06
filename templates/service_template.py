"""
[Service Name] Service Template

This module provides a template for creating new services.
It demonstrates:
1. Lazy initialization (Singleton pattern)
2. Safe configuration access
3. Graceful degradation
4. Standard logging and error handling

Usage:
    from services.my_service import get_my_service
    service = get_my_service()
    result = await service.process(...)
"""

import logging
import asyncio
from typing import Optional, Dict, Any

# Import your project's config and database modules
# from core.config import settings
# from core.database import get_db

logger = logging.getLogger(__name__)


class MyService:
    """
    [Service Description]
    
    Responsibility:
    - [Responsibility 1]
    - [Responsibility 2]
    """
    
    def __init__(self):
        """Initialize service with safe config access."""
        # ✅ Safe Config Access - use getattr with defaults
        # self.config = getattr(settings, 'MY_FEATURE_CONFIG', {})
        # self.timeout = self.config.get('timeout', 30)
        
        self.config = {}
        self.timeout = 30
        
        # ✅ Graceful Degradation
        self.api_client = None
        # api_key = getattr(settings, 'MY_API_KEY', None)
        api_key = None
        
        if api_key:
            try:
                # self.api_client = ExternalClient(api_key)
                logger.info("MyService initialized with API access")
            except Exception as e:
                logger.warning(f"Failed to initialize API client: {e}")
        else:
            logger.warning("MyService running in degraded mode (No API Key)")

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data.
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Processed result dictionary
            
        Raises:
            ServiceException: If processing fails
        """
        try:
            logger.info(f"Processing data: {input_data.get('id')}")
            
            # ✅ Async DB Context (uncomment when using database)
            # async with get_db() as session:
            #     result = await self._internal_logic(session, input_data)
            
            result = {"status": "success", "data": input_data}
            
            return result
            
        except Exception as e:
            # ✅ Standard Error Handling - log and re-raise with context
            logger.error(f"Process failed: {e}", exc_info=True)
            raise RuntimeError(
                f"Failed to process data: {e}"
            ) from e

    async def _internal_logic(self, session, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal processing logic.
        
        Args:
            session: Database session
            input_data: Input parameters
            
        Returns:
            Processed result
        """
        # Implement your logic here
        return {"processed": True}


# ✅ Lazy Initialization Pattern (Thread-Safe Singleton)
_service_instance: Optional[MyService] = None
_service_lock = asyncio.Lock()


async def get_my_service() -> MyService:
    """
    Get or create MyService instance.
    
    Returns:
        MyService singleton instance
    """
    global _service_instance
    
    if _service_instance is None:
        async with _service_lock:
            if _service_instance is None:
                _service_instance = MyService()
                
    return _service_instance


# ✅ Cleanup function for graceful shutdown
async def cleanup_my_service() -> None:
    """Clean up service resources."""
    global _service_instance
    
    if _service_instance is not None:
        # Add cleanup logic here (close connections, etc.)
        _service_instance = None
        logger.info("MyService cleaned up")
