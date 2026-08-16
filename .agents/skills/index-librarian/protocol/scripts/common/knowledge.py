"""Deterministic knowledge extraction for adjacent ``INDEX.md`` files."""

from __future__ import annotations

import hashlib
import fnmatch
import json
import re
from pathlib import Path
from typing import Any

import yaml

from .frontmatter import parse_any_frontmatter
from .ignore import IndexIgnorePolicy, should_skip_entry


TEXT_EXTENSIONS = frozenset({
    ".md", ".mdx", ".rst", ".txt", ".yaml", ".yml", ".json", ".toml",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".zsh", ".bash",
    ".go", ".rs", ".java", ".rb", ".php", ".c", ".h", ".cpp", ".hpp",
    ".css", ".html", ".xml", ".sql",
})
MAX_KNOWLEDGE_BYTES = 256 * 1024
SENSITIVE_SUFFIXES = frozenset({".key", ".pem", ".p12", ".pfx", ".crt", ".cer"})
SENSITIVE_NAMES = frozenset({"id_rsa", "id_ed25519", ".env", ".npmrc", ".netrc"})
SENSITIVE_PATH_PARTS = frozenset({"private", "secrets", "credentials"})
_WORDS = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,}|[\u4e00-\u9fff]{2,}")
_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
_COMMENT = re.compile(r"^\s*(?:#|//|/\*|\*)\s*(.+?)\s*$", re.MULTILINE)
_LOW_SIGNAL_TOPICS = frozenset({
    "为什么要把",
    "没有",
    "不是",
    "而是",
    "目录说明",
    "先说结论",
    "先知道这是什么",
    "什么时候该用",
    "最小接入流程",
    "这篇文档适合谁",
    "这轮在反思什么",
    "这轮验证在看什么",
})
_LOW_SIGNAL_PREFIXES = (
    "先看一个",
    "先说一个",
    "如果你只想知道",
    "用这个",
    "一个更像",
    "如果把这个",
    "如果把它",
)
_LOW_SIGNAL_SUBSTRINGS = frozenset({
    "真实样本",
    "真实场景",
    "更接近真实的场景",
})
_REFERENCE_LOW_SIGNAL_TOPICS = frozenset({
    "步骤",
    "可用状态",
    "状态",
    "执行序列",
    "执行逻辑",
    "下一步指令",
    "成功指标",
    "失败模式",
})
_ENGLISH_STOPWORDS = frozenset({
    "the",
    "and",
    "or",
})
_CJK_PREFIX_CHARS = "的"
_CJK_SUFFIX_CHARS = "的与和及或"
MAX_TOPICS = 6
MAX_NAVIGATION_TOPICS = 4


