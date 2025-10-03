# AI Context Dashboard - Usage Guide

**Version**: 1.0.0  
**Purpose**: Monitor and optimize AI context health during development sessions  
**Tool**: `scripts/context_dashboard.py`

---

## 📊 Overview

The AI Context Dashboard provides real-time visibility into AI context health, usage patterns, and optimization opportunities. It helps maintain high accuracy and efficiency throughout your development sessions.

**Key Benefits**:
- ✅ Proactive context management (refresh before degradation)
- ✅ Data-driven thread management (know when to start new thread)
- ✅ Self-diagnosis capability (understand why AI made mistakes)
- ✅ 90-180 minutes saved per week
- ✅ 95%+ accuracy maintained throughout sessions

---

## 🚀 Quick Start

### **Basic Usage**

```bash
# Display dashboard with current context state
python scripts/context_dashboard.py
```

### **With Specific Metrics**

```bash
# Display dashboard with known usage metrics
python scripts/context_dashboard.py --current-usage 45000 --messages 20
```

### **Full Session Info**

```bash
# Display dashboard with complete session statistics
python scripts/context_dashboard.py \
    --current-usage 45000 \
    --messages 20 \
    --files-viewed 12 \
    --files-modified 2 \
    --files-created 7 \
    --tool-calls 24
```

---

## 📖 Understanding the Dashboard

### **1. Context Health Overview**

```
📊 Context Health: ✅ HEALTHY (22.1% used)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Used:      44,196 tokens ███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Available: 155,804 tokens
```

**What It Means**:
- **✅ HEALTHY**: Context is in good shape, no action needed
- **⚠️ WARNING**: Context usage >70% or accuracy <85%, consider refreshing
- **🔴 CRITICAL**: Context usage >85% or accuracy <75%, refresh immediately

**Progress Bar**: Visual representation of token usage

---

### **2. Context Breakdown**

```
📈 Context Breakdown by Category:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  System Instructions:     5,000 tokens ( 2.5%)  [PERMANENT]  ████
  Supervisor Summary:     15,000 tokens ( 7.5%)  [HIGH]       ███████████
  Current Conversation:   12,000 tokens ( 6.0%)  [HIGH]       █████████
  Documentation Viewed:    8,000 tokens ( 4.0%)  [MEDIUM]     ██████
  Tool Results:            2,196 tokens ( 1.1%)  [LOW]        ██
  Workspace Info:          2,000 tokens ( 1.0%)  [HIGH]       ██
```

**What It Means**:
- **PERMANENT**: Never removed (system instructions)
- **HIGH**: Preserved as long as possible (recent conversation, workspace info)
- **MEDIUM**: Compressed when space needed (documentation)
- **LOW**: Removed first when space needed (old tool results)

**Mini Bars**: Visual representation of each category's size

---

### **3. Quality Metrics**

```
🎯 Context Quality Metrics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Overall Accuracy Score:        94/100  ✅ Excellent
    ├─ Documentation Freshness:  98/100  ✅ (Just loaded MASTER_CONTEXT_LOADER)
    ├─ Pattern Consistency:      95/100  ✅ (Following docFlow framework)
    ├─ Knowledge Retention:      90/100  ✅ (All key decisions preserved)
    └─ Retrieval Efficiency:     93/100  ✅ (Minimal redundant retrievals)
```

**What It Means**:
- **Documentation Freshness**: How recently standards/docs were loaded
  - <80: Refresh development_standards.md
- **Pattern Consistency**: How well AI follows established patterns
  - <85: Review project-specific tool patterns
- **Knowledge Retention**: How much information is preserved
  - <80: Consider starting new thread
- **Retrieval Efficiency**: How efficiently AI retrieves information
  - <85: Reduce redundant file retrievals

---

### **4. Efficiency Metrics**

```
⚡ Efficiency Metrics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Efficiency Score:              0.91    ✅ (Information Value / Token Cost)
  Retrieval Calls per Question:  1.8     ✅ (Target: <2.0)
  Knowledge Retention Rate:      95%     ✅ (Target: >85%)
```

**What It Means**:
- **Efficiency Score**: Information value per token (higher is better)
  - >0.85: Excellent
  - 0.70-0.85: Good
  - <0.70: Needs optimization
- **Retrieval Calls per Question**: How many times AI retrieves info per question
  - <2.0: Efficient
  - 2.0-3.0: Acceptable
  - >3.0: Too many redundant retrievals
- **Knowledge Retention Rate**: Percentage of information preserved
  - >85%: Good retention
  - <85%: Significant compression happening

---

### **5. Eviction Queue**

```
🔄 Eviction Queue Preview (Next to be removed if context fills):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. tool_result      (2 msgs old,   500 tokens, low    value)
  2. file_content     (5 msgs old, 1,200 tokens, low    value)
  3. conversation     (8 msgs old, 2,000 tokens, medium value)
  
  Total Reclaimable: ~3,700 tokens (if needed)
```

**What It Means**:
- Shows what will be removed first if context fills up
- Lower priority items (low value, old) are removed first
- Helps understand what AI might "forget" next

---

### **6. Recommendations**

