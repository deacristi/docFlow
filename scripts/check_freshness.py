#!/usr/bin/env python3
"""
docFlow v3.1 - Living Code Freshness Checker

Compares timestamps of documentation against source code
to detect when documentation may be stale.

Usage:
    python scripts/check_freshness.py
    
Exit Codes:
    0 - Documentation is fresh
    1 - Documentation is stale (needs regeneration)
    2 - Error occurred

Customize:
    - DOCS_DIR: Path to your documentation directory
    - SOURCE_DIRS: List of source code directories to check
"""

import sys
from pathlib import Path
from datetime import datetime

# Customize these for your project
DOCS_DIR = Path("docs/ai_context/living_code")
SOURCE_DIRS = [
    Path("src"),
    Path("app"),
    Path("lib"),
]


def get_newest_source_timestamp(directories: list[Path]) -> float:
    """Get the newest modification timestamp from source directories."""
    newest = 0.0
    
    for directory in directories:
        if not directory.exists():
            continue
        for file in directory.rglob("*.py"):
            try:
                mtime = file.stat().st_mtime
                if mtime > newest:
                    newest = mtime
            except (OSError, PermissionError):
                continue
    
    return newest


def get_oldest_docs_timestamp(docs_dir: Path) -> float:
    """Get the oldest modification timestamp from documentation files."""
    oldest = float('inf')
    
    if not docs_dir.exists():
        return oldest
    
    for file in docs_dir.glob("*.md"):
        try:
            mtime = file.stat().st_mtime
            if mtime < oldest:
                oldest = mtime
        except (OSError, PermissionError):
            continue
    
    return oldest


def format_timestamp(timestamp: float) -> str:
    """Format a timestamp as a human-readable string."""
    if timestamp == 0 or timestamp == float('inf'):
        return "N/A"
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def check_freshness() -> bool:
    """
    Compare documentation timestamps with source code.
    
    Returns:
        True if documentation is fresh, False if stale
    """
    # Check if docs directory exists
    if not DOCS_DIR.exists():
        print(f"⚠️  Documentation directory not found: {DOCS_DIR}")
        print(f"   Create documentation or update DOCS_DIR in this script")
        return False
    
    # Check if any doc files exist
    doc_files = list(DOCS_DIR.glob("*.md"))
    if not doc_files:
        print(f"⚠️  No documentation files found in: {DOCS_DIR}")
        return False
    
    # Get timestamps
    newest_source = get_newest_source_timestamp(SOURCE_DIRS)
    oldest_docs = get_oldest_docs_timestamp(DOCS_DIR)
    
    # Handle edge cases
    if newest_source == 0:
        print(f"⚠️  No source files found in configured directories")
        print(f"   Checked: {[str(d) for d in SOURCE_DIRS]}")
        return True  # Nothing to compare against
    
    if oldest_docs == float('inf'):
        print(f"⚠️  Could not read documentation file timestamps")
        return False
    
    # Compare timestamps
    print(f"📊 Documentation Freshness Check")
    print(f"   Newest source file:     {format_timestamp(newest_source)}")
    print(f"   Oldest documentation:   {format_timestamp(oldest_docs)}")
    print()
    
    if newest_source > oldest_docs:
        age_seconds = newest_source - oldest_docs
        age_hours = age_seconds / 3600
        age_days = age_hours / 24
        
        if age_days >= 1:
            age_str = f"{age_days:.1f} days"
        elif age_hours >= 1:
            age_str = f"{age_hours:.1f} hours"
        else:
            age_str = f"{age_seconds / 60:.0f} minutes"
        
        print(f"⚠️  Documentation is STALE by {age_str}")
        print(f"   Source code has been modified since documentation was generated.")
        print()
        print(f"   Consider regenerating your documentation.")
        return False
    else:
        freshness_seconds = oldest_docs - newest_source
        freshness_hours = freshness_seconds / 3600
        
        if freshness_hours >= 24:
            freshness_str = f"{freshness_hours / 24:.1f} days"
        elif freshness_hours >= 1:
            freshness_str = f"{freshness_hours:.1f} hours"
        else:
            freshness_str = f"{freshness_seconds / 60:.0f} minutes"
        
        print(f"✅ Documentation is FRESH")
        print(f"   Generated {freshness_str} after last source change.")
        return True


def main():
    """Main entry point."""
    try:
        is_fresh = check_freshness()
        sys.exit(0 if is_fresh else 1)
    except Exception as e:
        print(f"❌ Error checking freshness: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