def content_fingerprint(path: Path) -> str:
    """Return the SHA-256 fingerprint used for freshness checks."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tokens(value: str) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()

    def add(token: str) -> None:
        # Headings often repeat common labels such as "目标"; keep the first
        # occurrence so topic order remains meaningful without duplicate noise.
        if token not in seen:
            seen.add(token)
            tokens.append(token)

    for item in _WORDS.findall(value):
        normalized = _normalize_topic(item)
        if normalized:
            add(normalized)
    return tokens[:MAX_TOPICS]


def _normalize_topic(value: str) -> str:
    topic = value.strip().lower()
    if not topic:
        return ""
    if topic in _ENGLISH_STOPWORDS:
        return ""
    if re.fullmatch(r"[\u4e00-\u9fff]+", topic):
        topic = topic.lstrip(_CJK_PREFIX_CHARS)
        if len(topic) <= 5:
            topic = topic.rstrip(_CJK_SUFFIX_CHARS)
        if topic in _LOW_SIGNAL_TOPICS:
            return ""
        if any(topic.startswith(prefix) for prefix in _LOW_SIGNAL_PREFIXES):
            return ""
        if any(fragment in topic for fragment in _LOW_SIGNAL_SUBSTRINGS):
            return ""
    return topic


def _slug(value: str) -> str:
    compact = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", value).strip("-")
    return compact or "content"


def _markdown_description(text: str) -> tuple[str, list[str], list[str]]:
    headings = _HEADING.findall(text)
    summary = headings[0] if headings else ""
    if not summary:
        for paragraph in re.split(r"\n\s*\n", text):
            normalized = " ".join(line.strip() for line in paragraph.splitlines())
            if normalized and not normalized.startswith("---"):
                summary = normalized[:160]
                break
    topics = _tokens(" ".join(headings[:4]) or summary)
    evidence = [f"#{_slug(headings[0])}"] if headings else [":1"]
    return summary or "Markdown document", topics, evidence


def _filter_topics_for_path(path: Path, topics: list[str]) -> list[str]:
    if "references" not in path.parts:
        return topics[:MAX_TOPICS]
    filtered = [topic for topic in topics if topic not in _REFERENCE_LOW_SIGNAL_TOPICS]
    return filtered[:MAX_TOPICS]


def _structured_description(path: Path, text: str) -> tuple[str, list[str], list[str]]:
    try:
        data = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError):
        return "Structured text with invalid syntax", _tokens(path.stem), [":1"]
    if isinstance(data, dict):
        keys = [str(key) for key in list(data)[:8]]
        title = str(data.get("title") or data.get("name") or path.stem)
        return title, _tokens(" ".join(keys + [title])), [f":{key}" for key in keys[:3]] or [":1"]
    return f"{path.suffix.lstrip('.').upper()} value", _tokens(path.stem), [":1"]


def _source_description(path: Path, text: str) -> tuple[str, list[str], list[str]]:
    comment = _COMMENT.search(text)
    summary = comment.group(1) if comment else f"Source file {path.name}"
    return summary[:160], _tokens(f"{path.stem} {summary}"), [":1"]


def build_knowledge_record(path: Path, root_dir: Path, repository_root: Path | None = None) -> dict[str, Any]:
    """Extract a conservative, traceable record for one leaf file."""
    relative = path.relative_to(repository_root or root_dir).as_posix()
    record: dict[str, Any] = {
        "id": f"file:{relative}",
        "path": relative,
        "local_path": path.name,
        "kind": path.suffix.lstrip(".").lower() or "file",
        "content_fingerprint": "",
        "freshness": "current",
        "summary": "",
        "topics": [],
        "answers": [],
        "constraints": [],
        "evidence": [],
        "parse_status": "indexed",
    }
    path_parts = {part.casefold() for part in path.parts}
    if path.name.casefold() in SENSITIVE_NAMES or path.suffix.casefold() in SENSITIVE_SUFFIXES or path_parts & SENSITIVE_PATH_PARTS:
        record.update({"parse_status": "excluded", "degradation_reason": "sensitive_path"})
        return record
    record["content_fingerprint"] = content_fingerprint(path)
    raw = path.read_bytes()
    if b"\0" in raw:
        record.update({"parse_status": "degraded", "degradation_reason": "binary_content"})
        return record
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        record.update({"parse_status": "degraded", "degradation_reason": "unsupported_extension"})
        return record
    if len(raw) > MAX_KNOWLEDGE_BYTES:
        record.update({"parse_status": "degraded", "degradation_reason": "size_limit"})
        return record
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        record.update({"parse_status": "degraded", "degradation_reason": "non_utf8_text"})
        return record

    suffix = path.suffix.lower()
    if suffix in {".md", ".mdx", ".rst", ".txt"}:
        summary, topics, evidence = _markdown_description(text)
    elif suffix in {".yaml", ".yml", ".json", ".toml"}:
        summary, topics, evidence = _structured_description(path, text)
    else:
        summary, topics, evidence = _source_description(path, text)
    record["summary"] = summary
    record["topics"] = _filter_topics_for_path(path, topics)
    record["answers"] = [summary]
    record["evidence"] = [f"{relative}{item}" for item in evidence]
    return record


def _is_sensitive_path(path: Path) -> bool:
    parts = {part.casefold() for part in path.parts}
    return path.name.casefold() in SENSITIVE_NAMES or path.suffix.casefold() in SENSITIVE_SUFFIXES or bool(parts & SENSITIVE_PATH_PARTS)


def collapsed_leaf_file(
    directory: Path,
    root_dir: Path,
    ignore: set[str] | IndexIgnorePolicy,
    patterns: set[str] | None,
) -> Path | None:
    """Return the only content file when a configured leaf directory can collapse."""
    if not patterns:
        return None
    relative = directory.relative_to(root_dir).as_posix()
    if not any(fnmatch.fnmatch(relative, pattern) for pattern in patterns):
        return None
    if (directory / "README.md").exists():
        return None

    children = [
        child
        for child in directory.iterdir()
        if not should_skip_entry(child, ignore)
        and child.name.casefold() not in {"index.md", "readme.md"}
    ]
    files = [child for child in children if child.is_file()]
    if len(children) != 1 or len(files) != 1:
        return None
    return files[0]


def _directory_record(
    directory: Path,
    root_dir: Path,
    ignore: set[str] | IndexIgnorePolicy,
    repository_root: Path | None,
) -> dict[str, Any] | None:
    """Project a child directory's own entry material into its parent INDEX."""
    if _is_sensitive_path(directory):
        return None
    rel = directory.relative_to(repository_root or root_dir).as_posix()
    index_path = directory / "INDEX.md"
    readme_path = directory / "README.md"
    profile: dict[str, Any] = {}
    index_content = ""
    if index_path.is_file():
        parsed = parse_any_frontmatter(index_path)
        raw_profile = parsed.metadata.get("directory_profile")
        if isinstance(raw_profile, dict):
            profile = raw_profile
        index_content = parsed.content

    evidence: list[str]
    if isinstance(profile.get("summary"), str) and profile["summary"].strip():
        summary = profile["summary"].strip()
        topics = [str(item) for item in profile.get("topics", []) if isinstance(item, (str, int, float))] or _tokens(summary)
        answers = [str(item) for item in profile.get("answers", []) if isinstance(item, (str, int, float))] or [summary]
        evidence = [f"{rel}/INDEX.md:directory_profile"]
    elif readme_path.is_file() and not _is_sensitive_path(readme_path):
        readme = build_knowledge_record(readme_path, root_dir, repository_root)
        summary, topics, answers, evidence = readme["summary"], readme["topics"], readme["answers"], readme["evidence"]
    elif _has_authored_index_content(index_content, directory.name):
        summary, topics, anchor = _markdown_description(index_content)
        answers = [summary]
        evidence = [f"{rel}/INDEX.md{item}" for item in anchor]
    else:
        summary, topics = _structural_directory_fallback(directory, ignore)
        answers, evidence = [summary], [f"{rel}/INDEX.md"]

    child_count = sum(
        1
        for child in directory.iterdir()
        if not should_skip_entry(child, ignore)
        and child.name.casefold() not in {"index.md", "readme.md"}
    )
    return {
        "id": f"directory:{rel}",
        "path": f"{rel}/",
        "local_path": f"{directory.name}/",
        "kind": "directory",
        "directory_index": f"{rel}/INDEX.md",
        "content_fingerprint": content_fingerprint(index_path) if index_path.is_file() else "",
        "freshness": "current",
        "summary": summary,
        "topics": topics,
        "answers": answers,
        "constraints": [],
        "evidence": evidence,
        "child_count": child_count,
        "parse_status": "indexed",
        "navigation_role": "route",
    }


