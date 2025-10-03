# AI Context Dashboard

**Version**: 1.0.0  
**Status**: Production-Ready ✅

Real-time monitoring and optimization tool for AI context management in TradePulse v4.0 development.

---

## 📊 Overview

The AI Context Dashboard provides visibility into AI context health, usage patterns, and optimization opportunities. It helps maintain high accuracy and efficiency throughout development sessions.

**Key Features**:
- ✅ Real-time context health monitoring
- ✅ Token usage breakdown by category
- ✅ Accuracy and efficiency scoring
- ✅ Eviction queue preview
- ✅ Actionable recommendations
- ✅ Session statistics tracking

---

## 🚀 Quick Start

```bash
# Run dashboard with current context state
python scripts/context_dashboard.py

# Run with specific metrics
python scripts/context_dashboard.py --current-usage 45000 --messages 20
```

---

## 📁 Module Structure

```
scripts/context_dashboard/
├── __init__.py           # Package initialization
├── models.py             # Data structures (ContextState, MetricsSnapshot, etc.)
├── analyzer.py           # Context analysis engine
├── metrics.py            # Metrics calculator (health, accuracy, efficiency)
├── recommender.py        # Recommendation engine
├── renderer.py           # CLI dashboard renderer
└── README.md             # This file
```

---

## 🏗️ Architecture

### **Data Flow**

```
User Input (CLI args)
    ↓
ContextAnalyzer
    ├─ Analyze token usage
    ├─ Categorize context
    └─ Build eviction queue
    ↓
MetricsCalculator
    ├─ Calculate health score
    ├─ Calculate accuracy score
    └─ Calculate efficiency score
    ↓
RecommendationEngine
    ├─ Analyze metrics
    ├─ Generate recommendations
    └─ Prioritize actions
    ↓
DashboardRenderer
    ├─ Format output
    └─ Display dashboard
    ↓
Terminal Output
```

### **Key Components**

**1. ContextAnalyzer** (`analyzer.py`)
- Analyzes current context state
- Categorizes token usage
- Builds eviction queue
- Estimates capacity remaining

**2. MetricsCalculator** (`metrics.py`)
- Calculates health status
- Computes accuracy metrics (freshness, consistency, retention, retrieval)
- Computes efficiency metrics (score, calls per question, retention rate)
- Determines overall health status

**3. RecommendationEngine** (`recommender.py`)
- Analyzes context state and metrics
- Generates actionable recommendations
- Prioritizes recommendations by importance
- Provides simple text recommendations

**4. DashboardRenderer** (`renderer.py`)
- Formats dashboard output for CLI
- Creates progress bars and visualizations
- Renders all dashboard sections
- Provides color-coded status indicators

**5. Data Models** (`models.py`)
- `ContextState`: Complete context state
- `CategoryBreakdown`: Token breakdown by category
- `MetricsSnapshot`: All calculated metrics
- `EvictionItem`: Item in eviction queue
- `Recommendation`: Single recommendation
- `HealthStatus`: Health status enum
- `RetentionLevel`: Retention priority enum

---

## 🎯 Usage Examples

### **Basic Usage**

```python
from scripts.context_dashboard.analyzer import ContextAnalyzer
from scripts.context_dashboard.metrics import MetricsCalculator
from scripts.context_dashboard.recommender import RecommendationEngine
from scripts.context_dashboard.renderer import DashboardRenderer

# Initialize components
analyzer = ContextAnalyzer(total_tokens=200000)
metrics_calculator = MetricsCalculator(total_tokens=200000)
recommender = RecommendationEngine()
renderer = DashboardRenderer()

# Analyze context
context_state = analyzer.analyze_current_context(
    current_token_usage=45000,
    messages_exchanged=20,
    files_viewed=12,
)

# Calculate metrics
metrics = metrics_calculator.calculate_all_metrics(
    context_state=context_state,
    messages_exchanged=20,
    retrieval_calls=12,
)

# Generate recommendations
recommendations = recommender.generate_simple_recommendations(metrics)

# Render dashboard
dashboard = renderer.render_dashboard(
    context_state=context_state,
    metrics=metrics,
    recommendations=recommendations,
)

print(dashboard)
```

