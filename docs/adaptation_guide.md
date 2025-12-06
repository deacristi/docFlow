# docFlow v3.1 - Adaptation Guide

> How to adapt docFlow to any project or repository

---

## Overview

docFlow is designed to be project-agnostic. This guide walks you through customizing docFlow for your specific project, whether it's a Python backend, Node.js application, or any other codebase.

---

## Step 1: Understand Your Project

Before adapting docFlow, document your project's:

### Architecture
- **Framework**: FastAPI, Django, Express, Next.js, etc.
- **Database**: PostgreSQL, MySQL, MongoDB, etc.
- **Language**: Python, TypeScript, Go, etc.

### Patterns
- **Required patterns**: How should code be written?
- **Forbidden patterns**: What should never be done?
- **Configuration**: How are settings managed?

### Structure
- **Source code location**: `src/`, `app/`, `lib/`
- **Documentation location**: `docs/`, `documentation/`
- **Test location**: `tests/`, `__tests__/`

---

## Step 2: Customize Steering Rules

### context-monitoring.md

This file defines what the AI should always remember. Customize:

```markdown
## ⚠️ Critical Constraints (Customize for Your Project)

### Database Access
# Python/SQLAlchemy example:
async with get_db() as session:
    result = await session.execute(query)

# Node.js/Prisma example:
const result = await prisma.user.findMany()

# Go/GORM example:
db.Find(&users)

### Configuration
# Python example:
timeout = settings.API_TIMEOUT

# Node.js example:
const timeout = config.get('api.timeout')

# Go example:
timeout := viper.GetInt("api.timeout")
```

### phase-gates.md

This file is mostly universal. Customize only if you have:
- Different phase names
- Additional gates
- Project-specific validation requirements

---

## Step 3: Customize Scripts

### checkpoint.py

Update the `BACKUP_DIRS` list to match your project:

```python
# Python project
BACKUP_DIRS = [
    "docs/ai_context/living_code",
    ".kiro/steering",
    "app/core/",  # Core modules you want to backup
]

# Node.js project
BACKUP_DIRS = [
    "docs/ai_context/living_code",
    ".kiro/steering",
    "src/config/",
]

# Go project
BACKUP_DIRS = [
    "docs/ai_context/living_code",
    ".kiro/steering",
    "internal/config/",
]
```

### check_freshness.py

Update paths to match your project structure:

```python
# Python project
DOCS_DIR = Path("docs/ai_context/living_code")
SOURCE_DIRS = [
    Path("app"),
    Path("src"),
]

# Node.js project
DOCS_DIR = Path("docs/ai_context/living_code")
SOURCE_DIRS = [
    Path("src"),
    Path("lib"),
]
# Also update the file extension in get_newest_source_timestamp():
# for file in directory.rglob("*.ts"):  # or *.js

# Go project
DOCS_DIR = Path("docs/ai_context/living_code")
SOURCE_DIRS = [
    Path("cmd"),
    Path("internal"),
    Path("pkg"),
]
# Update extension: for file in directory.rglob("*.go"):
```

---

## Step 4: Create Living Code Context

Create your project's context structure:

```
your-project/
└── docs/
    └── ai_context/
        └── living_code/
            ├── MASTER_CONTEXT_LOADER.md
            ├── architecture/
            │   ├── system_overview.md
            │   └── data_flow.md
            ├── patterns/
            │   ├── approved_patterns.md
            │   └── forbidden_patterns.md
            └── services/
                └── service_registry.md
```

### MASTER_CONTEXT_LOADER.md

Copy from `examples/living_code/MASTER_CONTEXT_LOADER.md` and customize:

1. **Architecture section**: Fill in your actual architecture
2. **Key Components table**: List your actual components
3. **Current State**: Document your features
4. **Development Standards**: Add your actual patterns

### patterns/forbidden_patterns.md

Document patterns that should NEVER be used in your project:

```markdown
# Forbidden Patterns

## [Your Framework] Specific

### ❌ [Bad Pattern Name]
```[language]
# FORBIDDEN - [Why it's bad]
[bad code example]
```

### ✅ Correct Pattern
```[language]
# CORRECT - [Why it's good]
[good code example]
```
```

### patterns/approved_patterns.md

