from pathlib import Path

from codex_shared_mcp_broker.privacy_guard import render_markdown, scan_privacy


def test_privacy_guard_detects_secret_without_printing_value(tmp_path: Path) -> None:
    leaked = tmp_path / "README.md"
    secret = "sk" + "-" + "a" * 30
    key_name = "api" + "_key"
    leaked.write_text(f'{key_name} = "{secret}"\n', encoding="utf-8")

    findings = scan_privacy(tmp_path, allowlist=set())
    report = render_markdown(findings)

    assert findings
    assert any(finding.rule_id == "openai-api-key" for finding in findings)
    assert secret not in report


def test_privacy_guard_detects_private_runtime_paths(tmp_path: Path) -> None:
    config = tmp_path / "config.md"
    config.write_text("Use C:\\Users\\someone\\.codex\\config.toml\n", encoding="utf-8")

    findings = scan_privacy(tmp_path, allowlist=set())

    assert any(finding.rule_id == "windows-user-path" for finding in findings)


def test_privacy_guard_allowlist_suppresses_scanner_rules(tmp_path: Path) -> None:
    scanner = tmp_path / "scanner.py"
    scanner.write_text("pattern = 'sub' + '2api'\n", encoding="utf-8")

    findings = scan_privacy(tmp_path, allowlist={"scanner.py"})

    assert findings == []
