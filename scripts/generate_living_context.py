#!/usr/bin/env python3
"""
========================================================================
TradePulse v4.0 - Living Code Context Generator
========================================================================

🎯 PURPOSE:
Generate always-current code summaries and database state for AI context.
This is Layer 6 of docFlow v3.0 - "Living Code Context"

🔧 FEATURES:
- Auto-generate database schema from models
- Extract API endpoints from routes
- Map services and their dependencies
- Document agents and tools
- Pull actual database statistics and samples
- Create dependency graphs

📋 USAGE:
    python scripts/generate_living_context.py --all
    python scripts/generate_living_context.py --schema
    python scripts/generate_living_context.py --endpoints
    python scripts/generate_living_context.py --db-state

🔗 INTEGRATION:
- Outputs to docs/ai_context/living_code/
- Loaded via MASTER_CONTEXT_LOADER.md
- Run before major changes or on-demand
"""

import os
import sys
import ast
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import after path setup
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


class LivingContextGenerator:
    """Generate living code context documentation"""
    
    def __init__(self):
        self.project_root = project_root
        self.output_dir = self.project_root / "docs" / "ai_context" / "living_code"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Database connection
        database_url = settings.DATABASE_URL.replace('+asyncpg', '')
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🔗 Database: {settings.POSTGRES_DB}")
    
    def generate_all(self):
        """Generate all living context documents"""
        print("\n" + "="*70)
        print("🚀 Generating Living Code Context - docFlow v3.0 Layer 6")
        print("="*70 + "\n")
        
        self.generate_database_schema()
        self.generate_database_state()
        self.generate_api_endpoints()
        self.generate_services_inventory()
        self.generate_agents_tools()
        self.generate_architecture_map()
        self.generate_index()
        
        print("\n" + "="*70)
        print("✅ Living Code Context Generation Complete!")
        print("="*70)
        print(f"\n📁 Files generated in: {self.output_dir}")
        print("\n💡 Next step: Load via MASTER_CONTEXT_LOADER.md")
    
    def generate_database_schema(self):
        """Generate current database schema from models"""
        print("📊 Generating DATABASE_SCHEMA_CURRENT.md...")
        
        output = []
        output.append("# Current Database Schema - Auto-Generated\n")
        output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append(f"**Source**: app/models/database.py\n")
        output.append(f"**Database**: {settings.POSTGRES_DB}\n\n")
        
        # Parse database.py to extract models
        models_file = self.project_root / "app" / "models" / "database.py"
        with open(models_file, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        # Extract class definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's a SQLAlchemy model
                if any(base.id == 'Base' for base in node.bases if isinstance(base, ast.Name)):
                    output.append(f"## {node.name}\n\n")
                    
                    # Find __tablename__
                    table_name = None
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name) and target.id == '__tablename__':
                                    if isinstance(item.value, ast.Constant):
                                        table_name = item.value.value
                    
                    if table_name:
                        output.append(f"**Table**: `{table_name}`\n\n")
                    
                    output.append("**Columns**:\n")
                    
                    # Extract columns
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    # Check if it's a Column
                                    if isinstance(item.value, ast.Call):
                                        if isinstance(item.value.func, ast.Name) and item.value.func.id == 'Column':
                                            col_name = target.id
                                            col_info = self._extract_column_info(item.value)
                                            output.append(f"- `{col_name}`: {col_info}\n")
                    
                    output.append("\n")
        
        # Write to file
        output_file = self.output_dir / "DATABASE_SCHEMA_CURRENT.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output)
        
        print(f"  ✅ Generated: {output_file.name}")
    
    def _extract_column_info(self, call_node) -> str:
        """Extract column type and constraints from Column() call"""
        parts = []
        
        # Get column type (first argument)
        if call_node.args:
            arg = call_node.args[0]
            if isinstance(arg, ast.Call):
                if isinstance(arg.func, ast.Name):
                    parts.append(arg.func.id)
                elif isinstance(arg.func, ast.Attribute):
                    parts.append(arg.func.attr)
        
        # Get constraints from keywords
        constraints = []
        for keyword in call_node.keywords:
            if keyword.arg in ['primary_key', 'unique', 'nullable', 'index']:
                if isinstance(keyword.value, ast.Constant):
                    if keyword.value.value:
                        constraints.append(keyword.arg)
        
        if constraints:
            parts.append(f"({', '.join(constraints)})")
        
        return ' '.join(parts) if parts else "Column"
    
    def generate_database_state(self):
        """Generate current database state with counts and samples"""
        print("📊 Generating DATABASE_STATE_CURRENT.md...")
        
        output = []
        output.append("# Current Database State - Auto-Generated\n\n")
        output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append(f"**Database**: {settings.POSTGRES_DB}\n\n")
        
        session = self.SessionLocal()
        
        try:
            # Get all tables
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            output.append("## Table Statistics\n\n")
            output.append("| Table | Row Count | Sample Available |\n")
            output.append("|-------|-----------|------------------|\n")
            
            table_stats = {}
            
            for table in sorted(tables):
                try:
                    # Get row count
                    result = session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    table_stats[table] = count
                    
                    sample_available = "✅" if count > 0 else "❌"
                    output.append(f"| {table} | {count:,} | {sample_available} |\n")
                except Exception as e:
                    output.append(f"| {table} | Error | ❌ |\n")
            
            output.append("\n")
            
            # Generate samples for key tables
            key_tables = ['trading_signals', 'slack_messages', 'trades', 'user_feedback', 'trader_reputation']
            
            output.append("## Sample Data\n\n")
            
            for table in key_tables:
                if table in table_stats and table_stats[table] > 0:
                    output.append(f"### {table}\n\n")
                    output.append(f"**Total Rows**: {table_stats[table]:,}\n\n")
                    
                    try:
                        # Get sample rows
                        result = session.execute(text(f"SELECT * FROM {table} LIMIT 3"))
                        rows = result.fetchall()
                        columns = result.keys()
                        
                        if rows:
                            output.append("**Sample Rows**:\n```json\n")
                            for row in rows:
                                row_dict = dict(zip(columns, row))
                                # Convert non-serializable types
                                for key, value in row_dict.items():
                                    if hasattr(value, 'isoformat'):
                                        row_dict[key] = value.isoformat()
                                    elif isinstance(value, (bytes, memoryview)):
                                        row_dict[key] = str(value)
                                output.append(json.dumps(row_dict, indent=2, default=str))
                                output.append("\n")
                            output.append("```\n\n")
                    except Exception as e:
                        output.append(f"*Error fetching samples: {e}*\n\n")
            
        finally:
            session.close()
        
        # Write to file
        output_file = self.output_dir / "DATABASE_STATE_CURRENT.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output)
        
        print(f"  ✅ Generated: {output_file.name}")
    
    def generate_api_endpoints(self):
        """Generate current API endpoints from route files"""
        print("🌐 Generating API_ENDPOINTS_CURRENT.md...")
        
        output = []
        output.append("# Current API Endpoints - Auto-Generated\n\n")
        output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Scan app/api directory
        api_dir = self.project_root / "app" / "api"
        
        for api_file in sorted(api_dir.glob("*.py")):
            if api_file.name == "__init__.py":
                continue
            
            module_name = api_file.stem
            output.append(f"## {module_name.title()} Endpoints\n\n")
            output.append(f"**File**: `app/api/{api_file.name}`\n\n")
            
            # Parse file to extract route decorators
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check for route decorators
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Attribute):
                                method = decorator.func.attr.upper()
                                if method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                                    # Get path
                                    if decorator.args:
                                        path = decorator.args[0]
                                        if isinstance(path, ast.Constant):
                                            output.append(f"### {method} {path.value}\n\n")
                                            output.append(f"**Function**: `{node.name}`\n\n")
                                            
                                            # Get docstring
                                            docstring = ast.get_docstring(node)
                                            if docstring:
                                                output.append(f"**Description**: {docstring.split(chr(10))[0]}\n\n")
            
            output.append("\n")
        
        # Write to file
        output_file = self.output_dir / "API_ENDPOINTS_CURRENT.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output)

        print(f"  ✅ Generated: {output_file.name}")

    def generate_services_inventory(self):
        """Generate services inventory"""
        print("🔧 Generating SERVICES_INVENTORY.md...")

        output = []
        output.append("# Services Inventory - Auto-Generated\n\n")
        output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Scan app/services directory
        services_dir = self.project_root / "app" / "services"

        for service_file in sorted(services_dir.rglob("*.py")):
            if service_file.name == "__init__.py":
                continue

            rel_path = service_file.relative_to(self.project_root)
            output.append(f"## {service_file.stem}\n\n")
            output.append(f"**File**: `{rel_path}`\n\n")

            # Parse file to extract classes
            with open(service_file, 'r', encoding='utf-8') as f:
                try:
                    tree = ast.parse(f.read())

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            output.append(f"### Class: `{node.name}`\n\n")

                            # Get docstring
                            docstring = ast.get_docstring(node)
                            if docstring:
                                output.append(f"{docstring.split(chr(10))[0]}\n\n")

                            # List methods
                            methods = [item.name for item in node.body if isinstance(item, ast.FunctionDef) and not item.name.startswith('_')]
                            if methods:
                                output.append("**Public Methods**:\n")
                                for method in methods[:10]:  # Limit to first 10
                                    output.append(f"- `{method}()`\n")
                                output.append("\n")
                except:
                    pass

            output.append("\n")

        # Write to file
        output_file = self.output_dir / "SERVICES_INVENTORY.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output)

        print(f"  ✅ Generated: {output_file.name}")

    def generate_agents_tools(self):
        """Generate agents and tools documentation"""
        print("🤖 Generating AGENTS_AND_TOOLS_CURRENT.md...")

        output = []
        output.append("# Agents and Tools - Auto-Generated\n\n")
        output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Scan agents
        agents_dir = self.project_root / "app" / "agents"
        output.append("## Agents\n\n")

        for agent_file in sorted(agents_dir.glob("*.py")):
            if agent_file.name == "__init__.py":
                continue

            output.append(f"### {agent_file.stem}\n\n")
            output.append(f"**File**: `app/agents/{agent_file.name}`\n\n")

            # Parse file
            with open(agent_file, 'r', encoding='utf-8') as f:
                try:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            if 'Agent' in node.name:
                                docstring = ast.get_docstring(node)
                                if docstring:
                                    output.append(f"{docstring.split(chr(10))[0]}\n\n")
                except:
                    pass

        # Scan tools
        tools_dir = self.project_root / "app" / "tools"
        output.append("\n## Tools by Category\n\n")

        tool_categories = defaultdict(list)

        for tool_file in sorted(tools_dir.rglob("*_tool.py")):
            category = tool_file.parent.name
            tool_name = tool_file.stem.replace('_tool', '')
            tool_categories[category].append((tool_name, tool_file))

        for category, tools in sorted(tool_categories.items()):
            output.append(f"### {category.replace('_', ' ').title()}\n\n")
            for tool_name, tool_file in tools:
                output.append(f"- **{tool_name}**: `{tool_file.relative_to(self.project_root)}`\n")
            output.append("\n")

        # Write to file
        output_file = self.output_dir / "AGENTS_AND_TOOLS_CURRENT.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output)

        print(f"  ✅ Generated: {output_file.name}")

    def generate_architecture_map(self):
        """Generate architecture overview"""
        print("🏗️ Generating ARCHITECTURE_MAP.md...")

        output = []
        output.append("# Architecture Map - Auto-Generated\n\n")
        output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        output.append("## Project Structure\n\n")
        output.append("```\n")
        output.append("TradePulse v4.0/\n")

        # Key directories
        key_dirs = [
            ("app/", "Main application code"),
            ("app/agents/", "4 specialized AI agents"),
            ("app/api/", "FastAPI endpoints"),
            ("app/core/", "Core configuration and utilities"),
            ("app/models/", "Database models and schemas"),
            ("app/services/", "Business logic services"),
            ("app/tools/", "Agent tools (39 total)"),
            ("docs/", "Documentation"),
            ("scripts/", "Utility scripts"),
            ("tests/", "Test suite"),
        ]

        for dir_path, description in key_dirs:
            output.append(f"├── {dir_path:<20} # {description}\n")

        output.append("```\n\n")

        output.append("## Tech Stack\n\n")
        output.append("- **Backend**: FastAPI (Python 3.11+)\n")
        output.append("- **Database**: PostgreSQL 14+ with pgvector\n")
        output.append("- **AI/ML**: Azure OpenAI (GPT-4, GPT-4 Vision)\n")
        output.append("- **LangChain**: Agent orchestration\n")
        output.append("- **Real-time**: WebSocket, Polygon.io\n")
        output.append("- **Data Sources**: Tavily, TradeZero, Slack\n\n")

        output.append("## 4-Agent Architecture\n\n")
        output.append("1. **Market Intelligence Agent** (27 tools)\n")
        output.append("   - Technical analysis, chart patterns, indicators\n")
        output.append("   - Level 2 data, float rotation, SSR tracking\n\n")

        output.append("2. **Community Intelligence Agent** (7 tools)\n")
        output.append("   - Slack message processing\n")
        output.append("   - Sentiment analysis, pattern recognition\n")
        output.append("   - Trader reputation tracking\n\n")

        output.append("3. **Personal Intelligence Agent** (4 tools)\n")
        output.append("   - TradeZero CSV import\n")
        output.append("   - Performance analytics\n")
        output.append("   - Risk management\n\n")

        output.append("4. **ML Intelligence Agent** (1 tool)\n")
        output.append("   - Neural forecasting\n")
        output.append("   - Pattern prediction\n\n")

        # Write to file
        output_file = self.output_dir / "ARCHITECTURE_MAP.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output)

        print(f"  ✅ Generated: {output_file.name}")

    def generate_index(self):
        """Generate index file for all living context"""
        print("📑 Generating INDEX.md...")

        output = []
        output.append("# Living Code Context - Index\n\n")
        output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append("**docFlow v3.0 - Layer 6: Living Code Context**\n\n")

        output.append("## 📚 Available Documents\n\n")
        output.append("1. **[DATABASE_SCHEMA_CURRENT.md](DATABASE_SCHEMA_CURRENT.md)** - Current database schema from models\n")
        output.append("2. **[DATABASE_STATE_CURRENT.md](DATABASE_STATE_CURRENT.md)** - Live database statistics and samples\n")
        output.append("3. **[API_ENDPOINTS_CURRENT.md](API_ENDPOINTS_CURRENT.md)** - All API endpoints\n")
        output.append("4. **[SERVICES_INVENTORY.md](SERVICES_INVENTORY.md)** - Services and their methods\n")
        output.append("5. **[AGENTS_AND_TOOLS_CURRENT.md](AGENTS_AND_TOOLS_CURRENT.md)** - Agents and tools catalog\n")
        output.append("6. **[ARCHITECTURE_MAP.md](ARCHITECTURE_MAP.md)** - System architecture overview\n\n")

        output.append("## 🎯 Purpose\n\n")
        output.append("This living context provides AI assistants with:\n")
        output.append("- **Current code state** (not just documentation)\n")
        output.append("- **Actual database state** (row counts, samples)\n")
        output.append("- **Real implementation details** (endpoints, services, tools)\n")
        output.append("- **Up-to-date architecture** (auto-generated)\n\n")

        output.append("## 🔄 Update Frequency\n\n")
        output.append("Run `python scripts/generate_living_context.py --all` to regenerate:\n")
        output.append("- Before major features\n")
        output.append("- After significant changes\n")
        output.append("- When starting new conversation\n")
        output.append("- On-demand as needed\n\n")

        output.append("## 💡 Integration\n\n")
        output.append("Load via `MASTER_CONTEXT_LOADER.md`:\n")
        output.append("```markdown\n")
        output.append("Load living code context from @docs/ai_context/living_code/INDEX.md\n")
        output.append("```\n")

        # Write to file
        output_file = self.output_dir / "INDEX.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output)

        print(f"  ✅ Generated: {output_file.name}")


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Generate Living Code Context for TradePulse v4.0")
    parser.add_argument('--all', action='store_true', help='Generate all context documents')
    parser.add_argument('--schema', action='store_true', help='Generate database schema only')
    parser.add_argument('--db-state', action='store_true', help='Generate database state only')
    parser.add_argument('--endpoints', action='store_true', help='Generate API endpoints only')
    parser.add_argument('--services', action='store_true', help='Generate services inventory only')
    parser.add_argument('--agents', action='store_true', help='Generate agents/tools only')
    parser.add_argument('--architecture', action='store_true', help='Generate architecture map only')

    args = parser.parse_args()

    generator = LivingContextGenerator()

    if args.all or not any([args.schema, args.db_state, args.endpoints, args.services, args.agents, args.architecture]):
        generator.generate_all()
    else:
        if args.schema:
            generator.generate_database_schema()
        if args.db_state:
            generator.generate_database_state()
        if args.endpoints:
            generator.generate_api_endpoints()
        if args.services:
            generator.generate_services_inventory()
        if args.agents:
            generator.generate_agents_tools()
        if args.architecture:
            generator.generate_architecture_map()
        generator.generate_index()


if __name__ == "__main__":
    main()


