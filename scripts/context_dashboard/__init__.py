"""
AI Context Dashboard for TradePulse v4.0

Provides real-time monitoring and optimization for AI context management.
Helps maintain high accuracy and efficiency throughout development sessions.

Usage:
    python scripts/context_dashboard.py

Author: TradePulse Development Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "TradePulse Development Team"

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

