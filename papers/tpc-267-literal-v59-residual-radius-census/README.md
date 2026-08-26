# TPC-267 — Finite Literal V59 Residual-Radius and Signed-Phase Census

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS
```

TPC-266 left the literal V59 residual radius and phase open after the exact
Schur/radial firewall.  TPC-267 takes the next smallest testable step: it
instantiates the finite operator with the actual prime shell, both unit masks,
the deleted diagonal, the source β coefficient, and the shifted-prime
comparison (w=\Lambda(\cdot+2)-b^{(2)}).  It then projects the resulting
vectors onto the three consecutive-block Haar contrasts used upstream.

For twelve natural finite clock rows, with (s=1,2) in

\[
 K_{H,s}(h)=\bigl(1+(h/H)^2\bigr)^{-s},
\]

the rational interval certificate proves

\[
 0<\rho=\frac{|C_\perp|}
 {\|(I-P_3)w\|\,\|(I-P_3)A\beta\|}<\frac14.
\]

The largest stored upper bound is `0.2320126753`; ten residuals are negative
real and two positive real for this real even kernel family.  This is a finite
signed-phase observation and a useful physical replay, not an asymptotic
sector theorem.

## What is actually certified

- `PROVED_EXACT_FINITE`: the matrix (A), source β values, masks, shell, and
  rank-three projection identity;
- `NUMERICALLY_CERTIFIED`: the Euler-product/logarithm enclosures and all
  twelve quarter-contractions;
- `OPEN_ASYMPTOTIC`: the growing-(x) residual radius and phase, including
  the strict fixed-power saving required by the endpoint budget.

The (H,Q) values are explicit rounded finite representatives of the V59
clock, and the two rational Fourier profiles are modeling choices.  No
exponent is inferred from the table, and the residual is retained throughout.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-267-literal-v59-residual-radius-census/code/tpc267_literal_residual_radius_certificate.py --check
python -O -B papers/tpc-267-literal-v59-residual-radius-census/code/tpc267_literal_residual_radius_certificate.py --check
python -B papers/tpc-267-literal-v59-residual-radius-census/experiments/tpc267_independent_checker.py --check
python -O -B papers/tpc-267-literal-v59-residual-radius-census/experiments/tpc267_independent_checker.py --check
python -B papers/tpc-267-literal-v59-residual-radius-census/experiments/tpc267_kernel_stress.py --check
python -O -B papers/tpc-267-literal-v59-residual-radius-census/experiments/tpc267_kernel_stress.py --check
```

The next natural project is adversarial: vary the finite clock, local cutoff,
and a genuinely smooth profile to determine whether the observed phase
contraction is stable or merely a finite-profile effect.
