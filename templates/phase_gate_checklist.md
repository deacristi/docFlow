# docFlow v3.1 - Phase Gate Checklist

**Version**: 3.1.0  
**Purpose**: Enforce systematic development workflow with mandatory checkpoints

---

## Overview

This checklist ensures every change follows the Research → Plan → Implement workflow. Use this for complex features; simple changes can use the fast-track process.

---

## Phase 1: Investigation

### Checklist
- [ ] Loaded project context
- [ ] Examined all relevant files
- [ ] Identified all affected components
- [ ] Verified 100% certainty about requirements

### Deliverables
- Understanding of current implementation
- List of affected files/components
- Clear problem statement or requirements

### Gate Phrase
```
✅ Investigation complete. Findings:
- Current implementation: [summary]
- Affected components: [list]
- Root cause/Requirements: [description]
Proceeding to documentation.
```

---

## Phase 2: Documentation

### Checklist
- [ ] Created issue analysis (for bugs) OR feature specification (for features)
- [ ] Documented current state vs desired state
- [ ] Listed all constraints and requirements
- [ ] Identified potential risks

### Deliverables
- Issue analysis document (bugs) OR
- Feature specification (features) OR
- Inline documentation (simple changes)

### Gate Phrase
```
✅ Documentation complete.
- Document: [path or inline summary]
- Key constraints: [list]
Proceeding to solution design.
```

---

## Phase 3: Solution Design

### Checklist
- [ ] Solution follows project standards
- [ ] No forbidden patterns in proposed solution
- [ ] Backward compatibility verified
- [ ] Dependencies identified
- [ ] Performance impact considered

### Deliverables
- Technical approach description
- Code patterns to use
- Integration points identified

### Gate Phrase
```
✅ Solution design complete.
- Approach: [summary]
- Patterns: [list]
- Dependencies: [list]
Proceeding to implementation planning.
```

---

## Phase 4: Implementation Planning

### Checklist
- [ ] Implementation steps defined
- [ ] Validation checkpoints identified
- [ ] Rollback procedure documented
- [ ] Success criteria specified
- [ ] Estimated effort noted

### Deliverables
- Step-by-step implementation plan
- Test scenarios
- Success criteria

### Gate Phrase
```
✅ Implementation plan complete.
- Steps: [count]
- Validation: [approach]
- Success criteria: [list]
Proceeding to code implementation.
```

---

## Phase 5: Code Implementation

### Checklist
- [ ] Code follows templates and patterns
- [ ] No magic numbers (all values in config)
- [ ] Proper error handling with specific exceptions
- [ ] Type hints included
- [ ] Logging added where appropriate
- [ ] Tests written (if applicable)

### Deliverables
- Working code changes
- Updated tests (if applicable)
- Updated documentation (if applicable)

### Gate Phrase
```
✅ Implementation complete.
- Files modified: [list]
- Tests: [status]
Proceeding to validation.
```

---

## Phase 6: Validation

### Checklist
- [ ] Code compiles/runs without errors
- [ ] Tests pass (if applicable)
- [ ] Manual verification completed
- [ ] No regressions in existing functionality
- [ ] Documentation updated

### Deliverables
- Validation results
- Any issues found and resolved

### Completion Phrase
```
✅ Validation complete.
- Status: [PASS/FAIL]
- Results: [summary]
```

---

## Fast-Track Process

For simple, low-risk changes (< 20 lines, single file, no API changes):

### Combined Checklist
- [ ] Verified current implementation
- [ ] Change is backward compatible
- [ ] No forbidden patterns
- [ ] Success criteria clear

### Fast-Track Phrase
```
✅ Simple change verified (fast-track).
- Current state: [summary]
- Change: [description]
- Risk: Low
Implementing with validation.
```

---

## Examples

### Example 1: Bug Fix (Full Process)
```
✅ Investigation complete. Findings:
- Current implementation: Service generates events during off-hours
- Affected components: EventService class
- Root cause: No time filter
Proceeding to documentation.

✅ Documentation complete.
- Document: Inline (simple fix)
- Key constraints: Must not break existing logic
Proceeding to solution design.

✅ Solution design complete.
- Approach: Add time check before processing
- Patterns: Use existing time utilities
- Dependencies: time_utils module
Proceeding to implementation planning.

✅ Implementation plan complete.
- Steps: 3 (add import, add function, add check)
- Validation: Manual test
- Success criteria: No events generated off-hours
Proceeding to code implementation.

✅ Implementation complete.
- Files modified: services/event_service.py
- Tests: Manual verification
Proceeding to validation.

✅ Validation complete.
- Status: PASS
- Results: Events now filtered correctly
```

### Example 2: Simple Change (Fast-Track)
```
✅ Simple change verified (fast-track).
- Current state: Logging level set to DEBUG
- Change: Update to INFO for production
- Risk: Low
Implementing with validation.

✅ Validation complete.
- Status: PASS
- Results: Log level updated, verified in output
```

---

**Version**: 3.1.0  
**Last Updated**: December 2025