```
💡 Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Context is healthy - no immediate actions needed
  
  📋 Proactive Optimizations:
    • Continue following docFlow framework
    • Monitor if implementing large features (>20K tokens)
```

**What It Means**:
- **✅ Healthy**: No action needed
- **⚠️ Warning**: Recommended actions to maintain quality
- **🔴 Critical**: Immediate actions required

---

## 🎯 When to Use the Dashboard

### **1. Start of Development Session**

```bash
python scripts/context_dashboard.py
```

**Check**: Is context healthy? (Should be ~10-15% at start)

---

### **2. Before Major Implementation**

Before implementing new tools or complex features:

```bash
python scripts/context_dashboard.py
```

**Check**: 
- Are standards fresh? (Documentation Freshness >90%)
- Is accuracy high? (Overall Accuracy >90%)

**Action**: If not, refresh context first

---

### **3. Mid-Session Check**

Every 30-40 messages:

```bash
python scripts/context_dashboard.py
```

**Check**:
- Should I refresh context? (Accuracy <85%)
- Should I start new thread? (Usage >70%)

---

### **4. When AI Makes Mistakes**

If AI violates standards or makes unexpected errors:

```bash
python scripts/context_dashboard.py
```

**Check**:
- Is context stale? (Documentation Freshness <80%)
- What needs refresh? (See recommendations)

**Action**: Refresh identified documents

---

## 📋 Common Scenarios

### **Scenario 1: Context is Healthy**

```
Status: ✅ HEALTHY
Accuracy: 94/100
Usage: 22%
```

**Action**: Continue working, no changes needed

---

### **Scenario 2: Context Needs Refresh**

```
Status: ⚠️ WARNING
Accuracy: 83/100
Documentation Freshness: 78/100
```

**Recommendation**: Refresh development_standards.md

**Action**:
```
AI, please refresh development_standards.md before continuing.
```

---

### **Scenario 3: Start New Thread**

```
Status: ⚠️ WARNING
Usage: 75%
Messages Remaining: ~15
```

**Recommendation**: Start new thread after current feature

**Action**: Complete current task, then start new thread with fresh context

---

### **Scenario 4: Critical State**

```
Status: 🔴 CRITICAL
Usage: 87%
Accuracy: 72/100
```

**Recommendation**: Refresh context immediately or start new thread

**Action**: 
1. Save current state
2. Start new thread
3. Load MASTER_CONTEXT_LOADER.md
4. Resume work

---

## ⚙️ Configuration

Dashboard settings are in `config_specification.yaml`:

```yaml
context_dashboard:
  total_tokens: 200000
  health_warning_threshold: 70.0
  health_critical_threshold: 85.0
  accuracy_warning_threshold: 85
  accuracy_critical_threshold: 75
  efficiency_warning_threshold: 0.7
  efficiency_critical_threshold: 0.5
```

**Adjust thresholds** based on your preferences.

---

## 🔧 Command-Line Options

```bash
python scripts/context_dashboard.py --help
```

**Available Options**:
- `--current-usage`: Current token usage (default: 50000)
- `--messages`: Number of messages exchanged (default: 16)
- `--files-viewed`: Number of files viewed (default: 12)
- `--files-modified`: Number of files modified (default: 2)
- `--files-created`: Number of files created (default: 7)
- `--tool-calls`: Number of tool calls made (default: 24)
- `--retrieval-calls`: Number of retrieval calls (default: auto-estimate)
- `--session-duration`: Session duration in minutes (default: auto-estimate)
- `--width`: Terminal width for formatting (default: 80)

---

## 📊 Exit Codes

The dashboard returns different exit codes based on health status:

- **0**: HEALTHY - No action needed
- **1**: WARNING - Consider refreshing context
- **2**: CRITICAL - Refresh context immediately

**Use in scripts**:
```bash
python scripts/context_dashboard.py
if [ $? -eq 2 ]; then
    echo "Critical: Refresh context!"
fi
```

---

## 🎓 Best Practices

1. **Check at Start**: Always check context health at session start
2. **Check Before Major Work**: Verify context before implementing complex features
3. **Periodic Checks**: Check every 30-40 messages
4. **Act on Warnings**: Don't ignore WARNING status - refresh proactively
5. **Trust the Data**: Use dashboard metrics to make thread management decisions

---

## 🐛 Troubleshooting

### **Dashboard shows inaccurate metrics**

**Solution**: Provide actual metrics via command-line options:
```bash
python scripts/context_dashboard.py --current-usage 45000 --messages 20
```

### **Recommendations don't make sense**

**Solution**: Check if metrics are accurate. Dashboard uses estimation if actual metrics not provided.

### **Dashboard is slow**

**Solution**: Dashboard should run in <1 second. If slow, check Python environment.

---

## 📚 Related Documentation

- `docs/workflow_guide.md` - Integration with 6-phase workflow
- `docs/docflow_quickstart.md` - docFlow framework overview
- `docs/analysis/CONTEXT_DASHBOARD_VALUE_ANALYSIS.md` - Detailed value analysis
- `docs/implementation_plans/ai_context_dashboard_implementation_plan.md` - Implementation details

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-03  
**Status**: Production-Ready ✅


