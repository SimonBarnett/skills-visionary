# Fixture pack: parallel default under digests (FR #243 / VIS-G6)

Default park: implementation children `Depends-on: #<digest>` only (parallel).
Linear `#N` sibling chains need `**Sequencing (intra-batch):**` or
`**Child-hold (intra-batch):**`.

## Check

```text
python tools/check_fr_digest_parallel_default.py \
  docs/fixtures/fr-digest-parallel-default/park-manifest-parallel.json \
  docs/fixtures/fr-digest-parallel-default/park-manifest-nested-parallel.json
python tools/check_fr_digest_parallel_default.py \
  docs/fixtures/fr-digest-parallel-default/park-manifest-linear-fail.json
# expect FAIL on linear-fail
```
