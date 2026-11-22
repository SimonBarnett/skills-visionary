"""VIS-04: fake MCP must serve list_catalog and get_skill at start."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan_seat_mcp as seat  # noqa: E402


class _Resp:
    def __init__(self, body: bytes):
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_load_calls_list_catalog_and_get_skill():
    calls = []

    def opener(req, timeout=0):
        payload = json.loads(req.data.decode("utf-8"))
        calls.append(payload["method"] if payload["method"] != "tools/call" else payload["params"]["name"])
        if payload["method"] == "initialize":
            body = {"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2024-11-05"}}
        elif payload["params"]["name"] == "list_catalog":
            text = json.dumps({"skills": [{"name": "visionary", "title": "visionary"}]})
            body = {"jsonrpc": "2.0", "id": 2, "result": {"content": [{"type": "text", "text": text}]}}
        else:
            assert payload["params"]["arguments"]["name"] == "visionary"
            text = json.dumps({"name": "visionary", "skillMd": "# visionary"})
            body = {"jsonrpc": "2.0", "id": 3, "result": {"content": [{"type": "text", "text": text}]}}
        return _Resp(json.dumps(body).encode("utf-8"))

    loaded = seat.load_plan_seat_skills("https://plan.ntsa.uk/mcp", opener=opener)
    assert calls == ["initialize", "list_catalog", "get_skill"]
    assert loaded["skill"]["name"] == "visionary"
    assert "plan.ntsa.uk/mcp" in loaded["url"]


if __name__ == "__main__":
    test_load_calls_list_catalog_and_get_skill()
    print("ok")
