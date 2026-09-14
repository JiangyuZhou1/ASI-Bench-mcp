# Local MCP bridge

`python -m ai4sci_bench.mcp_bridge` exposes a dependency-free JSON-lines bridge
for open-source command-line tools installed on the worker. It never downloads
or emulates a solver: unavailable executables are reported as unavailable.

The bridge accepts requests such as:

```json
{"method":"status"}
{"method":"run","arguments":{"tool":"sumo","args":["--version"]}}
```

The initial allowlist covers OpenFOAM, SUMO, FreeCAD, Blender, OpenSCAD,
ParaView, Verilator, Yosys, ngspice, Gmsh, GDAL, QGIS, Pandoc, Snakemake and
Nextflow. Add a tool only when its command-line contract is understood and
covered by a test; proprietary or GUI-only catalog entries remain templates.
