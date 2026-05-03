"""Repository audit CLI for Codex Shared MCP Broker.

The audit intentionally validates only public, sanitized artifacts. It does
not read local Codex auth files, tokens, user profile directories, or live
gateway state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = [
    "README.md",
    "README.en.md",
    "README.zh.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/architecture.en.md",
    "docs/architecture.zh.md",
    "docs/github-landscape.en.md",
    "docs/github-landscape.zh.md",
    "docs/design-process.en.md",
    "docs/design-process.zh.md",
    "examples/codex-config.toml",
    "examples/named_servers.example.json",
    "scripts/preflight.ps1",
    "assets/svg/architecture.en.svg",
    "assets/svg/architecture.zh.svg",
    "assets/svg/workflow.en.svg",
    "assets/svg/workflow.zh.svg",
    "assets/svg/impact.en.svg",
    "assets/svg/impact.zh.svg",
    "assets/svg/product.en.svg",
    "assets/svg/product.zh.svg",
    "assets/image2/cover.png",
    "assets/image2/product-overview.png",
]

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

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"gh[opusr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|auth[_-]?token|bearer[_-]?token)\s*=\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"(?i)password\s*=\s*['\"][^'\"]{6,}['\"]"),
]

PRIVACY_PATTERNS = [
    re.compile(r"(?i)\bsub2api\b"),
    re.compile(r"(?i)\.codex_home"),
    re.compile(r"(?i)\bLAPTOP-[A-Z0-9\-]+"),
    re.compile(r"(?i)C:\\Users\\[^\\\s]+"),
    re.compile(r"(?i)D:\\(?!path\\to\\your\\b)[^ \n\r\t\"')]+"),
]

PRIVACY_ALLOWLIST = {
    "scripts/check-no-secrets.ps1",
    "src/codex_shared_mcp_broker/audit.py",
}


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    message: str


def _text_files(root: Path) -> Iterable[Path]:
    ignored_parts = {".git", ".pytest_cache", "__pycache__", "dist", "build"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_FILE_SUFFIXES:
            yield path


def audit_required_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            findings.append(Finding("error", rel, "required file is missing"))
    return findings


def audit_examples(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    toml_path = root / "examples" / "codex-config.toml"
    json_path = root / "examples" / "named_servers.example.json"

    if toml_path.is_file():
        with toml_path.open("rb") as handle:
            data = tomllib.load(handle)
        if data.get("model_reasoning_effort") != "xhigh":
            findings.append(Finding("error", str(toml_path), "example must keep xhigh reasoning"))
        if data.get("model_context_window") != 400000:
            findings.append(Finding("error", str(toml_path), "example must document 400000 context policy"))
        servers = data.get("mcp_servers", {})
        http_servers = [
            name
            for name, value in servers.items()
            if isinstance(value, dict) and str(value.get("url", "")).startswith("http://127.0.0.1:38808/")
        ]
        if len(http_servers) < 3:
            findings.append(Finding("error", str(toml_path), "example should include shared HTTP MCP servers"))

    if json_path.is_file():
        with json_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data.get("servers"), dict):
            findings.append(Finding("error", str(json_path), "named server example must contain a servers object"))

    return findings


def audit_no_secrets(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _text_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = str(path.relative_to(root)).replace("\\", "/")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(Finding("error", rel, "possible secret pattern found"))
    return findings


def audit_no_private_machine_details(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _text_files(root):
        rel = str(path.relative_to(root)).replace("\\", "/")
        if rel in PRIVACY_ALLOWLIST:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PRIVACY_PATTERNS:
            if pattern.search(text):
                findings.append(Finding("error", rel, "possible private machine detail found"))
    return findings


def audit_bilingual_docs(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    pairs = [
        ("README.en.md", "README.zh.md"),
        ("docs/architecture.en.md", "docs/architecture.zh.md"),
        ("docs/github-landscape.en.md", "docs/github-landscape.zh.md"),
        ("docs/design-process.en.md", "docs/design-process.zh.md"),
        ("docs/release-checklist.en.md", "docs/release-checklist.zh.md"),
    ]
    for en, zh in pairs:
        if (root / en).is_file() != (root / zh).is_file():
            findings.append(Finding("error", f"{en} / {zh}", "bilingual document pair is incomplete"))
    return findings


def run_audit(root: Path) -> list[Finding]:
    return [
        *audit_required_files(root),
        *audit_examples(root),
        *audit_no_secrets(root),
        *audit_no_private_machine_details(root),
        *audit_bilingual_docs(root),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a Codex shared MCP broker repository.")
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--json", action="store_true", help="print machine-readable findings")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    findings = run_audit(root)

    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], ensure_ascii=False, indent=2))
    elif findings:
        for finding in findings:
            print(f"[{finding.level}] {finding.path}: {finding.message}")
    else:
        print("audit-ok")

    return 1 if any(finding.level == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
