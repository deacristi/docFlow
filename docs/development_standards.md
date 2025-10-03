# Development Standards - [YOUR PROJECT NAME]

**Production-Grade Development Standards**

Version: 1.0.0  
Last Updated: [DATE]  
Purpose: Define coding standards, patterns, and best practices

---

## 🎯 CORE PRINCIPLES

### **1. Configuration-First Development**

**Principle**: ALL numeric values, URLs, and settings MUST be in `config_specification.yaml`

**✅ CORRECT**:
```[language]
from config import settings

max_retries = settings.api_max_retries
timeout = settings.api_timeout_seconds
```

**❌ WRONG**:
```[language]
max_retries = 3  # Magic number!
timeout = 30     # Magic number!
```

**Why**: Maintainability, flexibility, single source of truth

---

### **2. Production-Grade Code Only**

**Requirements**:
- ✅ No mock data
- ✅ No TODO comments
- ✅ No placeholder implementations
- ✅ No commented-out code
- ✅ Complete error handling
- ✅ Proper logging
- ✅ Type hints/annotations

**If code isn't production-ready, don't commit it.**

---

### **3. Template-Driven Development**

**Principle**: Use templates for all plans, reports, and documentation

**Templates Available**:
- `docs/templates/implementation_plan_template.md`
- `docs/templates/issue_root_cause_analysis_template.md`
- `docs/templates/feature_specification_template.md`
- `docs/templates/implementation_report_template.md`

**Why**: Consistency, completeness, efficiency

---

## 🏗️ PROJECT-SPECIFIC PATTERNS

### **Pattern 1: [Your Pattern Name]**

**When to Use**: [Describe when this pattern applies]

**Template**:
```[language]
# Your pattern code template here
# Include comments explaining each part
```

**Example**:
```[language]
# Real-world example of the pattern
```

**Why**: [Explain the reasoning behind this pattern]

---

### **Pattern 2: [Your Pattern Name]**

**When to Use**: [Describe when this pattern applies]

**Template**:
```[language]
# Your pattern code template here
```

**Example**:
```[language]
# Real-world example
```

**Why**: [Explain the reasoning]

---

### **Pattern 3: [Your Pattern Name]**

**When to Use**: [Describe when this pattern applies]

**Template**:
```[language]
# Your pattern code template here
```

**Example**:
```[language]
# Real-world example
```

**Why**: [Explain the reasoning]

---

## 🚫 FORBIDDEN PATTERNS

### **Anti-Pattern 1: [What NOT to do]**

**❌ WRONG**:
```[language]
# Bad example showing what NOT to do
```

**✅ CORRECT**:
```[language]
# Good example showing the right way
```

**Why Forbidden**: [Explain why this is bad]

---

### **Anti-Pattern 2: [What NOT to do]**

**❌ WRONG**:
```[language]
# Bad example
```

**✅ CORRECT**:
```[language]
# Good example
```

**Why Forbidden**: [Explain why this is bad]

---

### **Anti-Pattern 3: [What NOT to do]**

**❌ WRONG**:
```[language]
# Bad example
```

**✅ CORRECT**:
```[language]
# Good example
```

**Why Forbidden**: [Explain why this is bad]

---

## 📝 NAMING CONVENTIONS

### **Files**
- Format: `[your_convention]`
- Example: `user_service.py`, `UserService.ts`, etc.

### **Classes**
- Format: `[YourConvention]`
- Example: `UserService`, `DataProcessor`, etc.

### **Functions/Methods**
- Format: `[your_convention]`
- Example: `get_user_data()`, `processPayment()`, etc.

### **Variables**
- Format: `[your_convention]`
- Example: `user_id`, `totalAmount`, etc.

### **Constants**
- Format: `[YOUR_CONVENTION]`
- Example: `MAX_RETRIES`, `API_BASE_URL`, etc.

---

## 🧪 TESTING STANDARDS

### **Test Coverage**
- **Minimum**: 80% code coverage
- **Target**: 90%+ code coverage
- **Critical Paths**: 100% coverage

### **Test Structure**
```[language]
# Test template
def test_[feature]_[scenario]_[expected_result]():
    # Arrange
    [setup test data]
    
    # Act
    [execute the code being tested]
    
    # Assert
    [verify the results]
```

### **Test Categories**
1. **Unit Tests**: Test individual functions/methods
2. **Integration Tests**: Test component interactions
3. **E2E Tests**: Test complete user flows

---

## 📚 DOCUMENTATION STANDARDS

### **Code Comments**
- **When**: Complex logic, non-obvious decisions
- **Format**: Clear, concise explanations
- **Avoid**: Obvious comments, commented-out code

**✅ GOOD**:
```[language]
# Use exponential backoff to avoid overwhelming the API during retries
retry_delay = base_delay * (2 ** attempt)
```

