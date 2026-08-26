# TPC-268 proof and certificate package

## Main finite proposition

For the 16 listed rows in results/tpc268_certificate.json, the exact finite
operator and rank-three projection are assembled without deleting the
orthogonal residual. Six z=2 controls and four additional z=3/clock
controls have rho^2<1/16; six rows have rho^2>1/16 with an outward
interval lower endpoint. In particular the matched central pair changes
classification when only z changes from 2 to 3.

## Proof status

- PROVED_EXACT_FINITE: source beta arithmetic, masks, prime shell, deleted
  diagonal, operator summation, and projection identity.
- NUMERICALLY_CERTIFIED: logarithm/Euler-product enclosures and the strict
  threshold separation in all 16 rows.
- REFUTED_SCOPED: a universal quarter bound over this declared finite
  parameter family.
- OPEN: growing V59 cutoff/profile uniformity, actual residual radius and
  phase, arithmetic L2, and full Gate B.

The independent checker reimplements the finite replay with double precision
and verifies all six obstruction rows remain above 1/4 and all ten
contraction rows remain below it. The interval producer remains the
claim-bearing certificate; the float replay is a separate audit, not a
replacement for the interval enclosure.

## Reproducibility

The producer is deterministic and emits canonical JSON. Normal and optimized
Python runs must have byte-identical output. The independent checker contains
no import of the producer and includes mutation rejection. The adversarial
stress script checks the matched cutoff flip, clock neighborhood, kernel
control, and threshold semantics.

## Limitation

The obstruction is finite and model-relative. It is not a counterexample to
the literal growing V59 theorem, because the latter has a source-specified
cutoff and profile that are not proved equivalent to every finite row here.
