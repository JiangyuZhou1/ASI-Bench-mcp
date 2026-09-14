"""Audit catalog entries without claiming that candidates are runnable.

Usage: ``python tools/verify_mcp_catalog.py``. The command emits JSON so CI or
operators can archive the result. Verification is intentionally conservative:
placeholder paths, missing commands, and GitHub search URLs never pass.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any


def classify(name: str, entry: dict[str, Any]) -> dict[str, str]:
    server = entry.get("server", {})
    source = str(entry.get("source", ""))
    if "url" in server:
        backend = "remote_endpoint"
    else:
        command = str(server.get("command", ""))
        args = " ".join(map(str, server.get("args", [])))
        if "/path/to/" in command or "/path/to/" in args:
            backend = "placeholder"
        elif command in {"uv", "uvx", "npx", "docker", "ros2"}:
            # A generic launcher being installed says nothing about whether
            # its package/image/subcommand exists or starts an MCP server.
            backend = "launcher_unverified"
        elif os.path.isabs(command):
            backend = "installed" if os.access(command, os.X_OK) else "missing_absolute"
        else:
            backend = "installed" if shutil.which(command) else "missing_command"
    if "github.com/search?" in source:
        provenance = "search_only"
    elif "github.com/" in source and "mcp" not in source.lower():
        provenance = "software_repo"
    else:
        provenance = "explicit_source"
    if backend in {"installed", "remote_endpoint"} and provenance == "explicit_source":
        verdict = "verified"
    elif backend == "installed" and provenance == "software_repo":
        verdict = "runtime_only"
    else:
        verdict = "unverified"
    return {"backend": backend, "provenance": provenance, "verdict": verdict}


def audit(path: str | Path | None = None) -> dict[str, Any]:
    catalog_path = Path(path) if path else Path(__file__).parents[1] / "ai4sci_bench/data/science_mcp_catalog.json"
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))["servers"]
    results = {name: classify(name, entry) for name, entry in entries.items()}
    summary: dict[str, int] = {}
    for result in results.values():
        key = result["verdict"]
        summary[key] = summary.get(key, 0) + 1
    return {"total": len(results), "summary": summary, "entries": results}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False, sort_keys=True))
