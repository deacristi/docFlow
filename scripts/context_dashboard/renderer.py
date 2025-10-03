"""
Dashboard Renderer - Renders beautiful CLI dashboard output.

Formats context state and metrics for terminal display.
"""

from typing import List, Optional
from datetime import datetime

from .models import (
    ContextState,
    MetricsSnapshot,
    HealthStatus,
    Recommendation,
)


class DashboardRenderer:
    """Renders context dashboard for CLI output."""
    
    def __init__(self, width: int = 80):
        """
        Initialize dashboard renderer.
        
        Args:
            width: Terminal width for formatting
        """
        self.width = width
    
    def render_dashboard(
        self,
        context_state: ContextState,
        metrics: MetricsSnapshot,
        recommendations: List[str],
        capacity_info: Optional[dict] = None,
    ) -> str:
        """
        Render complete dashboard.
        
        Args:
            context_state: Current context state
            metrics: Calculated metrics
            recommendations: List of recommendation strings
            capacity_info: Optional capacity estimation info
            
        Returns:
            Formatted dashboard string
        """
        lines = []
        
        # Header
        lines.append(self._render_header())
        lines.append("")
        
        # Context health overview
        lines.append(self._render_health_overview(metrics))
        lines.append("")
        
        # Context breakdown
        lines.append(self._render_context_breakdown(context_state))
        lines.append("")
        
        # Quality metrics
        lines.append(self._render_quality_metrics(metrics))
        lines.append("")
        
        # Efficiency metrics
        lines.append(self._render_efficiency_metrics(metrics))
        lines.append("")
        
        # Eviction queue
        if metrics.eviction_queue:
            lines.append(self._render_eviction_queue(metrics))
            lines.append("")
        
        # Recommendations
        lines.append(self._render_recommendations(recommendations))
        lines.append("")
        
        # Session statistics
        if metrics.messages_exchanged:
            lines.append(self._render_session_stats(context_state, metrics, capacity_info))
            lines.append("")
        
        # Footer
        lines.append(self._render_footer(metrics))
        
        return "\n".join(lines)
    
    def _render_header(self) -> str:
        """Render dashboard header."""
        header = "TradePulse AI Context Dashboard v1.0"
        border = "═" * self.width
        
        return f"╔{border}╗\n║{header.center(self.width)}║\n╚{border}╝"
    
    def _render_health_overview(self, metrics: MetricsSnapshot) -> str:
        """Render context health overview."""
        # Status emoji
        status_emoji = {
            HealthStatus.HEALTHY: "✅",
            HealthStatus.WARNING: "⚠️",
            HealthStatus.CRITICAL: "🔴",
        }
        emoji = status_emoji.get(metrics.health_status, "❓")
        
        # Progress bar
        bar_width = 50
        filled = int((metrics.usage_percentage / 100) * bar_width)
        empty = bar_width - filled
        bar = "█" * filled + "░" * empty
        
        lines = [
            f"📊 Context Health: {emoji} {metrics.health_status.value} ({metrics.usage_percentage:.1f}% used)",
            "━" * self.width,
            f"Used:      {metrics.used_tokens:,} tokens {bar}",
            f"Available: {metrics.available_tokens:,} tokens",
        ]
        
        return "\n".join(lines)
    
    def _render_context_breakdown(self, context_state: ContextState) -> str:
        """Render context breakdown by category."""
        lines = [
            "📈 Context Breakdown by Category:",
            "━" * self.width,
        ]
        
        for category in context_state.categories:
            # Create mini bar
            bar_width = 10
            filled = int((category.percentage / 10) * bar_width)  # Scale to 10% per char
            bar = "█" * filled
            
            line = (
                f"  {category.name:25s} "
                f"{category.tokens:>6,} tokens "
                f"({category.percentage:4.1f}%)  "
                f"[{category.retention.value:12s}]  "
                f"{bar}"
            )
            lines.append(line)
        
        return "\n".join(lines)
    
    def _render_quality_metrics(self, metrics: MetricsSnapshot) -> str:
        """Render quality metrics."""
        # Overall score emoji
        if metrics.accuracy_score >= 90:
            score_emoji = "✅"
        elif metrics.accuracy_score >= 80:
            score_emoji = "⚠️"
        else:
            score_emoji = "🔴"
        
        lines = [
            f"🎯 Context Quality Metrics:",
            "━" * self.width,
            f"  Overall Accuracy Score:        {metrics.accuracy_score}/100  {score_emoji}",
            f"    ├─ Documentation Freshness:  {metrics.documentation_freshness}/100  {self._score_emoji(metrics.documentation_freshness)}",
            f"    ├─ Pattern Consistency:      {metrics.pattern_consistency}/100  {self._score_emoji(metrics.pattern_consistency)}",
            f"    ├─ Knowledge Retention:      {metrics.knowledge_retention}/100  {self._score_emoji(metrics.knowledge_retention)}",
            f"    └─ Retrieval Efficiency:     {metrics.retrieval_efficiency}/100  {self._score_emoji(metrics.retrieval_efficiency)}",
        ]
        
        return "\n".join(lines)
    
    def _render_efficiency_metrics(self, metrics: MetricsSnapshot) -> str:
        """Render efficiency metrics."""
        lines = [
            f"⚡ Efficiency Metrics:",
            "━" * self.width,
            f"  Efficiency Score:              {metrics.efficiency_score:.2f}    {self._efficiency_emoji(metrics.efficiency_score)} (Information Value / Token Cost)",
            f"  Retrieval Calls per Question:  {metrics.retrieval_calls_per_question:.1f}      {self._calls_emoji(metrics.retrieval_calls_per_question)} (Target: <2.0)",
            f"  Knowledge Retention Rate:      {metrics.knowledge_retention_rate:.0%}     {self._score_emoji(int(metrics.knowledge_retention_rate * 100))} (Target: >85%)",
        ]
        
        return "\n".join(lines)
    
    def _render_eviction_queue(self, metrics: MetricsSnapshot) -> str:
        """Render eviction queue preview."""
        lines = [
            "🔄 Eviction Queue Preview (Next to be removed if context fills):",
            "━" * self.width,
        ]
        
        for i, item in enumerate(metrics.eviction_queue[:5], 1):
            line = (
                f"  {i}. {item.type:15s} "
                f"({item.age_messages:2d} msgs old, "
                f"{item.tokens:>5,} tokens, "
                f"{item.value:6s} value)"
            )
            lines.append(line)
        
        if metrics.total_reclaimable > 0:
            lines.append("")
            lines.append(f"  Total Reclaimable: ~{metrics.total_reclaimable:,} tokens")
        
        return "\n".join(lines)
    
    def _render_recommendations(self, recommendations: List[str]) -> str:
        """Render recommendations."""
        lines = [
            "💡 Recommendations:",
            "━" * self.width,
        ]
        
        for rec in recommendations:
            lines.append(f"  {rec}")
        
        return "\n".join(lines)
    
    def _render_session_stats(
        self,
        context_state: ContextState,
        metrics: MetricsSnapshot,
        capacity_info: Optional[dict],
    ) -> str:
        """Render session statistics."""
        lines = [
            "📊 Session Statistics:",
            "━" * self.width,
        ]
        
        if metrics.session_duration_minutes:
            lines.append(f"  Session Duration:        ~{metrics.session_duration_minutes} minutes")
        
        if metrics.messages_exchanged:
            lines.append(f"  Messages Exchanged:      {metrics.messages_exchanged} messages")
        
        if context_state.files_modified > 0:
            lines.append(f"  Files Modified:          {context_state.files_modified}")
        
        if context_state.files_created > 0:
            lines.append(f"  Files Created:           {context_state.files_created}")
        
        if context_state.files_viewed > 0:
            lines.append(f"  Files Viewed:            {context_state.files_viewed}")
        
        if context_state.tool_calls_made > 0:
            lines.append(f"  Tool Calls Made:         {context_state.tool_calls_made}")
        
        if capacity_info:
            lines.append("")
            tokens_per_msg = capacity_info.get("tokens_per_message", 0)
            msgs_remaining = capacity_info.get("messages_remaining", 0)
            lines.append(f"  Context Growth Rate:     ~{tokens_per_msg:.0f} tokens/message")
            lines.append(f"  Estimated Capacity:      ~{msgs_remaining} more messages at current rate")
        
        return "\n".join(lines)
    
    def _render_footer(self, metrics: MetricsSnapshot) -> str:
        """Render dashboard footer."""
        status_text = {
            HealthStatus.HEALTHY: "✅ HEALTHY - No action needed",
            HealthStatus.WARNING: "⚠️ WARNING - Consider refreshing context",
            HealthStatus.CRITICAL: "🔴 CRITICAL - Refresh context immediately",
        }
        status = status_text.get(metrics.health_status, "❓ UNKNOWN")
        
        border = "━" * self.width
        timestamp = metrics.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"{border}\nLast Updated: {timestamp}\nStatus: {status}\n{border}"
    
    def _score_emoji(self, score: int) -> str:
        """Get emoji for score."""
        if score >= 90:
            return "✅"
        elif score >= 80:
            return "⚠️"
        else:
            return "🔴"
    
    def _efficiency_emoji(self, score: float) -> str:
        """Get emoji for efficiency score."""
        if score >= 0.85:
            return "✅"
        elif score >= 0.70:
            return "⚠️"
        else:
            return "🔴"
    
    def _calls_emoji(self, calls: float) -> str:
        """Get emoji for retrieval calls."""
        if calls <= 2.0:
            return "✅"
        elif calls <= 3.0:
            return "⚠️"
        else:
            return "🔴"