def _structural_directory_fallback(
    directory: Path,
    ignore: set[str] | IndexIgnorePolicy,
) -> tuple[str, list[str]]:
    visible_children = [
        child
        for child in sorted(directory.iterdir())
        if not should_skip_entry(child, ignore)
        and child.name.casefold() not in {"index.md", "readme.md"}
    ]
    count = len(visible_children)
    if count == 0:
        return "Directory containing 0 visible item(s)", _tokens(directory.name)

    descriptors: list[str] = []
    topic_seed = [directory.name]
    for child in visible_children[:2]:
        descriptor = child.stem if child.is_file() else child.name
        if child.is_file() and child.suffix.lower() in {".md", ".mdx", ".rst", ".txt"} and not _is_sensitive_path(child):
            child_record = build_knowledge_record(child, directory, directory)
            if child_record.get("summary"):
                descriptor = str(child_record["summary"])
            topic_seed.extend(child_record.get("topics") or [])
        else:
            topic_seed.append(descriptor)
        descriptors.append(descriptor)

    summary = f"{directory.name} 目录入口，包含 {count} 个可见对象"
    if descriptors:
        summary = f"{summary}：{ '、'.join(descriptors) }"
        if count > len(descriptors):
            summary = f"{summary} 等"
    return summary, _tokens(" ".join(topic_seed))


