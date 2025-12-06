#!/usr/bin/env python3
"""
docFlow v3.1 - Checkpoint System

Creates and restores development state checkpoints for safe recovery.
Checkpoints include context files and metadata.

Usage:
    python scripts/checkpoint.py create <name> "<description>"
    python scripts/checkpoint.py restore <checkpoint_name>
    python scripts/checkpoint.py list
    python scripts/checkpoint.py delete <checkpoint_name>
    python scripts/checkpoint.py clean [--keep N]

Examples:
    python scripts/checkpoint.py create pre-refactor "Before major refactoring"
    python scripts/checkpoint.py list
    python scripts/checkpoint.py restore 20251206_143022_pre-refactor
"""

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

CHECKPOINT_DIR = Path(".docflow_checkpoints")

# Directories to backup (customize for your project)
BACKUP_DIRS = [
    "docs/ai_context/living_code",  # Living Code context
    ".kiro/steering",                # Kiro steering rules
    ".cursor/rules",                 # Cursor rules (if using Cursor)
]


def get_git_hash() -> str:
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()[:8]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def get_git_branch() -> str:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def get_uncommitted_changes() -> list[str]:
    """Get list of uncommitted changed files."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def create_checkpoint(name: str, description: str) -> Optional[str]:
    """
    Create a named checkpoint of current state.
    
    Args:
        name: Short name for the checkpoint (alphanumeric and hyphens)
        description: Human-readable description
        
    Returns:
        Checkpoint name if successful, None otherwise
    """
    # Sanitize name
    safe_name = "".join(c if c.isalnum() or c == "-" else "_" for c in name)
    
    # Create checkpoint directory
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_name = f"{timestamp}_{safe_name}"
    checkpoint_path = CHECKPOINT_DIR / checkpoint_name
    
    try:
        checkpoint_path.mkdir()
        
        # Save metadata
        metadata = {
            "name": name,
            "description": description,
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat(),
            "git_hash": get_git_hash(),
            "git_branch": get_git_branch(),
            "uncommitted_changes": get_uncommitted_changes(),
        }
        
        (checkpoint_path / "metadata.json").write_text(
            json.dumps(metadata, indent=2)
        )
        
        # Backup configured directories
        for dir_path in BACKUP_DIRS:
            src = Path(dir_path)
            if src.exists():
                dest_name = dir_path.replace("/", "_").replace(".", "_")
                shutil.copytree(src, checkpoint_path / dest_name)
                print(f"   📄 Saved {dir_path}")
        
        # Save git diff (uncommitted changes)
        try:
            result = subprocess.run(
                ["git", "diff"],
                capture_output=True,
                check=True
            )
            if result.stdout:
                (checkpoint_path / "uncommitted.patch").write_bytes(result.stdout)
                print(f"   🔧 Saved uncommitted changes as patch")
        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            pass
        
        print(f"\n✅ Checkpoint created: {checkpoint_name}")
        return checkpoint_name
        
    except Exception as e:
        print(f"❌ Failed to create checkpoint: {e}")
        if checkpoint_path.exists():
            shutil.rmtree(checkpoint_path, ignore_errors=True)
        return None


def restore_checkpoint(checkpoint_name: str) -> bool:
    """
    Restore from a checkpoint.
    
    Args:
        checkpoint_name: Name of checkpoint to restore
        
    Returns:
        True if successful, False otherwise
    """
    checkpoint_path = CHECKPOINT_DIR / checkpoint_name
    
    if not checkpoint_path.exists():
        # Try partial match
        matches = list(CHECKPOINT_DIR.glob(f"*{checkpoint_name}*"))
        if len(matches) == 1:
            checkpoint_path = matches[0]
            print(f"   Found matching checkpoint: {checkpoint_path.name}")
        elif len(matches) > 1:
            print(f"❌ Multiple checkpoints match '{checkpoint_name}':")
            for m in matches:
                print(f"   - {m.name}")
            return False
        else:
            print(f"❌ Checkpoint not found: {checkpoint_name}")
            return False
    
    try:
        # Load metadata
        metadata_file = checkpoint_path / "metadata.json"
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            print(f"📋 Checkpoint: {metadata.get('name', 'Unknown')}")
            print(f"   Description: {metadata.get('description', 'No description')}")
            print(f"   Created: {metadata.get('created_at', 'Unknown')}")
            print(f"   Git hash: {metadata.get('git_hash', 'Unknown')}")
            print()
        
        # Restore backed up directories
        for dir_path in BACKUP_DIRS:
            dest_name = dir_path.replace("/", "_").replace(".", "_")
            backup = checkpoint_path / dest_name
            if backup.exists():
                dest = Path(dir_path)
                if dest.exists():
                    shutil.rmtree(dest)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(backup, dest)
                print(f"   ✅ Restored {dir_path}")
        
        # Show patch info (don't auto-apply)
        patch_file = checkpoint_path / "uncommitted.patch"
        if patch_file.exists():
            print(f"   📄 Patch file available: {patch_file}")
            print(f"      To apply: git apply {patch_file}")
        
        print(f"\n✅ Restored from checkpoint: {checkpoint_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to restore checkpoint: {e}")
        return False


def list_checkpoints() -> None:
    """List all available checkpoints."""
    if not CHECKPOINT_DIR.exists():
        print("📭 No checkpoints found")
        print(f"   Create one with: python scripts/checkpoint.py create <name> \"<description>\"")
        return
    
    checkpoints = sorted(CHECKPOINT_DIR.iterdir(), reverse=True)
    
    if not checkpoints:
        print("📭 No checkpoints found")
        return
    
    print(f"📋 Available Checkpoints ({len(checkpoints)} total)")
    print("=" * 70)
    
    for cp in checkpoints:
        if not cp.is_dir():
            continue
            
        metadata_file = cp / "metadata.json"
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                name = metadata.get("name", "Unknown")
                desc = metadata.get("description", "No description")
                created = metadata.get("created_at", "Unknown")[:19]
                git_hash = metadata.get("git_hash", "?")
                
                if len(desc) > 40:
                    desc = desc[:37] + "..."
                
                print(f"\n  {cp.name}")
                print(f"    📝 {desc}")
                print(f"    🕐 {created}  |  🔗 {git_hash}")
            except json.JSONDecodeError:
                print(f"\n  {cp.name}")
                print(f"    ⚠️  Invalid metadata")
        else:
            print(f"\n  {cp.name}")
            print(f"    ⚠️  No metadata")


def delete_checkpoint(checkpoint_name: str) -> bool:
    """Delete a checkpoint."""
    checkpoint_path = CHECKPOINT_DIR / checkpoint_name
    
    if not checkpoint_path.exists():
        matches = list(CHECKPOINT_DIR.glob(f"*{checkpoint_name}*"))
        if len(matches) == 1:
            checkpoint_path = matches[0]
        elif len(matches) > 1:
            print(f"❌ Multiple checkpoints match '{checkpoint_name}':")
            for m in matches:
                print(f"   - {m.name}")
            return False
        else:
            print(f"❌ Checkpoint not found: {checkpoint_name}")
            return False
    
    try:
        shutil.rmtree(checkpoint_path)
        print(f"✅ Deleted checkpoint: {checkpoint_path.name}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete checkpoint: {e}")
        return False


def clean_checkpoints(keep: int = 5) -> None:
    """Remove old checkpoints, keeping the N most recent."""
    if not CHECKPOINT_DIR.exists():
        print("📭 No checkpoints to clean")
        return
    
    checkpoints = sorted(
        [cp for cp in CHECKPOINT_DIR.iterdir() if cp.is_dir()],
        reverse=True
    )
    
    if len(checkpoints) <= keep:
        print(f"✅ Only {len(checkpoints)} checkpoints exist, keeping all")
        return
    
    to_delete = checkpoints[keep:]
    print(f"🧹 Cleaning {len(to_delete)} old checkpoints (keeping {keep} most recent)")
    
    for cp in to_delete:
        try:
            shutil.rmtree(cp)
            print(f"   Deleted: {cp.name}")
        except Exception as e:
            print(f"   ❌ Failed to delete {cp.name}: {e}")
    
    print(f"✅ Cleanup complete")


def print_usage():
    """Print usage information."""
    print(__doc__)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "create":
        if len(sys.argv) < 4:
            print("❌ Usage: python scripts/checkpoint.py create <name> \"<description>\"")
            sys.exit(1)
        name = sys.argv[2]
        description = " ".join(sys.argv[3:])
        result = create_checkpoint(name, description)
        sys.exit(0 if result else 1)
        
    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ Usage: python scripts/checkpoint.py restore <checkpoint_name>")
            sys.exit(1)
        checkpoint_name = sys.argv[2]
        result = restore_checkpoint(checkpoint_name)
        sys.exit(0 if result else 1)
        
    elif command == "list":
        list_checkpoints()
        sys.exit(0)
        
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Usage: python scripts/checkpoint.py delete <checkpoint_name>")
            sys.exit(1)
        checkpoint_name = sys.argv[2]
        result = delete_checkpoint(checkpoint_name)
        sys.exit(0 if result else 1)
        
    elif command == "clean":
        keep = 5
        if len(sys.argv) >= 4 and sys.argv[2] == "--keep":
            try:
                keep = int(sys.argv[3])
            except ValueError:
                print("❌ --keep must be a number")
                sys.exit(1)
        clean_checkpoints(keep)
        sys.exit(0)
        
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
