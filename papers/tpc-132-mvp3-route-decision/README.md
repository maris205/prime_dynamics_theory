# TPC-132 / MVP3: typed route decision

Paper title:

> *TPC-MVP3: A Typed Route Decision after TPC-121--131:
> Executable Archives, the Arithmetic Frontier, and Certified
> Branching*

## Core result

The paper gives seven ordered, exhaustive route outcomes after a
snapshot manifest passes consistency validation:

```text
GO
ARCHITECTURE_INFEASIBLE
REROUTE
STOP_ROUTE
NOT_TESTABLE
ARITHMETIC_FRONTIER
OPEN
```

The v2 validator rejects contradictory node, scope, route, stop-cover,
reroute, or endpoint records before applying this precedence. `GO`
requires one compatible fixed-`h0` carrier, theorem-backed H1--H9
records, and strict endpoint slack. `ARCHITECTURE_INFEASIBLE` requires
an exact proved cover of the declared route universe and a sourced
stop certificate for every route; it is not a negative theorem about
twin primes.

`ARITHMETIC_FRONTIER` is deliberately hard to reach. Every structural,
provenance, fixed-shift, and endpoint interface must already be proved,
and every unresolved node must have status `OPEN`, positive L2
evidence, and compatible scope. A conditional, refuted,
not-testable, or scope-mismatched record blocks this outcome; a
collection of reductions or conditional interfaces is not enough.

The frozen v2 manifest records source content hashes, the route
universe and selected route, the explicit H1--H9 DAG and validated
topological order, scope/carrier records, stop metadata, an incomplete
occurrence registry, and an incomplete endpoint certificate. The
first-missing item is therefore computed from the validated machine
DAG, rather than from paper order.

The audit also keeps finite L0/L1 results separate from their missing
growing instantiations. In particular, the current H3 target is the
actual Fejer four-Liouville estimate together with participation,
masks, phases, weights, origins, and prefixes. H7 is `NOT_TESTABLE`
because the shift-tagged growing archive/localization certificate is
incomplete. TPC-128 already proves its elementary divisor/CRT
expansion; what remains is a positive relative tail exponent at the
actual scales, modulus uniformity, a weighted census, and signed
retained-fiber estimates.

## Snapshot verdict

For the audited certificate bundle, the DAG-checked first missing item
is `H1.archive`, the complete actual-carrier native archive. Therefore

```text
MVP3 VERDICT = NOT_TESTABLE
```

The result is not `GO`, not `ARITHMETIC_FRONTIER`, and not
`ARCHITECTURE_INFEASIBLE`. No paper in TPC-121--131 is entered as a
proved positive L2 theorem.

## Reproduce

```powershell
python experiments/tpc132_mvp3_route_audit.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-132-mvp3-route-decision.pdf`

SHA-256:

`035a92bfa237d1369625f52a851eeb26b6b1e76dc1c2199167dfde1b925dcb57`
