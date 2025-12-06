"""
[Tool Name] Tool Template

This module provides a template for creating new AI tools.
It demonstrates:
1. Pydantic input models
2. Base class inheritance
3. Standard error handling
4. Async execution

Usage:
    tool = MyTool()
    result = await tool.run(query="search term", limit=10)
"""

from typing import Type, Dict, Any, Optional
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class MyToolInput(BaseModel):
    """Input schema for MyTool."""
    
    query: str = Field(
        ..., 
        description="The search query or input string"
    )
    limit: int = Field(
        default=10, 
        description="Maximum number of results",
        ge=1,
        le=100
    )
    options: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional options for the tool"
    )


class MyToolOutput(BaseModel):
    """Output schema for MyTool."""
    
    success: bool = Field(description="Whether the operation succeeded")
    data: Dict[str, Any] = Field(description="Result data")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class MyTool:
    """
    [Tool Description]
    
    This tool is useful for:
    - [Use case 1]
    - [Use case 2]
    
    Example:
        tool = MyTool()
        result = await tool.run(query="example", limit=5)
    """
    
    name: str = "my_tool_name"
    description: str = "Description of what the tool does and when to use it."
    
    def __init__(self):
        """Initialize the tool."""
        self.input_schema = MyToolInput
        self.output_schema = MyToolOutput
        logger.info(f"Initialized {self.name}")

    def validate_input(self, **kwargs) -> MyToolInput:
        """
        Validate input parameters.
        
        Args:
            **kwargs: Input parameters
            
        Returns:
            Validated input model
            
        Raises:
            ValidationError: If input is invalid
        """
        return MyToolInput(**kwargs)

    async def run(self, **kwargs) -> MyToolOutput:
        """
        Execute the tool.
        
        Args:
            **kwargs: Input parameters matching MyToolInput schema
            
        Returns:
            MyToolOutput with results
        """
        try:
            # Validate input
            input_data = self.validate_input(**kwargs)
            
            logger.info(f"Running {self.name} with query: {input_data.query}")
            
            # Execute tool logic
            result = await self._execute(input_data)
            
            return MyToolOutput(
                success=True,
                data=result
            )
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}", exc_info=True)
            return MyToolOutput(
                success=False,
                data={},
                error=str(e)
            )

    async def _execute(self, input_data: MyToolInput) -> Dict[str, Any]:
        """
        Internal execution logic.
        
        Args:
            input_data: Validated input
            
        Returns:
            Result dictionary
        """
        # Implement your tool logic here
        
        # Example: Search operation
        results = []
        
        # Simulate processing
        for i in range(min(input_data.limit, 5)):
            results.append({
                "id": i,
                "match": f"Result {i} for '{input_data.query}'"
            })
        
        return {
            "query": input_data.query,
            "count": len(results),
            "results": results
        }


# ✅ Factory function for creating tool instances
def create_my_tool() -> MyTool:
    """
    Create a new MyTool instance.
    
    Returns:
        Configured MyTool instance
    """
    return MyTool()


# ✅ Example usage
async def example_usage():
    """Example of how to use the tool."""
    tool = MyTool()
    
    # Run with parameters
    result = await tool.run(
        query="example search",
        limit=5,
        options={"filter": "active"}
    )
    
    if result.success:
        print(f"Found {result.data['count']} results")
        for item in result.data['results']:
            print(f"  - {item['match']}")
    else:
        print(f"Error: {result.error}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
