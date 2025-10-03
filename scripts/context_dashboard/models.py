"""
Data models for AI Context Dashboard.

Defines the core data structures used throughout the dashboard.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime


class HealthStatus(str, Enum):
    """Context health status levels."""
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class RetentionLevel(str, Enum):
    """Information retention priority levels."""
    PERMANENT = "PERMANENT"
    HIGH = "HIGH"
    MEDIUM_HIGH = "MEDIUM-HIGH"
    MEDIUM = "MEDIUM"
    LOW_MEDIUM = "LOW-MEDIUM"
    LOW = "LOW"


@dataclass
class CategoryBreakdown:
    """Token breakdown for a specific context category."""
    
    name: str
    tokens: int
    percentage: float
    retention: RetentionLevel
    description: str = ""
    
    def __post_init__(self):
        """Validate data after initialization."""
        if self.tokens < 0:
            raise ValueError("Tokens cannot be negative")
        if not 0 <= self.percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")


@dataclass
class EvictionItem:
    """Item in the eviction queue (next to be removed)."""
    
    type: str
    age_messages: int
    tokens: int
    value: str  # "high", "medium", "low"
    description: str
    priority: int = 0  # Lower = removed first
    
    def __post_init__(self):
        """Validate and calculate priority."""
        if self.age_messages < 0:
            raise ValueError("Age cannot be negative")
        if self.tokens < 0:
            raise ValueError("Tokens cannot be negative")
        
        # Calculate priority based on age and value
        value_scores = {"low": 1, "medium": 5, "high": 10}
        value_score = value_scores.get(self.value.lower(), 5)
        
        # Priority = value_score - (age / 10)
        # Lower priority = removed first
        self.priority = value_score - (self.age_messages / 10)


@dataclass
class MetricsSnapshot:
    """Snapshot of all context metrics at a point in time."""
    
    # Health metrics
    total_tokens: int
    used_tokens: int
    available_tokens: int
    usage_percentage: float
    health_status: HealthStatus
    
    # Accuracy metrics
    accuracy_score: int  # 0-100
    documentation_freshness: int  # 0-100
    pattern_consistency: int  # 0-100
    knowledge_retention: int  # 0-100
    retrieval_efficiency: int  # 0-100
    
    # Efficiency metrics
    efficiency_score: float  # 0-1.0
    retrieval_calls_per_question: float
    context_refresh_frequency: Optional[int]  # messages
    knowledge_retention_rate: float  # 0-1.0
    
    # Eviction queue
    eviction_queue: List[EvictionItem] = field(default_factory=list)
    total_reclaimable: int = 0
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    session_duration_minutes: Optional[int] = None
    messages_exchanged: Optional[int] = None
    
    def __post_init__(self):
        """Validate metrics."""
        if self.total_tokens <= 0:
            raise ValueError("Total tokens must be positive")
        if self.used_tokens < 0:
            raise ValueError("Used tokens cannot be negative")
        if self.used_tokens > self.total_tokens:
            raise ValueError("Used tokens cannot exceed total tokens")
        
        # Validate scores are in range
        for score_name in ["accuracy_score", "documentation_freshness", 
                          "pattern_consistency", "knowledge_retention", 
                          "retrieval_efficiency"]:
            score = getattr(self, score_name)
            if not 0 <= score <= 100:
                raise ValueError(f"{score_name} must be between 0 and 100")
        
        if not 0 <= self.efficiency_score <= 1.0:
            raise ValueError("Efficiency score must be between 0 and 1.0")
        if not 0 <= self.knowledge_retention_rate <= 1.0:
            raise ValueError("Knowledge retention rate must be between 0 and 1.0")


@dataclass
class ContextState:
    """Complete state of AI context at a point in time."""
    
    # Token breakdown by category
    categories: List[CategoryBreakdown] = field(default_factory=list)
    
    # Overall metrics
    metrics: Optional[MetricsSnapshot] = None
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    
    # Session info
    session_start: Optional[datetime] = None
    last_refresh: Optional[datetime] = None
    files_modified: int = 0
    files_created: int = 0
    files_viewed: int = 0
    tool_calls_made: int = 0
    
    @property
    def total_tokens(self) -> int:
        """Calculate total tokens from categories."""
        return sum(cat.tokens for cat in self.categories)
    
    @property
    def health_status(self) -> HealthStatus:
        """Get health status from metrics."""
        if self.metrics:
            return self.metrics.health_status
        return HealthStatus.HEALTHY
    
    def get_category(self, name: str) -> Optional[CategoryBreakdown]:
        """Get category breakdown by name."""
        for cat in self.categories:
            if cat.name.lower() == name.lower():
                return cat
        return None
    
    def add_category(self, category: CategoryBreakdown) -> None:
        """Add a category breakdown."""
        # Remove existing category with same name
        self.categories = [c for c in self.categories if c.name != category.name]
        self.categories.append(category)
    
    def sort_categories_by_tokens(self, descending: bool = True) -> None:
        """Sort categories by token count."""
        self.categories.sort(key=lambda c: c.tokens, reverse=descending)


@dataclass
class Recommendation:
    """A single recommendation for context optimization."""
    
    priority: int  # 1-10, higher = more important
    category: str  # "critical", "warning", "proactive"
    action: str
    reason: str
    impact: str  # Expected impact (e.g., "Save ~5K tokens")
    
    def __post_init__(self):
        """Validate recommendation."""
        if not 1 <= self.priority <= 10:
            raise ValueError("Priority must be between 1 and 10")
        if self.category not in ["critical", "warning", "proactive"]:
            raise ValueError("Category must be critical, warning, or proactive")
    
    def __str__(self) -> str:
        """Format recommendation as string."""
        emoji = "🔴" if self.category == "critical" else "⚠️" if self.category == "warning" else "📋"
        return f"{emoji} {self.action} - {self.reason} ({self.impact})"


@dataclass
class ContextTrend:
    """Trend data for context usage over time."""
    
    start_usage: float  # percentage
    current_usage: float  # percentage
    trend_direction: str  # "up", "down", "stable"
    growth_rate: float  # tokens per message
    projected_capacity_at_50_messages: float  # percentage
    projected_capacity_at_100_messages: float  # percentage
    
    def __post_init__(self):
        """Validate trend data."""
        if not 0 <= self.start_usage <= 100:
            raise ValueError("Start usage must be between 0 and 100")
        if not 0 <= self.current_usage <= 100:
            raise ValueError("Current usage must be between 0 and 100")
        if self.trend_direction not in ["up", "down", "stable"]:
            raise ValueError("Trend direction must be up, down, or stable")
    
    @property
    def trend_emoji(self) -> str:
        """Get emoji for trend direction."""
        return "↗️" if self.trend_direction == "up" else "↘️" if self.trend_direction == "down" else "→"


# Type aliases for clarity
TokenCount = int
Percentage = float
Score = int  # 0-100

