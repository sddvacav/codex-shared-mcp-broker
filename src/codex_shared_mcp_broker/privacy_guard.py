"""Agent runtime privacy guard.

The guard scans public-release artifacts for common secret shapes and local
agent runtime details that should not be published. It is intentionally small
and deterministic so it can run in CI before a repository is pushed.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


TEXT_FILE_SUFFIXES = {
    ".md",
    ".py",
    ".ps1",
    ".toml",
    ".json",
    ".svg",
    ".yml",
    ".yaml",
    ".txt",
}

IGNORED_PARTS = {".git", ".pytest_cache", "__pycache__", "dist", "build", ".ruff_cache", ".mypy_cache"}

DEFAULT_ALLOWLIST = {
    "scripts/check-no-secrets.ps1",
    "src/codex_shared_mcp_broker/audit.py",
    "src/codex_shared_mcp_broker/diagnostics.py",
    "src/codex_shared_mcp_broker/privacy_guard.py",
}

RISKY_FILE_NAMES = {
    ".env",
    ".env.local",
    "auth.json",
    "credentials.json",
    "token.json",
    "secrets.json",
}


@dataclass(frozen=True)
class PrivacyRule:
    rule_id: str
    severity: str
    category: str
    description: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class PrivacyFinding:
    rule_id: str
    severity: str
    category: str
    path: str
    line: int
    message: str


DEFAULT_RULES = [
    PrivacyRule(
        "openai-api-key",
        "high",
        "secret",
        "OpenAI-style API key shape",
        re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    ),
    PrivacyRule(
        "github-token",
        "high",
        "secret",
        "GitHub token shape",
        re.compile(r"gh[opusr]_[A-Za-z0-9_]{20,}"),
    ),
    PrivacyRule(
        "key-assignment",
        "high",
        "secret",
        "API key or token assignment",
        re.compile(r"(?i)(api[_-]?key|auth[_-]?token|bearer[_-]?token)\s*=\s*['\"][^'\"]{8,}['\"]"),
    ),
    PrivacyRule(
        "password-assignment",
        "high",
        "secret",
        "Password assignment",
        re.compile(r"(?i)password\s*=\s*['\"][^'\"]{6,}['\"]"),
    ),
    PrivacyRule(
        "local-gateway-name",
        "high",
        "agent-runtime",
        "Private local gateway reference",
        re.compile(r"(?i)\bsub2api\b"),
    ),
    PrivacyRule(
        "codex-home",
        "high",
        "agent-runtime",
        "Private Codex home reference",
        re.compile(r"(?i)\.codex_home"),
    ),
    PrivacyRule(
        "windows-user-path",
        "high",
        "private-path",
        "Windows user profile path",
        re.compile(r"(?i)C:\\Users\\[^\\\s]+"),
    ),
    PrivacyRule(
        "private-drive-path",
        "medium",
        "private-path",
        "Non-example Windows drive path",
        re.compile(r"(?i)D:\\(?!path\\to\\your\\b)[^ \n\r\t\"')]+"),
    ),
    PrivacyRule(
        "machine-name",
        "medium",
        "private-host",
        "Machine name shape",
        re.compile(r"(?i)\bLAPTOP-[A-Z0-9\-]+"),
    ),
]


def _normalize_rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_FILE_SUFFIXES or path.name in RISKY_FILE_NAMES:
            yield path


def _line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def scan_privacy(
    root: Path,
    *,
    allowlist: set[str] | None = None,
    rules: list[PrivacyRule] | None = None,
) -> list[PrivacyFinding]:
    root = root.resolve()
    allowlist = DEFAULT_ALLOWLIST if allowlist is None else allowlist
    rules = DEFAULT_RULES if rules is None else rules
    findings: list[PrivacyFinding] = []

    for path in iter_text_files(root):
        rel = _normalize_rel(path, root)
        if rel in allowlist:
            continue

        if path.name in RISKY_FILE_NAMES:
            findings.append(
                PrivacyFinding(
                    rule_id="risky-file-name",
                    severity="high",
                    category="secret-container",
                    path=rel,
                    line=1,
                    message="risky secret-bearing file name should not be committed",
                )
            )

        text = path.read_text(encoding="utf-8", errors="ignore")
        for rule in rules:
            for match in rule.pattern.finditer(text):
                findings.append(
                    PrivacyFinding(
                        rule_id=rule.rule_id,
                        severity=rule.severity,
                        category=rule.category,
                        path=rel,
                        line=_line_for_offset(text, match.start()),
                        message=rule.description,
                    )
                )

    return findings


def render_markdown(findings: list[PrivacyFinding]) -> str:
    lines: list[str] = []
    lines.append("# Agent Runtime Privacy Guard Report")
    lines.append("")
    if not findings:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("No configured secret or private runtime patterns were detected.")
    else:
        lines.append("Status: FAIL")
        lines.append("")
        lines.append("| Severity | Category | Rule | Path | Line | Message |")
        lines.append("| --- | --- | --- | --- | ---: | --- |")
        for finding in findings:
            lines.append(
                f"| {finding.severity} | {finding.category} | {finding.rule_id} | "
                f"{finding.path} | {finding.line} | {finding.message} |"
            )
    lines.append("")
    lines.append("Privacy note: matched secret values and private path contents are not printed.")
    return "\n".join(lines).rstrip() + "\n"


def render_json(findings: list[PrivacyFinding]) -> str:
    return json.dumps([asdict(finding) for finding in findings], ensure_ascii=False, indent=2)


def has_blocking_findings(findings: list[PrivacyFinding], fail_on: str) -> bool:
    rank = {"low": 0, "medium": 1, "high": 2}
    threshold = rank[fail_on]
    return any(rank.get(finding.severity, 2) >= threshold for finding in findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a repository for agent runtime privacy leaks.")
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="output format")
    parser.add_argument("--output", type=Path, default=None, help="optional output file path")
    parser.add_argument("--fail-on", choices=("low", "medium", "high"), default="high", help="minimum severity that returns exit code 1")
    args = parser.parse_args(argv)

    findings = scan_privacy(Path(args.root))
    payload = render_markdown(findings) if args.format == "markdown" else render_json(findings)

    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="" if payload.endswith("\n") else "\n")

    return 1 if has_blocking_findings(findings, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
