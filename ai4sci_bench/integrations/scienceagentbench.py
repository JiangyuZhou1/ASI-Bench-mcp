"""Convert a private ScienceAgentBench input bundle to ASI task instances."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


def _safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_")
    return value or "instance"


def convert_scienceagentbench(source_dir: str | Path, output_dir: str | Path) -> list[str]:
    """Convert JSON inputs without copying reference/answer fields publicly.

    The resulting task is deliberately ``in_development`` and stores the
    source record under ``private/``.  This keeps the benchmark's no-redistribution
    policy intact while allowing local runners and private scorers to use it.
    """
    source = Path(source_dir).expanduser().resolve()
    output = Path(output_dir).expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f"ScienceAgentBench source is not a directory: {source}")
    created: list[str] = []
    for record_path in sorted(source.rglob("*.json")):
        record: Any = json.loads(record_path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            continue
        raw_id = str(record.get("id") or record_path.stem)
        name = _safe_name(raw_id)
        task_id = f"scienceagentbench.{name}"
        task_dir = output / "scienceagentbench" / name
        task_dir.mkdir(parents=True, exist_ok=True)
        private_dir = task_dir / "private"
        private_dir.mkdir(exist_ok=True)
        (private_dir / record_path.name).write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (private_dir / "input.json").write_text(
            json.dumps(record.get("input", {}), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        prompt = str(record.get("prompt", "Solve the scientific programming task."))
        for level in ("b1", "b2", "b3", "b4"):
            (private_dir / f"prompt_{level}.md").write_text(prompt + "\n", encoding="utf-8")
        public = {
            "id": task_id, "name": raw_id, "version": "1.0",
            "status": "in_development", "domain": "computer_science",
            "subdomain": "scientific_programming",
            "source": {"paper": "ScienceAgentBench", "repo": "https://github.com/OSU-NLP-Group/ScienceAgentBench"},
            "difficulty": {"estimated_lines": 100, "estimated_time_minutes": 30,
                           "requires_gpu": False, "requires_network": False},
            "tags": ["scienceagentbench", "private-input-bundle"],
            "runtime": {"python": ">=3.11", "packages": []},
            "prompts": {"b1": "private/prompt_b1.md", "b2": "private/prompt_b2.md", "b3": "private/prompt_b3.md", "b4": "private/prompt_b4.md"},
            "input": {"files": [{"name": "private/input.json", "type": "data", "description": "Private benchmark input record"}]},
            "output": {"files": [{"name": "solution.py", "type": "code", "description": "Self-contained Python solution"}]},
        }
        (task_dir / "task_meta.yaml").write_text(yaml.safe_dump(public, sort_keys=False), encoding="utf-8")
        created.append(task_id)
    return created
