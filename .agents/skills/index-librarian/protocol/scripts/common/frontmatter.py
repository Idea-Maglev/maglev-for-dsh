"""
Strict YAML frontmatter parser for INDEX.md files.

Design authority: index-schema.md
Execution authority: THIS FILE — if contradictions exist, this behavior is correct.

Rules:
  - Non-compliant frontmatter → error (not warning)
  - Missing required fields → error
  - Unknown type/scope → error
"""

import re
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    raise SystemExit(
        "Error: pyyaml is required. Install with: pip install pyyaml"
    )

FRONTMATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n?(.*)",
    re.DOTALL,
)

REQUIRED_INDEX_FIELDS = {"type", "scope", "child_count", "stats", "updated"}
REQUIRED_ROOT_FIELDS = REQUIRED_INDEX_FIELDS | {
    "entity_type",
    "index_protocol_version",
    "stats_schema",
}
VALID_SCOPES = {"root", "year", "month", "collection"}
INDEX_TYPE = "entity-index"


class ParseError(Exception):
    """Raised when frontmatter is non-compliant."""

    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"{path}: {reason}")


class ParseResult:
    """Result of parsing an INDEX.md file."""

    def __init__(
        self,
        path: str,
        metadata: dict[str, Any],
        content: str,
        errors: list[str],
    ):
        self.path = path
        self.metadata = metadata
        self.content = content
        self.errors = errors

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def scope(self) -> Optional[str]:
        return self.metadata.get("scope")

    @property
    def is_root(self) -> bool:
        return self.scope == "root"

    def __repr__(self) -> str:
        status = "valid" if self.is_valid else f"invalid({len(self.errors)} errors)"
        return f"ParseResult({self.path}, {status})"


def parse_file(filepath: str | Path) -> ParseResult:
    """Parse an INDEX.md file with strict validation.

    Args:
        filepath: Path to INDEX.md file.

    Returns:
        ParseResult with metadata, content, and any validation errors.
    """
    filepath = Path(filepath)
    errors: list[str] = []

    if not filepath.exists():
        return ParseResult(str(filepath), {}, "", [f"File not found: {filepath}"])

    text = filepath.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)

    if not match:
        return ParseResult(
            str(filepath), {}, text, ["No YAML frontmatter found (missing --- delimiters)"]
        )

    yaml_text, content = match.group(1), match.group(2)

    try:
        metadata = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        return ParseResult(str(filepath), {}, content, [f"YAML parse error: {e}"])

    if not isinstance(metadata, dict):
        return ParseResult(
            str(filepath), {}, content, ["Frontmatter is not a YAML mapping"]
        )

    # Validate type
    if metadata.get("type") != INDEX_TYPE:
        errors.append(
            f"type must be '{INDEX_TYPE}', got '{metadata.get('type', '<missing>')}'"
        )

    # Validate scope
    scope = metadata.get("scope")
    if scope not in VALID_SCOPES:
        errors.append(
            f"scope must be one of {VALID_SCOPES}, got '{scope}'"
        )

    # Check required fields based on scope
    required = REQUIRED_ROOT_FIELDS if scope == "root" else REQUIRED_INDEX_FIELDS
    for field in required:
        if field not in metadata:
            errors.append(f"Missing required field: {field}")

    # Validate stats structure
    stats = metadata.get("stats")
    if isinstance(stats, dict):
        if "total" not in stats:
            errors.append("stats.total is required")
        elif not isinstance(stats["total"], (int, float)):
            errors.append(f"stats.total must be numeric, got {type(stats['total']).__name__}")
    elif stats is not None:
        errors.append(f"stats must be a mapping, got {type(stats).__name__}")

    # Validate child_count is numeric
    cc = metadata.get("child_count")
    if cc is not None and not isinstance(cc, (int, float)):
        errors.append(f"child_count must be numeric, got {type(cc).__name__}")

    # Validate updated format
    updated = metadata.get("updated")
    if updated is not None:
        updated_str = str(updated)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", updated_str):
            errors.append(f"updated must be YYYY-MM-DD format, got '{updated_str}'")

    return ParseResult(str(filepath), metadata, content, errors)


def parse_any_frontmatter(filepath: str | Path) -> ParseResult:
    """Parse any markdown file's frontmatter without index-specific validation.

    Used to read child entity frontmatter for stats computation.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return ParseResult(str(filepath), {}, "", [f"File not found: {filepath}"])

    text = filepath.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)

    if not match:
        return ParseResult(str(filepath), {}, text, [])

    yaml_text, content = match.group(1), match.group(2)

    try:
        metadata = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError:
        return ParseResult(str(filepath), {}, content, [f"YAML parse error in {filepath}"])

    if not isinstance(metadata, dict):
        metadata = {}

    return ParseResult(str(filepath), metadata, content, [])


def write_frontmatter(filepath: str | Path, metadata: dict, content: str) -> None:
    """Write frontmatter + content back to a markdown file.

    Args:
        filepath: Target file path.
        metadata: Frontmatter dict.
        content: Body content (markdown).
    """
    filepath = Path(filepath)
    yaml_str = yaml.dump(
        metadata,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    ).rstrip("\n")

    filepath.write_text(f"---\n{yaml_str}\n---\n{content}", encoding="utf-8")


def get_nested(d: dict, dotted_key: str, default=None):
    """Get a value from a nested dict using dotted notation.

    Example: get_nested(meta, "analysis.decisions") → meta["analysis"]["decisions"]
    """
    keys = dotted_key.split(".")
    current = d
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    return current
