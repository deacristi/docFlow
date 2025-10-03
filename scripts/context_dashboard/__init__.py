"""
AI Context Dashboard for MyProject

A comprehensive monitoring and optimization tool for AI development context management.
Provides real-time insights into context health, token usage, and optimization opportunities.

Features:
- Context health monitoring
- Token usage tracking
- Optimization recommendations

Author: MyProject Development Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "MyProject Development Team"

from .models import (
    ContextState,
    CategoryBreakdown,
    EvictionItem,
    MetricsSnapshot,
    HealthStatus,
    RetentionLevel,
)
from .analyzer import ContextAnalyzer
from .metrics import MetricsCalculator
from .recommender import RecommendationEngine
from .renderer import DashboardRenderer

__all__ = [
    "ContextState",
    "CategoryBreakdown",
    "EvictionItem",
    "MetricsSnapshot",
    "HealthStatus",
    "RetentionLevel",
    "ContextAnalyzer",
    "MetricsCalculator",
    "RecommendationEngine",
    "DashboardRenderer",
]

