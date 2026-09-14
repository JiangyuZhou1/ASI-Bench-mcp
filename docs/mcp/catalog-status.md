# MCP catalog status

The formal `science_mcp_catalog.json` now contains 510 entries. It includes
the original 17 server definitions plus the 49-entry additional catalog, the
415-entry second catalog, and the 29-entry extended catalog.

Promotion makes every entry discoverable through `asibench mcp catalog` and
validates a server configuration for it. It does not claim that every backend
is installed or that every candidate has a maintained upstream MCP project.
Entries marked `availability: candidate_wrapper` use an explicit executable
placeholder and list the software, bridge, license, hardware, or endpoint
prerequisites required by an operator.

Before running a task, use `asibench mcp check --config <file>` and perform a
local capability check. Commercial GUI applications, physical instruments,
and services requiring credentials remain operator-configured.
