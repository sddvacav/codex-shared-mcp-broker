from pathlib import Path

from codex_shared_mcp_broker.diagnostics import build_report, render_markdown


def _write_config(root: Path, *, stdio: bool = False) -> None:
    root.mkdir(parents=True, exist_ok=True)
    config = """
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
model_context_window = 400000
model_auto_compact_token_limit = 360000
service_tier = "fast"

[features]
fast_mode = true

[agents]
max_threads = 96
max_depth = 8

[mcp_servers.git]
url = "http://127.0.0.1:38808/servers/git/mcp"
"""
    if stdio:
        config += """
[mcp_servers.fetch]
command = "npx"
args = ["mcp-server-fetch"]
"""
    (root / "config.toml").write_text(config.strip() + "\n", encoding="utf-8")


def test_diagnostic_report_is_sanitized(tmp_path: Path) -> None:
    codex_home = tmp_path / "private" / "codex-home"
    _write_config(codex_home)

    report = build_report(
        codex_home,
        codex_config_source="test-fixture",
        codex_mcp_text="git http://127.0.0.1:38808/servers/git/mcp",
        broker_port=9,
    )
    markdown = render_markdown(report)

    assert "test-fixture" in markdown
    assert str(codex_home) not in markdown
    assert "model_reasoning_effort | xhigh" in markdown
    assert "Live HTTP URLs detected | 1" in markdown


def test_diagnostic_report_flags_stdio_config(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex-home"
    _write_config(codex_home, stdio=True)

    report = build_report(
        codex_home,
        codex_config_source="test-fixture",
        codex_mcp_text="fetch npx mcp-server-fetch",
        broker_port=9,
    )

    assert report.config.stdio_like_entries == 1
    assert "npx" in report.transport.live_stdio_keywords
    assert report.overall_status == "red"


def test_diagnostic_report_includes_broker_port_pressure(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex-home"
    _write_config(codex_home)

    report = build_report(
        codex_home,
        codex_config_source="test-fixture",
        codex_mcp_text="git http://127.0.0.1:38808/servers/git/mcp",
        broker_port=9,
        broker_ports=[9, 10],
    )
    markdown = render_markdown(report)

    assert "Broker Port Pressure" in markdown
    assert "| 9 |" in markdown
    assert "| 10 |" in markdown
