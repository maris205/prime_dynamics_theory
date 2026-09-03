# TPC-363 route evaluation and proof package

## Object

The object is the TPC-362 normalized finite prime-shell matrix
`A# = D_G^(-1/2) A D_G^(-1/2)` on the frozen high-origin panel.  The new
operation is a declared principal restriction: delete `floor(N/20)` indices
chosen by a stated score, then recompute the finite spectrum.

## Established facts

* `PROVED_EXACT_FINITE`: the Schur and Frobenius inequalities used as finite
  envelopes are standard exact inequalities for the declared matrices.
* `NUMERICALLY_CERTIFIED_FINITE_144_ROWS`: all four laws are replayed at all
  144 declared settings.  The inherited spectral cap has no failure at
  `Q=80`, six failures at `Q=128`, and twelve at `Q=256`.
* `NUMERICALLY_CERTIFIED_FINITE_SCOPED`: every one of the 18 failing rows
  remains above `0.64` after both five-percent restrictions.  The smallest
  retained restricted spectral value is `0.86120283374232454`; the smallest
  value among the six `Q=128` failures is `1.1843597700033823`.
* `NUMERICALLY_CERTIFIED_FINITE_SCOPED`: all 18 failures are all-plus rows;
  the other three fixed laws contribute zero failures in this panel.
* `NUMERICALLY_CERTIFIED_FINITE_SCOPED`: the largest principal-eigenvector
  coordinate mass among failing rows is `0.0065671250441509798`, and the
  minimum effective-support fraction is `0.55114876369112986`.

## Interpretation and obstruction

The declared high-Q cap failure is not removed by deleting five percent of
the rows selected by either of two natural leverage scores.  This rejects the
specific single-row/single-coordinate explanation on the declared finite
trims.  It does not prove a universal bulk theorem, nor does it rule out a
different normalization, shell weighting, or an asymptotic cancellation.

## Claim firewall

```text
TPC363_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC363_FINITE_ENVELOPE_INEQUALITIES = PROVED_EXACT_FINITE
TPC363_FIRST_Q128_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_BULK_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_SINGLE_ROW_SPIKE_EXPLANATION = REFUTED_SCOPED_ON_DECLARED_TRIMS
TPC363_EIGENVECTOR_DELOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_RENORMALIZED_REPAIR = OPEN
TPC363_GROWING_OPERATOR_BOUND = OPEN
TPC363_SOURCE_UNIFORM_L2 = OPEN
TPC363_ARITHMETIC_ADVANCE = NO
TPC363_FIXED_POWER_CREDIT = 0
TPC363_FULL_GATE_B = OPEN
TPC363_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are not present in
this checkout.  Therefore no official evaluator pass is claimed; the local
Bridge-B checker is only a fail-closed reproducibility control.  The proof
package certifies finite definitions, replay, and mutation rejection, not an
arithmetic reassembly.

## Reusable structure and next clue

```text
frozen high-Q failure
  -> deterministic leverage scores
  -> five-percent principal restrictions
  -> all-failure persistence census
  -> eigenvector mass audit
  -> scoped bulk obstruction
```

`ROUND2_CLUE = TEST_RENORMALIZED_HIGH_Q_REPAIR_ON_EXPLICIT_HOLDOUT`.
