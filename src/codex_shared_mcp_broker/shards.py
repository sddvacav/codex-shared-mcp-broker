"""Shard planning for high-concurrency Codex MCP broker setups.

The shared broker removes per-window stdio process fan-out. Under heavier
loads, a single broker port can still become the hot spot. This module keeps
the same MCP server set intact while assigning configuration roots to multiple
broker ports.
"""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


LOCAL_BROKER_URL_RE = re.compile(
    r"http://127\.0\.0\.1:(?P<port>\d+)/servers/(?P<server>[^/]+)/mcp"
)


@dataclass(frozen=True)
class ShardAssignment:
    config_path: str
    shard_index: int
    port: int
    local_broker_urls: int
    rewritten_urls: int
    exists: bool


@dataclass(frozen=True)
class ShardPlan:
    generated_at: str
    ports: tuple[int, ...]
    from_ports: tuple[int, ...] | None
    assignments: tuple[ShardAssignment, ...]
    broker_commands: tuple[str, ...]
    apply_requested: bool
    backups: tuple[str, ...]
    note: str


def parse_ports(text: str) -> tuple[int, ...]:
    ports: list[int] = []
    for raw in text.split(","):
        item = raw.strip()
        if not item:
            continue
        port = int(item)
        if port <= 0 or port > 65535:
            raise ValueError(f"invalid port: {port}")
        ports.append(port)
    if not ports:
        raise ValueError("at least one port is required")
    if len(set(ports)) != len(ports):
        raise ValueError("ports must be unique")
    return tuple(ports)


def config_path_from_home(path: Path) -> Path:
    return path if path.name.lower() == "config.toml" else path / "config.toml"


def normalize_config_paths(paths: Iterable[Path]) -> tuple[Path, ...]:
    seen: set[str] = set()
    result: list[Path] = []
    for raw_path in paths:
        path = config_path_from_home(raw_path).expanduser().resolve()
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return tuple(result)


def count_local_broker_urls(text: str) -> int:
    return len(LOCAL_BROKER_URL_RE.findall(text))


def rewrite_config_text(
    text: str,
    target_port: int,
    from_ports: Sequence[int] | None = None,
) -> tuple[str, int]:
    allowed_ports = set(from_ports) if from_ports is not None else None
    rewritten = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal rewritten
        source_port = int(match.group("port"))
        if allowed_ports is not None and source_port not in allowed_ports:
            return match.group(0)
        if source_port == target_port:
            return match.group(0)
        rewritten += 1
        return f"http://127.0.0.1:{target_port}/servers/{match.group('server')}/mcp"

    return LOCAL_BROKER_URL_RE.sub(replace, text), rewritten


def _ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def build_broker_commands(
    named_server_config: Path | None,
    ports: Sequence[int],
    *,
    python_executable: str = "python",
    host: str = "127.0.0.1",
) -> tuple[str, ...]:
    if named_server_config is None:
        return tuple()
    config = str(named_server_config)
    commands = []
    for port in ports:
        commands.append(
            " ".join(
                [
                    "&",
                    _ps_quote(python_executable),
                    "-m",
                    "mcp_proxy",
                    "--named-server-config",
                    _ps_quote(config),
                    "--host",
                    _ps_quote(host),
                    "--port",
                    str(port),
                    "--allow-origin",
                    _ps_quote("*"),
                    "--log-level",
                    "INFO",
                ]
            )
        )
    return tuple(commands)


def build_shard_plan(
    config_paths: Sequence[Path],
    ports: Sequence[int],
    *,
    from_ports: Sequence[int] | None = None,
    named_server_config: Path | None = None,
    python_executable: str = "python",
    host: str = "127.0.0.1",
    apply_requested: bool = False,
    backups: Sequence[str] = (),
) -> ShardPlan:
    if not ports:
        raise ValueError("at least one shard port is required")
    normalized = normalize_config_paths(config_paths)
    assignments: list[ShardAssignment] = []
    for index, path in enumerate(normalized):
        port = ports[index % len(ports)]
        exists = path.is_file()
        text = path.read_text(encoding="utf-8") if exists else ""
        rewritten_text, rewritten = rewrite_config_text(text, port, from_ports=from_ports)
        if rewritten_text:
            tomllib.loads(rewritten_text)
        assignments.append(
            ShardAssignment(
                config_path=str(path),
                shard_index=index % len(ports),
                port=port,
                local_broker_urls=count_local_broker_urls(text),
                rewritten_urls=rewritten,
                exists=exists,
            )
        )

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    return ShardPlan(
        generated_at=generated_at,
        ports=tuple(ports),
        from_ports=tuple(from_ports) if from_ports is not None else None,
        assignments=tuple(assignments),
        broker_commands=build_broker_commands(
            named_server_config,
            ports,
            python_executable=python_executable,
            host=host,
        ),
        apply_requested=apply_requested,
        backups=tuple(backups),
        note=(
            "Sharding keeps the MCP server set intact. It changes only local "
            "broker URL ports in selected Codex config files."
        ),
    )


