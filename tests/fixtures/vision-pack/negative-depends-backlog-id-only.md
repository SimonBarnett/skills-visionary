# Vision: fixture-negative-depends-backlog-id

**Depends-on:** BOB-06

## Objective

Negative fixture: bare backlog-id Depends-on must fail (VIS-D3 / FR #149).

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Example metric | 100% | `pytest tests/ -q` | never |

## Shape

Primary: website

Hybrid note: fixture only.

LOCKED

## Stack

Default: markdown

Why: tests

Why-not: none

LOCKED