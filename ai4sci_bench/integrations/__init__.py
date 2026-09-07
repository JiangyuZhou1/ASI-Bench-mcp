"""Adapters and local runtime scaffolds for external science benchmarks.

The package intentionally contains integration metadata and small bridges only;
upstream benchmark data and licensed software remain operator-provided.
"""

from .profiles import INTEGRATION_PROFILES, build_runtime_dockerfile
from .scienceagentbench import convert_scienceagentbench
from .tool_registry import load_tool_registry

__all__ = [
    "INTEGRATION_PROFILES", "build_runtime_dockerfile",
    "convert_scienceagentbench", "load_tool_registry",
]
