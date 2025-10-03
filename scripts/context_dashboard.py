#!/usr/bin/env python3
"""
AI Context Dashboard - Main CLI Entry Point

Displays real-time context health, usage, and optimization recommendations.

Usage:
    python scripts/context_dashboard.py
    python scripts/context_dashboard.py --current-usage 45000 --messages 20

Author: MyProject Development Team
Version: 1.0.0
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.context_dashboard.analyzer import ContextAnalyzer
from scripts.context_dashboard.metrics import MetricsCalculator
from scripts.context_dashboard.recommender import RecommendationEngine
from scripts.context_dashboard.renderer import DashboardRenderer


def load_config() -> dict:
    """
    Load configuration from config_specification.yaml.
    
    Returns:
        Dict with configuration values
    """
    # Default configuration
    config = {
        "total_tokens": 200000,
        "health_warning_threshold": 70.0,
        "health_critical_threshold": 85.0,
        "accuracy_warning_threshold": 85,
        "accuracy_critical_threshold": 75,
        "efficiency_warning_threshold": 0.7,
        "efficiency_critical_threshold": 0.5,
        "eviction_preview_count": 5,
        "max_recommendations": 5,
        "recommendation_priority_threshold": 7,
    }
    
    # Try to load from config file
    try:
        import yaml
        config_path = Path(__file__).parent.parent / "config_specification.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config and "context_dashboard" in yaml_config:
                    config.update(yaml_config["context_dashboard"])
    except Exception:
        # If config loading fails, use defaults
        pass
    
    return config


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="MyProject AI Context Dashboard - Monitor context health and optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Display dashboard with estimated current usage
  python scripts/context_dashboard.py
  
  # Display dashboard with specific usage metrics
  python scripts/context_dashboard.py --current-usage 45000 --messages 20
  
  # Display dashboard with full session info
  python scripts/context_dashboard.py --current-usage 45000 --messages 20 \\
      --files-viewed 12 --files-modified 2 --files-created 7 --tool-calls 24
        """
    )
    
    parser.add_argument(
        "--current-usage",
        type=int,
        default=50000,
        help="Current token usage (default: 50000)",
    )
    
    parser.add_argument(
        "--messages",
        type=int,
        default=16,
        help="Number of messages exchanged (default: 16)",
    )
    
    parser.add_argument(
        "--files-viewed",
        type=int,
        default=12,
        help="Number of files viewed (default: 12)",
    )
    
    parser.add_argument(
        "--files-modified",
        type=int,
        default=2,
        help="Number of files modified (default: 2)",
    )
    
    parser.add_argument(
        "--files-created",
        type=int,
        default=7,
        help="Number of files created (default: 7)",
    )
    
    parser.add_argument(
        "--tool-calls",
        type=int,
        default=24,
        help="Number of tool calls made (default: 24)",
    )
    
    parser.add_argument(
        "--retrieval-calls",
        type=int,
        default=None,
        help="Number of retrieval calls (default: auto-estimate)",
    )
    
    parser.add_argument(
        "--session-duration",
        type=int,
        default=None,
        help="Session duration in minutes (default: auto-estimate)",
    )
    
    parser.add_argument(
        "--width",
        type=int,
        default=80,
        help="Terminal width for formatting (default: 80)",
    )
    
    return parser.parse_args()


def main():
    """Main entry point for context dashboard."""
    # Parse arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config()
    
    # Initialize components
    analyzer = ContextAnalyzer(total_tokens=config["total_tokens"])
    
    metrics_calculator = MetricsCalculator(
        total_tokens=config["total_tokens"],
        health_warning_threshold=config["health_warning_threshold"],
        health_critical_threshold=config["health_critical_threshold"],
        accuracy_warning_threshold=config["accuracy_warning_threshold"],
        accuracy_critical_threshold=config["accuracy_critical_threshold"],
        efficiency_warning_threshold=config["efficiency_warning_threshold"],
        efficiency_critical_threshold=config["efficiency_critical_threshold"],
    )
    
    recommender = RecommendationEngine(
        max_recommendations=config["max_recommendations"],
        priority_threshold=config["recommendation_priority_threshold"],
    )
    
    renderer = DashboardRenderer(width=args.width)
    
    # Analyze current context
    context_state = analyzer.analyze_current_context(
        current_token_usage=args.current_usage,
        messages_exchanged=args.messages,
        files_viewed=args.files_viewed,
        files_modified=args.files_modified,
        files_created=args.files_created,
        tool_calls_made=args.tool_calls,
    )
    
    # Calculate metrics
    retrieval_calls = args.retrieval_calls if args.retrieval_calls is not None else args.files_viewed
    session_duration = args.session_duration if args.session_duration is not None else max(25, args.messages * 2)
    
    metrics = metrics_calculator.calculate_all_metrics(
        context_state=context_state,
        messages_exchanged=args.messages,
        retrieval_calls=retrieval_calls,
        session_duration_minutes=session_duration,
    )
    
    # Generate recommendations
    recommendations = recommender.generate_simple_recommendations(metrics)
    
    # Calculate capacity info
    capacity_info = analyzer.estimate_capacity_remaining(
        current_usage=args.current_usage,
        messages_exchanged=args.messages,
    )
    
    # Render dashboard
    dashboard = renderer.render_dashboard(
        context_state=context_state,
        metrics=metrics,
        recommendations=recommendations,
        capacity_info=capacity_info,
    )
    
    # Display dashboard
    print(dashboard)
    
    # Return exit code based on health status
    from scripts.context_dashboard.models import HealthStatus
    if metrics.health_status == HealthStatus.CRITICAL:
        return 2
    elif metrics.health_status == HealthStatus.WARNING:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())

