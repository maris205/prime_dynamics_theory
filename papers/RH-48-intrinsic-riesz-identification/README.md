# RH-48: Intrinsic Riesz identification

This paper resolves the algebraic part of the intrinsic finite-matrix
peripheral-identification defect left by RH-47.

For

\[
\mathcal I_{n,\sigma}
=Q_{\rm per}(E_nK_\sigma E_n)-E_nQ_{\rm per}(K_\sigma)E_n,
\]

the exact block Schur formula is quadratic in the two coarse-detail
couplings. If

\[
K=\begin{pmatrix}A&B\\C&D\end{pmatrix},\qquad
\Sigma(z)=B(z-D)^{-1}C,
\]

then, on either peripheral contour,

\[
E_nQ_\Gamma(K)E_n-Q_\Gamma(A)
=\frac1{2\pi i}\int_\Gamma
z(z-A-\Sigma(z))^{-1}B(z-D)^{-1}C(z-A)^{-1}\,dz.
\]

The Hilbert--Schmidt bound uses only the directional actions

\[
(z-A-\Sigma(z))^{-1}B,
\qquad C(z-A)^{-1},
\]

not two global L2 resolvent norms.

## Dyadic closure theorem

For nested cell spaces, define the adjacent defect

\[
\Delta_{n,\sigma}
=Q_{\rm per}(A_{n,\sigma})
-E_nQ_{\rm per}(A_{2n,\sigma})E_n.
\]

Then

\[
\mathcal I_{n,\sigma}
=\sum_{j\ge0}E_n\Delta_{2^jn,\sigma}E_n.
\]

A quadratic dyadic ledger therefore costs only the geometric factor `4/3`.
The Gaussian derivative bounds give the generic self-energy clock

\[
\|B_n\|_{S_2},\|C_n\|_{S_2}
=O(n^{-1}\sigma^{-3/2}),
\qquad
\|D_n\|=O(n^{-2}\sigma^{-5/2}).
\]

If the product of the normalized directional gains is
`O(sigma^(-gamma))`, then

\[
\|\mathcal I_{n,\sigma}\|_{S_2}
=O(n^{-2}\sigma^{-3-\gamma}).
\]

Hence every schedule `n sigma^2 -> infinity` remains sufficient when
`gamma <= 1/2`. A polylogarithmic directional loss is more than sufficient.

## Exact-Haar floating audit

The numerical experiment builds one finest sparse row-stochastic matrix and
obtains every coarser matrix by exact orthogonal Haar compression. It audits
18 adjacent defects at six noise levels.

| quantity | result |
|---|---:|
| largest dimension | 204800 |
| largest nonzero count | 133873007 |
| fitted dimension power | -1.9952369867 |
| fitted sigma power | -1.9719711832 |
| maximum joint log residual | 0.0157905622 |
| maximum double-resolution replay difference | 0.0001567544 |

The data are consistent with the sharper candidate law

\[
\|\Delta_{n,\sigma}\|_{S_2}\asymp C(n\sigma)^{-2}.
\]

That law is a binary64 finite-matrix observation, not a proved analytic
bound.

## Exact remaining gate

RH-48 does **not** prove a uniform small-noise upper for the reduced
directional resolvents. The next sufficient target is either

\[
\sup_{j\ge0}\mathcal L_{2^jn,\sigma}
=O((\log(1/\sigma))^m)
\]

for a fixed `m`, or at least `O(sigma^(-1/2))`. The global L2 residue lower
bound from RH-47 neither proves nor rules out this directional estimate.

No arithmetic trace formula, prime-power identity, zeta-zero
identification, self-adjoint Hilbert--Polya operator, `T log T` counting law,
or Riemann-hypothesis conclusion is claimed.

## Complete replay

From this directory:

```bash
OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
  PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_dyadic_identification_pilot.py

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
  PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_dyadic_identification_pilot.py \
  --smoke --fine-resolution 81.92

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_identification_certificate.py

MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/make_figures.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  -m pytest -q -p no:cacheprovider

latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf quadratic-schur-intrinsic-riesz-identification.pdf

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The full sparse audit takes roughly two minutes on the reference server; the
remaining steps take seconds.

## Layout

- `main.tex`, `references.bib`: manuscript sources.
- `src/intrinsic_identification/`: Schur, dyadic, power-law, and low-rank
  utilities.
- `experiments/run_dyadic_identification_pilot.py`: exact-Haar sparse audit.
- `experiments/build_identification_certificate.py`: theorem and regression
  certificate.
- `experiments/make_figures.py`: publication figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: hashed
  archive and theorem-boundary verification.
- `tests/`: exact Schur identity, low-rank algebra, power thresholds, and
  archived result gates.
- `results/`: pilots, theorem certificate, summary, dependency manifest, and
  archive verification.
