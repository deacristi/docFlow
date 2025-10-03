# Master AI Context Loader - docFlow Framework

**Single Entry Point for Complete AI Context**

Version: 2.0.0  
Last Updated: 2025-10-03  
Purpose: Load complete, accurate context for AI assistants in one step

---

## 🎯 QUICK START

**Copy this into every new AI thread**:

```
Load context from @docs/ai_context/MASTER_CONTEXT_LOADER.md
```

**AI will automatically load**:
1. ✅ docFlow framework (context management system)
2. ✅ Project architecture and standards
3. ✅ Development workflow and patterns
4. ✅ Current project state
5. ✅ Active tasks and priorities

---

## 📚 LAYER 1: FRAMEWORK CONTEXT (Read First)

### **docFlow Framework** - AI Context Engineering System

**Primary Document**:
@docs/docflow_quickstart.md

**What You'll Learn**:
- docFlow philosophy: Research → Plan → Implement
- 6-phase development process
- Template-driven development
- Compliance validation
- Context management best practices

**Key Takeaways**:
- ✅ Always start with context loading
- ✅ Always plan before implementing
- ✅ Always use templates from standards
- ✅ Always validate with compliance checker
- ✅ Always document lessons learned

---

## 📚 LAYER 2: PROJECT CONTEXT (Core Knowledge)

### **2.1 Complete Project Context**

**Primary Document**:
@docs/ai_context/LOAD_CONTEXT.md

**What You'll Learn**:
- Project vision and architecture
- Technology stack
- Current implementation status
- Active features and priorities

**Customize This**: Update LOAD_CONTEXT.md with your project details

### **2.2 Development Standards**

**Primary Document**:
@docs/development_standards.md

**What You'll Learn**:
- Configuration-first development principle
- Project-specific patterns (REQUIRED)
- Code templates (copy-paste ready)
- Forbidden patterns (NEVER use)
- Required patterns (ALWAYS use)

**Customize This**: Replace with your tech stack patterns

### **2.3 Workflow Process**

**Primary Document**:
@docs/workflow_guide.md

**What You'll Learn**:
- 6-phase development workflow
- Phase 1: Root Cause Investigation
- Phase 2: Documentation
- Phase 3: Solution Design
- Phase 4: Implementation Planning
- Phase 5: Code Implementation
- Phase 6: Code Review & Validation

**Key Principle**: Research → Plan → Implement (never skip phases)

---

## 📚 LAYER 3: TEMPLATES (Tools for Execution)

### **3.1 Implementation Plan Template**

**Document**: @docs/templates/implementation_plan_template.md

**When to Use**: Before implementing any feature or fix

**Purpose**: Create detailed, reviewable implementation plan

**Key Sections**:
- Overview & objectives
- Architecture (for senior engineers)
- Architecture (for junior engineers)
- Implementation phases
- Testing strategy
- Success criteria

### **3.2 Issue Root Cause Analysis Template**

**Document**: @docs/templates/issue_root_cause_analysis_template.md

**When to Use**: When investigating bugs or issues

**Purpose**: Systematic root cause investigation

**Key Sections**:
- Issue description
- Investigation findings
- Root cause analysis
- Proposed solution
- Prevention measures

### **3.3 Feature Specification Template**

**Document**: @docs/templates/feature_specification_template.md

**When to Use**: When planning new features

**Purpose**: Complete feature specification

**Key Sections**:
- Feature overview
- User stories
- Technical requirements
- API specifications
- UI/UX requirements

### **3.4 Implementation Report Template**

**Document**: @docs/templates/implementation_report_template.md

**When to Use**: After completing any implementation

**Purpose**: Document what was built and lessons learned

**Key Sections**:
- Executive summary
- Requirements fulfillment
- Implementation details
- Testing results
- Lessons learned

---

## 📚 LAYER 4: CONTEXT MANAGEMENT (Quality Assurance)

### **4.1 Context Dashboard**

**Tool**: `python scripts/context_dashboard.py`

**Usage Guide**: @docs/tools/context_dashboard_guide.md

**When to Use**:
- ✅ Start of every development session
- ✅ Before major implementations
- ✅ Every 30-40 messages
- ✅ When AI makes unexpected mistakes

**What It Shows**:
- Context health status (HEALTHY/WARNING/CRITICAL)
- Token usage breakdown
- Accuracy metrics (freshness, consistency, retention)
- Efficiency metrics
- Recommendations for optimization

**Key Metrics**:
- **Context Usage**: Keep <40% (ideally <30%)
- **Accuracy Score**: Maintain >90%
- **Documentation Freshness**: Keep >85%
- **Efficiency Score**: Target >0.7

### **4.2 Context Best Practices**

**DO**:
- ✅ Check context health at session start
- ✅ Refresh context when accuracy <90%
- ✅ Start new thread when usage >70%
- ✅ Use templates for consistency
- ✅ Keep plans concise (<5,000 tokens)

**DON'T**:
- ❌ Let context usage exceed 70%
- ❌ Continue when accuracy <85%
- ❌ Load unnecessary documentation
- ❌ Repeat information already in context
- ❌ Ignore dashboard warnings

