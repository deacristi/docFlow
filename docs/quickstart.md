# docFlow v3.1 - Quick Start Guide

## 🎯 What is docFlow?

**docFlow** is an AI Context Engineering Framework - a systematic approach to human-AI collaboration that ensures high-quality, production-ready code through structured documentation, context management, and template-driven development.

**Core Philosophy**: Manage AI context quality through Research → Plan → Implement workflow with proactive context monitoring, automated enforcement, and safe recovery protocols.

**Version**: 3.1.0

---

## 🏗️ Architecture

### The 6 Layers

```
docFlow Framework v3.1
├── Layer 1: Philosophy (Research → Plan → Implement)
├── Layer 2: Process (6-phase workflow with gates)
├── Layer 3: Templates (Structured documentation)
├── Layer 4: Validation (Compliance checker)
├── Layer 5: Context Management (Dashboard + Steering Rules)
└── Layer 6: Recovery (Protocols + Checkpoint System)
```

**Layer 1: Philosophy**
- Research before planning
- Plan before implementing
- Validate before committing

**Layer 2: Process**
- 6-phase development workflow
- Mandatory phase gates with gate phrases
- Fast-track for simple changes

**Layer 3: Templates**
- Implementation plans
- Issue root cause analysis
- Feature specifications
- Implementation reports
- Phase gate checklist

**Layer 4: Validation**
- Compliance checker
- Automated pattern validation
- Standards enforcement

**Layer 5: Context Management**
- Real-time context health monitoring
- IDE steering rules for automatic enforcement
- Proactive context optimization

**Layer 6: Recovery**
- Recovery protocols for common failure scenarios
- Checkpoint system for safe rollback
- Living Code freshness checker

---

## 🚀 For AI Assistants

### Quick Onboarding

#### Step 1: Load Context
At the start of every session, load the project context and docFlow framework.

#### Step 2: Follow the 6-Phase Workflow
1. **Investigation**: Examine code, understand current state
2. **Documentation**: Document findings or requirements
3. **Solution Design**: Design solution following standards
4. **Implementation Planning**: Create detailed plan
5. **Code Implementation**: Write code following plan
6. **Validation**: Test and verify

#### Step 3: Use Phase Gates
Signal phase completion with gate phrases:
```
✅ Investigation complete. Proceeding to documentation.
✅ Documentation complete. Proceeding to solution design.
✅ Solution design complete. Proceeding to implementation planning.
✅ Implementation plan complete. Proceeding to code implementation.
✅ Implementation complete. Proceeding to validation.
```

#### Step 4: Fast-Track for Simple Changes
For low-risk changes (< 20 lines, single file, no API changes):
```
✅ Simple change verified. Implementing with validation.
```

---

## 🛠️ For New Features

### Step-by-Step Process

1. **Check Context Health**
   - Verify you understand the project architecture
   - Confirm you know the coding standards
   - If uncertain, reload context

2. **Create Feature Specification**
   - Use `templates/feature_documentation.md`
   - Fill out all sections
   - Get approval before proceeding

3. **Create Implementation Plan**
   - Use `templates/implementation_plan.md`
   - Define phases and tasks
   - Specify validation checkpoints

4. **Follow Workflow Phases**
   - Phase 1: Investigation
   - Phase 2: Documentation
   - Phase 3: Solution Design
   - Phase 4: Implementation Planning
   - Phase 5: Code Implementation
   - Phase 6: Validation

5. **Validate Compliance**
   - Check code follows standards
   - No magic numbers
   - Proper error handling
   - Tests written (if applicable)

---

## 🐛 For Bug Fixes

### Issue Resolution Process

1. **Create Issue Analysis**
   - Use `templates/issue_analysis.md`
   - Document root cause
   - List affected components

2. **Follow Investigation Phase**
   - Examine relevant code
   - Understand current behavior
   - Identify root cause with 100% certainty

3. **Document Root Cause**
   - Complete all template sections
   - Include lessons learned
   - Propose prevention strategies

4. **Implement Fix**
   - Follow the 6-phase workflow
   - Use fast-track if appropriate

---

## 📋 Templates

| Template | Purpose | When to Use |
|----------|---------|-------------|
| `implementation_plan.md` | Feature planning | New features |
| `issue_analysis.md` | Problem analysis | Bug fixes |
| `feature_documentation.md` | User-facing docs | After feature completion |
| `phase_gate_checklist.md` | Phase reference | During development |
| `recovery_protocols.md` | Recovery procedures | When issues occur |
| `service_template.py` | Code pattern | New services |
| `tool_template.py` | Tool creation | New AI tools |

---

## 🔧 Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `checkpoint.py` | Save/restore state | `python scripts/checkpoint.py create name "description"` |
| `check_freshness.py` | Check doc freshness | `python scripts/check_freshness.py` |

### Checkpoint Commands

```bash
# Create checkpoint before risky changes
python scripts/checkpoint.py create pre-refactor "Before major refactoring"

# List all checkpoints
python scripts/checkpoint.py list

# Restore from checkpoint
python scripts/checkpoint.py restore pre-refactor

# Clean old checkpoints (keep 5 most recent)
python scripts/checkpoint.py clean --keep 5
```

---

## 🎯 Best Practices

### 1. Always Start with Context
Load project context at the start of every session.

### 2. Monitor Context Health
Check context health every 30-40 messages. If accuracy degrades, reload context.

### 3. Plan Before Implementing
```
❌ Bad: "Implement feature X"
✅ Good: "Create implementation plan for feature X" → Review → "Implement according to plan"
```

### 4. Use Templates
Don't write from scratch - copy and modify templates.

### 5. Validate Continuously
Check compliance before committing changes.

### 6. Capture Lessons Learned
Every issue → issue analysis → update standards if needed.

---

## 📊 Success Metrics

### Context Health
- **Healthy**: Accuracy >90%, can answer architecture questions
- **Warning**: Accuracy 75-90%, some uncertainty
- **Critical**: Accuracy <75%, frequent mistakes

### Phase Compliance
- **Excellent**: All phases followed, gates passed
- **Good**: Most phases followed, fast-track used appropriately
- **Needs Improvement**: Phases skipped, no documentation

---

**Version**: 3.1.0  
**Last Updated**: December 2025
