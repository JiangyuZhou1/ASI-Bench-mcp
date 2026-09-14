"""A conservative JSON-lines bridge for command-line science applications.

The bridge deliberately executes only explicitly allowlisted commands. It is
useful for open-source tools already installed on a worker and reports missing
tools instead of pretending that a catalog entry is runnable.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolSpec:
    name: str
    executable: str
    description: str
    args: tuple[str, ...] = ()

    @property
    def installed(self) -> bool:
        if os.path.isabs(self.executable):
            return os.path.isfile(self.executable) and os.access(self.executable, os.X_OK)
        return shutil.which(self.executable) is not None


TOOL_SPECS: tuple[ToolSpec, ...] = (
    ToolSpec("openfoam", "blockMesh", "OpenFOAM mesh generation command"),
    ToolSpec("sumo", "sumo", "SUMO traffic simulation command"),
    ToolSpec("freecad", "FreeCADCmd", "FreeCAD headless command"),
    ToolSpec("blender", "blender", "Blender background command"),
    ToolSpec("openscad", "openscad", "OpenSCAD command-line renderer"),
    ToolSpec("paraview", "pvpython", "ParaView Python command"),
    ToolSpec("verilator", "verilator", "Verilator HDL simulator"),
    ToolSpec("yosys", "yosys", "Yosys synthesis command"),
    ToolSpec("ngspice", "ngspice", "ngspice circuit simulator"),
    ToolSpec("gmsh", "gmsh", "Gmsh mesh generator"),
    ToolSpec("gdal", "gdalinfo", "GDAL geospatial inspection command"),
    ToolSpec("qgis", "qgis_process", "QGIS processing command"),
    ToolSpec("pandoc", "pandoc", "Pandoc document conversion command"),
    ToolSpec("snakemake", "snakemake", "Snakemake workflow command"),
    ToolSpec("nextflow", "nextflow", "Nextflow workflow command"),
)


def available_tools() -> list[ToolSpec]:
    """Return only tools actually present in the current PATH."""
    return [spec for spec in TOOL_SPECS if spec.installed]


class BridgeServer:
    def __init__(self, specs: tuple[ToolSpec, ...] = TOOL_SPECS):
        self._specs = {spec.name: spec for spec in specs}

    def list_tools(self) -> list[dict[str, Any]]:
        tools = [
            {
                "name": "status",
                "description": "Report locally installed bridge commands.",
                "inputSchema": {"type": "object"},
            },
            {
                "name": "run",
                "description": "Run an allowlisted command with argv arguments.",
                "inputSchema": {
                    "type": "object",
                    "required": ["tool", "args"],
                    "properties": {
                        "tool": {"type": "string"},
                        "args": {"type": "array", "items": {"type": "string"}},
                        "timeout": {"type": "integer", "minimum": 1, "maximum": 3600},
                    },
                },
            },
        ]
        tools.extend([
            {"name": "pubchem_get", "description": "Fetch a PubChem compound record by name or CID.", "inputSchema": {"type": "object", "required": ["query"]}},
            {"name": "gns3_request", "description": "Call a configured GNS3 REST API endpoint.", "inputSchema": {"type": "object", "required": ["url"]}},
            {"name": "text2sim_validate", "description": "Validate a JSON discrete-event simulation configuration.", "inputSchema": {"type": "object", "required": ["config"]}},
        ])
        return tools

    def call(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        arguments = arguments or {}
        if name == "pubchem_get":
            query = arguments.get("query")
            if not isinstance(query, str) or not query.strip():
                raise ValueError("query must be a non-empty string")
            encoded = urllib.parse.quote(query.strip(), safe="")
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded}/property/MolecularFormula,MolecularWeight,CanonicalSMILES/JSON"
            try:
                with urllib.request.urlopen(url, timeout=15) as response:
                    return {"ok": True, "data": json.loads(response.read())}
            except Exception as exc:
                return {"ok": False, "error": str(exc)}
        if name == "gns3_request":
            url = arguments.get("url")
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                raise ValueError("url must be an HTTP(S) URL")
            request = urllib.request.Request(url, method=str(arguments.get("method", "GET")).upper())
            try:
                with urllib.request.urlopen(request, timeout=15) as response:
                    body = response.read().decode("utf-8")
                    try: body = json.loads(body)
                    except json.JSONDecodeError: pass
                    return {"ok": True, "status": response.status, "data": body}
            except Exception as exc:
                return {"ok": False, "error": str(exc)}
        if name == "text2sim_validate":
            config = arguments.get("config")
            if not isinstance(config, dict):
                raise ValueError("config must be an object")
            required = ("entities", "events")
            missing = [key for key in required if key not in config]
            return {"ok": not missing, "missing": missing, "config": config}
        if name == "status":
            return {
                "tools": {
                    key: {"executable": spec.executable, "installed": spec.installed}
                    for key, spec in self._specs.items()
                }
            }
        if name != "run":
            raise KeyError(f"Unknown bridge tool: {name}")
        tool = arguments.get("tool")
        spec = self._specs.get(tool)
        if spec is None:
            raise ValueError(f"Tool is not allowlisted: {tool}")
        if not spec.installed:
            return {"ok": False, "tool": tool, "error": f"Executable not found: {spec.executable}"}
        raw_args = arguments.get("args", [])
        if not isinstance(raw_args, list) or not all(isinstance(arg, str) for arg in raw_args):
            raise ValueError("args must be a list of strings")
        timeout = int(arguments.get("timeout", 60))
        if timeout < 1 or timeout > 3600:
            raise ValueError("timeout must be between 1 and 3600 seconds")
        completed = subprocess.run(
            [spec.executable, *spec.args, *raw_args],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=os.environ.copy(),
        )
        return {
            "ok": completed.returncode == 0,
            "tool": tool,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }


def serve_stdio(server: BridgeServer | None = None) -> None:
    server = server or BridgeServer()
    for line in sys.stdin:
        if not line.strip():
            continue
        request = json.loads(line)
        try:
            result = server.call(request.get("method", ""), request.get("arguments"))
            response = {"ok": True, "result": result}
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            response = {"ok": False, "error": str(exc)}
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()
