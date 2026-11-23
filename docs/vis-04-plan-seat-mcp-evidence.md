# VIS-04 / FR #141 evidence

Plan seat start loads skills from `https://plan.ntsa.uk/mcp`.

`tools/plan_seat_mcp.py` posts JSON-RPC `initialize`, then `tools/call` `list_catalog`, then `tools/call` `get_skill` for one catalog name.

Live smoke on this seat returned catalog skills including `visionary`, and `get_skill` for `visionary` returned `skillMd`.

Fail-when: a start path that does not call the MCP. The unit test rejects a loader that skips `list_catalog` or `get_skill`.
