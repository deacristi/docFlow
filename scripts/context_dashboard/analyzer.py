"""
Context Analyzer - Analyzes current AI context state.

Reads conversation history and categorizes token usage.
"""

from typing import Dict, List, Optional
from datetime import datetime
import re

from .models import (
    ContextState,
    CategoryBreakdown,
    EvictionItem,
    RetentionLevel,
    HealthStatus,
)


class ContextAnalyzer:
    """Analyzes AI context state and categorizes token usage."""
    
    # Estimated token counts for different content types
    SYSTEM_INSTRUCTIONS_TOKENS = 5000
    WORKSPACE_INFO_TOKENS = 2000
    
    def __init__(self, total_tokens: int = 200000):
        """
        Initialize context analyzer.
        
        Args:
            total_tokens: Total token budget available
        """
        self.total_tokens = total_tokens
        self.context_state = ContextState()
    
    def analyze_current_context(
        self,
        current_token_usage: int,
        messages_exchanged: int = 0,
        files_viewed: int = 0,
        files_modified: int = 0,
        files_created: int = 0,
        tool_calls_made: int = 0,
    ) -> ContextState:
        """
        Analyze current context state.
        
        Args:
            current_token_usage: Current total token usage
            messages_exchanged: Number of messages in conversation
            files_viewed: Number of files viewed
            files_modified: Number of files modified
            files_created: Number of files created
            tool_calls_made: Number of tool calls made
            
        Returns:
            ContextState with complete analysis
        """
        # Create context state
        state = ContextState(
            session_start=datetime.now(),
            files_modified=files_modified,
            files_created=files_created,
            files_viewed=files_viewed,
            tool_calls_made=tool_calls_made,
        )
        
        # Estimate token breakdown
        categories = self._estimate_token_breakdown(
            current_token_usage,
            messages_exchanged,
            files_viewed,
            tool_calls_made,
        )
        
        for category in categories:
            state.add_category(category)
        
        # Sort by token count
        state.sort_categories_by_tokens(descending=True)
        
        self.context_state = state
        return state
    
    def _estimate_token_breakdown(
        self,
        total_used: int,
        messages: int,
        files_viewed: int,
        tool_calls: int,
    ) -> List[CategoryBreakdown]:
        """
        Estimate token breakdown by category.
        
        This is an estimation based on typical patterns.
        In a real implementation, this would analyze actual conversation history.
        """
        categories = []
        
        # System instructions (permanent)
        categories.append(CategoryBreakdown(
            name="System Instructions",
            tokens=self.SYSTEM_INSTRUCTIONS_TOKENS,
            percentage=(self.SYSTEM_INSTRUCTIONS_TOKENS / self.total_tokens) * 100,
            retention=RetentionLevel.PERMANENT,
            description="AI role, tools, and behavior rules",
        ))
        
        # Workspace info (high priority)
        categories.append(CategoryBreakdown(
            name="Workspace Info",
            tokens=self.WORKSPACE_INFO_TOKENS,
            percentage=(self.WORKSPACE_INFO_TOKENS / self.total_tokens) * 100,
            retention=RetentionLevel.HIGH,
            description="Working directory, file structure, git info",
        ))
        
        # Estimate remaining tokens
        remaining = total_used - self.SYSTEM_INSTRUCTIONS_TOKENS - self.WORKSPACE_INFO_TOKENS
        
        # Supervisor summary (compressed history) - ~30% of remaining
        supervisor_tokens = int(remaining * 0.30)
        categories.append(CategoryBreakdown(
            name="Supervisor Summary",
            tokens=supervisor_tokens,
            percentage=(supervisor_tokens / self.total_tokens) * 100,
            retention=RetentionLevel.HIGH,
            description="Compressed conversation history",
        ))
        
        # Current conversation - ~25% of remaining
        conversation_tokens = int(remaining * 0.25)
        categories.append(CategoryBreakdown(
            name="Current Conversation",
            tokens=conversation_tokens,
            percentage=(conversation_tokens / self.total_tokens) * 100,
            retention=RetentionLevel.HIGH,
            description="Recent messages and exchanges",
        ))
        
        # Documentation viewed - ~30% of remaining
        docs_tokens = int(remaining * 0.30)
        categories.append(CategoryBreakdown(
            name="Documentation Viewed",
            tokens=docs_tokens,
            percentage=(docs_tokens / self.total_tokens) * 100,
            retention=RetentionLevel.MEDIUM,
            description="Files and docs loaded into context",
        ))
        
        # Tool results - remaining tokens
        tool_tokens = remaining - supervisor_tokens - conversation_tokens - docs_tokens
        if tool_tokens > 0:
            categories.append(CategoryBreakdown(
                name="Tool Results",
                tokens=tool_tokens,
                percentage=(tool_tokens / self.total_tokens) * 100,
                retention=RetentionLevel.LOW,
                description="Tool execution results and outputs",
            ))
        
        return categories
    
    def build_eviction_queue(
        self,
        messages_exchanged: int = 0,
    ) -> List[EvictionItem]:
        """
        Build eviction queue (what gets removed first).
        
        Args:
            messages_exchanged: Number of messages in conversation
            
        Returns:
            List of EvictionItem sorted by priority (lowest first)
        """
        queue = []
        
        # Estimate what would be evicted first
        # In real implementation, this would analyze actual conversation history
        
        # Old tool results (low value, old)
        if messages_exchanged > 5:
            queue.append(EvictionItem(
                type="tool_result",
                age_messages=max(2, messages_exchanged // 4),
                tokens=500,
                value="low",
                description="File save confirmations",
            ))
        
        # Old file contents (low value if not recently referenced)
        if messages_exchanged > 8:
            queue.append(EvictionItem(
                type="file_content",
                age_messages=max(5, messages_exchanged // 3),
                tokens=1200,
                value="low",
                description="Old template views",
            ))
        
        # Old conversation (medium value, compressed not removed)
        if messages_exchanged > 10:
            queue.append(EvictionItem(
                type="conversation",
                age_messages=max(8, messages_exchanged // 2),
                tokens=2000,
                value="medium",
                description="Initial context loading",
            ))
        
        # Sort by priority (lowest first = removed first)
        queue.sort(key=lambda x: x.priority)
        
        return queue
    
    def calculate_health_status(
        self,
        usage_percentage: float,
        accuracy_score: int,
    ) -> HealthStatus:
        """
        Calculate overall health status.
        
        Args:
            usage_percentage: Percentage of tokens used
            accuracy_score: Accuracy score (0-100)
            
        Returns:
            HealthStatus enum
        """
        # Critical if usage > 85% OR accuracy < 75
        if usage_percentage >= 85 or accuracy_score < 75:
            return HealthStatus.CRITICAL
        
        # Warning if usage > 70% OR accuracy < 85
        if usage_percentage >= 70 or accuracy_score < 85:
            return HealthStatus.WARNING
        
        # Otherwise healthy
        return HealthStatus.HEALTHY
    
    def estimate_capacity_remaining(
        self,
        current_usage: int,
        messages_exchanged: int,
    ) -> Dict[str, float]:
        """
        Estimate remaining capacity in messages.
        
        Args:
            current_usage: Current token usage
            messages_exchanged: Messages so far
            
        Returns:
            Dict with capacity estimates
        """
        if messages_exchanged == 0:
            return {
                "tokens_per_message": 0,
                "messages_remaining": 0,
                "projected_at_50": 0,
                "projected_at_100": 0,
            }
        
        # Calculate growth rate
        tokens_per_message = current_usage / messages_exchanged
        
        # Estimate remaining capacity
        available = self.total_tokens - current_usage
        messages_remaining = int(available / tokens_per_message) if tokens_per_message > 0 else 0
        
        # Project usage at 50 and 100 messages
        projected_50 = min(100, (tokens_per_message * 50 / self.total_tokens) * 100)
        projected_100 = min(100, (tokens_per_message * 100 / self.total_tokens) * 100)
        
        return {
            "tokens_per_message": tokens_per_message,
            "messages_remaining": messages_remaining,
            "projected_at_50": projected_50,
            "projected_at_100": projected_100,
        }

