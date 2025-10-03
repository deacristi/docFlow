# docFlow Framework v2.0 - Quick Start Guide

## 🎯 What is docFlow?

**docFlow** is an AI Context Engineering Framework - a systematic approach to human-AI collaboration that ensures high-quality, production-ready code through structured documentation, context management, and template-driven development.

**Core Philosophy**: Manage AI context quality through Research → Plan → Implement workflow with proactive context monitoring and executable patterns.

**Version**: 2.0.0 (Now includes Context Management as core pillar)

---

## 🏗️ docFlow v2.0 Architecture

### **The 5 Layers**

```
docFlow Framework v2.0
├── Layer 1: Philosophy (Research → Plan → Implement)
├── Layer 2: Process (6-phase workflow)
├── Layer 3: Templates (Structured documentation)
├── Layer 4: Validation (Compliance checker)
└── Layer 5: Context Management (Dashboard + Best Practices) ← NEW in v2.0
```

**Layer 1: Philosophy**
- Research before planning
- Plan before implementing
- Validate before committing

**Layer 2: Process**
- 6-phase development workflow
- Structured investigation and documentation
- Systematic implementation and validation

**Layer 3: Templates**
- Implementation plans
- Issue root cause analysis
- Feature specifications
- Implementation reports

**Layer 4: Validation**
- Compliance checker
- Automated pattern validation
- Standards enforcement

**Layer 5: Context Management** ⭐ NEW
- Real-time context health monitoring
- Proactive context optimization
- Data-driven thread management
- Accuracy and efficiency tracking

---

## 🚀 For New AI Assistants

### Quick Onboarding (10 minutes)

1. **Load Context**
   ```
   Load context from @docs/ai_context/MASTER_CONTEXT_LOADER.md
   ```
   - Complete project context
   - docFlow framework
   - Development standards
   - Templates and workflow

2. **Check Context Health**
   ```bash
   python scripts/context_dashboard.py
   ```
   - Verify context is healthy (usage <30%)
   - Accuracy score >95%
   - All documentation fresh

3. **Review `workflow_guide.md`**
   - 6-phase development process
   - Context health checkpoints
   - Investigation → Documentation → Solution → Planning → Implementation → Validation

4. **You're ready!** ✅

### Validation

Answer these questions to confirm readiness:
- What is the configuration-first development principle?
- What are the 5 layers of docFlow v2.0?
- When should you check context health?
- What is the Research-Plan-Implement workflow?
- Where should all numeric values be stored?

---

## 🛠️ For New Features

### Step-by-Step Process (with Context Management)

1. **Check Context Health** ⭐ NEW
   ```bash
   python scripts/context_dashboard.py
   ```
   - Verify context is healthy before starting
   - Accuracy >90%, Usage <70%
   - If not healthy, refresh context first

2. **Create Feature Specification**
   ```bash
   # Copy feature template
   cp docs/new_features/FEATURE_TEMPLATE.md \
      docs/new_features/my_feature_spec.md
   ```

   **Fill out all sections:**
   - Problem statement and solution
   - Requirements (functional and non-functional)
   - Technical design (architecture, data model, API)
   - Implementation plan (phases and tasks)
   - Testing strategy
   - Deployment plan

3. **Create Implementation Plan**
   ```bash
   # Copy implementation plan template
   cp docs/implementation_plans/implementation_plan_template.md \
      docs/implementation_plans/my_feature_implementation.md
   ```

4. **Follow Workflow Phases** (from `workflow_guide.md`)
   - **Phase 1**: Context Health Check + Root Cause Investigation
   - **Phase 2**: Documentation
   - **Phase 3**: Solution Design
   - **Phase 4**: Implementation Planning
   - **Phase 5**: Code Implementation (monitor context)
   - **Phase 6**: Code Review & Validation

5. **Copy Templates** (from `development_standards.md`)
   ```python
   # Example: Async database operation
   async def async_database_operation():
       async with get_db() as session:
           try:
               result = session.query(Model).filter(Model.id == 1).first()
               session.commit()
               return result
           except Exception as e:
               session.rollback()
               raise e
   ```

6. **Monitor Context During Implementation** ⭐ NEW
   ```bash
   # Check context health every 30-40 messages
   python scripts/context_dashboard.py

   # If usage >70% or accuracy <85%, consider:
   # - Starting new thread
   # - Refreshing context
   # - Removing low-value content
   ```

7. **Validate Compliance**
   ```bash
   # Run compliance checker
   python scripts/docflow_compliance_checker.py

   # Or use quick launcher
   .\scripts\check_compliance.bat  # Windows batch
   .\scripts\check_compliance.ps1  # PowerShell
   ```

