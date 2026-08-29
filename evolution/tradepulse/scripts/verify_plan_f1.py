"""
verify_plan_f1.py — Plan reference verifier.

Usage:
    python scripts/verify_plan_f1.py docs/implementation_plans/<plan>.md

Per docs/docflow.md §4 — F1 Pre-Implementation Verification.

For every plan:
  1. Extract every `file:line` reference in the plan and confirm:
       - the cited line is in range for the live file,
       - any code snippet in the nearest python block matches the cited
         lines within a ±5-line tolerance.
  2. Exit 0 on success, 1 on any unrecoverable drift.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
SNIPPET_TOLERANCE_LINES = 5


@dataclass
class Ref:
    path: str
    line: int
    snippet: list[str] | None = None


def extract_references(plan_text: str) -> list[Ref]:
    """Walk the plan text and return one Ref per `file:line` reference.

    Each Ref's `snippet` is the content of the nearest preceding fenced
    python block (or None if there is no such block above the reference).
    """
    refs: list[Ref] = []
    last_python_block: list[str] = []
    in_block = False
    current_block: list[str] = []
    lines = plan_text.splitlines()

    for i, raw in enumerate(lines):
        stripped = raw.strip()
        if stripped.startswith("```python"):
            in_block = True
            current_block = []
            continue
        if in_block and stripped.startswith("```"):
            in_block = False
            last_python_block = current_block
            continue
        if in_block:
            current_block.append(raw)

        for m in re.finditer(r"`?([a-zA-Z0-9_./-]+\.py)[: ](?:line )?(\d+)`?", raw):
            path, line = m.group(1), int(m.group(2))
            if path.endswith(".py"):
                refs.append(Ref(path=path, line=line, snippet=last_python_block or None))

    return refs


def extract_references_existence_unchecked(plan_text: str) -> list[tuple[str, int]]:
    """Return [(file, line_no), ...] for every file:line reference.

    Existence is NOT pre-filtered here; the caller (main) does the
    single existence check.
    """
    refs: list[tuple[str, int]] = []
    for m in re.finditer(r"`?([a-zA-Z0-9_./-]+\.py)[: ](?:line )?(\d+)`?", plan_text):
        path, line = m.group(1), int(m.group(2))
        if path.endswith(".py"):
            refs.append((path, line))
    return refs


def line_in_range(file_path: Path, line_no: int) -> bool:
    """True if line_no is within the file.

    Re-raises any I/O / encoding error so the caller can see the
    underlying cause (e.g. permission denied, BOM-decoding error).
    """
    with file_path.open("r", encoding="utf-8", errors="strict") as f:
        for current, _ in enumerate(f, start=1):
            if current == line_no:
                return True
            if current > line_no:
                return False
    return False


def snippet_matches_file(snippet: Iterable[str], file_path: Path, near_line: int) -> bool:
    """Return True if every non-blank line in `snippet` appears within
    `SNIPPET_TOLERANCE_LINES` of `near_line` in `file_path`.

    Used to confirm that a plan's quoted code matches the live source.
    Snippets with zero non-blank lines (or only comments) match trivially.
    """
    if not snippet:
        return True
    lines = file_path.read_text(encoding="utf-8", errors="strict").splitlines()
    non_blank = [l.strip() for l in snippet if l.strip() and not l.strip().startswith("#")]
    if not non_blank:
        return True
    window_lo = max(0, near_line - SNIPPET_TOLERANCE_LINES - 1)
    window_hi = min(len(lines), near_line + SNIPPET_TOLERANCE_LINES)
    window = "\n".join(lines[window_lo:window_hi])
    return all(snip in window for snip in non_blank)


def main(argv: list[str]) -> int:
    """CLI entry point. Parses each file:line reference in the plan, verifies
    the file exists and the line number is in range; exits 0 if all references
    resolve, 1 on any unrecoverable drift. See docs/docflow_v4.md §4 — F1."""
    if len(argv) < 2:
        print("Usage: python scripts/verify_plan_f1.py <plan.md>", file=sys.stderr)
        return 2

    plan_path = Path(argv[1])
    if not plan_path.exists():
        print(f"FAIL: plan file not found: {plan_path}", file=sys.stderr)
        return 2

    text = plan_path.read_text(encoding="utf-8", errors="strict")
    refs = extract_references(text)

    print(f"Plan: {plan_path}")
    print(f"Refs found: {len(refs)}")

    failures: list[str] = []
    for ref in refs:
        abs_path = REPO_ROOT / ref.path
        # Single-point existence check
        if not abs_path.exists():
            failures.append(f"file not found: {ref.path}:{ref.line}")
            continue
        # Line-in-range
        try:
            if not line_in_range(abs_path, ref.line):
                failures.append(f"line drift: {ref.path}:{ref.line}")
                continue
        except (OSError, UnicodeDecodeError) as exc:
            failures.append(
                f"read-failed: {ref.path}:{ref.line} ({type(exc).__name__}: {exc})"
            )
            continue
        # Snippet match (only if a code block preceded the reference)
        if ref.snippet is not None:
            try:
                if not snippet_matches_file(ref.snippet, abs_path, ref.line):
                    failures.append(
                        f"snippet-mismatch: {ref.path}:{ref.line}"
                    )
            except (OSError, UnicodeDecodeError) as exc:
                failures.append(
                    f"read-failed: {ref.path}:{ref.line} ({type(exc).__name__}: {exc})"
                )

    if failures:
        print(f"\n{len(failures)} F1 issue(s):")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\n✅ F1 verification passed. All file:line refs in range; all snippets match.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
