# Scientific MCP discipline groups

The catalog is organized into small review groups (approximately two MCP
interfaces per group). Each entry remains an operator-configured template; the
catalog does not bundle proprietary software, credentials, or vendor data.

- **Multiphysics / CFD:** COMSOL, OpenFOAM; SU2, ParaView
- **Scientific computing:** MATLAB, Jupyter Server; Julia, MWORKS; OpenModelica
- **Robotics simulation:** Isaac Sim, MuJoCo; Gazebo, PyBullet; Webots, CARLA
- **Structural / finite elements:** PyNite, CalculiX; OpenSees, FEniCSx; Abaqus
- **System and agent simulation:** Simulink, EnergyPlus; Text2Sim, NetLogo
- **Flight dynamics / SITL:** JSBSim, PX4 SITL; ArduPilot SITL, AFSIM
- **CAD / 3D modeling:** Blender, FreeCAD; OpenSCAD, SketchUp; AutoCAD, Fusion 360
- **EDA / hardware:** OpenROAD, Verilator; Yosys, ngspice; KLayout, Arduino
- **Traffic / networks:** SUMO, GNS3
- **Chemistry / research data:** PubChem, Zotero
- **Laboratory / instrumentation:** Opentrons, SCPI/PyVISA

Use `asibench mcp catalog` to inspect the complete machine-readable catalog and
`asibench mcp init --servers ...` to generate a selected client configuration.
