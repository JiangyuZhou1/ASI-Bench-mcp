# Local MCP validation

Validated on 2026-09-14. A server handshake means `initialize` and
`tools/list` returned valid MCP JSON-RPC responses. A functional pass requires
an actual tool or backend operation, not only process discovery.

## MCP server handshakes

| Server | Result | Tools | Notes |
| --- | --- | ---: | --- |
| MuJoCo | Passed | 65 | Local source environment |
| Gazebo | Passed | 12 | Server tools enumerate; Gazebo runtime not exercised |
| OpenSCAD | Passed | 12 | Local source environment |
| OpenSees | Passed | 26 | Uses legacy-compatible `mcp<2` environment |
| ParaView | Passed | 34 | Uses legacy-compatible `mcp<2` environment |
| Zotero | Passed | 38 | Zotero desktop backend not exercised |
| Abaqus | Passed | 8 | Licensed Abaqus backend unavailable |
| CalculiX | Passed | 8 | Deno stdio server |
| Verilator | Passed | 4 | Node MCP server |
| Jupyter Server | Failed | 0 | Requires a running Jupyter MCP HTTP endpoint |

## Functional smoke tests

| Tool | Result | Operation |
| --- | --- | --- |
| OpenFOAM | Passed | Run pipe-flow MCP operation in local image |
| EnergyPlus | Passed | Run annual single-zone simulation and produce outputs |
| NetLogo | Passed | Create a headless random-walk model |
| PyNite | Passed | Create model, add two nodes, inspect model over MCP RPC |
| Text2Sim | Passed | Execute discrete-event queue simulation |
| PubChem | Passed | Query caffeine through MCP |
| FreeCAD | Passed | Create and save a parametric box headlessly |
| LAMMPS | Passed | Build a 32-atom Lennard-Jones crystal |
| Gmsh | Passed | Generate a 3D cube mesh |
| OpenMM | Passed | Evaluate a two-particle system |
| RadonPy | Passed | Create an ethanol molecular model |
| MDAnalysis | Passed | Calculate a center of mass |
| AFSIM MCP | Partial | Scenario management works; licensed simulator is absent |
| Blender MCP | Blocked | Blender CLI works; interactive addon socket is absent |
| SketchUp MCP | Blocked | Linux host has no SketchUp desktop/extension socket |
| GNS3 MCP | Failed | MCP handshake works, but server expects a different GNS3 API version |

The catalog audit remains conservative. `uv`, `uvx`, `npx`, `docker`, and
`ros2` are generic launchers; their presence alone does not verify the package,
image, subcommand, MCP handshake, or application backend.
