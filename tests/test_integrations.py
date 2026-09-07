import json
from pathlib import Path

from ai4sci_bench.integrations import (
    INTEGRATION_PROFILES,
    build_runtime_dockerfile,
    convert_scienceagentbench,
    load_tool_registry,
)


def test_profiles_cover_requested_integrations():
    assert set(INTEGRATION_PROFILES) == {
        "scienceagentbench", "cfdllmbench", "sciagentgym", "cosmo-agent"
    }
    assert "openfoam" in INTEGRATION_PROFILES["cfdllmbench"].runtime_tools
    assert "freecadcmd" in INTEGRATION_PROFILES["cosmo-agent"].runtime_tools


def test_scienceagentbench_converter_preserves_private_inputs(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "task-001.json").write_text(json.dumps({
        "id": "task-001",
        "prompt": "analyze input",
        "input": {"x": [1, 2]},
        "reference": {"answer": 3},
    }), encoding="utf-8")
    out = tmp_path / "tasks"
    result = convert_scienceagentbench(source, out)
    assert result == ["scienceagentbench.task_001"]
    task = out / "scienceagentbench" / "task_001"
    assert (task / "task_meta.yaml").exists()
    assert (task / "private" / "task-001.json").exists()
    assert not (task / "task_meta.yaml").read_text(encoding="utf-8").__contains__("answer")


def test_runtime_dockerfiles_are_headless_and_fail_closed():
    openfoam = build_runtime_dockerfile("cfdllmbench")
    cosmo = build_runtime_dockerfile("cosmo-agent")
    assert "openfoam" in openfoam.lower()
    assert "freecad" in cosmo.lower()
    assert "Xvfb" in cosmo
    assert "set -eu" in cosmo


def test_tool_registry_validates_names_and_invokes(tmp_path: Path):
    registry_file = tmp_path / "tools.json"
    registry_file.write_text(json.dumps({
        "tools": [{
            "name": "add",
            "description": "add two numbers",
            "input_schema": {"type": "object"},
            "command": ["python3", "-c", "print(3)"],
        }]
    }), encoding="utf-8")
    registry = load_tool_registry(registry_file)
    assert [tool["name"] for tool in registry.list_tools()] == ["add"]
    result = registry.call("add", {})
    assert result["stdout"].strip() == "3"