8. **Generate Implementation Report**
   ```bash
   # Copy implementation report template
   cp docs/implementation_reports/IMPLEMENTATION_REPORT_TEMPLATE.md \
      docs/implementation_reports/my_feature_report.md
   ```

   **Document:**
   - What was implemented
   - Requirements fulfillment
   - Testing results
   - Quality metrics
   - Issues and resolutions
   - Lessons learned

---

## 🐛 For Bug Fixes

### Issue Resolution Process

1. **Create Issue Analysis**
   ```bash
   # Copy template
   cp docs/issues/issue_root_cause_analysis_template.md \
      docs/issues/my_issue_analysis.md
   ```

2. **Follow Investigation Phase** (from `workflow_guide.md`)
   - Thorough analysis using codebase-retrieval
   - Context refresh from initial_prompt.md
   - MCP tool utilization
   - 100% certainty requirement

3. **Document Root Cause**
   - Complete all template sections
   - Include development standards compliance analysis
   - Add lessons learned
   - Propose prevention strategies

4. **Update Standards**
   - Add new constraints to `development_standards.md`
   - Update templates if needed
   - Add validation scripts

5. **Validate Fix**
   ```bash
   # Run compliance checker
   python scripts/docflow_compliance_checker.py
   ```

---

## 🔍 Compliance Checker

### Quick Usage

```bash
# Basic check
python scripts/docflow_compliance_checker.py

# Generate detailed report
python scripts/docflow_compliance_checker.py --report compliance_report.md

# Windows shortcuts
.\scripts\check_compliance.bat
.\scripts\check_compliance.ps1
```

### What It Checks

- ✅ **Documentation Structure**: All required docs exist
- ✅ **Implementation Plans**: Follow template structure
- ✅ **Issue Analyses**: Complete root cause analysis
- ✅ **Code Standards**: No forbidden patterns
- ✅ **Import Patterns**: Proper absolute imports
- ✅ **Async/Sync Patterns**: Correct database patterns
- ✅ **Configuration**: No magic numbers
- ✅ **Template Usage**: BaseTool pattern, service pattern
- ✅ **Testing**: Test coverage requirements

### Severity Levels

- **❌ CRITICAL**: Must fix before committing
- **⚠️ WARNING**: Should fix soon
- **ℹ️ INFO**: Consider addressing

### Example Output

```
🔍 Running docFlow Framework Compliance Checks...
============================================================

📚 Checking Documentation Structure...
  ✅ AI onboarding documentation
  ✅ Development standards
  ✅ Workflow guide

💻 Checking Code Standards...
  ❌ app/services/example.py:23 - enhanced_config usage
  ⚠️  app/tools/custom_tool.py - Not using BaseTool pattern

============================================================
📊 COMPLIANCE SUMMARY
============================================================
Files Checked: 45
Compliance Score: 87.5%
✅ Passed: 35
❌ Critical: 1
⚠️  Warnings: 3
ℹ️  Info: 6
```

---

## 📋 Framework Components

### Core Documentation

| File | Purpose | When to Use |
|------|---------|-------------|
| `ai_context/MASTER_CONTEXT_LOADER.md` | AI onboarding & context | Start of every AI conversation |
| `development_standards.md` | Constraints & patterns | Before writing any code |
| `workflow_guide.md` | Development process | For every feature/fix |
| `ContextEngineering.md` | Framework philosophy | Understanding the "why" |
| `tools/context_dashboard_guide.md` | Context management | When monitoring context health |

### Templates

| Template | Purpose | When to Use |
|----------|---------|-------------|
| `templates/feature_specification_template.md` | Feature specification | New features (before implementation) |
| `templates/implementation_plan_template.md` | Implementation planning | New features (detailed plan) |
| `templates/implementation_report_template.md` | Implementation documentation | After feature completion |
| `templates/issue_root_cause_analysis_template.md` | Problem analysis | Bug fixes, issues |
| Service templates (in `development_standards.md`) | Code patterns | New services |
| Tool templates (in `development_standards.md`) | Tool creation | New tools |

### Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `context_dashboard.py` ⭐ NEW | Context health monitoring | Start of session, every 30-40 messages |
| `docflow_compliance_checker.py` | Framework compliance | Before commits |
| `check_enhanced_config_compliance.py` | Config validation | Pre-commit |
| `pre-commit-enhanced-config-check.sh` | Git hook | Automatic |

---

## 🎯 Best Practices

### 1. Always Start with Context ⭐ UPDATED

```bash
# AI should always load context first
Load context from @docs/ai_context/MASTER_CONTEXT_LOADER.md

# Then verify context health
python scripts/context_dashboard.py
```

**Expected State**:
- Context usage <30%
- Accuracy score >95%
- Documentation freshness >90%

