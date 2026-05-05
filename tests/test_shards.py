from pathlib import Path

from codex_shared_mcp_broker.shards import (
    build_shard_plan,
    parse_ports,
    render_markdown,
    rewrite_config_text,
)


def _write_config(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """
[mcp_servers.git]
url = "http://127.0.0.1:38808/servers/git/mcp"

[mcp_servers.fetch]
url = "http://127.0.0.1:38808/servers/fetch/mcp"

[mcp_servers.openaiDeveloperDocs]
url = "https://developers.openai.com/mcp"
""".strip()
        + "\n",
        encoding="utf-8",
    )


def test_parse_ports() -> None:
    assert parse_ports("38808,38809,38810") == (38808, 38809, 38810)


def test_rewrite_config_text_keeps_server_names() -> None:
    text = 'url = "http://127.0.0.1:38808/servers/git/mcp"\n'

    rewritten, count = rewrite_config_text(text, 38809, from_ports=(38808,))

    assert count == 1
    assert "38809/servers/git/mcp" in rewritten


def test_build_shard_plan_round_robins_configs(tmp_path: Path) -> None:
    slot1 = tmp_path / "slot1" / "config.toml"
    slot2 = tmp_path / "slot2" / "config.toml"
    slot3 = tmp_path / "slot3" / "config.toml"
    for path in (slot1, slot2, slot3):
        _write_config(path)

    plan = build_shard_plan(
        [slot1.parent, slot2.parent, slot3.parent],
        ports=(38808, 38809),
        from_ports=(38808,),
        named_server_config=tmp_path / "named_servers.json",
    )
    markdown = render_markdown(plan)

    assert [item.port for item in plan.assignments] == [38808, 38809, 38808]
    assert plan.assignments[1].rewritten_urls == 2
    assert "Broker Commands" in markdown
    assert str(slot1) in markdown
