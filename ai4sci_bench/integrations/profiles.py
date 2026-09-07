"""Declarative integration profiles and reproducible runtime templates."""

from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationProfile:
    name: str
    runtime_tools: tuple[str, ...]
    notes: str


INTEGRATION_PROFILES = {
    "scienceagentbench": IntegrationProfile(
        "scienceagentbench", ("python",),
        "Private benchmark bundle; only inputs are copied into an instance.",
    ),
    "cfdllmbench": IntegrationProfile(
        "cfdllmbench", ("openfoam",),
        "Use a pinned OpenFOAM image for FoamBench; CFDQuery/CodeBench need no solver.",
    ),
    "sciagentgym": IntegrationProfile(
        "sciagentgym", ("python", "tool-registry-mcp"),
        "Expose only the tools listed by each instance registry.",
    ),
    "cosmo-agent": IntegrationProfile(
        "cosmo-agent", ("freecadcmd", "fem", "xvfb"),
        "Headless CAD/FEA runtime; exchange STEP/FCStd/VTK through declared outputs.",
    ),
}


def build_runtime_dockerfile(integration: str) -> str:
    """Return a conservative Dockerfile for an integration task.

    Images are intentionally not built by the framework: operators pin and
    build them locally, so licensed/proprietary applications never enter the
    public package or task repository.
    """
    if integration == "cfdllmbench":
        return """FROM opencfd/openfoam-org:ubuntu
SHELL [\"/bin/bash\", \"-o\", \"pipefail\", \"-c\"]
RUN set -eu; test -x /usr/lib/openfoam/openfoam*/etc/bashrc
WORKDIR /workspace
ENTRYPOINT [\"/bin/bash\", \"-lc\"]
"""
    if integration == "cosmo-agent":
        return """FROM ubuntu:24.04
SHELL [\"/bin/bash\", \"-o\", \"pipefail\", \"-c\"]
RUN set -eu; apt-get update; apt-get install -y --no-install-recommends \\
    freecad xvfb python3 python3-pip; rm -rf /var/lib/apt/lists/*
ENV DISPLAY=:99
WORKDIR /workspace
ENTRYPOINT [\"/bin/bash\", \"-lc\", \"set -eu; Xvfb :99 -screen 0 1280x1024x24 & exec \\\"$@\\\"\", \"--\"]
"""
    if integration in INTEGRATION_PROFILES:
        return """FROM python:3.12-slim
WORKDIR /workspace
"""
    raise ValueError(f"Unknown integration: {integration}")
