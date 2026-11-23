# Fixture: fr-digest-no-double-park (VIS-G5 / FR #220)

Prove Plan does **not** double-park children with `hold` when
`Depends-on: #<digest>` is already the go-gate.

## Rules

- Digest: `fr-digest` + `hold` (unchanged VIS-G1).
- Default child: `feature-request` only + `Depends-on: #<digest>` — **no** `hold`.
- Unhold the digest alone releases children (BOB-G1 / chair Depends-on gate).
- Child `hold` only with an explicit `**Child-hold (intra-batch):**` body stamp
  for sequencing beyond the digest.

## Fail-when

- Child has `hold` / `on-hold` and Depends-on digest without a Child-hold reason.
- Vision text that says "unhold digest to release children" while still
  requiring per-child hold for every row.

## Check

```text
python tools/check_fr_digest_no_double_park.py docs/fixtures/fr-digest-no-double-park/park-manifest.json
```
