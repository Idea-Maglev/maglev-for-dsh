#!/usr/bin/env python3
"""spec_integrity_check.py — Maglev for DSH 项目 spec 完整性检查

验证一个 Maglev for DSH 派生的项目是否具备完整的知识资产结构与治理骨架。
这是"验证门禁机械化"的核心：不依赖模型自觉，而是用可执行的机械约束检查。

用法:
    python3 spec_integrity_check.py [--root <project_root>] [--json]

退出码:
    0  无 FAIL
    1  存在 FAIL
    2  参数/路径错误

检查项以注册式组织，可扩展。设计上跨宿主（dsh / Claude Code / Codex 均可通过
bash 调用），保证验证结论不随 AI 体系漂移。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Tuple

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"

Result = Tuple[str, str, str]  # (level, check_name, detail)

# Maglev 知识分层骨架目录（相对项目根）
SPECS_SKELETON_DIRS = [
    "specs/00_vision",
    "specs/10_reality",
    "specs/20_evolution/active",
    "specs/90_archive",
]

# 主链路技能（相对 .agents/skills/）
MAINLINE_SKILLS = [
    "entry-router",
    "reality-sync",
    "requirement-convergence",
    "spec-designer",
    "integrated-validator",
    "crystallization",
    "maglev-discipline",
]

# AGENTS.md 纪律区块 marker（与 Maglev installer 对齐）
DISCIPLINE_MARKER_START = "<!-- maglev:managed:discipline -->"
DISCIPLINE_MARKER_END = "<!-- /maglev:managed:discipline -->"


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_specs_skeleton(root: Path) -> List[Result]:
    """检查 specs/ 知识分层骨架目录齐全。"""
    results: List[Result] = []
    for rel in SPECS_SKELETON_DIRS:
        if (root / rel).is_dir():
            results.append((PASS, "specs_skeleton", rel))
        else:
            results.append((FAIL, "specs_skeleton", f"{rel} (missing)"))
    return results


def check_specs_readme(root: Path) -> List[Result]:
    """检查 specs/README.md 存在且非空（≥3 非空行）。"""
    path = root / "specs" / "README.md"
    if not path.is_file():
        return [(FAIL, "specs_readme", "specs/README.md (missing)")]
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return [(FAIL, "specs_readme", "specs/README.md (unreadable)")]
    non_blank = sum(1 for line in lines if line.strip())
    if non_blank < 3:
        return [(FAIL, "specs_readme", f"specs/README.md ({non_blank} lines, too short)")]
    return [(PASS, "specs_readme", f"specs/README.md ({non_blank} lines)")]


def check_discipline_block(root: Path) -> List[Result]:
    """检查 AGENTS.md 含会话纪律区块 marker。"""
    path = root / "AGENTS.md"
    if not path.is_file():
        return [(FAIL, "discipline_block", "AGENTS.md (missing)")]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return [(FAIL, "discipline_block", "AGENTS.md (unreadable)")]
    start = DISCIPLINE_MARKER_START in text
    end = DISCIPLINE_MARKER_END in text
    if start and end:
        return [(PASS, "discipline_block", "AGENTS.md")]
    missing = []
    if not start:
        missing.append("start marker")
    if not end:
        missing.append("end marker")
    return [(FAIL, "discipline_block", f"AGENTS.md (missing {', '.join(missing)})")]


def check_mainline_skills(root: Path) -> List[Result]:
    """检查主链路技能 SKILL.md 存在。"""
    results: List[Result] = []
    skills_dir = root / ".agents" / "skills"
    if not skills_dir.is_dir():
        return [(FAIL, "mainline_skills", ".agents/skills (missing)")]
    for name in MAINLINE_SKILLS:
        sk = skills_dir / name / "SKILL.md"
        if sk.is_file():
            results.append((PASS, "mainline_skills", name))
        else:
            results.append((FAIL, "mainline_skills", f"{name} (missing SKILL.md)"))
    return results


def check_llms_txt(root: Path) -> List[Result]:
    """检查 llms.txt 存在。"""
    if (root / "llms.txt").is_file():
        return [(PASS, "llms_txt", "llms.txt")]
    return [(FAIL, "llms_txt", "llms.txt (missing)")]


def check_reality_record(root: Path) -> List[Result]:
    """检查 specs/10_reality/README.md 存在且非空（当前事实已结晶）。"""
    path = root / "specs" / "10_reality" / "README.md"
    if not path.is_file():
        return [(FAIL, "reality_record", "specs/10_reality/README.md (missing)")]
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return [(FAIL, "reality_record", "specs/10_reality/README.md (unreadable)")]
    non_blank = sum(1 for line in lines if line.strip())
    if non_blank < 5:
        return [(FAIL, "reality_record", f"specs/10_reality/README.md ({non_blank} lines, too short)")]
    return [(PASS, "reality_record", f"specs/10_reality/README.md ({non_blank} lines)")]


# ---------------------------------------------------------------------------
# Registry & Runner
# ---------------------------------------------------------------------------

UNIVERSAL_CHECKS = [
    check_specs_skeleton,
    check_specs_readme,
    check_discipline_block,
    check_mainline_skills,
    check_llms_txt,
    check_reality_record,
]


def run_checks(root: Path) -> List[Result]:
    results: List[Result] = []
    for check_fn in UNIVERSAL_CHECKS:
        results.extend(check_fn(root))
    return results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_text(results: List[Result]) -> str:
    lines = [f"[{level}] {name}   {detail}" for level, name, detail in results]
    lines.append("---")
    counts = {PASS: 0, WARN: 0, FAIL: 0}
    for level, _, _ in results:
        counts[level] = counts.get(level, 0) + 1
    lines.append(f"summary: pass={counts[PASS]} warn={counts[WARN]} fail={counts[FAIL]}")
    return "\n".join(lines)


def format_json(results: List[Result]) -> str:
    output = {
        "results": [
            {"level": level, "check": name, "detail": detail}
            for level, name, detail in results
        ],
        "summary": {
            "pass": sum(1 for r in results if r[0] == PASS),
            "warn": sum(1 for r in results if r[0] == WARN),
            "fail": sum(1 for r in results if r[0] == FAIL),
        },
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Maglev for DSH 项目 spec 完整性检查"
    )
    parser.add_argument("--root", default=".", help="项目根路径（默认当前目录）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: '{args.root}' is not a directory", file=sys.stderr)
        return 2

    results = run_checks(root)
    if args.json:
        print(format_json(results))
    else:
        print(format_text(results))

    has_fail = any(r[0] == FAIL for r in results)
    return 1 if has_fail else 0


if __name__ == "__main__":
    sys.exit(main())
