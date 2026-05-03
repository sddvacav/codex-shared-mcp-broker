"""Synthetic benchmark reports for Codex MCP process fan-out.

This module intentionally does not inspect live process trees. It produces a
privacy-safe, reproducible model for explaining why shared MCP broker setups
reduce duplicated local backend process trees in multi-window workflows.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class BenchmarkScenario:
    name: str
    windows: int
    mcp_servers_per_window: int
    process_trees: int
    backend_processes: int
    broker_processes: int
    total_process_units: int
    pattern: str


@dataclass(frozen=True)
class BenchmarkReport:
    generated_at: str
    windows: int
    mcp_servers_per_window: int
    backend_processes_per_server: int
    broker_processes: int
    direct_stdio: BenchmarkScenario
    shared_broker: BenchmarkScenario
    process_unit_reduction: int
    process_unit_reduction_percent: float
    privacy_note: str


def build_benchmark(
    windows: int = 10,
    mcp_servers_per_window: int = 8,
    backend_processes_per_server: int = 1,
    broker_processes: int = 1,
) -> BenchmarkReport:
    if windows <= 0:
        raise ValueError("windows must be positive")
    if mcp_servers_per_window <= 0:
        raise ValueError("mcp_servers_per_window must be positive")
    if backend_processes_per_server <= 0:
        raise ValueError("backend_processes_per_server must be positive")
    if broker_processes <= 0:
        raise ValueError("broker_processes must be positive")

    direct_backend_processes = windows * mcp_servers_per_window * backend_processes_per_server
    broker_backend_processes = mcp_servers_per_window * backend_processes_per_server
    shared_total = broker_backend_processes + broker_processes
    reduction = direct_backend_processes - shared_total
    reduction_percent = round((reduction / direct_backend_processes) * 100, 2)

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    return BenchmarkReport(
        generated_at=generated_at,
        windows=windows,
        mcp_servers_per_window=mcp_servers_per_window,
        backend_processes_per_server=backend_processes_per_server,
        broker_processes=broker_processes,
        direct_stdio=BenchmarkScenario(
            name="Direct stdio",
            windows=windows,
            mcp_servers_per_window=mcp_servers_per_window,
            process_trees=windows * mcp_servers_per_window,
            backend_processes=direct_backend_processes,
            broker_processes=0,
            total_process_units=direct_backend_processes,
            pattern="duplicated backend trees per window",
        ),
        shared_broker=BenchmarkScenario(
            name="Shared broker",
            windows=windows,
            mcp_servers_per_window=mcp_servers_per_window,
            process_trees=mcp_servers_per_window,
            backend_processes=broker_backend_processes,
            broker_processes=broker_processes,
            total_process_units=shared_total,
            pattern="one broker-owned backend pool",
        ),
        process_unit_reduction=reduction,
        process_unit_reduction_percent=reduction_percent,
        privacy_note=(
            "Synthetic benchmark only. It does not inspect live process lists, "
            "private paths, tokens, account IDs, or local routing state."
        ),
    )


def render_markdown(report: BenchmarkReport) -> str:
    lines: list[str] = []
    lines.append("# Codex MCP Fan-Out Benchmark")
    lines.append("")
    lines.append(f"Generated: {report.generated_at}")
    lines.append("")
    lines.append("## Scenario")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("| --- | ---: |")
    lines.append(f"| Windows | {report.windows} |")
    lines.append(f"| MCP servers per window | {report.mcp_servers_per_window} |")
    lines.append(f"| Backend process units per server | {report.backend_processes_per_server} |")
    lines.append(f"| Broker process units | {report.broker_processes} |")
    lines.append("")
    lines.append("## Before / After")
    lines.append("")
    lines.append("| Scenario | Process trees | Backend process units | Broker process units | Total process units | Pattern |")
    lines.append("| --- | ---: | ---: | ---: | ---: | --- |")
    for scenario in (report.direct_stdio, report.shared_broker):
        lines.append(
            f"| {scenario.name} | {scenario.process_trees} | {scenario.backend_processes} | "
            f"{scenario.broker_processes} | {scenario.total_process_units} | {scenario.pattern} |"
        )
    lines.append("")
    lines.append("## Result")
    lines.append("")
    lines.append(f"- Synthetic process unit reduction: {report.process_unit_reduction}")
    lines.append(f"- Synthetic reduction percentage: {report.process_unit_reduction_percent}%")
    lines.append("- This is a local runtime fan-out model, not a model intelligence benchmark.")
    lines.append("")
    lines.append("## Privacy Note")
    lines.append("")
    lines.append(report.privacy_note)
    return "\n".join(lines).rstrip() + "\n"


def report_to_json(report: BenchmarkReport) -> str:
    return json.dumps(asdict(report), ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a privacy-safe synthetic MCP fan-out benchmark.")
    parser.add_argument("--windows", type=int, default=10, help="number of Codex windows")
    parser.add_argument("--servers", type=int, default=8, help="MCP servers per window")
    parser.add_argument("--backend-processes-per-server", type=int, default=1, help="synthetic backend process units per server")
    parser.add_argument("--broker-processes", type=int, default=1, help="synthetic broker process units")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="output format")
    parser.add_argument("--output", type=Path, default=None, help="optional output file path")
    args = parser.parse_args(argv)

    report = build_benchmark(
        windows=args.windows,
        mcp_servers_per_window=args.servers,
        backend_processes_per_server=args.backend_processes_per_server,
        broker_processes=args.broker_processes,
    )
    payload = render_markdown(report) if args.format == "markdown" else report_to_json(report)

    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")

    print(payload, end="" if payload.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
