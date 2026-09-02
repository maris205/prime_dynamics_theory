# TPC-351 paper plan

## Research question

Can a single, predeclared shell-scale rule repair the high-shell loss of the
fixed balanced incidence witness without fitting coefficients to each row?

## Minimal continuation

TPC-350 found that the balanced step rule has a `0.0657381187306` finite floor
and no half-defect row at `Q=256`.  TPC-351 keeps the identical literal matrix
and the identical fresh panel, but replaces the fitted-looking rank split by
the fixed rational rule

```text
gamma_j = 1/p_j - (1/r) sum_k 1/p_k.
```

The rule depends only on the ordered shell primes, has exact zero sum, and is
chosen before seeing an origin, length, source law, matrix, or response.

## Primary outputs

1. Prove exact coefficient balance, the reciprocal incidence identity, its Gram
   expansion, and the induced-norm lower witness.
2. Recompute all 192 rows and compare each reciprocal response with the locked
   TPC-350 balanced-step response on the same key.
3. Audit scale breakdown, four-length series, coordinate baseline, and exact
   rational multi-hit anchor.
4. Use reverse-shell replay and mutation stress to distinguish a real finite
   repair from a reporting or parent-alignment error.

## Decision rule

If the reciprocal rule improves the parent on most rows, record a finite
scale-repair result.  If a low row or a nonmonotone series remains, retain the
obstruction and do not promote the improvement to a uniform theorem.  In either
case, do not infer a source-uniform arithmetic `L2` theorem, a fixed power of
`x`, or a twin-prime result.

## Planned next question

Use the result to decide whether an adversarial holdout for the reciprocal rule
is worthwhile.  If it fails, freeze this incidence branch and return to the
source-native arithmetic `L2` gate.
