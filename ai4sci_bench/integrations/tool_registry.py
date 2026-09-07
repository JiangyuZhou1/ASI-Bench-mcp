"""Minimal allowlisted tool registry used by SciAgentGym-style instances."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class ToolRegistry:
    def __init__(self, tools: list[dict[str, Any]]):
        self._tools = {tool["name"]: tool for tool in tools}

    def list_tools(self) -> list[dict[str, Any]]:
        return [
            {"name": t["name"], "description": t.get("description", ""),
             "inputSchema": t.get("input_schema", {"type": "object"})}
            for t in self._tools.values()
        ]

    def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Tool is not allowlisted for this instance: {name}")
        command = tool.get("command")
        if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
            raise ValueError(f"Tool {name} must define a string command argv")
        completed = subprocess.run(command, input=json.dumps(arguments), text=True,
                                   capture_output=True, timeout=int(tool.get("timeout", 60)),
                                   cwd=tool.get("cwd"), check=False)
        return {"returncode": completed.returncode, "stdout": completed.stdout,
                "stderr": completed.stderr}


def load_tool_registry(path: str | Path) -> ToolRegistry:
    p = Path(path).expanduser().resolve()
    if not p.is_file() or p.is_symlink():
        raise ValueError(f"Tool registry must be a regular file: {p}")
    document = json.loads(p.read_text(encoding="utf-8"))
    tools = document.get("tools") if isinstance(document, dict) else None
    if not isinstance(tools, list) or not tools:
        raise ValueError("Tool registry must contain a non-empty tools list")
    names: set[str] = set()
    for tool in tools:
        if not isinstance(tool, dict) or not isinstance(tool.get("name"), str):
            raise ValueError("Each tool must be an object with a name")
        if tool["name"] in names:
            raise ValueError(f"Duplicate tool name: {tool['name']}")
        names.add(tool["name"])
    return ToolRegistry(tools)
