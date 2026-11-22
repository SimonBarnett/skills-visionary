"""VIS-04: Plan seat loads skills from the plan.ntsa.uk MCP at start.

Calls list_catalog then get_skill. No secrets. The URL can be overridden
for a fake opener in tests.
"""
from __future__ import annotations

import json
import urllib.request
from typing import Any, Callable

DEFAULT_URL = "https://plan.ntsa.uk/mcp"


def _post(url: str, payload: dict, opener: Callable | None, timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "plan-seat/vis-04",
        },
    )
    open_fn = opener or urllib.request.urlopen
    with open_fn(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
    doc = json.loads(raw or "{}")
    if not isinstance(doc, dict) or doc.get("error"):
        raise RuntimeError("plan MCP error")
    return doc


def _tool_text(doc: dict) -> str:
    result = doc.get("result") or {}
    content = result.get("content") or []
    if not content or not isinstance(content[0], dict):
        raise RuntimeError("plan MCP tool returned no text")
    return str(content[0].get("text") or "")


def load_plan_seat_skills(
    url: str = DEFAULT_URL,
    *,
    opener: Callable | None = None,
    skill_name: str = "",
    timeout: float = 20.0,
) -> dict[str, Any]:
    """Start load: list_catalog, then get_skill for one catalog name."""
    _post(
        url,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "plan-seat", "version": "1"},
            },
        },
        opener,
        timeout,
    )
    listed = _post(
        url,
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "list_catalog", "arguments": {}},
        },
        opener,
        timeout,
    )
    catalog = json.loads(_tool_text(listed))
    skills = catalog.get("skills") or []
    if not isinstance(skills, list) or not skills:
        raise RuntimeError("plan catalog has no skills")
    name = skill_name.strip() or str((skills[0] or {}).get("name") or "").strip()
    if not name:
        raise RuntimeError("plan catalog skill has no name")
    got = _post(
        url,
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "get_skill", "arguments": {"name": name}},
        },
        opener,
        timeout,
    )
    skill = json.loads(_tool_text(got))
    if str(skill.get("name") or "") != name:
        raise RuntimeError("get_skill name mismatch")
    return {"url": url, "catalog": catalog, "skill": skill}


def main() -> int:
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    loaded = load_plan_seat_skills(url)
    skill = loaded["skill"]
    print("plan-seat mcp %s skill=%s" % (loaded["url"], skill.get("name")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