def apply_shard_plan(
    config_paths: Sequence[Path],
    ports: Sequence[int],
    *,
    from_ports: Sequence[int] | None = None,
    backup_suffix: str | None = None,
) -> tuple[str, ...]:
    normalized = normalize_config_paths(config_paths)
    backups: list[str] = []
    suffix = backup_suffix or datetime.now().strftime("%Y%m%d_%H%M%S")
    for index, path in enumerate(normalized):
        if not path.is_file():
            continue
        target_port = ports[index % len(ports)]
        text = path.read_text(encoding="utf-8")
        rewritten_text, rewritten = rewrite_config_text(text, target_port, from_ports=from_ports)
        if rewritten == 0:
            continue
        tomllib.loads(rewritten_text)
        backup_path = path.with_name(f"{path.name}.bak_mcp_shards_{suffix}")
        backup_path.write_text(text, encoding="utf-8")
        path.write_text(rewritten_text, encoding="utf-8")
        backups.append(str(backup_path))
    return tuple(backups)


def render_markdown(plan: ShardPlan) -> str:
    lines: list[str] = []
    lines.append("# Codex MCP Broker Shard Plan")
    lines.append("")
    lines.append(f"Generated: {plan.generated_at}")
    lines.append(f"Shard ports: {', '.join(str(port) for port in plan.ports)}")
    lines.append(
        "Source ports: "
        + (", ".join(str(port) for port in plan.from_ports) if plan.from_ports else "any local broker port")
    )
    lines.append(f"Apply requested: {'yes' if plan.apply_requested else 'no'}")
    lines.append("")
    lines.append("## Assignments")
    lines.append("")
    lines.append("| Config | Shard | Port | Local broker URLs | Rewritten URLs | Exists |")
    lines.append("| --- | ---: | ---: | ---: | ---: | --- |")
    for item in plan.assignments:
        lines.append(
            f"| {item.config_path} | {item.shard_index} | {item.port} | "
            f"{item.local_broker_urls} | {item.rewritten_urls} | {'yes' if item.exists else 'no'} |"
        )

    if plan.broker_commands:
        lines.append("")
        lines.append("## Broker Commands")
        lines.append("")
        lines.append("Run one command per shard, or wrap them in your existing service manager.")
        lines.append("")
        lines.append("```powershell")
        lines.extend(plan.broker_commands)
        lines.append("```")

    if plan.backups:
        lines.append("")
        lines.append("## Backups")
        lines.append("")
        for backup in plan.backups:
            lines.append(f"- {backup}")

    lines.append("")
    lines.append("## Note")
    lines.append("")
    lines.append(plan.note)
    return "\n".join(lines).rstrip() + "\n"


def plan_to_json(plan: ShardPlan) -> str:
    return json.dumps(asdict(plan), ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan or apply Codex MCP broker shard assignments.")
    parser.add_argument(
        "--config",
        type=Path,
        action="append",
        default=[],
        help="Codex configuration directory or config.toml path. Repeat for multiple configs.",
    )
    parser.add_argument("--ports", default="38808", help="comma-separated broker shard ports")
    parser.add_argument("--from-ports", default=None, help="optional comma-separated source ports to rewrite")
    parser.add_argument("--named-server-config", type=Path, default=None, help="named server config for command output")
    parser.add_argument("--python", default="python", help="Python executable used in broker command output")
    parser.add_argument("--host", default="127.0.0.1", help="broker bind host")
    parser.add_argument("--apply", action="store_true", help="rewrite config files and create backups")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="output format")
    parser.add_argument("--output", type=Path, default=None, help="optional output file")
    args = parser.parse_args(argv)

    ports = parse_ports(args.ports)
    from_ports = parse_ports(args.from_ports) if args.from_ports else None
    config_paths = args.config
    if not config_paths:
        parser.error("provide at least one --config")

    backups: tuple[str, ...] = tuple()
    if args.apply:
        backups = apply_shard_plan(config_paths, ports, from_ports=from_ports)

    plan = build_shard_plan(
        config_paths,
        ports,
        from_ports=from_ports,
        named_server_config=args.named_server_config,
        python_executable=args.python,
        host=args.host,
        apply_requested=args.apply,
        backups=backups,
    )
    payload = render_markdown(plan) if args.format == "markdown" else plan_to_json(plan)

    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")

    print(payload, end="" if payload.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
