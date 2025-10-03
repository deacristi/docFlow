# docFlow v3.0 Installation & Setup Guide

**Get docFlow v3.0 with Living Code Context running in your project in 15 minutes**

Version: 3.0.0
Last Updated: 2025-10-03

---

## 📋 Prerequisites

### **Required**
- Python 3.8+ (for context dashboard and living context generator)
- Git (for version control)
- Text editor or IDE

### **Optional**
- AI assistant (Claude, GPT-4, etc.)
- YAML support in your editor
- Database (PostgreSQL, MySQL, etc.) for Living Code Context database features

---

## 🚀 Quick Installation (5 Minutes)

### **Step 1: Copy docFlow to Your Project**

```bash
# Navigate to your project root
cd /path/to/your/project

# Copy the entire docflow_portable folder
cp -r /path/to/docflow_portable/* .

# Or on Windows PowerShell:
Copy-Item -Path "path\to\docflow_portable\*" -Destination "." -Recurse -Force
```

**What gets copied**:
```
your-project/
├── docs/
│   ├── ai_context/
│   │   ├── living_code/              ← NEW in v3.0
│   │   ├── MASTER_CONTEXT_LOADER.md
│   │   └── LOAD_CONTEXT.md
│   ├── templates/
│   ├── tools/
│   ├── docflow_quickstart.md
│   ├── workflow_guide.md
│   ├── development_standards.md
│   └── DOCFLOW_V3_LIVING_CODE_CONTEXT.md  ← NEW
├── scripts/
│   ├── context_dashboard.py
│   ├── generate_living_context.py    ← NEW in v3.0
│   └── context_dashboard/
├── config_specification.yaml
└── README.md (docFlow README)
```

---

### **Step 2: Install Python Dependencies**

```bash
# Install required packages
pip install pyyaml

# Or add to your requirements.txt:
echo "pyyaml>=6.0" >> requirements.txt
pip install -r requirements.txt
```

**That's it!** No heavy dependencies.

---

### **Step 3: Verify Installation**

```bash
# Test context dashboard
python scripts/context_dashboard.py

# Should display dashboard with default values
```

**Expected output**:
```
╔════════════════════════════════════════════════════════════════╗
║         TradePulse AI Context Dashboard v1.0                   ║
╚════════════════════════════════════════════════════════════════╝

📊 Context Health: ✅ HEALTHY (25.0% used)
...
```

✅ **Installation complete!**

---

## ⚙️ Configuration (5 Minutes)

### **Step 1: Update Project Metadata**

Edit `config_specification.yaml`:

```yaml
project:
  name: "YourProjectName"        # ← Change this
  version: "1.0.0"                # ← Change this
  environment: "development"
  description: "Your description" # ← Change this
```

---

### **Step 2: Customize Development Standards**

Edit `docs/development_standards.md`:

1. **Replace placeholders** with your tech stack:
   - Language (Python, JavaScript, TypeScript, etc.)
   - Framework (React, Django, FastAPI, etc.)
   - Patterns specific to your stack

2. **Add your patterns**:
   ```markdown
   ### **Pattern 1: Your Pattern Name**
   
   **When to Use**: [When this applies]
   
   **Template**:
   ```python
   # Your code template
   ```
   ```

3. **Define forbidden patterns**:
   ```markdown
   ### **Anti-Pattern 1: What NOT to do**
   
   **❌ WRONG**:
   ```python
   # Bad example
   ```
   
   **✅ CORRECT**:
   ```python
   # Good example
   ```
   ```

---

### **Step 3: Update Project Context**

Edit `docs/ai_context/LOAD_CONTEXT.md`:

1. **Fill in project overview**:
   - Project name and vision
   - Technology stack
   - Architecture diagram

2. **List core features**:
   - Current features
   - In-progress features
   - Planned features

3. **Define development patterns**:
   - Your specific patterns
   - Common gotchas
   - Project conventions

**Tip**: Keep it concise (target <5,000 tokens)

---

### **Step 4: Add Project-Specific Configuration**

Edit `config_specification.yaml`:

```yaml
# Add your configuration sections
api:
  base_url: "https://your-api.com"
  timeout_seconds: 30

database:
  host: "localhost"
  port: 5432

# Keep context_dashboard section as-is
context_dashboard:
  total_tokens: 200000
  # ... (don't change these unless you know what you're doing)
```

---

## 🎯 First Use (10 Minutes)

### **Step 1: Start AI Session**

In your AI assistant, paste:

```
Load context from @docs/ai_context/MASTER_CONTEXT_LOADER.md
```

**AI will load**:
- docFlow framework
- Your project context
- Development standards
- Templates

---

### **Step 2: Verify Context Health**

```bash
python scripts/context_dashboard.py
```

**Check**:
- ✅ Context usage <30%
- ✅ Accuracy score >95%
- ✅ Health status: HEALTHY

---

### **Step 3: Try Your First Feature**

Follow the workflow for a small feature:

1. **Phase 1: Research**
   ```
   AI, let's implement [small feature]. First, let's investigate the codebase.
   ```

2. **Phase 2: Document**
   ```
   AI, create an implementation plan using @docs/templates/implementation_plan_template.md
   ```

3. **Review the plan** (this is key!)

4. **Phase 3-4: Design & Plan**
   ```
   AI, the plan looks good. Let's proceed with design.
   ```

5. **Phase 5: Implement**
   ```
   AI, implement the feature following the plan.
   ```

