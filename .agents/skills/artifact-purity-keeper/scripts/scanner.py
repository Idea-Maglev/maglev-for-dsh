#!/usr/bin/env python3
"""
scanner.py — AI 协作产物洁净度扫描器 v0.1

设计原则:
  1. 单文件零外部依赖 (stdlib only). yaml 规则文件用 try-import, 缺则降级.
  2. 不绑任何项目结构, 接受任意路径作输入.
  3. 默认 dry-run 仅识别报告; --fix-interactive 才进入逐条修复.
  4. 规则集与代码分离 (--rules 指定 yaml/json), 用户可自定义.

用法:
  scanner.py [paths...]
  scanner.py --rules my_rules.yaml docs/
  scanner.py --severity hard --format json README.md
  scanner.py --fix-interactive path/to/file.md

退出码:
  0 - 无 hard 级 finding
  1 - 含 hard 级 finding
  2 - 参数/规则文件错误
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    import yaml as _yaml  # noqa
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

DEFAULT_RULES_PATH = Path(__file__).parent / "rules.yaml"
SEVERITY_RANK = {"hard": 3, "soft": 2, "info": 1}
SEVERITY_ICON = {"hard": "🔴", "soft": "🟡", "info": "🔵"}


@dataclass
class Rule:
    id: str
    severity: str
    category: str
    description: str
    pattern: re.Pattern
    exclude_paths: list[re.Pattern] = field(default_factory=list)


@dataclass
class Finding:
    file: Path
    line_num: int
    line_text: str
    rule: Rule
    match_text: str
    match_start: int
    match_end: int


def load_rules(rules_path: Path) -> tuple[list[Rule], list[re.Pattern], list[str]]:
    """Load rule set from YAML/JSON. Returns (rules, default_excludes, default_exts)."""
    if not rules_path.exists():
        sys.stderr.write(f"[ERROR] Rules file not found: {rules_path}\n")
        sys.exit(2)
    text = rules_path.read_text(encoding="utf-8")
    if rules_path.suffix in (".yaml", ".yml"):
        if not _HAS_YAML:
            sys.stderr.write("[ERROR] PyYAML not installed; use JSON rules or `pip install pyyaml`\n")
            sys.exit(2)
        data = _yaml.safe_load(text)
    else:
        data = json.loads(text)

    rules: list[Rule] = []
    for r in data.get("rules", []):
        try:
            rules.append(Rule(
                id=r["id"],
                severity=r["severity"],
                category=r["category"],
                description=r.get("description", ""),
                pattern=re.compile(r["pattern"]),
                exclude_paths=[re.compile(p) for p in r.get("exclude_paths", [])],
            ))
        except (KeyError, re.error) as e:
            sys.stderr.write(f"[WARN] Skip invalid rule {r.get('id', '?')}: {e}\n")

    default_excludes = [re.compile(p) for p in data.get("default_exclude_paths", [])]
    default_exts = data.get("default_extensions", [".md", ".txt"])
    return rules, default_excludes, default_exts


def iter_target_files(
    paths: list[Path],
    extensions: list[str],
    excludes: list[re.Pattern],
) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            yield path
            continue
        if not path.is_dir():
            continue
        for root, dirs, files in os.walk(path):
            root_p = Path(root)
            rel = str(root_p)
            if any(p.search(rel) for p in excludes):
                dirs[:] = []
                continue
            for f in files:
                fp = root_p / f
                if extensions and fp.suffix not in extensions:
                    continue
                if any(p.search(str(fp)) for p in excludes):
                    continue
                yield fp


def is_rules_file(file: Path) -> bool:
    """识别 purity 规则文件: yaml/json 含顶层 'rules:' 或 '"rules":' 且子项含 'pattern:'.

    避免规则文件中的字面量被自身扫描误报为污染.
    """
    if file.suffix not in (".yaml", ".yml", ".json"):
        return False
    try:
        content = file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    has_rules_key = re.search(r'^\s*"?rules"?\s*:', content, re.MULTILINE) is not None
    has_pattern_field = re.search(r'^\s*-?\s*"?pattern"?\s*:', content, re.MULTILINE) is not None
    return has_rules_key and has_pattern_field


def scan_file(file: Path, rules: list[Rule]) -> list[Finding]:
    findings: list[Finding] = []
    if is_rules_file(file):
        return findings
    try:
        lines = file.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return findings
    file_str = str(file)
    for line_num, line in enumerate(lines, 1):
        for rule in rules:
            if any(p.search(file_str) for p in rule.exclude_paths):
                continue
            for m in rule.pattern.finditer(line):
                findings.append(Finding(
                    file=file,
                    line_num=line_num,
                    line_text=line,
                    rule=rule,
                    match_text=m.group(0),
                    match_start=m.start(),
                    match_end=m.end(),
                ))
    return findings


def filter_severity(findings: list[Finding], min_severity: str) -> list[Finding]:
    threshold = SEVERITY_RANK[min_severity]
    return [f for f in findings if SEVERITY_RANK[f.rule.severity] >= threshold]


def render_markdown(findings: list[Finding]) -> str:
    if not findings:
        return "✅ No findings.\n"
    by_severity: dict[str, list[Finding]] = {}
    for f in findings:
        by_severity.setdefault(f.rule.severity, []).append(f)

    out = ["# Artifact Purity Scan Report\n"]
    out.append(f"**Total findings**: {len(findings)}\n")
    counts = ", ".join(f"{SEVERITY_ICON[s]} {s}: {len(by_severity.get(s, []))}"
                       for s in ("hard", "soft", "info") if s in by_severity)
    out.append(f"**By severity**: {counts}\n")

    for sev in ("hard", "soft", "info"):
        items = by_severity.get(sev, [])
        if not items:
            continue
        out.append(f"\n## {SEVERITY_ICON[sev]} {sev.upper()} ({len(items)})\n")
        out.append("| File | Line | Rule | Match |")
        out.append("|------|------|------|-------|")
        for f in items:
            snippet = f.match_text.replace("|", "\\|")
            out.append(f"| `{f.file}` | {f.line_num} | {f.rule.id} ({f.rule.category}) | `{snippet}` |")
        out.append("")
    return "\n".join(out) + "\n"


def render_json(findings: list[Finding]) -> str:
    return json.dumps([{
        "file": str(f.file),
        "line": f.line_num,
        "line_text": f.line_text,
        "rule_id": f.rule.id,
        "severity": f.rule.severity,
        "category": f.rule.category,
        "match": f.match_text,
        "start": f.match_start,
        "end": f.match_end,
    } for f in findings], ensure_ascii=False, indent=2)


def interactive_fix(findings: list[Finding]) -> int:
    """Iterate findings, prompt user for action: skip / delete / edit. Return num fixed."""
    fixed = 0
    files_to_save: dict[Path, list[str]] = {}

    for i, f in enumerate(findings, 1):
        if f.file not in files_to_save:
            files_to_save[f.file] = f.file.read_text(encoding="utf-8").splitlines()
        lines = files_to_save[f.file]
        cur_line = lines[f.line_num - 1]

        sys.stderr.write(f"\n[{i}/{len(findings)}] {SEVERITY_ICON[f.rule.severity]} {f.rule.id} - {f.rule.category}\n")
        sys.stderr.write(f"  File: {f.file}:{f.line_num}\n")
        sys.stderr.write(f"  Line: {cur_line}\n")
        sys.stderr.write(f"  Match: '{f.match_text}'\n")
        sys.stderr.write("  Action [s=skip, d=delete match, e=edit line, q=quit]: ")
        sys.stderr.flush()
        try:
            choice = input().strip().lower()
        except EOFError:
            break

        if choice == "q":
            break
        elif choice == "s" or choice == "":
            continue
        elif choice == "d":
            new_line = cur_line[:f.match_start] + cur_line[f.match_end:]
            new_line = re.sub(r"\s+", " ", new_line).rstrip()
            lines[f.line_num - 1] = new_line
            fixed += 1
        elif choice == "e":
            sys.stderr.write(f"  New line: ")
            sys.stderr.flush()
            try:
                new_line = input()
                lines[f.line_num - 1] = new_line
                fixed += 1
            except EOFError:
                break

    for fp, lines in files_to_save.items():
        fp.write_text("\n".join(lines) + ("\n" if lines and not lines[-1].endswith("\n") else ""), encoding="utf-8")

    return fixed


def main():
    parser = argparse.ArgumentParser(description="AI 协作产物洁净度扫描器 v0.1")
    parser.add_argument("paths", nargs="+", type=Path, help="要扫描的文件或目录")
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES_PATH, help="规则文件 (yaml/json)")
    parser.add_argument("--severity", choices=["hard", "soft", "info"], default="info",
                        help="最低 severity (默认 info, 即全部)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--fix-interactive", action="store_true",
                        help="逐条提示修复 (s/d/e/q). 不指定时仅 dry-run 报告.")
    parser.add_argument("--exclude", action="append", default=[],
                        help="额外排除路径正则 (可多次)")
    args = parser.parse_args()

    rules, default_excludes, default_exts = load_rules(args.rules)
    excludes = default_excludes + [re.compile(p) for p in args.exclude]

    targets = list(iter_target_files(args.paths, default_exts, excludes))
    findings: list[Finding] = []
    for f in targets:
        findings.extend(scan_file(f, rules))
    findings = filter_severity(findings, args.severity)

    if args.fix_interactive:
        n_fixed = interactive_fix(findings)
        sys.stderr.write(f"\n✓ Fixed {n_fixed}/{len(findings)} findings.\n")
        return 0 if n_fixed == len(findings) else 1

    if args.format == "json":
        sys.stdout.write(render_json(findings))
    else:
        sys.stdout.write(render_markdown(findings))

    has_hard = any(f.rule.severity == "hard" for f in findings)
    return 1 if has_hard else 0


if __name__ == "__main__":
    sys.exit(main())
