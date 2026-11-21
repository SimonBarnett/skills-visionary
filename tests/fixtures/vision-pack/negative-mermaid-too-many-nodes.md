# Vision: mermaid too many nodes

## Objective

One sentence win.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | pack validates | exit 0 | `python tools/validate-vision-pack.py` | non-zero |

LOCKED

## Shape

Primary: service

LOCKED

## Stack

Default: Python tools.

LOCKED

## Architecture

Giant flow that must be split (FR #22 ceiling 12).
```mermaid
flowchart TD
  N1[A] --> N2[B]
  N2 --> N3[C]
  N3 --> N4[D]
  N4 --> N5[E]
  N5 --> N6[F]
  N6 --> N7[G]
  N7 --> N8[H]
  N8 --> N9[I]
  N9 --> N10[J]
  N10 --> N11[K]
  N11 --> N12[L]
  N12 --> N13[M]
  N13 --> N14[N]
```

LOCKED