6. **Phase 6: Validate**
   ```
   AI, create an implementation report using @docs/templates/implementation_report_template.md
   ```

---

## 📚 Directory Structure Explained

```
your-project/
├── docs/
│   ├── ai_context/
│   │   ├── MASTER_CONTEXT_LOADER.md    # ← AI entry point (load this first)
│   │   └── LOAD_CONTEXT.md             # ← Your project context (customize!)
│   │
│   ├── templates/
│   │   ├── implementation_plan_template.md        # ← Use for features
│   │   ├── issue_root_cause_analysis_template.md  # ← Use for bugs
│   │   ├── feature_specification_template.md      # ← Use for specs
│   │   └── implementation_report_template.md      # ← Use after implementation
│   │
│   ├── analysis/                       # ← Store analysis docs here
│   ├── implementation_plans/           # ← Store plans here
│   ├── implementation_reports/         # ← Store reports here
│   │
│   ├── tools/
│   │   └── context_dashboard_guide.md  # ← Dashboard usage guide
│   │
│   ├── docflow_quickstart.md           # ← Framework intro (read first!)
│   ├── workflow_guide.md               # ← 6-phase process (read second!)
│   └── development_standards.md        # ← Your coding standards (customize!)
│
├── scripts/
│   ├── context_dashboard.py            # ← Main dashboard CLI
│   └── context_dashboard/              # ← Dashboard modules (don't modify)
│       ├── __init__.py
│       ├── models.py
│       ├── analyzer.py
│       ├── metrics.py
│       ├── recommender.py
│       └── renderer.py
│
└── config_specification.yaml           # ← All configuration (customize!)
```

---

## 🎓 Learning Path

### **Day 1: Setup & Basics** (1 hour)

1. ✅ Install docFlow (5 min)
2. ✅ Customize configuration (5 min)
3. ✅ Read `docs/docflow_quickstart.md` (15 min)
4. ✅ Read `docs/workflow_guide.md` (20 min)
5. ✅ Run context dashboard (5 min)
6. ✅ Load context in AI (10 min)

---

### **Day 2: First Feature** (2 hours)

1. ✅ Pick a small feature to implement
2. ✅ Follow workflow_guide.md step-by-step
3. ✅ Use implementation_plan_template.md
4. ✅ Monitor context with dashboard
5. ✅ Document with implementation_report_template.md

**Goal**: Complete one feature using docFlow

---

### **Day 3: Optimization** (1 hour)

1. ✅ Review what worked/didn't work
2. ✅ Adjust templates to your needs
3. ✅ Refine development_standards.md
4. ✅ Add project-specific patterns

**Goal**: Customize docFlow for your project

---

### **Week 2+: Mastery**

1. ✅ docFlow becomes second nature
2. ✅ Context management is automatic
3. ✅ Templates speed up work significantly
4. ✅ Quality and consistency improve

**Goal**: Efficient, high-quality development

---

## 🔧 Troubleshooting

### **Problem: Context dashboard not working**

**Solution**:
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
pip install pyyaml

# Verify config file exists
ls config_specification.yaml
```

---

### **Problem: AI not following standards**

**Solution**:
1. Check context health: `python scripts/context_dashboard.py`
2. If freshness <80%, reload MASTER_CONTEXT_LOADER.md
3. Verify development_standards.md is up to date

---

### **Problem: Templates don't fit my project**

**Solution**:
1. Customize templates in `docs/templates/`
2. Keep structure, change content
3. Add project-specific sections

---

### **Problem: Too much context usage**

**Solution**:
1. Run dashboard to see breakdown
2. Remove low-value content (see eviction queue)
3. Start new thread if usage >70%

---

## ✅ Installation Checklist

- [ ] Copied docflow_portable to project
- [ ] Installed Python dependencies (`pip install pyyaml`)
- [ ] Updated `config_specification.yaml` with project name
- [ ] Customized `docs/development_standards.md`
- [ ] Updated `docs/ai_context/LOAD_CONTEXT.md`
- [ ] Tested context dashboard (`python scripts/context_dashboard.py`)
- [ ] Loaded MASTER_CONTEXT_LOADER.md in AI
- [ ] Read `docs/docflow_quickstart.md`
- [ ] Read `docs/workflow_guide.md`
- [ ] Completed first feature using docFlow

---

## 🎯 Success Criteria

You'll know docFlow is properly installed when:

1. ✅ Context dashboard runs without errors
2. ✅ AI loads context successfully
3. ✅ AI follows your development standards
4. ✅ Templates are available and usable
5. ✅ Configuration is project-specific
6. ✅ You can complete a feature using the workflow

---

## 📞 Next Steps

After installation:

1. **Read**: `docs/docflow_quickstart.md` (framework intro)
2. **Read**: `docs/workflow_guide.md` (detailed process)
3. **Try**: Implement a small feature following the workflow
4. **Optimize**: Customize templates and standards
5. **Master**: Use docFlow for all development

---

## 📚 Additional Resources

- **Framework Intro**: `docs/docflow_quickstart.md`
- **Workflow Guide**: `docs/workflow_guide.md`
- **Dashboard Guide**: `docs/tools/context_dashboard_guide.md`
- **Templates**: `docs/templates/`

---

**Welcome to efficient, high-quality AI-assisted development!** 🚀

---

**Version**: 2.0.0  
**Last Updated**: 2025-10-03  
**Status**: ✅ Production-Ready

