# TPC-162: MVP6 actual-carrier endpoint route decision

Paper title:

> *MVP6 on the Actual-Carrier Endpoint Corridor: A Source-Locked
> Route Decision after Occurrence and Almost-Prefix Return*

## Decision

TPC-161 is imported under canonical UTF-8/LF source locks, with
independent consistency checks against the TPC-156 structural route
decision and the TPC-160 Abel-return audit. The current verdict is

```text
current_verdict = NOT_TESTABLE
first_missing = H1.theorem_backed_occurrence_provenance_crosswalk
```

The selected synthesis root has the typed minimal blocker antichain:

```text
H1.theorem_backed_occurrence_provenance_crosswalk
H9.endpoint_registry
H9.literal_weight_registry
H9.normalization_registry
H9.phase_cell_registry
```

The first line is the canonical selected representative. It must not
erase the other four incomparable blockers. Separately, the two
parent-ready `OPEN` nodes are:

```text
O161.bad_endpoint_pointwise_core
O161.direct_additive_twist_core
```

The current-artifacts-only actual-lift route has a scoped stop. This
does not stop either the occurrence-augmented map route or the
scalar-plus-ETO route. The route universe has no completeness theorem,
so `ARCHITECTURE_INFEASIBLE` is unavailable.

## What advanced

TPC-159 proves an actual determinant-two, fixed-`h0=2`, periodic-core
prefix estimate outside a sparse dyadic shadow. Its level is
`L1_ACTUAL_PREFIX_ALMOST_ENDPOINT`. TPC-160 proves the exact
exceptional-variation Abel interface for passing such prefix
information through a weight.

These results do not provide a deterministic all-prefix theorem, a
source-locked literal physical weight, a fixed positive power of `X`,
or the complete physical endpoint. They are therefore not a positive
fixed-`X` `L2` result.

## Classifier

Validation has the outer result `INVALID`. On a valid snapshot the
ordered verdicts are:

```text
GO
ARCHITECTURE_INFEASIBLE
REROUTE
STOP_ROUTE
NOT_TESTABLE
ARITHMETIC_FRONTIER
OPEN
```

The audit distinguishes a typed minimal `NOT_TESTABLE` blocker
antichain from a parent-ready `OPEN` frontier. Rerouting still requires
a theorem-backed typed crosswalk and a fresh registry. Architecture
infeasibility still requires an independently proved complete route
universe.

The production run uses `SOURCE_LOCKED` evidence. Every route stop,
completeness claim, and crosswalk must resolve through a typed
route-evidence registry; file-backed entries are checked by canonical
path and hash. Verdict reachability is tested separately in
`SYNTHETIC_REACHABILITY` mode. Those fixtures and inline assumptions
carry no theorem semantics and cannot satisfy the production mode.
The blocker antichain records the transitive ancestor closure computed
from the TPC-161 DAG, and a scope-incompatible node is accepted as a
typed blocker even if its local status is `PROVED`.

## Next forced objects

Structural:

```text
H1.theorem_backed_occurrence_provenance_crosswalk
```

Arithmetic/physical-return:

```text
source-locked literal physical weight
production phase-cell registry
actual endpoint registry
literal normalization registry
small exceptional-set variation or pointwise bad-endpoint control
```

Only after the structural carrier and physical endpoint close may the
program honestly expose a pure positive-`L2` arithmetic frontier.

## Reproduce

Run TPC-161 in default mode first, then:

```powershell
python experiments/tpc162_mvp6_route_audit.py
python experiments/tpc162_mvp6_route_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc162_mvp6_snapshot.json
experiments/tpc162_mvp6_route_audit.json
experiments/fixtures/tpc162_route_universe_complete_fixture.json
experiments/fixtures/tpc162_r1_r2_crosswalk_fixture.json
```

Stable archival PDF:

`tpc-162-mvp6-actual-carrier-endpoint-route-decision.pdf`

## Claim boundary

This paper proves a source-locked L0/L1 route decision. It does not
prove a production occurrence crosswalk, a complete actual carrier, a
deterministic all-prefix estimate, positive fixed-`X` L2, the strict
`1/400` endpoint, a prime-pair lower bound, or the twin-prime
conjecture.
