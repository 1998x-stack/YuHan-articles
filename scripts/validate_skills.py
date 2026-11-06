#!/usr/bin/env python3
"""Validate portable Han Yu Agent Skills without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_PATHS = (
    Path(".opencode/skills/han-yu-argumentation/SKILL.md"),
    Path(".pi/skills/han-yu-argumentation/SKILL.md"),
)
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "prompts/han-yu-master-prompt.md",
    "prompts/han-yu-quick-prompt.md",
    "docs/method-and-evidence.md",
    "docs/quality-rubric.md",
    "examples/short-rewrite.md",
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    errors: list[str] = []
    contents: list[str] = []

    for relative in (*SKILL_PATHS, *(Path(p) for p in REQUIRED)):
        if not (ROOT / relative).is_file():
            errors.append(f"Missing file: {relative}")

    for relative in SKILL_PATHS:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_text(encoding="utf-8")
        contents.append(data)
        if not data.startswith("---\n"):
            errors.append(f"{relative}: missing opening YAML frontmatter")
            continue
        parts = data.split("---", 2)
        if len(parts) < 3 or not parts[2].strip():
            errors.append(f"{relative}: incomplete frontmatter or empty body")
            continue
        header = parts[1]
        match_name = re.search(r"^name:\s*(\S+)\s*$", header, re.MULTILINE)
        match_desc = re.search(r"^description:\s*(.+)\s*$", header, re.MULTILINE)
        name = match_name.group(1).strip() if match_name else ""
        description = match_desc.group(1).strip() if match_desc else ""
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append(f"{relative}: invalid name")
        if name != path.parent.name:
            errors.append(f"{relative}: name differs from directory")
        if not 1 <= len(description) <= 1024:
            errors.append(f"{relative}: description must have 1-1024 characters")
        if not data.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        if "../../../prompts/han-yu-master-prompt.md" not in data:
            errors.append(f"{relative}: missing optional canonical prompt link")

    if len(contents) == 2 and contents[0] != contents[1]:
        errors.append("OpenCode and Pi SKILL.md content differ")

    master = ROOT / "prompts/han-yu-master-prompt.md"
    if master.is_file():
        master_text = master.read_text(encoding="utf-8")
        for phrase in ("推原究本", "设难诘问", "辨名核实", "七维质量", "待改写原文"):
            if phrase not in master_text:
                errors.append(f"Master prompt missing topic: {phrase}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED ({len(errors)} issue(s))", file=sys.stderr)
        return 1

    print("OK: 2 matching portable Skills; frontmatter and required docs validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
