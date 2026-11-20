#!/usr/bin/env python3
"""FR #81: rebuild docs/skill-sources/skills-visionary/_dag from .grok/skills.

Also refreshes apps/mcp-catalog/catalog/<id>/{meta.json,SKILL.md} mirrors.
.source of truth remains .grok/skills.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".grok" / "skills"
CATALOG_ROOT = ROOT / "apps" / "mcp-catalog" / "catalog"
DAG_DIR = ROOT / "docs" / "skill-sources" / "skills-visionary" / "_dag"

# Logical depends_on (frontmatter is empty; orchestrator prose defines these)
DEPENDS = {
    "plan-git-from-plan": [
        "visionary",
        "plan-create-repo",
        "plan-bob-webhooks",
        "plan-enable-prs",
    ],
    "plan-create-repo": ["plan-bob-webhooks", "plan-enable-prs"],
    "harvest-skills-visionary": ["harvest-agent-skills"],
}

TOPIC = {
    "visionary": "plan",
    "plan-git-from-plan": "plan",
    "plan-create-repo": "plan",
    "plan-bob-webhooks": "plan",
    "plan-enable-prs": "plan",
    "harvest-skills-visionary": "harvest",
    "harvest-agent-skills": "harvest",
}


def main() -> None:
    skills = []
    for d in sorted(SKILLS_ROOT.iterdir()):
        sk = d / "SKILL.md"
        if not sk.is_file():
            continue
        text = sk.read_text(encoding="utf-8")
        name_m = re.search(r"^name:\s*[\"']?([\w.-]+)", text, re.M)
        name = name_m.group(1) if name_m else d.name
        desc = ""
        dm = re.search(r"^description:\s*>\s*\n((?:[ \t].+\n)+)", text, re.M)
        if dm:
            desc = " ".join(x.strip() for x in dm.group(1).splitlines() if x.strip())
        else:
            dm2 = re.search(r"^description:\s*[\"']?(.+)", text, re.M)
            if dm2:
                desc = dm2.group(1).strip()
        desc_ascii = desc.encode("ascii", "replace").decode("ascii")[:240]
        title = name.replace("-", " ")
        topic = TOPIC.get(name, "plan")
        skills.append(
            {
                "id": name,
                "title": title,
                "description": desc_ascii,
                "topic": topic,
            }
        )

        out = CATALOG_ROOT / name
        out.mkdir(parents=True, exist_ok=True)
        meta = {
            "name": name,
            "title": title,
            "description": desc_ascii,
            "version": "1.0.0",
            "topic": topic,
            "source": f".grok/skills/{name}/SKILL.md",
        }
        (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        shutil.copy2(sk, out / "SKILL.md")

    built = date.today().isoformat()
    nodes = []
    edges = []
    for topic in sorted(set(TOPIC.values())):
        nodes.append(
            {
                "id": f"topic:{topic}",
                "type": "topic",
                "title": topic,
                "path": topic,
                "triggers": [topic],
                "weight": "normal",
            }
        )
    # topic navigation loops are OK for check-dag
    edges.append({"from": "topic:plan", "to": "topic:harvest", "rel": "related"})
    edges.append({"from": "topic:harvest", "to": "topic:plan", "rel": "related"})

    for s in skills:
        sid = f"skill:{s['id']}"
        nodes.append(
            {
                "id": sid,
                "type": "catalog-skill",
                "title": s["title"],
                "path": f"apps/mcp-catalog/catalog/{s['id']}/SKILL.md",
                "topic": s["topic"],
                "summary": s["description"][:200],
                "triggers": [s["id"].replace("-", " "), s["id"]],
            }
        )
        edges.append({"from": sid, "to": f"topic:{s['topic']}", "rel": "loads_topic"})
        for dep in DEPENDS.get(s["id"], []):
            edges.append({"from": sid, "to": f"skill:{dep}", "rel": "depends_on"})

    dag = {
        "version": 1,
        "built": built,
        "repo": "SimonBarnett/skills-visionary",
        "lessonsRoot": "docs/skill-sources/skills-visionary",
        "nodeCount": len(nodes),
        "edgeCount": len(edges),
        "defaults": {"maxSkills": 8, "maxBytes": 24000},
        "nodes": nodes,
        "edges": edges,
    }
    index = {
        "version": 1,
        "built": built,
        "note": "Slim index for skills-visionary plan DAG (FR #81).",
        "nodeCount": len(nodes),
        "defaults": dag["defaults"],
        "nodes": [
            {"id": n["id"], "type": n["type"], "title": n.get("title", "")} for n in nodes
        ],
    }
    DAG_DIR.mkdir(parents=True, exist_ok=True)
    (DAG_DIR / "dag.json").write_text(json.dumps(dag, indent=2) + "\n", encoding="utf-8")
    (DAG_DIR / "dag-index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"build-skill-dag: skills={len(skills)} nodes={len(nodes)} edges={len(edges)}")


if __name__ == "__main__":
    main()
