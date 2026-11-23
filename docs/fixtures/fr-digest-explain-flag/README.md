# Fixture: VIS-G4 digest explain + Digest flag

Pass pack for `tools/check_fr_digest_explain_flag.py`.

## Success S1

- Digest body has `Kind: fr-digest` / `Digest: true`.
- `## Vision` summarizes intent, success, out of scope.
- Docs / vision pack / index links present.
- Labels include `digest` and `fr-digest` (+ `hold` at create).

## Fail-when

- Body is only a Children table (no vision summary).
- Missing Digest flag or docs link.
- Missing `digest`/`fr-digest` label.
- `digest`/`hold` labels on a PR-shaped stamp.

```text
python tools/check_fr_digest_explain_flag.py docs/fixtures/fr-digest-explain-flag/park-stamp.json
```
