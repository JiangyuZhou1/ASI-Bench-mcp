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


def test_generic_launcher_is_not_treated_as_server(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda command: "/usr/bin/uvx")
    result = classify("tool", {
        "source": "https://example.com/tool-mcp",
        "server": {"command": "uvx", "args": ["tool-mcp"]},
    })
    assert result["backend"] == "launcher_unverified"
    assert result["verdict"] == "unverified"
