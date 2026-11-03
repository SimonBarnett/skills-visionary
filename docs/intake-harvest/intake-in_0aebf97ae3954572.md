what: When a Plan FR needs deterministic detection on a chair/ops host and a wake/notify on a named cloud-agent desktop host, lock those hosts separately in the vision pack.
where: Plan seat visionary FR packs (bobiverse ticket-closure → Grok Bot Bob pattern).
evidence: Operator locked wake on Bob desktop while detection can stay on ionos; single require_machine=ionos would strand wake work.
fix / lesson: Split small FRs (detect vs wake), stamp require_machine per host, require a de-dupe cursor before any wake transport, and keep monitor non-chair (wake ≠ !assign). Test: would help plan a different product with chair detect + desktop agent notify.
---
_via-intake id=`in_0aebf97ae3954572` ts=`2026-11-03T13:53:19Z`_
_source machine=`marchhare` agent=`Report-BobiverseIntakeIssue` book=`harvest-skills-visionary` ver=`-`_