**❌ BAD**:
```[language]
# Set x to 5
x = 5
```

### **Docstrings/JSDoc**
- **Required**: All public functions, classes, modules
- **Format**: [Your preferred format - Google, NumPy, JSDoc, etc.]

**Example**:
```[language]
"""
Brief description of what this function does.

Args:
    param1: Description of param1
    param2: Description of param2

Returns:
    Description of return value

Raises:
    ExceptionType: When this exception is raised
"""
```

---

## 🔒 SECURITY STANDARDS

### **Secrets Management**
- ✅ Use environment variables
- ✅ Use secret management services
- ❌ NEVER commit secrets to Git
- ❌ NEVER hardcode API keys

### **Input Validation**
- ✅ Validate all user input
- ✅ Sanitize data before database operations
- ✅ Use parameterized queries

### **Authentication/Authorization**
- [Your auth pattern]
- [Your permission checking pattern]

---

## 🎨 CODE STYLE

### **Formatting**
- **Tool**: [e.g., Black, Prettier, ESLint, etc.]
- **Config**: [Location of config file]
- **Run**: `[command to format code]`

### **Linting**
- **Tool**: [e.g., pylint, ESLint, etc.]
- **Config**: [Location of config file]
- **Run**: `[command to lint code]`

### **Type Checking** (if applicable)
- **Tool**: [e.g., mypy, TypeScript, etc.]
- **Config**: [Location of config file]
- **Run**: `[command to type check]`

---

## 🔄 VERSION CONTROL

### **Commit Messages**
**Format**:
```
type(scope): brief description

Detailed explanation (if needed)

- Bullet points for changes
- More details
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Example**:
```
feat(auth): Add OAuth2 authentication

Implement OAuth2 flow for user authentication with Google and GitHub providers.

- Add OAuth2 client configuration
- Implement callback handlers
- Add user session management
```

### **Branch Naming**
- Format: `[type]/[brief-description]`
- Examples: `feat/oauth-login`, `fix/user-validation`, `docs/api-guide`

### **Pull Requests**
- **Title**: Clear, descriptive
- **Description**: What, why, how
- **Tests**: All tests passing
- **Review**: At least one approval

---

## 📊 PERFORMANCE STANDARDS

### **Response Times**
- API endpoints: [target, e.g., <200ms]
- Database queries: [target, e.g., <100ms]
- Page load: [target, e.g., <2s]

### **Optimization**
- ✅ Use caching where appropriate
- ✅ Optimize database queries
- ✅ Lazy load when possible
- ✅ Minimize bundle size (frontend)

---

## 🔧 ERROR HANDLING

### **Pattern**:
```[language]
try:
    # Attempt operation
    result = risky_operation()
except SpecificException as e:
    # Handle specific exception
    logger.error(f"Operation failed: {e}")
    # Recover or re-raise
except Exception as e:
    # Handle unexpected exceptions
    logger.exception("Unexpected error")
    # Re-raise or return error response
finally:
    # Cleanup (if needed)
    cleanup_resources()
```

### **Logging**:
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Format**: [Your log format]
- **Location**: [Where logs are stored]

---

## 📋 CODE REVIEW CHECKLIST

Before submitting code for review:

- [ ] Follows all patterns in this document
- [ ] No magic numbers (all in config)
- [ ] Production-grade (no TODOs, mocks, placeholders)
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Type hints/annotations added
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Security considerations addressed
- [ ] Performance acceptable
- [ ] Code formatted and linted

---

## 🎓 LEARNING RESOURCES

### **Internal**
- This document (development_standards.md)
- `docs/workflow_guide.md`
- `docs/docflow_quickstart.md`

### **External**
- [Framework docs]: [URL]
- [Language docs]: [URL]
- [Best practices guide]: [URL]

---

## 🔄 MAINTENANCE

**Update this document when**:
- New patterns emerge
- Anti-patterns discovered
- Technology stack changes
- Team conventions evolve

**Review Schedule**: Monthly

---

## ✅ COMPLIANCE

All code MUST comply with these standards before merging.

**Validation**:
```bash
# Run compliance checker
python scripts/docflow_compliance_checker.py

# Should output: PASS
```

---

## 📝 CUSTOMIZATION INSTRUCTIONS

**To use this template**:

1. Replace all `[placeholders]` with your project specifics
2. Add your tech stack patterns (React, Django, etc.)
3. Define your naming conventions
4. Add your testing framework details
5. Specify your code style tools
6. Remove sections that don't apply
7. Add project-specific sections

**Remember**: These standards ensure consistency and quality. Follow them rigorously!

---

**Version**: 1.0.0  
**Status**: [Draft / Active]  
**Maintained By**: [Team/Person]

