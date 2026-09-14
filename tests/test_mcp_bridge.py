import json
import sys

from ai4sci_bench.mcp_bridge.server import BridgeServer, ToolSpec


def test_status_reports_installation(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda command: "/bin/echo" if command == "echo" else None)
    server = BridgeServer((ToolSpec("echo", "echo", "test"), ToolSpec("missing", "missing", "test")))
    status = server.call("status")
    assert status["tools"]["echo"]["installed"] is True
    assert status["tools"]["missing"]["installed"] is False


def test_run_allowlisted_command(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda command: sys.executable if command == "python" else None)
    server = BridgeServer((ToolSpec("python", sys.executable, "test"),))
    result = server.call("run", {"tool": "python", "args": ["-c", "print('ok')"]})
    assert result["ok"]
    assert result["stdout"].strip() == "ok"


def test_missing_command_is_reported():
    server = BridgeServer((ToolSpec("missing", "definitely-not-installed", "test"),))
    result = server.call("run", {"tool": "missing", "args": []})
    assert result["ok"] is False
    assert "not found" in result["error"]


def test_stdio_protocol(monkeypatch, capsys):
    from ai4sci_bench.mcp_bridge.server import serve_stdio
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({"method": "status"}) + "\n"))
    serve_stdio(BridgeServer(()))
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True


def test_text2sim_validation():
    from ai4sci_bench.mcp_bridge.server import BridgeServer
    server = BridgeServer(())
    assert server.call("text2sim_validate", {"config": {"entities": [], "events": []}})["ok"]
    assert not server.call("text2sim_validate", {"config": {}})["ok"]
