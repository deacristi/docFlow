# docFlow Framework - 5-Minute Quick Start

## 🎯 What is docFlow?

**docFlow** is TradePulse's AI Context Engineering Framework - a systematic approach to human-AI collaboration that ensures high-quality, production-ready code through structured documentation, constraints, and templates.

**Core Philosophy**: Manage AI context quality through Research → Plan → Implement workflow with hard constraints and executable patterns.

---

## 🚀 For New AI Assistants

### Quick Onboarding (10 minutes)

1. **Read `initial_prompt_compressed.md`**
   - Complete project context
   - 4-step knowledge acquisition sequence
   - MCP ecosystem capabilities
   - Production-grade standards

2. **Skim `development_standards_comnpressed.md`**
   - Constraint-based guidelines
   - Executable code templates
   - Hard constraints (never violate)
   - Performance targets

3. **Review `workflow_guide.md`**
   - 6-phase development process
   - Investigation → Documentation → Solution → Planning → Implementation → Validation
   - 100% certainty requirement

4. **You're ready!** ✅

### Validation

Answer these questions to confirm readiness:
- What is the configuration-first development principle?
- What are the forbidden async/sync patterns?
- What is the Research-Plan-Implement workflow?
- Where should all numeric values be stored?

---

## 🛠️ For New Features

### Step-by-Step Process

1. **Create Feature Specification**
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

2. **Create Implementation Plan**
   ```bash
   # Copy implementation plan template
   cp docs/implementation_plans/implementation_plan_template.md \
      docs/implementation_plans/my_feature_implementation.md
   ```

3. **Follow Workflow Phases** (from `workflow_guide.md`)
   - **Phase 1**: Root Cause Investigation (if applicable)
   - **Phase 2**: Documentation
   - **Phase 3**: Solution Design
   - **Phase 4**: Implementation Planning
   - **Phase 5**: Code Implementation
   - **Phase 6**: Code Review & Validation

4. **Copy Templates** (from `development_standards_compressed.md`)
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

5. **Validate Compliance**
   ```bash
   # Run compliance checker
   python scripts/docflow_compliance_checker.py

   # Or use quick launcher
   .\scripts\check_compliance.bat  # Windows batch
   .\scripts\check_compliance.ps1  # PowerShell
   ```

6. **Generate Implementation Report**
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
| `initial_prompt.md` | AI onboarding & context | Start of every AI conversation |
| `development_standards.md` | Constraints & patterns | Before writing any code |
| `workflow_guide.md` | Development process | For every feature/fix |
| `ContextEngineering.md` | Framework philosophy | Understanding the "why" |

### Templates

| Template | Purpose | When to Use |
|----------|---------|-------------|
| `new_features/FEATURE_TEMPLATE.md` | Feature specification | New features (before implementation) |
| `implementation_plans/implementation_plan_template.md` | Implementation planning | New features (detailed plan) |
| `implementation_reports/IMPLEMENTATION_REPORT_TEMPLATE.md` | Implementation documentation | After feature completion |
| `issues/issue_root_cause_analysis_template.md` | Problem analysis | Bug fixes, issues |
| Service templates (in `development_standards_compressed.md`) | Code patterns | New services |
| Tool templates (in `development_standards_compressed.md`) | Tool creation | New tools |

### Validation Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `docflow_compliance_checker.py` | Framework compliance | Before commits |
| `check_enhanced_config_compliance.py` | Config validation | Pre-commit |
| `pre-commit-enhanced-config-check.sh` | Git hook | Automatic |

---

## 🎯 Best Practices

### 1. Always Start with Context

```bash
# AI should always read these first
1. docs/initial_prompt.md
2. docs/development_standards.md
3. docs/workflow_guide.md
```

### 2. Plan Before Implementing

```
❌ Bad: "Implement feature X"
✅ Good: "Create implementation plan for feature X" → Review → "Implement according to plan"
```

### 3. Use Templates

```
❌ Bad: Write code from scratch
✅ Good: Copy template from development_standards.md → Modify
```

### 4. Validate Continuously

```bash
# Before committing
python scripts/docflow_compliance_checker.py

# Weekly reports
python scripts/docflow_compliance_checker.py --report weekly_compliance.md
```

### 5. Capture Lessons Learned

```
Every issue → issue_root_cause_analysis_template.md → Update standards
```

---

## 🚀 Quick Reference

### Common Commands

```bash
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

- **Full Documentation**: See `scripts/README_COMPLIANCE_CHECKER.md`
- **Development Standards**: See `docs/development_standards.md`
- **Workflow Guide**: See `docs/workflow_guide.md`
- **Context Engineering**: See `docs/ContextEngineering.md`

---

## 🎓 Success Metrics

### Compliance Score Interpretation

- **90-100%**: Excellent - Framework fully adopted ✅
- **75-89%**: Good - Minor improvements needed ⚠️
- **60-74%**: Fair - Several issues to address ⚠️
- **Below 60%**: Needs attention - Review framework adoption ❌

### Framework Adoption Checklist

- [ ] All team members read `initial_prompt.md`
- [ ] All new features use `implementation_plan_template.md`
- [ ] All issues use `issue_root_cause_analysis_template.md`
- [ ] Compliance checker runs before commits
- [ ] Weekly compliance reports generated
- [ ] Standards updated with lessons learned

---

**Version**: 1.0.0
**Last Updated**: 2025-10-01
**Framework**: docFlow - AI Context Engineering Framework