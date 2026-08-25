# TPC-256 route evaluation

## Evaluator outcome

```text
maximum_status = PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC
route_advance = YES_LITERAL_ARITHMETIC
arithmetic_advance = YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE
fixed_atom_credit = 0
L2 = NONE
full_gate_B = OPEN
strict_1_over_400 = UNPAID_GLOBAL
twin_prime_result = NONE
```

The result is a genuine arithmetic advance over TPC-255 because it evaluates
the literal beta midpoint and all three correction lanes, rather than merely
rearranging them.  Its scope remains one coefficient-independent ordered-rank
Haar projection.

## Strongest positive result

```text
<z_mid,beta> has an explicit positive asymptotic, and the returned B_Q
diagonal forces a nonzero negative-real leading asymptotic for
<z_mid,A_x beta> with normalized phase tending to -1.
```

## Strongest obstruction

```text
The Poisson zero does not make the literal adjoint Haar lane small: deleting
the diagonal returns the asymptotically dominant B_Q term.  The output-unit
pieces remain noncentered separately and cannot be Poisson-split.
```

## Open theorem

Control the transverse/full-output component of `A_x beta` and couple it to
the physical `w` lane on the same V59 clock while retaining the prime shell,
both unit masks, deleted diagonal, hard window, and rank-child geometry.  One
Haar projection does not imply full Gate B or the strict global `1/400`
payment.

## Reusable structure

```text
consecutive-interval divisor-density cancellation
 -> second-order PNT curvature
 -> explicit literal beta Haar main term
 -> B_Q diagonal amplification
 -> combined-unit-mask Schwartz first moment
 -> one-boundary crossing count
 -> fixed-power boundary separation
 -> branch-safe complex phase.
```

## ROUND2_CLUE

```text
EXPLOIT_EXACT_DIVISOR_DENSITY_CANCELLATION_BEFORE_ANY_TRIANGLE__THEN_USE_THE_BQ_DIAGONAL_MAIN_AND_H2_OVER_Q_BOUNDARY_MOMENT_TO_ISOLATE_THE_TRANSVERSE_FULL_GATE_B_REMAINDER
```

## Recommended next action

The natural next paper should attack the orthogonal/transverse remainder on
the same literal system family.  It should reuse the exact diagonal/boundary
normal form and the combined-mask first moment, but must not infer a
full-output theorem merely from the present one-dimensional projection.
