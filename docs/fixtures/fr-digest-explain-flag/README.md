# Fixture: VIS-G4 digest explain + Digest flag

Pass pack for `tools/check_fr_digest_explain_flag.py`.

## Success S1

- Digest body has `Kind: fr-digest` / `Digest: true`.
- `## Vision` summarizes intent, success, out of scope.
- Docs / vision pack / index links present.
- Labels include `fr-digest` only (+ `hold` at create).

## Fail-when

- Body is only a Children table (no vision summary).
- Missing Digest flag or docs link.
- Missing `fr-digest` label; or dual `digest`+`fr-digest`.
- `digest`/`hold` labels on a PR-shaped stamp.

```text
python tools/check_fr_digest_explain_flag.py docs/fixtures/fr-digest-explain-flag/park-stamp.json
```

## Dual-label fail (FR #253)

`python tools/check_fr_digest_explain_flag.py docs/fixtures/fr-digest-explain-flag/park-stamp-dual-fail.json` must exit non-zero (`digest` + `fr-digest` dual stamp).
