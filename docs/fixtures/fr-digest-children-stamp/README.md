# Fixture: VIS-G2 children Depends-on digest

Pass pack for `tools/check_fr_digest_children_stamp.py`.

## Success S1

- Each child body has `Depends-on: #100` (the digest).
- Digest `## Children` table lists `#101` and `#102`.

## Fail-when

- Child missing Depends-on digest.
- Digest body empty of children (table missing child `#N`).

```text
python tools/check_fr_digest_children_stamp.py docs/fixtures/fr-digest-children-stamp/park-stamp.json
```
