# Vision: mermaid small captioned

## Objective

One sentence win.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | pack validates | exit 0 | `python tools/validate-vision-pack.py` | non-zero |

LOCKED

## Shape

Primary: website

LOCKED

## Stack

Default: static HTML mocks.

LOCKED

## Architecture

Request path from browser to store.
```mermaid
flowchart LR
  A[Browser] --> B[API]
  B --> C[Store]
```

LOCKED
