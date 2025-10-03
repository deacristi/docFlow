# Living Code Context - Auto-Generated Files

**docFlow v3.0 - Layer 6: Living Code Context**

**Purpose**: This directory contains auto-generated, always-current summaries of your actual code and database state.

**Version**: 3.0.0  
**Date**: 2025-10-03

---

## 📁 What Goes Here

When you run `python scripts/generate_living_context.py --all`, this directory will be populated with:

### **1. INDEX.md**
- Entry point for all living context
- Links to all generated documents
- Usage instructions

### **2. DATABASE_SCHEMA_CURRENT.md**
- Current database schema from your models
- Table names, columns, types, constraints
- Auto-generated from actual code

### **3. DATABASE_STATE_CURRENT.md**
- Row counts for all tables
- Sample data (3 rows per table)
- Date ranges for time-series data
- Data availability insights

### **4. API_ENDPOINTS_CURRENT.md**
- All API endpoints from your routes
- HTTP methods (GET, POST, PUT, DELETE)
- Paths and function names
- Docstrings

### **5. SERVICES_INVENTORY.md**
- All services from your services directory
- Class names and descriptions
- Public methods

### **6. AGENTS_AND_TOOLS_CURRENT.md** (if applicable)
- All agents (if you have an agent-based architecture)
- All tools organized by category
- File locations

### **7. ARCHITECTURE_MAP.md**
- Project structure
- Tech stack
- System architecture overview

---

## 🚀 How to Generate

```bash
# Generate all living context
python scripts/generate_living_context.py --all

# Generate specific components
python scripts/generate_living_context.py --schema
python scripts/generate_living_context.py --db-state
python scripts/generate_living_context.py --endpoints
python scripts/generate_living_context.py --services
python scripts/generate_living_context.py --architecture
```

---

## 🔄 When to Regenerate

1. **Before starting new conversation** (most important)
2. Before major features
3. After significant changes
4. When accuracy drops

---

## 💡 Customization

Edit `scripts/generate_living_context.py` to match your project structure:

```python
# Update paths to your models
models_file = self.project_root / "app" / "models" / "database.py"

# Update paths to your routes
api_dir = self.project_root / "app" / "api"

# Update paths to your services
services_dir = self.project_root / "app" / "services"

# Update database connection
database_url = settings.DATABASE_URL
```

---

## 📊 Benefits

**With Living Code Context**, AI assistants have:
- ✅ **Exact current schema** (not just documentation)
- ✅ **Actual database data** (row counts, samples, distributions)
- ✅ **Real implementation details** (endpoints, services, tools as they exist NOW)
- ✅ **Always up-to-date** (regenerate before major changes)

**Result**:
- 90-95% implementation confidence (vs 60-70% without)
- Zero pre-research time
- Minimal risk of breaking code
- No schema mismatches
- No missing dependencies

---

## 🎯 Integration

Living Code Context is automatically loaded when you use:

```
Load context from @docs/ai_context/MASTER_CONTEXT_LOADER.md
```

AI will load all 6 layers including Living Code Context!

---

## 📝 Example Output

After running the generator, you'll see:

```
======================================================================
🚀 Generating Living Code Context - docFlow v3.0 Layer 6
======================================================================

📊 Generating DATABASE_SCHEMA_CURRENT.md...
  ✅ Generated: DATABASE_SCHEMA_CURRENT.md
📊 Generating DATABASE_STATE_CURRENT.md...
  ✅ Generated: DATABASE_STATE_CURRENT.md
🌐 Generating API_ENDPOINTS_CURRENT.md...
  ✅ Generated: API_ENDPOINTS_CURRENT.md
🔧 Generating SERVICES_INVENTORY.md...
  ✅ Generated: SERVICES_INVENTORY.md
🤖 Generating AGENTS_AND_TOOLS_CURRENT.md...
  ✅ Generated: AGENTS_AND_TOOLS_CURRENT.md
🏗️ Generating ARCHITECTURE_MAP.md...
  ✅ Generated: ARCHITECTURE_MAP.md
📑 Generating INDEX.md...
  ✅ Generated: INDEX.md

======================================================================
✅ Living Code Context Generation Complete!
======================================================================
```

---

## 🔍 Verification

Check that Living Code Context is loaded:

```bash
python scripts/context_dashboard.py
```

Look for the "📚 Loaded Context Knowledge" section showing:
- ✅ Living Code - Database Schema
- ✅ Living Code - Database State
- ✅ Living Code - API Endpoints
- ✅ Living Code - Services
- ✅ Living Code - Architecture

---

## 📚 Learn More

See `docs/DOCFLOW_V3_LIVING_CODE_CONTEXT.md` for:
- Complete implementation guide
- Impact analysis (before/after)
- Confidence improvement metrics
- Workflow integration
- Real-world examples

---

**Version**: 3.0.0  
**Status**: Ready for generation  
**Next Step**: Run `python scripts/generate_living_context.py --all`

