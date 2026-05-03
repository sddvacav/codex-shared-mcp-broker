"""Runtime diagnostics for the Codex Shared MCP Broker repository.

The diagnostics are designed to be privacy-safe by default. They summarize
local runtime state without printing private absolute paths, account IDs,
tokens, or live gateway configuration.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import shutil
import socket
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import tomllib


BROKER_DEFAULT_PORT = 38808
BROKER_HTTP_PREFIX = "http://127.0.0.1:38808/servers/"
STDIO_KEYWORDS = ("npx", "uvx", "python", "powershell")


@dataclass(frozen=True)
class ConfigSummary:
    present: bool
    model: str | None
    reasoning_effort: str | None
    context_window: int | None
    compact_limit: int | None
    service_tier: str | None
    fast_mode: bool | None
    agent_max_threads: int | None
    agent_max_depth: int | None
    shared_http_urls: int
    other_http_urls: int
    stdio_like_entries: int


@dataclass(frozen=True)
class TransportSummary:
    codex_mcp_list_available: bool
    live_http_urls: int
    live_stdio_keywords: tuple[str, ...]
    live_output_hint: str


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str


@dataclass(frozen=True)
class DiagnosticReport:
    generated_at: str
    broker_port: int
    codex_cli_available: bool
    codex_cli_version_hint: str
    codex_config_source: str
    config: ConfigSummary
    transport: TransportSummary
    broker_listening: bool
    broker_http_reachable: bool
    broker_http_status: str
    overall_status: str
    checks: list[CheckResult]
    recommendations: list[str]


def _status_rank(status: str) -> int:
    return {"green": 0, "yellow": 1, "red": 2}.get(status, 2)


def _worst_status(statuses: list[str]) -> str:
    if any(_status_rank(status) == 2 for status in statuses):
        return "red"
    if any(_status_rank(status) == 1 for status in statuses):
        return "yellow"
    return "green"


def _safe_bool_text(value: bool | None) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "unknown"


def _safe_value(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _load_config_summary(codex_home: Path | None) -> tuple[str, ConfigSummary]:
    if codex_home is None:
        return "unset", ConfigSummary(
            present=False,
            model=None,
            reasoning_effort=None,
            context_window=None,
            compact_limit=None,
            service_tier=None,
            fast_mode=None,
            agent_max_threads=None,
            agent_max_depth=None,
            shared_http_urls=0,
            other_http_urls=0,
            stdio_like_entries=0,
        )

    config_path = codex_home / "config.toml"
    if not config_path.is_file():
        return "configured", ConfigSummary(
            present=False,
            model=None,
            reasoning_effort=None,
            context_window=None,
            compact_limit=None,
            service_tier=None,
            fast_mode=None,
            agent_max_threads=None,
            agent_max_depth=None,
            shared_http_urls=0,
            other_http_urls=0,
            stdio_like_entries=0,
        )

    with config_path.open("rb") as handle:
        data = tomllib.load(handle)

    servers = data.get("mcp_servers", {})
    shared_http_urls = 0
    other_http_urls = 0
    stdio_like_entries = 0
    if isinstance(servers, dict):
        for value in servers.values():
            if not isinstance(value, dict):
                continue
            url = str(value.get("url", ""))
            if url.startswith(BROKER_HTTP_PREFIX):
                shared_http_urls += 1
            elif url.startswith("http://") or url.startswith("https://"):
                other_http_urls += 1
            if any(key in value for key in ("command", "args", "spawn", "stdio")):
                stdio_like_entries += 1

    features = data.get("features", {})
    agents = data.get("agents", {})

    return "configured", ConfigSummary(
        present=True,
        model=data.get("model"),
        reasoning_effort=data.get("model_reasoning_effort"),
        context_window=data.get("model_context_window"),
        compact_limit=data.get("model_auto_compact_token_limit"),
        service_tier=data.get("service_tier"),
        fast_mode=features.get("fast_mode") if isinstance(features, dict) else None,
        agent_max_threads=agents.get("max_threads") if isinstance(agents, dict) else None,
        agent_max_depth=agents.get("max_depth") if isinstance(agents, dict) else None,
        shared_http_urls=shared_http_urls,
        other_http_urls=other_http_urls,
        stdio_like_entries=stdio_like_entries,
    )


def _probe_broker_http(port: int, timeout: float = 1.0) -> tuple[bool, str]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)
    try:
        connection.request("GET", "/")
        response = connection.getresponse()
        response.read()
        return True, str(response.status)
    except Exception as exc:  # pragma: no cover - depends on local runtime
        return False, exc.__class__.__name__
    finally:
        connection.close()


def _probe_broker_listen(port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def _run_codex_mcp_list(timeout: float = 10.0) -> tuple[bool, str, str]:
    codex = shutil.which("codex")
    if not codex:
        return False, "", "codex command not found"

    try:
        completed = subprocess.run(
            [codex, "mcp", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "", "timed out"
    except OSError as exc:  # pragma: no cover - depends on local runtime
        return False, "", exc.__class__.__name__

    output = (completed.stdout or "") + (completed.stderr or "")
    if completed.returncode != 0 and not output.strip():
        return False, "", f"exit {completed.returncode}"
    return True, output, "ok"


def _parse_live_transport(text: str | None) -> tuple[int, tuple[str, ...]]:
    if not text:
        return 0, tuple()
    http_urls = len(re.findall(r"https?://", text))
    keywords = {
        keyword
        for keyword in STDIO_KEYWORDS
        if re.search(rf"\b{keyword}\b", text, flags=re.IGNORECASE)
        and not re.search(rf"{keyword}\s*:\s*disabled", text, flags=re.IGNORECASE)
    }
    keywords = tuple(sorted(keywords))
    return http_urls, keywords


def _build_checks(
    config: ConfigSummary,
    transport: TransportSummary,
    broker_port: int,
    broker_listening: bool,
    broker_http_reachable: bool,
    broker_http_status: str,
) -> tuple[list[CheckResult], str, list[str]]:
    checks: list[CheckResult] = []

    checks.append(
        CheckResult(
            "Codex config present",
            "green" if config.present else "red",
            "config.toml found" if config.present else "config.toml not found under the configured Codex home",
        )
    )
    checks.append(
        CheckResult(
            "Reasoning effort",
            "green" if config.reasoning_effort == "xhigh" else ("yellow" if config.reasoning_effort else "red"),
            _safe_value(config.reasoning_effort),
        )
    )
    checks.append(
        CheckResult(
            "Context policy",
            "green" if config.context_window == 400000 else ("yellow" if config.context_window else "red"),
            _safe_value(config.context_window),
        )
    )
    checks.append(
        CheckResult(
            "Compaction policy",
            "green" if config.compact_limit == 360000 else ("yellow" if config.compact_limit else "red"),
            _safe_value(config.compact_limit),
        )
    )
    checks.append(
        CheckResult(
            "Shared HTTP MCP URLs",
            "green" if config.shared_http_urls > 0 else "yellow",
            str(config.shared_http_urls),
        )
    )
    checks.append(
        CheckResult(
            "Stdio-like MCP entries in config",
            "green" if config.stdio_like_entries == 0 else "red",
            str(config.stdio_like_entries),
        )
    )
    checks.append(
        CheckResult(
            "Broker listening",
            "green" if broker_listening else "red",
            f"127.0.0.1:{broker_port}",
        )
    )
    checks.append(
        CheckResult(
            "Broker HTTP reachable",
            "green" if broker_http_reachable else "red",
            broker_http_status,
        )
    )
    checks.append(
        CheckResult(
            "Codex MCP list available",
            "green" if transport.codex_mcp_list_available else "yellow",
            transport.live_output_hint,
        )
    )
    checks.append(
        CheckResult(
            "Live MCP transport",
            (
                "yellow"
                if not transport.codex_mcp_list_available
                else "green"
                if transport.live_http_urls > 0 and not transport.live_stdio_keywords
                else "red"
            ),
            f"http_urls={transport.live_http_urls}, stdio_keywords={', '.join(transport.live_stdio_keywords) if transport.live_stdio_keywords else 'none'}",
        )
    )

    statuses = [check.status for check in checks]
    overall_status = _worst_status(statuses)
    recommendations: list[str] = []

    if overall_status == "red":
        recommendations.append("Fix red checks first: config, broker reachability, or live stdio fan-out.")
    elif overall_status == "yellow":
        recommendations.append("The runtime is partially verified. Re-run after Codex CLI and broker are fully available.")
    else:
        recommendations.append("The shared HTTP MCP path is active and the public runtime checks are clean.")

    if transport.live_stdio_keywords:
        recommendations.append("Remove or disable direct stdio MCP entries before publishing the next benchmark screenshot.")
    if not broker_listening:
        recommendations.append("Start the shared broker and verify port 38808 is listening.")
    if config.shared_http_urls == 0:
        recommendations.append("Point Codex MCP entries at shared HTTP URLs before promoting the repo as the working setup.")

    return checks, overall_status, recommendations


def build_report(
    codex_home: Path | None,
    broker_port: int = BROKER_DEFAULT_PORT,
    codex_mcp_text: str | None = None,
    timeout: float = 10.0,
    codex_config_source: str | None = None,
) -> DiagnosticReport:
    config_source, config = _load_config_summary(codex_home)
    if codex_config_source is not None:
        config_source = codex_config_source

    codex_cli_available = shutil.which("codex") is not None
    codex_cli_version_hint = "available" if codex_cli_available else "missing"
    codex_mcp_list_available = False
    live_transport_text = codex_mcp_text or ""
    live_http_urls = 0
    live_stdio_keywords: tuple[str, ...] = tuple()
    live_output_hint = "not collected"

    if codex_mcp_text is None:
        codex_mcp_list_available, live_transport_text, live_output_hint = _run_codex_mcp_list(timeout=timeout)
    else:
        codex_mcp_list_available = True
        live_output_hint = "provided"

    live_http_urls, live_stdio_keywords = _parse_live_transport(live_transport_text)
    transport = TransportSummary(
        codex_mcp_list_available=codex_mcp_list_available,
        live_http_urls=live_http_urls,
        live_stdio_keywords=live_stdio_keywords,
        live_output_hint=live_output_hint,
    )

    broker_listening = _probe_broker_listen(broker_port)
    broker_http_reachable, broker_http_status = _probe_broker_http(broker_port) if broker_listening else (False, "not-listening")
    checks, overall_status, recommendations = _build_checks(
        config,
        transport,
        broker_port,
        broker_listening,
        broker_http_reachable,
        broker_http_status,
    )

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    return DiagnosticReport(
        generated_at=generated_at,
        broker_port=broker_port,
        codex_cli_available=codex_cli_available,
        codex_cli_version_hint=codex_cli_version_hint,
        codex_config_source=config_source,
        config=config,
        transport=transport,
        broker_listening=broker_listening,
        broker_http_reachable=broker_http_reachable,
        broker_http_status=broker_http_status,
        overall_status=overall_status,
        checks=checks,
        recommendations=recommendations,
    )


def render_markdown(report: DiagnosticReport) -> str:
    lines: list[str] = []
    lines.append("# Codex Runtime Diagnostics")
    lines.append("")
    lines.append(f"Generated: {report.generated_at}")
    lines.append(f"Overall status: {report.overall_status.upper()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Check | Status | Detail |")
    lines.append("| --- | --- | --- |")
    for check in report.checks:
        lines.append(f"| {check.name} | {check.status.upper()} | {check.detail} |")

    lines.append("")
    lines.append("## Config Snapshot")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Codex config source | {report.codex_config_source} |")
    lines.append(f"| Codex CLI available | {_safe_bool_text(report.codex_cli_available)} |")
    lines.append(f"| Codex CLI version hint | {report.codex_cli_version_hint} |")
    lines.append(f"| model | {_safe_value(report.config.model)} |")
    lines.append(f"| model_reasoning_effort | {_safe_value(report.config.reasoning_effort)} |")
    lines.append(f"| model_context_window | {_safe_value(report.config.context_window)} |")
    lines.append(f"| model_auto_compact_token_limit | {_safe_value(report.config.compact_limit)} |")
    lines.append(f"| service_tier | {_safe_value(report.config.service_tier)} |")
    lines.append(f"| fast_mode | {_safe_value(report.config.fast_mode)} |")
    lines.append(f"| agents.max_threads | {_safe_value(report.config.agent_max_threads)} |")
    lines.append(f"| agents.max_depth | {_safe_value(report.config.agent_max_depth)} |")

    lines.append("")
    lines.append("## MCP Transport Snapshot")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Shared HTTP URLs in config | {report.config.shared_http_urls} |")
    lines.append(f"| Other HTTP URLs in config | {report.config.other_http_urls} |")
    lines.append(f"| Stdio-like entries in config | {report.config.stdio_like_entries} |")
    lines.append(f"| `codex mcp list` available | {_safe_bool_text(report.transport.codex_mcp_list_available)} |")
    lines.append(f"| Live HTTP URLs detected | {report.transport.live_http_urls} |")
    lines.append(f"| Live stdio keywords detected | {', '.join(report.transport.live_stdio_keywords) if report.transport.live_stdio_keywords else 'none'} |")

    lines.append("")
    lines.append("## Broker Snapshot")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Broker port | {report.broker_port} |")
    lines.append(f"| Broker listening | {_safe_bool_text(report.broker_listening)} |")
    lines.append(f"| Broker HTTP reachable | {_safe_bool_text(report.broker_http_reachable)} |")
    lines.append(f"| Broker HTTP status | {report.broker_http_status} |")

    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    for item in report.recommendations:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Privacy Note")
    lines.append("")
    lines.append("This report intentionally avoids emitting private absolute paths, account IDs, tokens, or live routing details.")

    return "\n".join(lines).rstrip() + "\n"


def report_to_json(report: DiagnosticReport) -> str:
    return json.dumps(asdict(report), ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a privacy-safe Codex runtime diagnostic report.")
    parser.add_argument("--codex-home", type=Path, default=None, help="path to the Codex home directory")
    parser.add_argument("--broker-port", type=int, default=BROKER_DEFAULT_PORT, help="shared broker port")
    parser.add_argument("--timeout", type=float, default=10.0, help="timeout in seconds for live Codex queries")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="output format")
    parser.add_argument("--output", type=Path, default=None, help="optional output file path")
    args = parser.parse_args(argv)

    codex_home = args.codex_home
    config_source = "argument"
    if codex_home is None:
        env_codex_home = os.environ.get("CODEX_HOME")
        if env_codex_home:
            codex_home = Path(env_codex_home)
            config_source = "env:CODEX_HOME"
        else:
            config_source = "unset"

    report = build_report(
        codex_home,
        broker_port=args.broker_port,
        timeout=args.timeout,
        codex_config_source=config_source,
    )
    payload = render_markdown(report) if args.format == "markdown" else report_to_json(report)

    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")

    print(payload, end="" if payload.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
