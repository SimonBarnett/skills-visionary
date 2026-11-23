# Fixture pack: create fr-digest on hold first (VIS-G1)

**VIS-G1 / FR #155.** At batch park, Plan opens **one digest per target
repo** with labels `fr-digest` + `hold` **before** any child FR issues.

## Files

| File | Role |
|------|------|
| `park-manifest.json` | Ordered park: digest first, then children |
| `digest-issue-body.md` | Sample `gh issue create` body for the digest |

## Fail-when

- Children created with **no digest**
- Digest created **without** `hold` (or without `fr-digest`)
- Park order that creates children before the digest

Check:

```text
python tools/check_fr_digest_create_hold.py docs/fixtures/fr-digest-create-hold/park-manifest.json
```
