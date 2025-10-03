"""
Metrics Calculator - Calculates context quality metrics.

Computes health, accuracy, and efficiency scores.
"""

from typing import Dict, Optional
from datetime import datetime

from .models import (
    MetricsSnapshot,
    HealthStatus,
    EvictionItem,
    ContextState,
)


class MetricsCalculator:
    """Calculates context quality metrics."""
    
    def __init__(
        self,
        total_tokens: int = 200000,
        health_warning_threshold: float = 70.0,
        health_critical_threshold: float = 85.0,
        accuracy_warning_threshold: int = 85,
        accuracy_critical_threshold: int = 75,
        efficiency_warning_threshold: float = 0.7,
        efficiency_critical_threshold: float = 0.5,
    ):
        """
        Initialize metrics calculator.
        
        Args:
            total_tokens: Total token budget
            health_warning_threshold: Usage % for warning status
            health_critical_threshold: Usage % for critical status
            accuracy_warning_threshold: Accuracy score for warning
            accuracy_critical_threshold: Accuracy score for critical
            efficiency_warning_threshold: Efficiency score for warning
            efficiency_critical_threshold: Efficiency score for critical
        """
        self.total_tokens = total_tokens
        self.health_warning_threshold = health_warning_threshold
        self.health_critical_threshold = health_critical_threshold
        self.accuracy_warning_threshold = accuracy_warning_threshold
        self.accuracy_critical_threshold = accuracy_critical_threshold
        self.efficiency_warning_threshold = efficiency_warning_threshold
        self.efficiency_critical_threshold = efficiency_critical_threshold
    
    def calculate_all_metrics(
        self,
        context_state: ContextState,
        messages_exchanged: int = 0,
        retrieval_calls: int = 0,
        session_duration_minutes: Optional[int] = None,
    ) -> MetricsSnapshot:
        """
        Calculate all context metrics.
        
        Args:
            context_state: Current context state
            messages_exchanged: Number of messages in conversation
            retrieval_calls: Number of retrieval tool calls made
            session_duration_minutes: Session duration in minutes
            
        Returns:
            MetricsSnapshot with all calculated metrics
        """
        # Calculate basic health metrics
        used_tokens = context_state.total_tokens
        available_tokens = self.total_tokens - used_tokens
        usage_percentage = (used_tokens / self.total_tokens) * 100
        
        # Calculate accuracy metrics
        accuracy_metrics = self._calculate_accuracy_metrics(
            context_state,
            messages_exchanged,
        )
        
        # Calculate efficiency metrics
        efficiency_metrics = self._calculate_efficiency_metrics(
            used_tokens,
            messages_exchanged,
            retrieval_calls,
        )
        
        # Determine health status
        health_status = self._calculate_health_status(
            usage_percentage,
            accuracy_metrics["overall"],
        )
        
        # Build eviction queue
        from .analyzer import ContextAnalyzer
        analyzer = ContextAnalyzer(self.total_tokens)
        eviction_queue = analyzer.build_eviction_queue(messages_exchanged)
        total_reclaimable = sum(item.tokens for item in eviction_queue)
        
        # Create metrics snapshot
        snapshot = MetricsSnapshot(
            total_tokens=self.total_tokens,
            used_tokens=used_tokens,
            available_tokens=available_tokens,
            usage_percentage=usage_percentage,
            health_status=health_status,
            accuracy_score=accuracy_metrics["overall"],
            documentation_freshness=accuracy_metrics["freshness"],
            pattern_consistency=accuracy_metrics["consistency"],
            knowledge_retention=accuracy_metrics["retention"],
            retrieval_efficiency=accuracy_metrics["retrieval"],
            efficiency_score=efficiency_metrics["score"],
            retrieval_calls_per_question=efficiency_metrics["calls_per_question"],
            context_refresh_frequency=efficiency_metrics["refresh_frequency"],
            knowledge_retention_rate=efficiency_metrics["retention_rate"],
            eviction_queue=eviction_queue,
            total_reclaimable=total_reclaimable,
            timestamp=datetime.now(),
            session_duration_minutes=session_duration_minutes,
            messages_exchanged=messages_exchanged,
        )
        
        return snapshot
    
    def _calculate_accuracy_metrics(
        self,
        context_state: ContextState,
        messages_exchanged: int,
    ) -> Dict[str, int]:
        """
        Calculate accuracy-related metrics.
        
        Returns dict with:
        - overall: Overall accuracy score (0-100)
        - freshness: Documentation freshness (0-100)
        - consistency: Pattern consistency (0-100)
        - retention: Knowledge retention (0-100)
        - retrieval: Retrieval efficiency (0-100)
        """
        # Documentation freshness (based on how recently docs were loaded)
        # In real implementation, would track actual doc load times
        # For now, estimate based on message count
        if messages_exchanged < 10:
            freshness = 98  # Very fresh
        elif messages_exchanged < 30:
            freshness = 95  # Fresh
        elif messages_exchanged < 50:
            freshness = 88  # Moderately fresh
        elif messages_exchanged < 80:
            freshness = 78  # Getting stale
        else:
            freshness = 65  # Stale, needs refresh
        
        # Pattern consistency (based on context quality)
        # Higher if standards docs are in context
        docs_category = context_state.get_category("Documentation Viewed")
        if docs_category and docs_category.tokens > 5000:
            consistency = 95  # Good documentation in context
        elif docs_category and docs_category.tokens > 2000:
            consistency = 90  # Some documentation
        else:
            consistency = 85  # Minimal documentation
        
        # Knowledge retention (based on context usage)
        usage_pct = (context_state.total_tokens / self.total_tokens) * 100
        if usage_pct < 30:
            retention = 95  # Low usage, everything retained
        elif usage_pct < 60:
            retention = 90  # Moderate usage, most retained
        elif usage_pct < 80:
            retention = 85  # High usage, some compression
        else:
            retention = 75  # Very high usage, significant compression
        
        # Retrieval efficiency (based on redundant retrievals)
        # In real implementation, would track actual retrieval patterns
        # For now, estimate based on message count
        if messages_exchanged < 20:
            retrieval = 95  # Few messages, efficient
        elif messages_exchanged < 50:
            retrieval = 90  # Moderate, still efficient
        else:
            retrieval = 85  # Many messages, some redundancy
        
        # Overall accuracy (weighted average)
        overall = int(
            freshness * 0.30 +
            consistency * 0.30 +
            retention * 0.20 +
            retrieval * 0.20
        )
        
        return {
            "overall": overall,
            "freshness": freshness,
            "consistency": consistency,
            "retention": retention,
            "retrieval": retrieval,
        }
    
    def _calculate_efficiency_metrics(
        self,
        used_tokens: int,
        messages_exchanged: int,
        retrieval_calls: int,
    ) -> Dict[str, float]:
        """
        Calculate efficiency-related metrics.
        
        Returns dict with:
        - score: Efficiency score (0-1.0)
        - calls_per_question: Retrieval calls per question
        - refresh_frequency: Messages between refreshes
        - retention_rate: Knowledge retention rate (0-1.0)
        """
        # Efficiency score (Information Value / Token Cost)
        # Higher is better
        # Estimate based on token usage efficiency
        if messages_exchanged == 0:
            efficiency_score = 0.0
        else:
            tokens_per_message = used_tokens / messages_exchanged
            # Ideal: ~1500-2000 tokens per message
            # Calculate efficiency relative to ideal
            ideal_tokens_per_message = 1750
            if tokens_per_message <= ideal_tokens_per_message:
                efficiency_score = 0.95  # Very efficient
            else:
                # Decrease efficiency as tokens per message increases
                efficiency_score = max(0.5, ideal_tokens_per_message / tokens_per_message)
        
        # Retrieval calls per question
        # Estimate: ~half of messages are questions
        questions = max(1, messages_exchanged // 2)
        calls_per_question = retrieval_calls / questions if questions > 0 else 0
        
        # Context refresh frequency
        # In real implementation, would track actual refreshes
        # For now, return None (not tracked yet)
        refresh_frequency = None
        
        # Knowledge retention rate
        # Based on how much information is preserved vs evicted
        # Higher usage = lower retention
        usage_pct = (used_tokens / self.total_tokens) * 100
        if usage_pct < 30:
            retention_rate = 0.95
        elif usage_pct < 60:
            retention_rate = 0.90
        elif usage_pct < 80:
            retention_rate = 0.85
        else:
            retention_rate = 0.75
        
        return {
            "score": efficiency_score,
            "calls_per_question": calls_per_question,
            "refresh_frequency": refresh_frequency,
            "retention_rate": retention_rate,
        }
    
    def _calculate_health_status(
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
        # Critical if usage >= critical threshold OR accuracy < critical threshold
        if (usage_percentage >= self.health_critical_threshold or 
            accuracy_score < self.accuracy_critical_threshold):
            return HealthStatus.CRITICAL
        
        # Warning if usage >= warning threshold OR accuracy < warning threshold
        if (usage_percentage >= self.health_warning_threshold or 
            accuracy_score < self.accuracy_warning_threshold):
            return HealthStatus.WARNING
        
        # Otherwise healthy
        return HealthStatus.HEALTHY

