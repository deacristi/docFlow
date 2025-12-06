# docFlow v3.1 - Workflow Guide

> The 6-phase development workflow for AI-assisted development with mandatory gate checks.

---

## Overview

docFlow enforces a structured approach to development that ensures quality, traceability, and maintainability. Each phase has specific deliverables and gate checks before proceeding.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Investigation  │───▶│  Documentation  │───▶│ Solution Design │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
┌─────────────────┐    ┌─────────────────┐           │
│   Validation    │◀───│ Implementation  │◀──────────┘
└─────────────────┘    └─────────────────┘
                              ▲
                              │
                    ┌─────────────────┐
                    │Implementation   │
                    │   Planning      │
                    └─────────────────┘
```

---

## Phase 1: Root Cause Investigation

### Objective
Achieve 100% certainty about the problem or requirements before proceeding.

### Activities
1. **Context Health Check**: Verify AI context is healthy and up-to-date
2. **Thorough Analysis**: Use codebase-retrieval tools to examine ALL relevant files
3. **Context Refresh**: Review project architecture and development standards
4. **Tool Utilization**: Leverage available tools (filesystem, database, etc.) to gather comprehensive information

### Deliverables
- [ ] List of all affected files identified
- [ ] Root cause or requirements clearly understood
- [ ] Current state documented

### Gate Check
**Gate Phrase**: "✅ Investigation complete. Proceeding to documentation."

Before proceeding, confirm:
- Used codebase-retrieval to examine ALL relevant files
- Checked Living Code Context for current state
- Identified all affected components
- Have 100% certainty about root cause/requirements

---

## Phase 2: Documentation

### Objective
Create comprehensive documentation of the issue or feature before designing a solution.

### Activities
1. **Issue Analysis**: Create a root cause analysis document (for bugs)
2. **Feature Specification**: Create a feature specification (for new features)
3. **State Documentation**: Document current state vs desired state

### Deliverables
- [ ] Issue analysis OR feature specification document created
- [ ] Current state vs desired state documented
- [ ] All constraints and requirements listed

### Templates
- `templates/issue_analysis.md` - For bug fixes and issues
- `templates/feature_documentation.md` - For new features

### Gate Check
**Gate Phrase**: "✅ Documentation complete. Proceeding to solution design."

---

## Phase 3: Solution Design

### Objective
Design a solution that follows established patterns and standards.

### Activities
1. **Standards Review**: Analyze development standards to ensure compliance
2. **Pattern Selection**: Choose appropriate design patterns
3. **Dependency Analysis**: Identify all dependencies and impacts
4. **Backward Compatibility**: Verify no breaking changes

### Deliverables
- [ ] Solution design documented
- [ ] Standards compliance verified
- [ ] Dependencies identified
- [ ] Backward compatibility confirmed

### Gate Check
**Gate Phrase**: "✅ Solution design complete. Proceeding to implementation planning."

Before proceeding, confirm:
- Solution follows development standards
- No forbidden patterns in proposed solution
- Backward compatibility verified
- Dependencies identified

---

## Phase 4: Implementation Planning

### Objective
Create a detailed plan with testing strategy, rollback procedures, and verification steps.

### Activities
1. **Implementation Plan**: Create detailed step-by-step plan
2. **Testing Strategy**: Define what tests will be written
3. **Rollback Procedure**: Document how to revert if needed
4. **Success Criteria**: Define measurable success criteria

### Deliverables
- [ ] Implementation plan document created
- [ ] Testing strategy defined
- [ ] Rollback procedure documented
- [ ] Success criteria specified

### Templates
- `templates/implementation_plan.md` - Implementation plan template

### Gate Check
**Gate Phrase**: "✅ Implementation plan complete. Proceeding to code implementation."

---

## Phase 5: Code Implementation

### Objective
Write production-grade code that follows the implementation plan.

### Activities
1. **Code Development**: Write code following the plan
2. **Testing**: Implement unit tests, integration tests
3. **Documentation**: Update relevant documentation
4. **Code Review**: Self-review against standards

### Deliverables
- [ ] Code implemented following plan
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No magic numbers (all in config)
- [ ] Proper error handling

### Gate Check
**Gate Phrase**: "✅ Implementation complete. Proceeding to validation."

Before proceeding, confirm:
- All code follows templates and patterns
- No magic numbers (all in config)
- Proper error handling with specific exceptions
- Tests written (if applicable)

---

## Phase 6: Validation

### Objective
Verify the solution meets all requirements and quality standards.

### Activities
1. **Code Review**: Review against checklist
2. **Testing**: Run all tests
3. **Integration Testing**: Verify integration with existing code
4. **Documentation Review**: Ensure docs are complete

### Deliverables
- [ ] All tests passing
- [ ] Code review completed
- [ ] Integration verified
- [ ] Documentation complete

### Completion
**Completion Phrase**: "✅ Validation complete. Task finished."

---

## Fast-Track for Simple Changes

For simple, low-risk changes (< 20 lines, single file, no API changes):

**Criteria:**
- Less than 20 lines of code
- Single file modification
- No API changes
- No database schema changes
- No configuration changes

**Process:**
- Gates 1-4 can be combined into a single verification
- Still require Gate 5 validation

**Fast-Track Phrase**: "✅ Simple change verified. Implementing with validation."

---

## Gate Violation Response

If asked to skip phases or implement without investigation:

1. **Acknowledge** the request
2. **Explain** the risk briefly
3. **Offer** fast-track if appropriate
4. **Proceed** only with user confirmation

**Example Response:**
> "I can implement this quickly, but let me first verify the current implementation to avoid breaking changes. This will take 30 seconds."

---

## Quality Standards

Throughout all phases, maintain these standards:

- **100% Certainty**: Only proceed if you have complete understanding
- **Production-Grade**: Write code that adds real value
- **Backward Compatible**: Ensure all changes maintain system stability
- **Tested**: Test thoroughly before declaring success
- **Documented**: Keep documentation up-to-date

---

## Checkpoint System

Use checkpoints to save progress and enable recovery:

```bash
# Create checkpoint before major changes
python scripts/checkpoint.py create "Before implementing feature X"

# List available checkpoints
python scripts/checkpoint.py list

# Restore if needed
python scripts/checkpoint.py restore <checkpoint_id>
```

See `templates/recovery_protocols.md` for detailed recovery procedures.