### 2. Monitor Context Health ⭐ NEW

```bash
# Check context health:
# - At session start
# - Before major implementations
# - Every 30-40 messages
# - When AI makes unexpected mistakes

python scripts/context_dashboard.py

# If usage >70% or accuracy <85%:
# → Start new thread
# → Refresh context
# → Remove low-value content
```

### 3. Plan Before Implementing

```
❌ Bad: "Implement feature X"
✅ Good: "Create implementation plan for feature X" → Review → "Implement according to plan"
```

### 4. Use Templates

```
❌ Bad: Write code from scratch
✅ Good: Copy template from development_standards.md → Modify
```

### 5. Validate Continuously

```bash
# Before committing
python scripts/docflow_compliance_checker.py

# Weekly reports
python scripts/docflow_compliance_checker.py --report weekly_compliance.md
```

### 6. Capture Lessons Learned

```
Every issue → issue_root_cause_analysis_template.md → Update standards
```

---

## 🚀 Quick Reference

### Common Commands

```bash
# Check context health ⭐ NEW
python scripts/context_dashboard.py

# Check compliance
python scripts/docflow_compliance_checker.py

# Generate report
python scripts/docflow_compliance_checker.py --report report.md

# Run tests
.\venv\Scripts\activate
pytest tests/

# Start development environment
.\start_development.bat
```

### Context Management Commands ⭐ NEW

```bash
# Basic dashboard
python scripts/context_dashboard.py

# With specific metrics
python scripts/context_dashboard.py --current-usage 45000 --messages 20

# Full session info
python scripts/context_dashboard.py \
    --current-usage 45000 \
    --messages 20 \
    --files-viewed 12 \
    --files-modified 2
```

### Common Patterns

```python
# Configuration-first
from app.core.config import settings
timeout = settings.api_timeout  # ✅ Not: timeout = 30

# Async database
async with get_db() as session:  # ✅ Correct
    pass

# Sync database (FastAPI)
def endpoint(db: Session = Depends(get_db_session)):  # ✅ Correct
    pass

# Tool pattern
class MyTool(TradePulseLangchainTool):  # ✅ Correct
    name: str = "my_tool"
```

---

## 📚 Additional Resources

### **Core Documentation**
- **Context Loader**: `docs/ai_context/MASTER_CONTEXT_LOADER.md`
- **Development Standards**: `docs/development_standards.md`
- **Workflow Guide**: `docs/workflow_guide.md`
- **Context Engineering**: `docs/ContextEngineering.md`

### **Context Management** ⭐ NEW
- **Dashboard Guide**: `docs/tools/context_dashboard_guide.md`
- **Value Analysis**: `docs/analysis/CONTEXT_DASHBOARD_VALUE_ANALYSIS.md`
- **Alignment Analysis**: `docs/analysis/DOCFLOW_CONTEXT_ENGINEERING_ALIGNMENT.md`

### **Tools**
- **Compliance Checker**: `scripts/README_COMPLIANCE_CHECKER.md`
- **Context Dashboard**: `scripts/context_dashboard/README.md`

---

## 🎓 Success Metrics

### Compliance Score Interpretation

- **90-100%**: Excellent - Framework fully adopted ✅
- **75-89%**: Good - Minor improvements needed ⚠️
- **60-74%**: Fair - Several issues to address ⚠️
- **Below 60%**: Needs attention - Review framework adoption ❌

### Framework Adoption Checklist

- [ ] All team members load `MASTER_CONTEXT_LOADER.md` at session start
- [ ] Context dashboard checked at session start
- [ ] All new features use `implementation_plan_template.md`
- [ ] All issues use `issue_root_cause_analysis_template.md`
- [ ] Context health monitored every 30-40 messages
- [ ] Compliance checker runs before commits
- [ ] Weekly compliance reports generated
- [ ] Standards updated with lessons learned

---

## 🆕 What's New in v2.0

### **Layer 5: Context Management**

**New Features**:
- ✅ Real-time context health monitoring
- ✅ Token usage breakdown by category
- ✅ Accuracy and efficiency scoring
- ✅ Eviction queue preview
- ✅ Actionable recommendations
- ✅ Session statistics tracking

**Benefits**:
- ✅ 90-180 min/week time savings
- ✅ 67% reduction in code revisions
- ✅ 95%+ accuracy maintained
- ✅ 2-3x longer context lifespan
- ✅ Proactive context optimization

**How to Use**:
```bash
# Check context health
python scripts/context_dashboard.py

# See detailed guide
cat docs/tools/context_dashboard_guide.md
```

---

**Version**: 2.0.0
**Last Updated**: 2025-10-03
**Framework**: docFlow - AI Context Engineering Framework + Context Management