def _has_authored_index_content(content: str, directory_name: str) -> bool:
    """Avoid presenting the generator's own title/table as a semantic directory summary."""
    content = re.sub(
        r"\n?<!-- index-librarian:knowledge-start -->.*?<!-- index-librarian:knowledge-end -->\n?",
        "\n",
        content,
        flags=re.DOTALL,
    )
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if lines and lines[0].casefold() == f"# {directory_name}".casefold():
        lines.pop(0)
    meaningful = [line for line in lines if not line.startswith("|")]
    return bool(meaningful)


def build_directory_records(
    directory: Path,
    root_dir: Path,
    ignore: set[str] | IndexIgnorePolicy,
    repository_root: Path | None = None,
    collapse_single_file_dirs: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Build direct file records and projected records for public child directories."""
    records = []
    for child in sorted(directory.iterdir()):
        if should_skip_entry(child, ignore) or child.name.casefold() == "index.md":
            continue
        if child.is_dir():
            leaf_file = collapsed_leaf_file(
                child, root_dir, ignore, collapse_single_file_dirs
            )
            if leaf_file is not None:
                records.append(build_knowledge_record(leaf_file, root_dir, repository_root))
                continue
            record = _directory_record(child, root_dir, ignore, repository_root)
            if record:
                records.append(record)
        elif child.is_file():
            records.append(build_knowledge_record(child, root_dir, repository_root))
    return records


def build_navigation_block(records: list[dict[str, Any]]) -> str:
    """Render the generated human view while records remain in frontmatter."""
    lines = ["<!-- index-librarian:knowledge-start -->", "## 知识导航", "", "| 知识对象 | 类型 | 摘要 | 主题 | 证据 | 状态 |", "|:---|:---|:---|:---|:---|:---|"]
    for record in records:
        path = record["path"]
        link = record.get("local_path") or path
        evidence = ", ".join(record.get("evidence") or ["—"])
        topics = record.get("topics") or []
        if len(topics) > MAX_NAVIGATION_TOPICS:
            topic_display = f"{', '.join(topics[:MAX_NAVIGATION_TOPICS])} (+{len(topics) - MAX_NAVIGATION_TOPICS})"
        else:
            topic_display = ", ".join(topics) or "—"
        lines.append(
            f"| [{path}](./{link}) | {record.get('kind', 'file')} | {record.get('summary') or '—'} | "
            f"{topic_display} | {evidence} | "
            f"{record.get('parse_status', 'indexed')} |"
        )
    if not records:
        lines.append("| — | — | 当前目录没有可索引对象。 | — | — | — |")
    lines.extend(["", "<!-- index-librarian:knowledge-end -->"])
    return "\n".join(lines)


def replace_navigation_block(content: str, records: list[dict[str, Any]]) -> str:
    """Replace only the script-owned navigation block, preserving authored prose."""
    pattern = re.compile(
        r"\n?<!-- index-librarian:knowledge-start -->.*?<!-- index-librarian:knowledge-end -->\n?",
        re.DOTALL,
    )
    base = pattern.sub("\n", content).rstrip()
    return f"{base}\n\n{build_navigation_block(records)}\n"
