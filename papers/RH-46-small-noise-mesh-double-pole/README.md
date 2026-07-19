# RH-46: Small-noise mesh laws and the double-pole obstruction

This paper separates the two obstructions that appear when the intrinsic
two-step Fredholm determinant is pushed from fixed positive noise toward the
small-noise regime:

1. a narrowing Gaussian kernel must be resolved in an absolute trace ideal;
2. the deterministic parity-centered determinant germ has a genuine pole
   that no spatial mesh can remove.

The first part is unconditional for the folded Gaussian Markov kernel and its
orthogonal cell-average Galerkin lift. The extension to the full
Perron/parity-deflated bulk is stated under an explicit uniform peripheral
transport condition rather than silently assumed.

## Rigorous mesh laws

For `0 < sigma <= 0.03`, the normalized folded Gaussian kernel satisfies

\[
Z_\sigma(x)\ge c_0\sigma,
\qquad c_0=1.2533141373155,
\]

and

\[
\|K_\sigma\|_{S_2}\le A_0\sigma^{-1/2},
\qquad A_0=2.124503864054395,
\]

\[
\|(k_\sigma)_x\|_2+\|(k_\sigma)_y\|_2
\le A_1\sigma^{-3/2},
\qquad A_1=11.373709849581182.
\]

If `G_(n,sigma)` is the orthogonal cell-average lift, then

\[
\|G_{n,\sigma}-K_\sigma\|_{S_2}
\le \frac{3.620364287707642}{n\sigma^{3/2}},
\]

and the Hilbert--Schmidt product rule gives

\[
\|G_{n,\sigma}^2-K_\sigma^2\|_1
\le
\frac{15.38295583703884}{n\sigma^2}
+\frac{13.10703757570889}{n^2\sigma^3}.
\]

Consequently:

- `n(sigma) sigma^(3/2) -> infinity` is sufficient for one-step
  Hilbert--Schmidt convergence;
- `n(sigma) sigma^2 -> infinity` is sufficient for two-step trace-norm
  convergence;
- on shrinking disks `|w| <= rho sigma`, the standard determinant continuity
  estimate only requires `n(sigma) sigma -> infinity`;
- on a fixed disk, that same sufficient estimate develops an exponential
  `exp(C_R/sigma)` wall.

The normalized Gaussian-row model proves that the cell-projection exponent is
sharp. Its exact leading constant is

\[
C_G=\frac{1}{\sqrt{48}\,\pi^{1/4}}
=0.1084156338230097.
\]

The floating closed-CDF pilot reaches relative error
`9.48819920299574e-08` against this constant.

## The double-pole obstruction

The exact deterministic one-step bulk germ supplied by RH-15 is

\[
\widehat D_{0,\mathrm{bulk},2}(z)
=\frac{G(z)}{1-z^2/\lambda},
\qquad
\lambda=1.678573510428322\ldots,
\]

with a nonvanishing holomorphic numerator in the required disk. Symmetric
two-step completion therefore gives

\[
\widehat F_0(w)
=\frac{H(w)}{(1-w/\lambda)^2}.
\]

Thus `w = lambda` is a genuine double pole. Although every positive-noise
two-step determinant is entire and its Taylor coefficients have the stated
small-noise bridge, the family is not locally bounded on disks crossing this
point and cannot converge locally uniformly to an unrenormalized entire
small-noise determinant.

This is a theorem about the deterministic cycle germ and the positive-noise
determinant family. It is not the assertion that a separate `sigma = 0`
operator determinant has already been constructed.

## Conditional bulk route

Suppose the peripheral weighted-Riesz contribution obeys

\[
\|Q_{\mathrm{per},\sigma}\|_{S_2}=O(\sigma^{-q}),
\qquad
\|Q_{\mathrm{per},n,\sigma}-Q_{\mathrm{per},\sigma}\|_{S_2}
=O(n^{-1}\sigma^{-r}).
\]

Then a sufficient bulk-square mesh exponent is

\[
p=\max(1/2,q)+\max(3/2,r).
\]

For moving contours with `O(sigma^(-beta))` continuum and discrete resolvent
bounds, the direct resolvent-identity route gives

\[
q=\beta,
\qquad
r=\frac32+2\beta.
\]

Proving such a uniform moving-contour theorem is the next positive gate. RH-45
only closes the corresponding transport problem at the single fixed width
`sigma = 1e-2`.

## Canonical pole resolution and floating cloud audit

The exact finite section resolving the double pole is

\[
S_N(w)=\Pi_N(w/\lambda)^2,
\qquad
\Pi_N(q)=1+q+\cdots+q^N,
\]

with edge law

\[
\frac{S_N(\lambda e^{s/(N+1)})}{(N+1)^2}
\longrightarrow
\left(\frac{e^s-1}{s}\right)^2.
\]

The RH-15 archived clouds were reprocessed in the two-step variable. At
`sigma = 1e-4`, the selected one-step cloud has 14 points (`N = 7`) and the
mean observed-to-finite-section error on `s = -2,-1,-1/2,0,1/2,1,2` is
`0.12741416470835046`. On `|s| <= 1`, the mean is
`0.0363294353592265` and the maximum is `0.11589964727270274`.

These cloud values are floating diagnostics only. They do not prove residual
normality or identify the actual noisy cloud with the canonical geometric
section.

## Theorem boundary

- The unconditional mesh theorem concerns the folded Gaussian Markov kernel
  and the canonical cell-average lift.
- Uniform small-noise weighted-Riesz transport is an open condition.
- The fixed-disk determinant estimate is deliberately coarse and is not a
  necessary complexity law.
- The archived resonance-cloud comparison is binary64 evidence, not a
  validated convergence theorem.
- No arithmetic trace formula, prime-power identity, zeta-zero
  identification, self-adjoint Hilbert--Polya operator, `T log T` counting
  law, or Riemann-hypothesis conclusion is made.

## Complete replay

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_small_noise_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_gaussian_row_resolution_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_square_cloud_pilot.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf small-noise-mesh-double-pole.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The complete replay takes seconds on the reference server; it reuses the
archived RH-15 cloud CSV rather than recomputing large eigensystems.

## Layout

- `main.tex`, `references.bib`: manuscript sources.
- `small-noise-mesh-double-pole.pdf`: publication PDF.
- `src/small_noise_two_step/`: Gaussian bounds and exact geometric models.
- `experiments/build_small_noise_certificate.py`: analytic certificate and
  mesh-power audit.
- `experiments/run_gaussian_row_resolution_pilot.py`: sharp row-constant
  pilot.
- `experiments/build_square_cloud_pilot.py`: RH-15 cloud reprocessing.
- `experiments/make_figures.py`: publication figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: hashed
  archive construction and theorem-gate verification.
- `tests/`: analytic identities and archived theorem-boundary tests.
- `results/`: rigorous certificate, floating pilots, dependency manifest,
  summary, and archive verification.
