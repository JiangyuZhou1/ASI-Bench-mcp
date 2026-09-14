#!/usr/bin/env python3
"""Generate private/example tasks for every catalogued MCP interface."""
from __future__ import annotations
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parents[1] / "ai4sci_bench" / "data"

def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def load_catalog() -> dict:
    base = json.loads((PKG / "science_mcp_catalog.json").read_text())['servers']
    for path in sorted(PKG.glob('science_mcp_catalog_*.json')):
        extra = json.loads(path.read_text())
        base.update(extra)
    return base

def main() -> None:
    catalog = load_catalog()
    for name, entry in catalog.items():
        path = HERE / slug(entry['category']) / slug(name)
        (path / 'input').mkdir(parents=True, exist_ok=True)
        (path / 'outputs').mkdir(parents=True, exist_ok=True)
        tool = f'{name}.smoke'
        (path / 'task_meta.yaml').write_text(
            f'schema_version: 1\nid: examples.mcp.{slug(name)}\n'
            f'title: {name} MCP example\ndomain: {entry["category"]}\n'
            'visibility: example\n' f'requires_tool: {tool}\n', encoding='utf-8')
        (path / 'task_eval.yaml').write_text(
            f'schema_version: 1\nmode: tool_smoke\nrequire_tool: {tool}\n'
            'acceptance: tool_invoked_and_result_recorded\n', encoding='utf-8')
        (path / 'tool_requirement.json').write_text(json.dumps({
            'required_tool': tool, 'mcp_server': name, 'must_invoke': True,
        }, indent=2) + '\n', encoding='utf-8')
        (path / 'input' / 'task_input.json').write_text(json.dumps({
            'server': name, 'operation': 'minimal smoke operation',
            'source': entry['source'],
        }, indent=2) + '\n', encoding='utf-8')
        prompt = (f'Use only the {name} MCP interface to perform one minimal '
                  'safe smoke operation. Report the tool result and do not '
                  'substitute another tool.\n')
        for level in range(1, 5):
            (path / f'prompt_b{level}.md').write_text(prompt, encoding='utf-8')
        (path / 'outputs' / 'tool_result.json').write_text(json.dumps({
            'status': 'not_run', 'required_tool': tool,
            'note': 'Example task; run with a configured MCP backend.',
        }, indent=2) + '\n', encoding='utf-8')
    manifest = {'schema_version': 1, 'suite': 'MCP example tasks',
                'task_count': len(catalog), 'tasks': []}
    for name, entry in sorted(catalog.items()):
        manifest['tasks'].append({'id': f'examples.mcp.{slug(name)}',
                                  'server': name,
                                  'category': entry['category'],
                                  'path': f'{slug(entry["category"])}/{slug(name)}'})
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (HERE / 'README.md').write_text(
        '# MCP example tasks\n\n'
        'This folder contains one isolated example task for every MCP interface '
        'in the scientific catalog. It is intentionally separate from formal '
        '`tasks/`; examples require an operator-configured MCP backend. Each '
        'task requires exactly one named MCP tool and records its output under '
        '`outputs/`. Regenerate with `python3 generate.py`.\n', encoding='utf-8')
    print(f'generated {len(catalog)} example tasks')

if __name__ == '__main__':
    main()
