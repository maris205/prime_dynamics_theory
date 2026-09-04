# TPC-389 paper plan

## Research question

Does a count-slope interface that transfers across one finite family and one
endpoint remain predictive over a longer `1024 -> 1280` horizon on a fresh
coordinate family, when the parent slope is frozen before current responses?

## Contribution

The paper contributes a predeclared finite long-horizon stress protocol, a
256-row/32-cell certificate, a reverse-shell independent replay, and an
explicit separation between anchored transfer, local recalibration, and
recursive composition.  It also records the spectral-cap obstruction at the
larger endpoint.

## Locked hypotheses

* H1: the frozen TPC-388 slope remains within a 3% endpoint ratio cap.
* H2: a current-family 768-to-1024 slope is a useful local control.
* H3: recursively applying the frozen slope from 768 to 1280 remains within
  the same cap.
* H4: the inherited spectral diagnostic is not thereby repaired.

H1--H3 are tested only on the finite panel.  H4 is a diagnostic census, not an
operator theorem.

## Results to report

Report all 32 cells, the three pass counts, the three maximum absolute errors,
the stability census, and the spectral/Schur failure census.  Do not pool the
finite observations into an asymptotic claim or assign arithmetic power credit.

## Follow-up decision rule

If recursive composition remains inside the cap, test a second recursive
composition or a new independent family.  If it crosses the cap, freeze the
failure as a horizon-dependent obstruction and test whether the failure is
law-, normalization-, or band-specific.  In either branch the source-valid
growing theorem remains open.
