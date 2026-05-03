import pytest

from codex_shared_mcp_broker.benchmark import build_benchmark, render_markdown


def test_benchmark_default_scenario() -> None:
    report = build_benchmark()

    assert report.direct_stdio.total_process_units == 80
    assert report.shared_broker.total_process_units == 9
    assert report.process_unit_reduction == 71
    assert report.process_unit_reduction_percent == 88.75


def test_benchmark_markdown_is_privacy_safe() -> None:
    report = build_benchmark(windows=2, mcp_servers_per_window=3)
    markdown = render_markdown(report)

    assert "Codex MCP Fan-Out Benchmark" in markdown
    assert "Synthetic benchmark only" in markdown
    assert "C:\\Users" not in markdown
    assert "token" in markdown.lower()


def test_benchmark_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        build_benchmark(windows=0)