### **Custom Configuration**

```python
# Load custom configuration
config = {
    "total_tokens": 200000,
    "health_warning_threshold": 75.0,
    "health_critical_threshold": 90.0,
    "accuracy_warning_threshold": 80,
    "accuracy_critical_threshold": 70,
}

# Initialize with custom config
metrics_calculator = MetricsCalculator(
    total_tokens=config["total_tokens"],
    health_warning_threshold=config["health_warning_threshold"],
    health_critical_threshold=config["health_critical_threshold"],
    accuracy_warning_threshold=config["accuracy_warning_threshold"],
    accuracy_critical_threshold=config["accuracy_critical_threshold"],
)
```

---

## 📊 Metrics Explained

### **Health Metrics**
- **Total Tokens**: 200,000 (Claude Sonnet 4.5 budget)
- **Used Tokens**: Current token usage
- **Usage Percentage**: (Used / Total) × 100
- **Health Status**: HEALTHY | WARNING | CRITICAL

### **Accuracy Metrics** (0-100)
- **Documentation Freshness**: How recently docs were loaded
- **Pattern Consistency**: How well AI follows patterns
- **Knowledge Retention**: How much info is preserved
- **Retrieval Efficiency**: How efficiently AI retrieves info
- **Overall Accuracy**: Weighted average of above

### **Efficiency Metrics**
- **Efficiency Score** (0-1.0): Information value / token cost
- **Retrieval Calls per Question**: Avg retrieval calls per question
- **Knowledge Retention Rate** (0-1.0): % of info preserved

---

## 🔧 Configuration

Configuration is loaded from `config_specification.yaml`:

```yaml
context_dashboard:
  total_tokens: 200000
  health_warning_threshold: 70.0
  health_critical_threshold: 85.0
  accuracy_warning_threshold: 85
  accuracy_critical_threshold: 75
  efficiency_warning_threshold: 0.7
  efficiency_critical_threshold: 0.5
  eviction_preview_count: 5
  max_recommendations: 5
  recommendation_priority_threshold: 7
```

---

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest scripts/context_dashboard/tests/

# Run with coverage
pytest --cov=scripts/context_dashboard scripts/context_dashboard/tests/
```

---

## 📚 Documentation

- **Usage Guide**: `docs/tools/context_dashboard_guide.md`
- **Value Analysis**: `docs/analysis/CONTEXT_DASHBOARD_VALUE_ANALYSIS.md`
- **Implementation Plan**: `docs/implementation_plans/ai_context_dashboard_implementation_plan.md`
- **Workflow Integration**: `docs/workflow_guide.md`

---

## 🎯 Integration with docFlow

The dashboard integrates with the docFlow framework at Phase 1:

```markdown
## Phase 1: Root Cause Investigation
1. Context Health Check: Run `python scripts/context_dashboard.py`
2. Thorough Analysis: Use codebase-retrieval tools...
3. Context Refresh: Review initial_prompt.md...
```

---

## 🚀 Future Enhancements

**Phase 2** (Future):
- Web-based dashboard with real-time updates
- Context history tracking and trends
- Automated context optimization
- Integration with CI/CD pipeline
- Multi-project context comparison
- Machine learning-based recommendations

---

## 📝 Version History

**v1.0.0** (2025-10-03)
- Initial release
- CLI dashboard with all core features
- Integration with docFlow workflow
- Production-ready implementation

---

## 👥 Contributors

- TradePulse Development Team
- Built with docFlow framework principles

---

## 📄 License

Part of TradePulse v4.0 backend system.

---

**Status**: ✅ Production-Ready  
**Last Updated**: 2025-10-03

