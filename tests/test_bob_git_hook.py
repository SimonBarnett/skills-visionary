"""tools/bob_git_hook.py: exact fleet hook, ping 2xx, replay pre-hook items, Jeeves announce."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bob_git_hook", ROOT / "tools" / "bob_git_hook.py")
bgh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bgh)

REPO = "SimonBarnett/club-madeira-onboarding"
FLEET = {
    "id": 7,
    "active": True,
    "events": ["issues", "pull_request", "push"],
    "created_at": "2026-09-25T08:04:21Z",
    "config": {"url": "https://irc.ntsa.uk/bob/v1/git", "content_type": "json", "insecure_ssl": "0"},
}


class FakeGh:
    def __init__(self, hooks, deliveries=None, issues=None, pulls=None):
        self.hooks = hooks
        self.deliveries = deliveries if deliveries is not None else [
            {"id": 1, "event": "ping", "status_code": 204}
        ]
        self.issues = issues or []
        self.pulls = pulls or {}
        self.calls = []

    def __call__(self, args, stdin=None):
        self.calls.append((list(args), stdin))
        path = args[0]
        method = args[args.index("-X") + 1] if "-X" in args else "GET"
        if path == f"repos/{REPO}/hooks" and method == "GET":
            return json.dumps(self.hooks)
        if path == f"repos/{REPO}/hooks" and method == "POST":
            body = json.loads(stdin)
            hook = dict(FLEET, id=9, events=body["events"], active=body["active"], config=body["config"])
            self.hooks.append(hook)
            return json.dumps(hook)
        if path.startswith(f"repos/{REPO}/hooks/") and method == "PATCH":
            body = json.loads(stdin)
            hook = dict(self.hooks[0], events=body["events"], active=body["active"], config=body["config"])
            self.hooks[0] = hook
            return json.dumps(hook)
        if "/deliveries" in path:
            return json.dumps(self.deliveries)
        if path.endswith("/pings"):
            return ""
        if path == f"repos/{REPO}":
            return json.dumps({"full_name": REPO})
        if path.startswith(f"repos/{REPO}/issues"):
            return json.dumps(self.issues)
        if path.startswith(f"repos/{REPO}/pulls/"):
            return json.dumps(self.pulls[int(path.rsplit("/", 1)[1])])
        raise AssertionError(f"unexpected gh call {args}")


def _methods(gh):
    return [(c[0][0], c[0][c[0].index("-X") + 1] if "-X" in c[0] else "GET") for c in gh.calls]


def test_creates_exact_fleet_hook_when_absent():
    gh = FakeGh(hooks=[{"id": 3, "config": {"url": "https://amplify.example/x"}, "events": ["push"], "active": True}])
    hook, created = bgh.ensure_hook(REPO, gh)
    assert created
    posted = json.loads([c for c in gh.calls if "POST" in c[0]][0][1])
    assert posted == {
        "name": "web",
        "active": True,
        "events": ["issues", "pull_request", "push"],
        "config": {"url": "https://irc.ntsa.uk/bob/v1/git", "content_type": "json", "insecure_ssl": "0"},
    }
    assert "secret" not in posted["config"]  # fleet standard: no secret
    assert bgh.hook_drift(hook) == []
    assert len(gh.hooks) == 2  # unrelated hook left alone


def test_patches_drifted_hook_instead_of_adding_second():
    bad = dict(FLEET, events=["push"], config=dict(FLEET["config"], content_type="form"))
    gh = FakeGh(hooks=[bad])
    assert set(bgh.hook_drift(bad)) == {"events", "content_type"}
    hook, created = bgh.ensure_hook(REPO, gh)
    assert not created
    assert (f"repos/{REPO}/hooks/7", "PATCH") in _methods(gh)
    assert bgh.hook_drift(hook) == []
    assert len(gh.hooks) == 1


def test_matching_hook_is_left_untouched():
    gh = FakeGh(hooks=[dict(FLEET)])
    _, created = bgh.ensure_hook(REPO, gh)
    assert not created
    assert all(m == "GET" for _, m in _methods(gh))


def test_wait_ping_needs_2xx_and_sends_ping_when_none():
    gh = FakeGh(hooks=[dict(FLEET)], deliveries=[])
    assert bgh.wait_ping(REPO, 7, gh, timeout=0, sleep=lambda s: None) is None
    assert (f"repos/{REPO}/hooks/7/pings", "POST") in _methods(gh)
    assert bgh.ok_ping([{"event": "ping", "status_code": 500}]) is None
    assert bgh.ok_ping([{"event": "ping", "status_code": 204}])["status_code"] == 204


def test_missed_items_are_those_opened_before_the_hook():
    items = [
        {"number": 1, "state": "open", "created_at": "2026-09-25T08:04:00Z", "title": "Phase 0"},
        {"number": 2, "state": "open", "created_at": "2026-09-25T08:07:43Z", "pull_request": {}},
        {"number": 3, "state": "closed", "created_at": "2026-09-25T08:03:50Z"},
    ]
    assert [i["number"] for i in bgh.missed_items(items, "2026-09-25T08:04:21Z")] == [1]


def test_build_replay_shapes_match_github_opened_events():
    issue = {"number": 1, "title": "Phase 0", "user": {"login": "SimonBarnett"}}
    ev, payload = bgh.build_replay(issue, {"full_name": REPO})
    assert ev == "issues" and payload["action"] == "opened"
    assert payload["issue"]["number"] == 1 and payload["repository"]["full_name"] == REPO
    pr = {"number": 2, "title": "t", "user": {"login": "SimonBarnett"}}
    ev, payload = bgh.build_replay({"number": 2, "pull_request": {}}, {"full_name": REPO}, pr)
    assert ev == "pull_request" and payload["pull_request"]["number"] == 2


def test_post_replay_sets_github_headers():
    seen = {}

    def post(url, body, headers):
        seen.update(url=url, headers=headers, body=json.loads(body))
        return 204

    assert bgh.post_replay("issues", {"action": "opened"}, post=post) == 204
    assert seen["url"] == "https://irc.ntsa.uk/bob/v1/git"
    assert seen["headers"]["X-GitHub-Event"] == "issues"
    assert seen["headers"]["Content-Type"] == "application/json"


def test_announce_seen_requires_jeeves_on_bobiverse(tmp_path):
    log = tmp_path / "irc.log"
    log.write_text(
        ":bob-x!~u@h PRIVMSG #bobiverse :GIT issues SimonBarnett/club-madeira-onboarding opened #1 fake\n"
        ":Jeeves!~u@h PRIVMSG #marchhare :GIT issues SimonBarnett/club-madeira-onboarding opened #1 wrong chan\n"
        ":Jeeves!~u@h PRIVMSG #bobiverse :GIT issues SimonBarnett/club-madeira-onboarding opened #1 Phase 0 by SimonBarnett\n",
        encoding="utf-8",
    )
    needle = bgh.announce_needle("issues", REPO, 1)
    line = bgh.announce_seen(needle, [log])
    assert line and line.startswith(":Jeeves!") and "#bobiverse" in line
    assert bgh.announce_seen(bgh.announce_needle("ping", REPO), [log]) is None


def test_main_replays_pre_hook_issue_and_verifies_announce(tmp_path):
    log = tmp_path / "irc.log"
    log.write_text(
        f":Jeeves!~u@h PRIVMSG #bobiverse :GIT ping {REPO} Encourage flow. by SimonBarnett\n"
        f":Jeeves!~u@h PRIVMSG #bobiverse :GIT issues {REPO} opened #1 Phase 0 by SimonBarnett\n",
        encoding="utf-8",
    )
    gh = FakeGh(
        hooks=[dict(FLEET)],
        issues=[{"number": 1, "state": "open", "created_at": "2026-09-25T08:04:00Z", "user": {"login": "S"}}],
    )
    posted = []
    rc = bgh.main([REPO, "--replay-missed", "--irc-log", str(log), "--timeout", "0"], gh=gh,
                  post=lambda u, b, h: posted.append(h["X-GitHub-Event"]) or 204)
    assert rc == 0
    assert posted == ["issues"]


def test_main_fails_when_jeeves_never_announces(tmp_path):
    log = tmp_path / "irc.log"
    log.write_text("", encoding="utf-8")
    gh = FakeGh(hooks=[dict(FLEET)])
    assert bgh.main([REPO, "--irc-log", str(log), "--timeout", "0"], gh=gh, post=lambda *a: 204) == 2


def test_skills_gate_first_push_on_verified_hook():
    orch = (ROOT / ".grok/skills/plan-git-from-plan/SKILL.md").read_text(encoding="utf-8")
    hooks = (ROOT / ".grok/skills/plan-bob-webhooks/SKILL.md").read_text(encoding="utf-8")
    create = (ROOT / ".grok/skills/plan-create-repo/SKILL.md").read_text(encoding="utf-8")
    for text in (orch, hooks, create):
        assert "tools/bob_git_hook.py" in text
    assert orch.index("bob_git_hook.py") < orch.index("First commit")
    assert "before any push" in hooks.lower() or "before the first push" in hooks.lower()
    assert "--replay-missed" in hooks
