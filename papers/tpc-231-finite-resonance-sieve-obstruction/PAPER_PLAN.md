# TPC-231 paper plan

## Question

Does the first primitive `3--7` resonance matching occupy a positive proportion of the
prime shell, as required by the TPC-230 fixed-saving toll?

## Exact target

1. Parameterize `7p+3r=16Q` by two affine linear forms.
2. Compute every local root count and the determinant-dependent singular series.
3. Apply the classical dimension-two Selberg upper-bound sieve uniformly in `Q`.
4. Transfer edge sparsity through the TPC-230 matched-mass ceiling.
5. Generalize the density obstruction to any fixed finite primitive linear resonance
   family without promoting the conclusion to the actual V59 source object.

## Success criterion

Prove `E_3716(Q)/P(Q)->0`, hence `M_literal/D_literal->0`, and issue a precise
`STOP_SCOPED` for fixed finite resonance layers with comparable row masses.

## Invalidation conditions

- a local root count is wrong at `2`, `3`, `7`, or a divisor of `Q`;
- the two forms have determinant other than `16Q`;
- a finite scan is used as asymptotic evidence;
- the standard sieve theorem is applied without its interval remainder or admissibility
  hypotheses;
- the literal aligned row model is silently identified with the actual V59 source;
- an obstruction is promoted to arithmetic cancellation or full Gate B.
