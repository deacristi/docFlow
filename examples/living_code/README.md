# Living Code Context - Example Structure

This folder demonstrates the Living Code Context pattern used by docFlow to maintain accurate, up-to-date documentation that reflects the actual codebase state.

## What is Living Code Context?

Living Code Context is documentation that:
1. **Reflects actual code** - Not aspirational or outdated
2. **Auto-updates** - Freshness checks ensure accuracy
3. **AI-optimized** - Structured for AI consumption
4. **Single source of truth** - One place for each piece of information

## Directory Structure

```
living_code/
├── README.md                    # This file
├── MASTER_CONTEXT_LOADER.md     # Entry point for AI context loading
├── architecture/
│   ├── system_overview.md       # High-level architecture
│   ├── data_flow.md             # How data moves through system
│   └── api_contracts.md         # API specifications
├── services/
│   ├── service_registry.md      # List of all services
│   └── [service_name].md        # Individual service docs
├── patterns/
│   ├── approved_patterns.md     # Patterns to use
│   └── forbidden_patterns.md    # Anti-patterns to avoid
└── decisions/
    └── adr_template.md          # Architecture Decision Records
```

## MASTER_CONTEXT_LOADER.md

The master context loader is the entry point for AI assistants. It should:

1. **Load order** - Specify which files to read first
2. **Critical constraints** - List never-violate rules
3. **Current state** - What's implemented vs planned
4. **Quick reference** - Common patterns and examples

Example structure:

```markdown
# Master Context Loader

## Load Order
1. Read `architecture/system_overview.md`
2. Read `patterns/forbidden_patterns.md`
3. Read relevant service docs based on task

## Critical Constraints
- Never use bare `except:` statements
- Always use `settings.X` for configuration
- Database access via dependency injection only

## Current State
- Feature A: ✅ Complete
- Feature B: 🚧 In Progress
- Feature C: 📋 Planned
```

## Freshness Checking

Use the freshness checker to ensure Living Code stays current:

```bash
python scripts/check_freshness.py
```

This will:
- Check last modified dates
- Flag stale documentation (>30 days)
- Suggest files that need review

## Best Practices

1. **Update on change** - When code changes, update Living Code
2. **Review weekly** - Run freshness checks regularly
3. **Keep it minimal** - Only document what AI needs
4. **Use references** - Link to code, don't duplicate it
5. **Version control** - Track changes in git
