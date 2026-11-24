# Fixture pack: create fr-digest on hold first (VIS-G1)

**VIS-G1 / FR #155 + CAST IRON digests-must-hold (operator 2026-11-24).**
At batch park, Plan opens every digest with labels `fr-digest` + `hold`
**before** implementation children. Nested phase digests are digests:
they **must** start on `hold` too.

## Files

| File | Role |
|------|------|
| `park-manifest.json` | Ordered park: digest first, then children |
| `park-manifest-nested.json` | Epic + phase digest both have `hold` |
| `digest-issue-body.md` | Sample `gh issue create` body for the digest |

## Fail-when

- Children created with **no digest**
- Any digest created **without** `hold` (or without `fr-digest`), including phase digests
- Park order that creates children before the digest

Check:

```text
python tools/check_fr_digest_create_hold.py docs/fixtures/fr-digest-create-hold/park-manifest.json docs/fixtures/fr-digest-create-hold/park-manifest-nested.json
```
