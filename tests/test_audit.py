from pathlib import Path

from codex_shared_mcp_broker.audit import run_audit


def test_repository_audit_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    findings = run_audit(root)
    assert findings == []


def test_readmes_are_bilingual_entrypoints() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    assert "README.en.md" in readme
    assert "README.zh.md" in readme
