# TPC-150: Actual-corridor window and selector ledger

Paper title:

> *Returning the Determinant-Two Mobius Corridor:
> Terminal-Window Loss, Atomic Prefixes, and Split Log/Power Ledgers*

## Core results

TPC-149 gives a local exceptional set inside `[sqrt(X),X]`.  On a
terminal window

```text
J_X = [X/omega, X] subset [sqrt(X),X], 1 < omega <= sqrt(X)
```

with

```text
log(omega) = (log X)^(theta+o(1)),
```

a source exceptional exponent `kappa_src` becomes only

```text
kappa_exc = kappa_src + theta - 1.
```

Thus a short terminal window can erase a genuine global/local-shell
power-of-log density saving.

The paper also proves a sharp deterministic-prefix nonimplication:
adding any finite set of requested prefix endpoints to an exceptional
set changes its logarithmic measure by zero.  Hence exceptional-set
density alone cannot certify any predetermined discrete prefix list.
A pointwise theorem, proved exceptional avoidance, or a quantitative
smoothing/selector crosswalk is still necessary.

The log ledger is kept separate from the fixed-X-power ledger.  Even
a positive returned logarithmic exponent has

```text
sigma_power = 0.
```

It cannot pay a positive endpoint loss or `1/400`.

## Current route status

The TPC-143--146 occurrence lift is still
`H1.frontier_occurrence_lift = REQUIRED_MISSING`.  Therefore the
actual frontier consumption remains `NOT_TESTABLE`.  The script
records the consumer fields without inventing affine coefficients,
periods, intervals, weights or prefix data.

No positive L2, fixed-X-power, endpoint, prime-pair, or twin-prime
claim is made.

## Reproduce

Run TPC-147--149 first, then:

```powershell
python experiments/tpc150_actual_return_audit.py
python experiments/tpc150_actual_return_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc150_actual_return_manifest.json
experiments/tpc150_actual_return_audit.json
```

Stable archival PDF:

`tpc-150-actual-corridor-window-selector-ledger.pdf`
