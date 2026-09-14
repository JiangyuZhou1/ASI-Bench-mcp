from tools.verify_mcp_catalog import classify


def test_catalog_verifier_rejects_search_and_placeholder():
    result = classify("candidate", {
        "source": "https://github.com/search?q=candidate+MCP&type=repositories",
        "server": {"command": "candidate-mcp", "args": []},
    })
    assert result == {
        "backend": "missing_command",
        "provenance": "search_only",
        "verdict": "unverified",
    }


def test_catalog_verifier_accepts_explicit_installed_command(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda command: "/usr/bin/tool")
    result = classify("tool", {
        "source": "https://example.com/tool-mcp",
        "server": {"command": "tool-mcp", "args": []},
    })
    assert result["verdict"] == "verified"
