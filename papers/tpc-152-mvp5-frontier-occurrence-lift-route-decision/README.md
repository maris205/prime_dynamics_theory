# TPC-152: MVP5 frontier occurrence-lift route decision

Paper title:

> *MVP5 at the Frontier Occurrence Lift: A Source-Locked Route
> Decision after the Four-Map and Actual-Core Audits*

## Decision

For the source-locked TPC-143--151 snapshot:

```text
current_verdict = NOT_TESTABLE
first_missing = H1.frontier_occurrence_lift
minimal_missing_set = [H1.frontier_occurrence_lift]
```

The selected route is open.  Several narrower routes have exact
scoped stop certificates, but the declared route list has no
independent completeness theorem and therefore cannot support an
`ARCHITECTURE_INFEASIBLE` verdict.
In particular, current-schema nonidentifiability applies only to the
maximal formal completion class defined by archived fields; it is not
an impossibility result on the unknown actual carrier.

On the selected map route, the next object is the occurrence lift.
The separate scalar route remains open only as a two-clause route: a
complete original-frontier `o(X)` theorem must be accompanied by
theorem-backed totalization or softness for every eligible-tail-open
path.  One finite sample with no such row is not enough.

TPC-149 contributes a real `L1_ACTUAL_CORE` arithmetic theorem.  It
does not trigger `ARITHMETIC_FRONTIER`: H1 and the physical registry
remain unavailable, and an almost-scale log-power result is not a
scope-matched positive-X-power L2 theorem.
The string `L2_ACTUAL_POSITIVE` is retained only as a target level;
its status is `NOT_PROVED` and its achieved flag is false.

## Strengthened classifier

The valid-snapshot precedence is:

```text
GO
ARCHITECTURE_INFEASIBLE
REROUTE
STOP_ROUTE
NOT_TESTABLE
ARITHMETIC_FRONTIER
OPEN
```

Validation failure is the separate outer result `INVALID`.

The classifier additionally requires:

- a theorem-backed complete route universe before declaring
  architecture infeasibility;
- a distinct fresh registry and typed crosswalk before rerouting;
- exact scope, carrier, normalization, and complete route-cell
  coverage for every stop; and
- the full scalar-plus-ETO required-artifact contract imported from
  TPC-151, rather than a scalar-only abbreviation; and
- a physical endpoint pass independent of H2--H5 before declaring the
  arithmetic frontier.

## Reproduce

```powershell
python experiments/tpc152_mvp5_route_audit.py
python experiments/tpc152_mvp5_route_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc152_mvp5_snapshot.json
experiments/tpc152_mvp5_route_audit.json
```

Stable archival PDF:

`tpc-152-mvp5-frontier-occurrence-lift-route-decision.pdf`
