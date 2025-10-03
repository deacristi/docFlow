# Project Context - [YOUR PROJECT NAME]

**Complete Project Context for AI Assistants**

Version: 1.0.0  
Last Updated: [DATE]  
Purpose: Provide complete project understanding for AI-assisted development

---

## 🎯 PROJECT OVERVIEW

### **Project Name**
[Your Project Name]

### **Project Vision**
[Describe the high-level vision and purpose of your project]

Example:
> "Build a modern web application that helps users manage their tasks efficiently with AI-powered suggestions and real-time collaboration features."

### **Project Type**
- [ ] Backend API
- [ ] Frontend Application
- [ ] Full-Stack Application
- [ ] Mobile Application
- [ ] Data Pipeline / ML Project
- [ ] CLI Tool
- [ ] Library / Package
- [ ] Other: ___________

### **Current Status**
- **Phase**: [Planning / Development / Testing / Production]
- **Version**: [e.g., v1.0.0]
- **Completion**: [e.g., 75%]
- **Last Major Update**: [DATE]

---

## 🏗️ ARCHITECTURE

### **Technology Stack**

**Backend** (if applicable):
- Language: [e.g., Python 3.11, Node.js 18, etc.]
- Framework: [e.g., FastAPI, Django, Express, etc.]
- Database: [e.g., PostgreSQL, MongoDB, etc.]
- ORM/Query Builder: [e.g., SQLAlchemy, Prisma, etc.]
- Authentication: [e.g., JWT, OAuth2, etc.]

**Frontend** (if applicable):
- Language: [e.g., TypeScript, JavaScript]
- Framework: [e.g., React 18, Vue 3, Angular, etc.]
- State Management: [e.g., Redux, Zustand, Pinia, etc.]
- Styling: [e.g., Tailwind CSS, CSS Modules, etc.]
- Build Tool: [e.g., Vite, Webpack, etc.]

**Infrastructure**:
- Hosting: [e.g., AWS, Azure, Vercel, etc.]
- CI/CD: [e.g., GitHub Actions, GitLab CI, etc.]
- Monitoring: [e.g., Sentry, DataDog, etc.]

**AI/ML** (if applicable):
- Model Provider: [e.g., OpenAI, Azure OpenAI, etc.]
- Framework: [e.g., Langchain, LlamaIndex, etc.]
- Vector Database: [e.g., Pinecone, Weaviate, etc.]

### **System Architecture**

[Describe your system architecture]

Example:
```
┌─────────────┐
│   Frontend  │ (React + TypeScript)
└──────┬──────┘
       │ REST API
┌──────▼──────┐
│   Backend   │ (FastAPI + Python)
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │ (PostgreSQL)
└─────────────┘
```

### **Key Components**

1. **[Component 1 Name]**
   - Purpose: [What it does]
   - Location: [File path or directory]
   - Dependencies: [What it depends on]

2. **[Component 2 Name]**
   - Purpose: [What it does]
   - Location: [File path or directory]
   - Dependencies: [What it depends on]

3. **[Component 3 Name]**
   - Purpose: [What it does]
   - Location: [File path or directory]
   - Dependencies: [What it depends on]

---

## 📁 PROJECT STRUCTURE

```
your-project/
├── src/                    # Source code
│   ├── components/         # [Description]
│   ├── services/           # [Description]
│   ├── models/             # [Description]
│   ├── utils/              # [Description]
│   └── config/             # [Description]
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── config_specification.yaml  # All configuration
└── README.md
```