Document patterns that SHOULD be used:

```markdown
# Approved Patterns

## [Pattern Category]

### [Pattern Name]
```[language]
# [Description of when to use]
[code example]
```
```

---

## Step 5: Customize Templates

### implementation_plan.md

Add project-specific sections:
- Your deployment process
- Your testing requirements
- Your documentation standards

### issue_analysis.md

Add sections for common issues in your project:
- Framework-specific issues
- Database-specific issues
- Integration-specific issues

### Code Templates

Create language-specific templates:

**Python**: Use `service_template.py` and `tool_template.py` as-is or customize

**TypeScript/Node.js**: Create equivalents:
```typescript
// templates/service_template.ts
export class MyService {
  private static instance: MyService | null = null;
  
  static getInstance(): MyService {
    if (!MyService.instance) {
      MyService.instance = new MyService();
    }
    return MyService.instance;
  }
  
  async process(input: InputType): Promise<OutputType> {
    // Implementation
  }
}
```

**Go**: Create equivalents:
```go
// templates/service_template.go
package service

type MyService struct {
    config *Config
}

func NewMyService(config *Config) *MyService {
    return &MyService{config: config}
}

func (s *MyService) Process(input Input) (Output, error) {
    // Implementation
}
```

---

## Step 6: IDE Configuration

### Kiro IDE
```bash
mkdir -p .kiro/steering
cp docflow/steering/*.md .kiro/steering/
```

### Cursor
```bash
mkdir -p .cursor/rules
cp docflow/steering/*.md .cursor/rules/
```

### VS Code + GitHub Copilot
```bash
mkdir -p .github
cat docflow/steering/*.md > .github/copilot-instructions.md
```

### Other IDEs
Use steering rules as system prompts or AI instructions in your IDE's AI configuration.

---

## Step 7: Team Onboarding

### For New Team Members

1. Read `docs/quickstart.md`
2. Review `patterns/forbidden_patterns.md`
3. Understand the 6-phase workflow
4. Practice with a small change using fast-track

### For AI Assistants

At the start of each session, load:
1. `MASTER_CONTEXT_LOADER.md`
2. `patterns/forbidden_patterns.md`
3. Relevant service documentation

---

## Language-Specific Examples

### Python (FastAPI)

```python
# Forbidden
session = SessionLocal()  # Direct instantiation

# Required
async with get_db() as session:
    result = await session.execute(query)
```

### TypeScript (Node.js)

```typescript
// Forbidden
const db = new Database()  // Direct instantiation

// Required
const db = container.resolve<Database>('database')
```

### Go

```go
// Forbidden
db, _ := sql.Open("postgres", connStr)  // Ignoring error

// Required
db, err := sql.Open("postgres", connStr)
if err != nil {
    return nil, fmt.Errorf("failed to open database: %w", err)
}
```

---

## Checklist

### Initial Setup
- [ ] Cloned docFlow repository
- [ ] Copied files to your project
- [ ] Updated `.gitignore`

### Customization
- [ ] Customized `steering/context-monitoring.md`
- [ ] Customized `scripts/checkpoint.py` paths
- [ ] Customized `scripts/check_freshness.py` paths
- [ ] Created `docs/ai_context/living_code/` structure
- [ ] Wrote `MASTER_CONTEXT_LOADER.md`
- [ ] Documented forbidden patterns
- [ ] Documented approved patterns

### IDE Setup
- [ ] Copied steering rules to IDE config
- [ ] Tested AI assistant loads context correctly

### Team
- [ ] Documented in team wiki/README
- [ ] Onboarded team members
- [ ] Established review process

---

## Troubleshooting

### AI Doesn't Follow Patterns

1. Check steering rules are in correct location
2. Verify AI is loading context at session start
3. Add more explicit examples to forbidden_patterns.md

### Freshness Checker Fails

1. Verify `DOCS_DIR` path exists
2. Verify `SOURCE_DIRS` paths exist
3. Check file extensions match your language

### Checkpoints Not Working

1. Verify `BACKUP_DIRS` paths exist
2. Check git is initialized in project
3. Ensure write permissions on `.docflow_checkpoints/`

---

**Version**: 3.1.0  
**Last Updated**: December 2025
