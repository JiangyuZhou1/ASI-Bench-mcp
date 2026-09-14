"""Small, dependency-free MCP bridges for locally installed science tools."""

from .server import BridgeServer, ToolSpec, available_tools

__all__ = ["BridgeServer", "ToolSpec", "available_tools"]
