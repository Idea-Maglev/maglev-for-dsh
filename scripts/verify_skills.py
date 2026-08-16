#!/usr/bin/env python3
"""验证派生项目的技能是否符合 dsh skill 发现协议。

精确复刻 dsh 的 skill-filesystem 校验规则（packages/skill/skill-filesystem/src/index.ts）：
- 目录束 `<name>/SKILL.md`（或扁平 `<name>.md`）
- YAML frontmatter 必须存在且可解析
- name 必须满足 kebab-case（dsh 的 /^[a-z0-9]+(?:-[a-z0-9]+)*$/）
- name 必须与目录名一致（目录束场景）
- description 必须是非空字符串
- 顶层不得使用 legacy invocation 字段（disableModelInvocation / modelInvocable / userInvocable）

用法：
    python3 scripts/verify_skills.py --target /path/to/your-project
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("错误：需要 PyYAML。请先安装：pip install pyyaml")
    sys.exit(2)

# dsh 的 isSkillName 正则（packages/skill/skill/lib/index.js:17）
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# dsh 的 rejectLegacyInvocationKey 检查的旧字段名
LEGACY_INVOCATION_KEYS = ("disableModelInvocation", "modelInvocable", "userInvocable")


def parse_frontmatter(raw: str) -> dict | None:
    """复刻 dsh parseFrontmatter：首行必须是 ---，找 closing ---，yaml 解析。"""
    first_line_end = raw.find("\n")
    if first_line_end < 0:
        return None
    if raw[:first_line_end].replace("\r", "") != "---":
        return None
    start = first_line_end + 1
    line_start = start
    while line_start <= len(raw):
        next_newline = raw.find("\n", line_start)
        line_end = next_newline if next_newline >= 0 else len(raw)
        if raw[line_start:line_end].replace("\r", "") == "---":
            return {"data": yaml.safe_load(raw[start:line_start]), "body": raw[line_end + 1:]}
        if next_newline < 0:
            return None
        line_start = next_newline + 1
    return None


def string_field(data: dict, key: str) -> str | None:
    value = data.get(key)
    return value if isinstance(value, str) and len(value) > 0 else None


def verify_skill(skill_file: Path, expected_name: str | None) -> list[str]:
    """校验单个 SKILL.md，返回错误列表（空 = 通过）。"""
    errors: list[str] = []
    try:
        raw = skill_file.read_text(encoding="utf-8")
    except OSError as e:
        return [f"读取失败: {e}"]

    try:
        parsed = parse_frontmatter(raw)
    except yaml.YAMLError as e:
        return [f"YAML frontmatter 解析失败: {e}"]
    if parsed is None or parsed.get("data") is None:
        return ["缺 YAML frontmatter（首行必须为 ---）"]
    data = parsed["data"] if isinstance(parsed["data"], dict) else {}

    name = string_field(data, "name")
    description = string_field(data, "description")
    if name is None or description is None:
        return ["frontmatter 缺 name/description"]
    if not SKILL_NAME.match(name):
        return [f'name 非法（kebab-case）: "{name}"']
    if expected_name is not None and name != expected_name:
        return [f"name 与目录名不一致: {name} != {expected_name}"]
    for legacy in LEGACY_INVOCATION_KEYS:
        if legacy in data:
            errors.append(f"顶层使用了不支持的旧字段 {legacy}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="验证技能符合 dsh 发现协议")
    parser.add_argument(
        "--target",
        default=str(Path(__file__).resolve().parent.parent),
        help="目标项目路径（默认本仓库根）",
    )
    args = parser.parse_args()

    skills_dir = Path(args.target).resolve() / ".agents" / "skills"
    if not skills_dir.is_dir():
        print(f"错误：未找到 {skills_dir}")
        return 1

    total = 0
    failures: list[tuple[str, list[str]]] = []
    for entry in sorted(skills_dir.iterdir()):
        if entry.name == "_internal":
            continue  # 协议主体，非技能，dsh 会跳过无 SKILL.md 的目录
        if entry.is_dir():
            sk = entry / "SKILL.md"
            expected = entry.name
        elif entry.is_file() and entry.name.endswith(".md"):
            sk = entry
            expected = None
        else:
            continue
        total += 1
        errors = verify_skill(sk, expected)
        if errors:
            failures.append((entry.name, errors))

    print(f"=== dsh skill 发现协议验证 ===")
    print(f"通过: {total - len(failures)} 个技能")
    print(f"失败: {len(failures)} 个")
    for name, errors in failures:
        for e in errors:
            print(f"  ✗ {name}: {e}")
    if failures:
        print("结论: ✗ 存在不兼容项")
        return 1
    print("结论: ✓ 全部技能满足 dsh 发现协议（frontmatter + name kebab-case + description + invocation policy）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