**Key Directories**:
- `src/`: [Describe what's in here]
- `tests/`: [Describe testing approach]
- `docs/`: [Describe documentation structure]

---

## 🎯 CORE FEATURES

### **Feature 1: [Feature Name]**
- **Status**: [Planned / In Progress / Complete]
- **Description**: [What it does]
- **Implementation**: [Where the code is]
- **Dependencies**: [What it needs]

### **Feature 2: [Feature Name]**
- **Status**: [Planned / In Progress / Complete]
- **Description**: [What it does]
- **Implementation**: [Where the code is]
- **Dependencies**: [What it needs]

### **Feature 3: [Feature Name]**
- **Status**: [Planned / In Progress / Complete]
- **Description**: [What it does]
- **Implementation**: [Where the code is]
- **Dependencies**: [What it needs]

---

## 🔧 DEVELOPMENT PATTERNS

### **Pattern 1: [Pattern Name]**

**When to Use**: [Describe when this pattern applies]

**Example**:
```[language]
# Code example showing the pattern
```

**Why**: [Explain the reasoning]

### **Pattern 2: [Pattern Name]**

**When to Use**: [Describe when this pattern applies]

**Example**:
```[language]
# Code example showing the pattern
```

**Why**: [Explain the reasoning]

---

## 🚫 FORBIDDEN PATTERNS

### **Anti-Pattern 1: [What NOT to do]**

**Wrong**:
```[language]
# Bad example
```

**Correct**:
```[language]
# Good example
```

**Why**: [Explain why it's forbidden]

### **Anti-Pattern 2: [What NOT to do]**

**Wrong**:
```[language]
# Bad example
```

**Correct**:
```[language]
# Good example
```

**Why**: [Explain why it's forbidden]

---

## 📊 CURRENT STATE

### **Completed**
- ✅ [Feature/Component 1]
- ✅ [Feature/Component 2]
- ✅ [Feature/Component 3]

### **In Progress**
- 🔄 [Feature/Component 4]
- 🔄 [Feature/Component 5]

### **Planned**
- ⏳ [Feature/Component 6]
- ⏳ [Feature/Component 7]

### **Known Issues**
- ⚠️ [Issue 1]
- ⚠️ [Issue 2]

---

## 🎯 ACTIVE PRIORITIES

### **Priority 1: [Task Name]**
- **Goal**: [What needs to be achieved]
- **Status**: [Current status]
- **Blockers**: [Any blockers]
- **Next Steps**: [What to do next]

### **Priority 2: [Task Name]**
- **Goal**: [What needs to be achieved]
- **Status**: [Current status]
- **Blockers**: [Any blockers]
- **Next Steps**: [What to do next]

---

## 🧪 TESTING STRATEGY

### **Unit Tests**
- Framework: [e.g., pytest, Jest, etc.]
- Location: [Where tests are]
- Coverage Target: [e.g., >80%]
- Run Command: `[command to run tests]`

### **Integration Tests**
- Framework: [e.g., pytest, Cypress, etc.]
- Location: [Where tests are]
- Run Command: `[command to run tests]`

### **E2E Tests** (if applicable)
- Framework: [e.g., Playwright, Cypress, etc.]
- Location: [Where tests are]
- Run Command: `[command to run tests]`

---

## 🔐 SECURITY CONSIDERATIONS

- **Authentication**: [How auth works]
- **Authorization**: [How permissions work]
- **Data Protection**: [How sensitive data is protected]
- **API Security**: [Rate limiting, CORS, etc.]

---

## 📚 KEY DOCUMENTATION

### **Internal Docs**
- Architecture: `docs/architecture.md`
- API Docs: `docs/api.md`
- Deployment: `docs/deployment.md`

### **External Resources**
- [Framework Docs]: [URL]
- [Library Docs]: [URL]
- [Design System]: [URL]

---

## 🚀 GETTING STARTED

### **Setup**
```bash
# Clone repository
git clone [repo-url]

# Install dependencies
[install command]

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run development server
[run command]
```

### **Common Commands**
```bash
# Run tests
[test command]

# Build for production
[build command]

# Deploy
[deploy command]

# Check context health
python scripts/context_dashboard.py
```

---

## 🎓 ONBOARDING CHECKLIST

For new developers (including AI):

- [ ] Read this document (LOAD_CONTEXT.md)
- [ ] Read development_standards.md
- [ ] Read workflow_guide.md
- [ ] Set up development environment
- [ ] Run tests to verify setup
- [ ] Run context dashboard
- [ ] Complete first small task following docFlow

---

## 📝 NOTES FOR AI ASSISTANTS

### **Critical Information**
1. **Always** check config_specification.yaml for values
2. **Always** follow patterns in development_standards.md
3. **Always** use templates for plans and reports
4. **Never** use magic numbers (use config)
5. **Never** skip workflow phases

### **Project-Specific Conventions**
- [Convention 1]
- [Convention 2]
- [Convention 3]

### **Common Gotchas**
- [Gotcha 1 and how to avoid it]
- [Gotcha 2 and how to avoid it]

---

## 🔄 MAINTENANCE

**Update this document when**:
- Architecture changes
- New major features added
- Technology stack changes
- Development patterns change
- Priorities shift

**Last Review**: [DATE]  
**Next Review**: [DATE]

---

## ✅ CONTEXT LOADING VERIFICATION

After loading this context, AI should be able to answer:

1. ✅ What is the project's purpose?
2. ✅ What technology stack is used?
3. ✅ What are the key components?
4. ✅ What patterns should be followed?
5. ✅ What patterns should be avoided?
6. ✅ What are the current priorities?
7. ✅ How to run tests?
8. ✅ Where is configuration stored?

**If AI cannot answer these, reload context.**

---

**Version**: 1.0.0  
**Status**: [Draft / Active / Archived]  
**Maintained By**: [Team/Person]

---

## 📋 CUSTOMIZATION INSTRUCTIONS

**To use this template**:

1. Replace all `[placeholders]` with your project details
2. Remove sections that don't apply
3. Add sections specific to your project
4. Keep it concise (target <5,000 tokens)
5. Update regularly (at least monthly)
6. Commit to version control

**Remember**: This is the AI's primary source of project knowledge. Keep it accurate and up-to-date!

