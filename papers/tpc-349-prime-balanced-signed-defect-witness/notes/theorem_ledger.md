# TPC-349 theorem ledger

| Item | Status | Scope / evidence |
|---|---|---|
| Zero-sum prime split | `PROVED_EXACT_FINITE` | explicit coefficient definition |
| Incidence vector identity | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite shell incidence |
| Prime-incidence Gram expansion | `PROVED_EXACT_FINITE_DECLARED_MODEL` | bilinearity |
| Normalized signed lower witness | `PROVED_EXACT_FINITE_LINEAR_ALGEBRA` | induced Euclidean norm |
| Nonzero witness census | `NUMERICALLY_CERTIFIED_FINITE_192_OF_192` | producer + reverse replay |
| Positive response census | `NUMERICALLY_CERTIFIED_FINITE_192_OF_192` | finite panel |
| Coordinate baseline beaten | `NUMERICALLY_CERTIFIED_FINITE_136_OF_192` | finite comparison |
| Half-defect response census | `NUMERICALLY_CERTIFIED_FINITE_175_OF_192` | finite comparison |
| Universal balanced gain | `REFUTED_SCOPED` | 56 rows do not beat baseline |
| Exact multi-hit anchor | `PROVED_EXACT_FINITE` | interval `[1,14]`, shell `{5,7}` |
| Source-uniform arithmetic `L2` | `OPEN` | no growing estimate |
| Uniform masked operator bound | `OPEN` | no source-uniform control |
| Fixed-power credit | `0` | no asymptotic payment |
| Route-B Gate B | `OPEN` | reassembly and endpoint absent |
| Twin-prime conclusion | `NONE` | no implication asserted |

## Strongest positive

A zero-sum prime-incidence contrast is a deterministic unit test vector with an
exact cross-prime Gram expansion; it is stronger than the best coordinate
baseline on 136 of the 192 declared rows.

## Strongest obstruction

The finite signed response is not uniformly superior to the coordinate witness:
its response/coordinate ratio falls to `0.542800508699`, so no universal balanced
gain follows even on the locked panel.

## Open theorem

Determine whether a source-uniform estimate controls the signed incidence Gram
on growing panels, while retaining all masks and separating cross-prime terms.

## Reusable structure

```text
ordered shell -> zero-sum beta -> incidence contrast -> prime Gram
              -> normalized induced-norm witness -> finite baseline audit
```

## ROUND2_CLUE

`REPLICATE_SIGNED_INCIDENCE_GRAM_ON_GROWING_FRESH_PANELS`
