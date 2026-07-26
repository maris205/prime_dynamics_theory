# TPC-120 / MVP2: global route decision

Paper title:

> *TPC-MVP2: A Typed Global Route Decision after TPC-103--119:
> Certified Gates, Stopped Subroutes, Open Inputs, and the Next
> Minimal Tests*

## Core result

The paper maps TPC-103--119 into the nine working gates H1--H9 of
TPC-MVP1. It separates theorem-backed L0/L1 interfaces from open
arithmetic or growing-carrier inputs, and distinguishes a stopped
subroute from a global impossibility result.

The resulting decision is

```text
GLOBAL VERDICT = NOT_TESTABLE
```

This is a repository-snapshot decision for TPC-103--119 as audited on
2026-07-26, not a timeless impossibility statement. In particular,
the canonical H8 archive is one strong sufficient certificate format;
the snapshot also contains no alternative complete exact
intertwining.

It is not `GO`: no H1--H9 conjunction and no strict actual-carrier
endpoint certificate have been proved. It is not `INFEASIBLE`:
the stopped positive/geometric/phase-blind subroutes do not exclude
the remaining coefficient-specific signed routes. `REROUTE` applies
locally to those stopped subroutes.

## Strict endpoint rule

The physical ledger must satisfy

```text
Lambda_phys < 1/400.
```

Equality is a stop. Unknown physical costs may not be entered as
zero, and the determinant/zero-mode reserve may not be reused as
physical endpoint slack.

## Recommended next gates

1. TPC-121: certify the three actual post-bin inputs needed for a
   determinant-energy lower bound.
2. TPC-122: transfer signed-prefix, bounded-variation, and content
   remainder control to a zero-mode exponent.
3. TPC-123: build the complete native-atom reconnection matrix/archive.
4. TPC-124: test one literal H3 block with its fixed shift, prefixes,
   phases, signs, and physical normalization intact.

The first two attack H5. The latter two are parallel physical/H3
tests and must not be reported as substitutes for fixed-shift
arithmetic cancellation.

## Claim level

- Typed decision calculus and dependency audit: L0/L1.
- Several exact finite-dimensional identities in TPC-103--119: L1.
- No new L2 fixed-shift saving, parity breakthrough, Hardy--Littlewood
  asymptotic, prime-pair lower bound, or twin-prime theorem.

## Reproduce

```powershell
python experiments/tpc120_global_route_audit.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-120-mvp2-global-route-decision.pdf`

SHA-256:

`94094fae269f93f8a0e2108be6026deba5de321e9bdb6e91d9e35c4fdca71dd0`
