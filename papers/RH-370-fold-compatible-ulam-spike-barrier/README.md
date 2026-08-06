# RH-370: Fold-compatible Ulam quotients and the deterministic spike barrier

RH-370 audits the first continuation candidate left by RH-367.  The frozen
postcritically finite map is

```text
f(x) = 1 - u x^2,       J = [-(u-1), 1],
u^3 - 2u^2 + 2u - 2 = 0,
```

and the fold is `q(x)=|x|`, with `T q = q f` and
`T(y)=|1-u y^2|` on `[0,1]`.

The paper proves three separate statements.

1. For a partition whose cells are exactly mirror-compatible under `q`, the
   full exact cell-overlap matrix has a quotient equal to the folded matrix.
   The mirror-antisymmetric kernel is annihilated by the density transfer, so
   `chi_full(z)=z^m chi_fold(z)`.  All nonzero finite eigenvalues, including
   their Jordan multiplicities, are inherited by the quotient; the extra zero
   structure is not classified.
2. Conditional expectations give a genuine `L^1` bridge
   `E_h P_T E_h g -> P_T g` for every fixed `g`, and resolvents converge
   uniformly on compact subsets of `|z|>1`.  This is an exterior weak bridge,
   not a contour around the unit-circle eigenvalue `-1`.
3. On the natural BV strong space, the deterministic cell projection is not
   uniformly bounded.  For the terminal cells of width `h`,
   `P_T 1 = (2 sqrt(u))^(-1) (1-y)^(-1/2)` on `(u-1,1)`, and the adjacent
   cell-average jump is
   `(2-sqrt(2))/sqrt(u h)`.  Thus the BV variation grows like `h^(-1/2)`.

Consequently the positive RH-367 claim of a common deterministic strong-space
Riesz contour remains `STOP_SCOPED`.  The exact folding theorem and the
`L^1`/spike obstruction are a standalone Route-A theorem edge.  Arbitrary
band-aligned but non-mirror partitions, phase-shifted grids, noisy matrices,
and any universal noise exponent remain outside scope.

No finite spectrum is promoted to a continuum spectral limit.  No canonical
operator, von-Mangoldt trace, Riemann-zero identification, Hilbert--Polya
construction, or RH implication is claimed.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The executable checks use exact rational matrices for the quotient identities
and interval arithmetic for the displayed spike coefficient.  They are
finite algebra and reproduction checks only.
