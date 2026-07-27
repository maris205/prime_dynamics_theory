# TPC-142 / MVP4: Source-locked route decision

Paper title:

> *TPC-MVP4: A Source-Locked Route Decision after TPC-133--141:
> Frontier Totalization, Arithmetic Shadows, and the Strict Endpoint*

## Current decision

TPC-133--136 now provide an exact native entrance and a complete cut
archive.  The source-locked first-missing record has therefore moved
from the generic MVP3 item `H1.archive` to

```text
H1.frontier_totalization
```

“Complete cut” means an exact partition and reconnection of the three
declared cut classes. It does not mean that the frontier or the full
actual carrier has been totalized.

Every frontier terminal still needs total downstream `Q_D`, `Q_Z`,
`G`, fixed-`h0`, cover, reconnection, and physical occurrence records,
or a separate theorem bounding its complete original-scale sum by
`o(X)`.

TPC-137--140 provide a fixed-data logarithmic arithmetic shadow and a
restricted positive small-polylog affine power-of-log estimate outside
a small logarithmic-density exceptional set, together with scoped
non-transfer and selector firewalls and a conditional power ledger.
Actual CRT-family containment, squarefree/periodic reassembly,
local exceptional-set control on every terminal window, deterministic
prefixes, and a fixed `X`-power saving remain open. In particular, a
global cumulative exceptional-set density is not reused as a
same-rate terminal-window estimate. The physical occurrence registry
and strict `1/400` certificate also remain incomplete. Consequently:

```text
MVP4 VERDICT = NOT_TESTABLE
```

This is not `GO`, not `ARITHMETIC_FRONTIER`, and not
`ARCHITECTURE_INFEASIBLE`.

The recorded hashes detect source drift only. A matching hash does not
certify theorem correctness, generator completeness, or tuple
uniqueness. H9 is checked for both direct and indirect dependence on
H2--H5, and the current endpoint remains incomplete rather than
passed.

## Verdict calculus

Malformed snapshots return `INVALID_SNAPSHOT`, which is not a
mathematical route verdict.  Valid snapshots use this ordered,
exhaustive classifier:

```text
GO
ARCHITECTURE_INFEASIBLE
REROUTE
STOP_ROUTE
NOT_TESTABLE
ARITHMETIC_FRONTIER
OPEN
```

`ARITHMETIC_FRONTIER` requires all selected-route structural nodes and
the strict physical endpoint to be proved independently of the open
arithmetic nodes.  Frozen, logarithmic, almost-scale, conditional, or
scope-mismatched evidence cannot trigger it.

## Reproduce

Run TPC-141 first, then:

```powershell
python experiments/tpc142_mvp4_route_audit.py
python experiments/tpc142_mvp4_route_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc142_mvp4_snapshot.json
experiments/tpc142_mvp4_route_audit.json
```

Stable archival PDF:

`tpc-142-mvp4-source-locked-route-decision.pdf`
