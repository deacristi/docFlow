"""
Recommendation Engine - Generates actionable recommendations.

Analyzes context state and provides optimization suggestions.
"""

from typing import List, Dict
from .models import (
    ContextState,
    MetricsSnapshot,
    Recommendation,
    HealthStatus,
)


class RecommendationEngine:
    """Generates context optimization recommendations."""
    
    def __init__(
        self,
        max_recommendations: int = 5,
        priority_threshold: int = 7,
    ):
        """
        Initialize recommendation engine.
        
        Args:
            max_recommendations: Maximum recommendations to return
            priority_threshold: Minimum priority to include (1-10)
        """
        self.max_recommendations = max_recommendations
        self.priority_threshold = priority_threshold
    
    def generate_recommendations(
        self,
        context_state: ContextState,
        metrics: MetricsSnapshot,
    ) -> List[Recommendation]:
        """
        Generate recommendations based on context state and metrics.
        
        Args:
            context_state: Current context state
            metrics: Calculated metrics
            
        Returns:
            List of Recommendation objects, sorted by priority
        """
        recommendations = []
        
        # Check health status
        recommendations.extend(self._check_health_status(metrics))
        
        # Check accuracy metrics
        recommendations.extend(self._check_accuracy_metrics(metrics))
        
        # Check efficiency metrics
        recommendations.extend(self._check_efficiency_metrics(metrics))
        
        # Check token usage
        recommendations.extend(self._check_token_usage(metrics, context_state))
        
        # Check eviction queue
        recommendations.extend(self._check_eviction_queue(metrics))
        
        # Filter by priority threshold
        recommendations = [
            r for r in recommendations 
            if r.priority >= self.priority_threshold
        ]
        
        # Sort by priority (highest first)
        recommendations.sort(key=lambda r: r.priority, reverse=True)
        
        # Limit to max recommendations
        return recommendations[:self.max_recommendations]
    
    def _check_health_status(self, metrics: MetricsSnapshot) -> List[Recommendation]:
        """Check health status and generate recommendations."""
        recommendations = []
        
        if metrics.health_status == HealthStatus.CRITICAL:
            recommendations.append(Recommendation(
                priority=10,
                category="critical",
                action="CRITICAL: Refresh context immediately",
                reason=f"Context usage at {metrics.usage_percentage:.1f}% or accuracy at {metrics.accuracy_score}/100",
                impact="Prevent context degradation and errors",
            ))
        elif metrics.health_status == HealthStatus.WARNING:
            recommendations.append(Recommendation(
                priority=8,
                category="warning",
                action="WARNING: Consider refreshing context soon",
                reason=f"Context usage at {metrics.usage_percentage:.1f}% or accuracy at {metrics.accuracy_score}/100",
                impact="Maintain high quality before degradation",
            ))
        
        return recommendations
    
    def _check_accuracy_metrics(self, metrics: MetricsSnapshot) -> List[Recommendation]:
        """Check accuracy metrics and generate recommendations."""
        recommendations = []
        
        # Documentation freshness
        if metrics.documentation_freshness < 80:
            recommendations.append(Recommendation(
                priority=9,
                category="critical" if metrics.documentation_freshness < 70 else "warning",
                action="Refresh development_standards.md",
                reason=f"Documentation freshness at {metrics.documentation_freshness}/100",
                impact="Improve accuracy by 10-15 points",
            ))
        
        # Pattern consistency
        if metrics.pattern_consistency < 85:
            recommendations.append(Recommendation(
                priority=8,
                category="warning",
                action="Review project-specific tool patterns",
                reason=f"Pattern consistency at {metrics.pattern_consistency}/100",
                impact="Ensure consistent code quality",
            ))
        
        # Knowledge retention
        if metrics.knowledge_retention < 80:
            recommendations.append(Recommendation(
                priority=7,
                category="warning",
                action="Consider starting new thread",
                reason=f"Knowledge retention at {metrics.knowledge_retention}/100",
                impact="Restore full context capacity",
            ))
        
        # Retrieval efficiency
        if metrics.retrieval_efficiency < 85:
            recommendations.append(Recommendation(
                priority=7,
                category="proactive",
                action="Reduce redundant file retrievals",
                reason=f"Retrieval efficiency at {metrics.retrieval_efficiency}/100",
                impact="Save 2-3K tokens",
            ))
        
        return recommendations
    
    def _check_efficiency_metrics(self, metrics: MetricsSnapshot) -> List[Recommendation]:
        """Check efficiency metrics and generate recommendations."""
        recommendations = []
        
        # Efficiency score
        if metrics.efficiency_score < 0.7:
            recommendations.append(Recommendation(
                priority=8,
                category="warning",
                action="Optimize token usage",
                reason=f"Efficiency score at {metrics.efficiency_score:.2f}",
                impact="Improve information density",
            ))
        
        # Retrieval calls per question
        if metrics.retrieval_calls_per_question > 3:
            recommendations.append(Recommendation(
                priority=7,
                category="proactive",
                action="Load MASTER_CONTEXT_LOADER.md",
                reason=f"High retrieval rate: {metrics.retrieval_calls_per_question:.1f} calls per question",
                impact="Reduce retrieval calls by 50%",
            ))
        
        # Knowledge retention rate
        if metrics.knowledge_retention_rate < 0.85:
            recommendations.append(Recommendation(
                priority=7,
                category="proactive",
                action="Compress old conversation history",
                reason=f"Knowledge retention rate at {metrics.knowledge_retention_rate:.0%}",
                impact="Save 5-8K tokens",
            ))
        
        return recommendations
    
    def _check_token_usage(
        self,
        metrics: MetricsSnapshot,
        context_state: ContextState,
    ) -> List[Recommendation]:
        """Check token usage patterns and generate recommendations."""
        recommendations = []
        
        # High usage warning
        if metrics.usage_percentage > 80:
            recommendations.append(Recommendation(
                priority=9,
                category="critical",
                action="Start new thread after current task",
                reason=f"Context usage at {metrics.usage_percentage:.1f}%",
                impact="Restore full capacity and accuracy",
            ))
        elif metrics.usage_percentage > 70:
            recommendations.append(Recommendation(
                priority=7,
                category="warning",
                action="Plan to start new thread soon",
                reason=f"Context usage at {metrics.usage_percentage:.1f}%",
                impact="Prevent context degradation",
            ))
        
        # Check for large categories that could be optimized
        for category in context_state.categories:
            if category.name == "Tool Results" and category.tokens > 5000:
                recommendations.append(Recommendation(
                    priority=7,
                    category="proactive",
                    action="Clear old tool results",
                    reason=f"Tool results using {category.tokens} tokens",
                    impact=f"Save ~{category.tokens // 2} tokens",
                ))
            elif category.name == "Documentation Viewed" and category.tokens > 15000:
                recommendations.append(Recommendation(
                    priority=7,
                    category="proactive",
                    action="Remove duplicate documentation",
                    reason=f"Documentation using {category.tokens} tokens",
                    impact=f"Save ~{category.tokens // 3} tokens",
                ))
        
        return recommendations
    
    def _check_eviction_queue(self, metrics: MetricsSnapshot) -> List[Recommendation]:
        """Check eviction queue and generate recommendations."""
        recommendations = []
        
        # If significant tokens can be reclaimed
        if metrics.total_reclaimable > 5000:
            recommendations.append(Recommendation(
                priority=7,
                category="proactive",
                action="Proactively evict low-value content",
                reason=f"{metrics.total_reclaimable} tokens can be reclaimed",
                impact=f"Free up {metrics.total_reclaimable} tokens",
            ))
        
        return recommendations
    
    def generate_simple_recommendations(
        self,
        metrics: MetricsSnapshot,
    ) -> List[str]:
        """
        Generate simple text recommendations (for backward compatibility).
        
        Args:
            metrics: Calculated metrics
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Health-based recommendations
        if metrics.health_status == HealthStatus.HEALTHY:
            recommendations.append("✅ Context is healthy - no immediate actions needed")
        elif metrics.health_status == HealthStatus.WARNING:
            recommendations.append(f"⚠️ WARNING: Context usage at {metrics.usage_percentage:.1f}%")
            recommendations.append("   Consider refreshing context or starting new thread")
        else:  # CRITICAL
            recommendations.append(f"🔴 CRITICAL: Context usage at {metrics.usage_percentage:.1f}%")
            recommendations.append("   Refresh context immediately or start new thread")
        
        # Accuracy-based recommendations
        if metrics.accuracy_score < 85:
            recommendations.append(f"⚠️ Accuracy score: {metrics.accuracy_score}/100")
            if metrics.documentation_freshness < 80:
                recommendations.append("   • Refresh development_standards.md")
            if metrics.knowledge_retention < 80:
                recommendations.append("   • Consider starting new thread")
        
        # Proactive recommendations
        if metrics.health_status == HealthStatus.HEALTHY:
            recommendations.append("")
            recommendations.append("📋 Proactive Optimizations:")
            recommendations.append("  • Continue following docFlow framework")
            if metrics.messages_exchanged and metrics.messages_exchanged > 30:
                recommendations.append("  • Monitor if implementing large features (>20K tokens)")
        
        return recommendations

