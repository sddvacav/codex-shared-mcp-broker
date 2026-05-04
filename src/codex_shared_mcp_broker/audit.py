"""Repository audit CLI for Codex Shared MCP Broker.

The audit intentionally validates only public, sanitized artifacts. It does
not read local Codex auth files, tokens, user profile directories, or live
gateway state.
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .privacy_guard import PrivacyFinding, scan_privacy


REQUIRED_FILES = [
    "README.md",
    "README.en.md",
    "README.zh.md",
    "ROADMAP.md",
    "PUBLIC_STAGE.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/agent-runtime-privacy-guard.en.md",
    "docs/agent-runtime-privacy-guard.zh.md",
    "docs/architecture.en.md",
    "docs/architecture.zh.md",
    "docs/benchmark.en.md",
    "docs/benchmark.zh.md",
    "docs/github-landscape.en.md",
    "docs/github-landscape.zh.md",
    "docs/design-process.en.md",
    "docs/design-process.zh.md",
    "docs/current-source-check.en.md",
    "docs/current-source-check.zh.md",
    "docs/cross-client-runtime-notes.en.md",
    "docs/cross-client-runtime-notes.zh.md",
    "docs/deployment-commercial-chain.en.md",
    "docs/deployment-commercial-chain.zh.md",
    "docs/demo-script.en.md",
    "docs/demo-script.zh.md",
    "docs/demo-benchmark-plan.en.md",
    "docs/demo-benchmark-plan.zh.md",
    "docs/github-heat-roadmap.en.md",
    "docs/github-heat-roadmap.zh.md",
    "docs/hosted-product-blueprint.en.md",
    "docs/hosted-product-blueprint.zh.md",
    "docs/launch-post.en.md",
    "docs/launch-post.zh.md",
    "docs/release-asset-pack.en.md",
    "docs/release-asset-pack.zh.md",
    "docs/remotion-demo.en.md",
    "docs/remotion-demo.zh.md",
    "docs/material-library.en.md",
    "docs/material-library.zh.md",
    "docs/design-flow-v0.06.en.md",
    "docs/design-flow-v0.06.zh.md",
    "resources/brand-material-library.json",
    "site/index.html",
    "site/styles.css",
    ".github/workflows/pages.yml",
    "examples/codex-config.toml",
    "examples/named_servers.example.json",
    "examples/privacy-guard-ci.yml",
    "scripts/preflight.ps1",
    "src/codex_shared_mcp_broker/benchmark.py",
    "src/codex_shared_mcp_broker/diagnostics.py",
    "src/codex_shared_mcp_broker/privacy_guard.py",
    "assets/svg/architecture.en.svg",
    "assets/svg/architecture.zh.svg",
    "assets/svg/benchmark.en.svg",
    "assets/svg/benchmark.zh.svg",
    "assets/svg/demo-storyboard.en.svg",
    "assets/svg/demo-storyboard.zh.svg",
    "assets/svg/hosted-product-blueprint.en.svg",
    "assets/svg/hosted-product-blueprint.zh.svg",
    "assets/svg/workflow.en.svg",
    "assets/svg/workflow.zh.svg",
    "assets/svg/impact.en.svg",
    "assets/svg/impact.zh.svg",
    "assets/svg/product.en.svg",
    "assets/svg/product.zh.svg",
    "assets/image2/cover.png",
    "assets/image2/product-overview.png",
    "assets/remotion/codex-shared-mcp-demo.mp4",
    "assets/remotion/codex-shared-mcp-demo-poster.png",
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


def _privacy_to_finding(finding: PrivacyFinding) -> Finding:
    return Finding("error", finding.path, f"{finding.rule_id}: {finding.message}")


def audit_privacy_guard(root: Path) -> list[Finding]:
    return [_privacy_to_finding(finding) for finding in scan_privacy(root)]


def audit_bilingual_docs(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    pairs = [
        ("README.en.md", "README.zh.md"),
        ("docs/agent-runtime-privacy-guard.en.md", "docs/agent-runtime-privacy-guard.zh.md"),
        ("docs/architecture.en.md", "docs/architecture.zh.md"),
        ("docs/benchmark.en.md", "docs/benchmark.zh.md"),
        ("docs/github-landscape.en.md", "docs/github-landscape.zh.md"),
        ("docs/design-process.en.md", "docs/design-process.zh.md"),
        ("docs/current-source-check.en.md", "docs/current-source-check.zh.md"),
        ("docs/cross-client-runtime-notes.en.md", "docs/cross-client-runtime-notes.zh.md"),
        ("docs/deployment-commercial-chain.en.md", "docs/deployment-commercial-chain.zh.md"),
        ("docs/demo-script.en.md", "docs/demo-script.zh.md"),
        ("docs/demo-benchmark-plan.en.md", "docs/demo-benchmark-plan.zh.md"),
        ("docs/design-flow-v0.06.en.md", "docs/design-flow-v0.06.zh.md"),
        ("docs/github-heat-roadmap.en.md", "docs/github-heat-roadmap.zh.md"),
        ("docs/hosted-product-blueprint.en.md", "docs/hosted-product-blueprint.zh.md"),
        ("docs/launch-post.en.md", "docs/launch-post.zh.md"),
        ("docs/material-library.en.md", "docs/material-library.zh.md"),
        ("docs/release-asset-pack.en.md", "docs/release-asset-pack.zh.md"),
        ("docs/remotion-demo.en.md", "docs/remotion-demo.zh.md"),
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
        *audit_privacy_guard(root),
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
