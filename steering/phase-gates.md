---
inclusion: always
---

# docFlow v3.1 - Phase Gate Enforcement

> This steering rule enforces the 6-phase development workflow with mandatory gate checks.

## 🚦 Phase Gate System

### Gate 1: Investigation → Documentation
Before proceeding to documentation, confirm:
- [ ] Examined ALL relevant files
- [ ] Checked current state documentation
- [ ] Identified all affected components
- [ ] Have 100% certainty about root cause/requirements

**Gate Phrase**: "✅ Investigation complete. Proceeding to documentation."

### Gate 2: Documentation → Solution Design
Before proceeding to solution design, confirm:
- [ ] Created/updated issue analysis OR feature specification
- [ ] Documented current state vs desired state
- [ ] Listed all constraints and requirements

**Gate Phrase**: "✅ Documentation complete. Proceeding to solution design."

### Gate 3: Solution Design → Implementation Planning
Before proceeding to implementation planning, confirm:
- [ ] Solution follows project standards
- [ ] No forbidden patterns in proposed solution
- [ ] Backward compatibility verified
- [ ] Dependencies identified

**Gate Phrase**: "✅ Solution design complete. Proceeding to implementation planning."

### Gate 4: Implementation Planning → Code Implementation
Before proceeding to code implementation, confirm:
- [ ] Implementation plan created (or simple change documented)
- [ ] Validation checkpoints defined
- [ ] Rollback procedure known (git revert)
- [ ] Success criteria specified

**Gate Phrase**: "✅ Implementation plan complete. Proceeding to code implementation."

### Gate 5: Code Implementation → Validation
Before declaring complete, confirm:
- [ ] All code follows templates and patterns
- [ ] No magic numbers (all in config)
- [ ] Proper error handling with specific exceptions
- [ ] Tests written (if applicable)

**Gate Phrase**: "✅ Implementation complete. Proceeding to validation."

## ⚡ Fast-Track for Simple Changes

For simple, low-risk changes (< 20 lines, single file, no API changes):
- Gates 1-4 can be combined into a single verification
- Still require Gate 5 validation

**Fast-Track Phrase**: "✅ Simple change verified. Implementing with validation."

## 🛑 Gate Violation Response

If asked to skip phases or implement without investigation:
1. Acknowledge the request
2. Explain the risk briefly
3. Offer fast-track if appropriate
4. Proceed only with user confirmation

Example: "I can implement this quickly, but let me first verify the current implementation to avoid breaking changes. This will take 30 seconds."