---

## 📚 LAYER 5: CONFIGURATION (Single Source of Truth)

### **Configuration File**

**Document**: @config_specification.yaml

**Purpose**: All numeric values, URLs, settings in one place

**Key Principle**: NO MAGIC NUMBERS IN CODE

**What's Configured**:
- Project metadata
- Environment settings
- API endpoints
- Database connections
- Context dashboard thresholds
- All numeric constants

**Usage**:
```python
from app.core.config import settings

# Correct
max_retries = settings.api_max_retries

# Wrong
max_retries = 3  # Magic number!
```

---

## 🎯 LOADING CHECKLIST

When starting a new AI session, verify:

- [ ] Loaded MASTER_CONTEXT_LOADER.md
- [ ] AI confirmed understanding of docFlow framework
- [ ] AI confirmed understanding of project context
- [ ] AI confirmed understanding of development standards
- [ ] Ran context dashboard to verify health
- [ ] Context usage <30% at start
- [ ] Accuracy score >95% at start

**If any item fails**: Refresh context before proceeding

---

## 🔄 CONTEXT REFRESH TRIGGERS

**Refresh context when**:
- ⚠️ Accuracy score <90%
- ⚠️ Documentation freshness <85%
- ⚠️ AI violates development standards
- ⚠️ AI makes unexpected mistakes
- ⚠️ Context usage >70%
- ⚠️ Session >50 messages

**How to Refresh**:
1. Save current state
2. Start new thread
3. Load MASTER_CONTEXT_LOADER.md
4. Resume work

---

## 📊 CONTEXT LAYERS SUMMARY

```
Layer 1: Framework (docFlow)           [PERMANENT - Never remove]
Layer 2: Project Context               [HIGH - Keep fresh]
Layer 3: Templates                     [MEDIUM - Load as needed]
Layer 4: Context Management            [HIGH - Monitor continuously]
Layer 5: Configuration                 [HIGH - Single source of truth]
```

**Total Context Budget**: 200,000 tokens (Claude Sonnet 4.5)  
**Target Usage**: <40% (<80,000 tokens)  
**Optimal Usage**: <30% (<60,000 tokens)

---

## 🎓 LEARNING PATH

### **First Time Using docFlow**

1. Read `docs/docflow_quickstart.md` (10 minutes)
2. Read `docs/workflow_guide.md` (15 minutes)
3. Skim `docs/development_standards.md` (5 minutes)
4. Run `python scripts/context_dashboard.py` (1 minute)
5. Start first feature following workflow (hands-on learning)

### **Experienced with docFlow**

1. Load MASTER_CONTEXT_LOADER.md
2. Run context dashboard
3. Proceed with work

---

## 🚨 CRITICAL REMINDERS

### **For AI Assistants**

1. **ALWAYS** check context health before major work
2. **ALWAYS** follow development_standards.md patterns
3. **ALWAYS** use templates for plans and reports
4. **ALWAYS** validate with compliance checker
5. **NEVER** use magic numbers (use config)
6. **NEVER** skip phases in workflow
7. **NEVER** implement without a plan
8. **NEVER** ignore context dashboard warnings

### **For Human Developers**

1. **ALWAYS** load this file at session start
2. **ALWAYS** review plans before implementation
3. **ALWAYS** check context dashboard periodically
4. **ALWAYS** refresh context when warned
5. **NEVER** let AI implement without a plan
6. **NEVER** ignore accuracy warnings
7. **NEVER** continue when context >70%

---

## 📞 TROUBLESHOOTING

### **AI not following standards**

**Solution**: 
1. Run `python scripts/context_dashboard.py`
2. Check documentation freshness
3. If <85%, reload MASTER_CONTEXT_LOADER.md

### **AI making mistakes**

**Solution**:
1. Run context dashboard
2. Check accuracy score
3. If <90%, refresh context
4. Review if plan was detailed enough

### **Context usage too high**

**Solution**:
1. Run dashboard to see breakdown
2. Remove low-value content
3. Start new thread if >70%

---

## ✅ SUCCESS CRITERIA

You'll know context is properly loaded when:

1. ✅ AI follows all development standards
2. ✅ AI uses templates consistently
3. ✅ AI validates before implementing
4. ✅ Context usage <30%
5. ✅ Accuracy score >95%
6. ✅ No magic numbers in code
7. ✅ Plans are detailed and reviewable

---

## 🎯 NEXT STEPS

After loading this context:

1. **Verify**: Run `python scripts/context_dashboard.py`
2. **Confirm**: AI understands project and standards
3. **Proceed**: Follow workflow_guide.md for your task
4. **Monitor**: Check context health every 30-40 messages
5. **Document**: Use templates for all deliverables

---

**Remember**: Quality AI output = Quality AI input

**The docFlow framework ensures quality input every time.** ✅

---

**Version**: 2.0.0  
**Framework**: docFlow + Context Management  
**Status**: ✅ Production-Ready

