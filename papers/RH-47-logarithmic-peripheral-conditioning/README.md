# RH-47: Logarithmic peripheral conditioning

This paper resolves the first part of the small-noise peripheral-contour gate
left by RH-46.

The initial hope was that fixed-geometry Perron and parity contours might
have uniformly bounded L2 resolvents as sigma tends to zero. The endpoint
square-root spikes rule this out: the residues themselves become
logarithmically ill-conditioned.

## Mesoscopic endpoint theorem

Let pi_sigma be the stationary density and g_sigma the signed left density
of the negative-parity branch. If

\[
t\to0,\qquad \sigma/t\to0,
\]

then

\[
\sqrt t\,\pi_\sigma(1-t),
\quad
-\sqrt t\,g_\sigma(1-t)
\longrightarrow
c_R,
\]

where

\[
c_R=\frac{\rho_c}{2\sqrt{u_c}}
=0.22642358926050635\ldots.
\]

Combining this overlap law with the finite postcritical spike majorants gives

\[
\|\pi_\sigma\|_2,\ \|g_\sigma\|_2
=\Theta\!\left(\sqrt{\log(1/\sigma)}\right).
\]

Consequently the Perron and parity Riesz projections have the same
Hilbert--Schmidt growth.

## Resolvent obstruction

For a fixed-radius isolating circle,

\[
\sup_{z\in\Gamma}\|(z-K_\sigma)^{-1}\|
\ge \frac{\|P_\sigma\|}{\operatorname{radius}(\Gamma)}.
\]

Therefore

\[
\sup_{z\in\Gamma}\|(z-K_\sigma)^{-1}\|
=\Omega\!\left(\sqrt{\log(1/\sigma)}\right).
\]

A uniform O(1) L2 contour-resolvent theorem is impossible. This is a lower
bound forced by the Riesz residue; it does not determine a matching upper
for the reduced resolvent and does not identify a polynomial pseudospectral
exponent.

The peripheral term has regular-variation index zero: it is
O(sigma^(-epsilon)) for every epsilon greater than zero, but it is not O(1).

## Continuum-anchored bypass

Direct differentiation of the already identified rank-two kernel gives

\[
\|\partial_x q_{\mathrm{per},\sigma}\|_2
=O\!\left(\sigma^{-1}\sqrt{\log(1/\sigma)}\right),
\]

\[
\|\partial_y q_{\mathrm{per},\sigma}\|_2
=O(\sigma^{-3/2}).
\]

For orthogonal cell averaging E_n,

\[
\|E_nQ_{\mathrm{per},\sigma}E_n-Q_{\mathrm{per},\sigma}\|_{S_2}
=O(n^{-1}\sigma^{-3/2}).
\]

Define the continuum-anchored bulk

\[
\widetilde B_{n,\sigma}
=E_nK_\sigma E_n-E_nQ_{\mathrm{per},\sigma}E_n
=E_nB_\sigma E_n.
\]

Then

\[
\|\widetilde B_{n,\sigma}^2-B_\sigma^2\|_1
=O(n^{-1}\sigma^{-2})+O(n^{-2}\sigma^{-3}).
\]

Thus

\[
n(\sigma)\sigma^2\to\infty
\]

still suffices. In power notation, every p greater than 2 works for
n(sigma) asymptotic to sigma^(-p).

## Exact remaining gate

The actual finite matrix uses its own intrinsic weighted Riesz term. The
remaining defect is

\[
\mathcal I_{n,\sigma}
=Q_{\mathrm{per}}(E_nK_\sigma E_n)
-E_nQ_{\mathrm{per}}(K_\sigma)E_n.
\]

RH-47 proves the spatial compression term but does not prove

\[
\|\mathcal I_{n,\sigma}\|_{S_2}
=O(n^{-1}\sigma^{-3/2}).
\]

This is now the precise next spectral problem. A reduced-resolvent or
one-sided Feshbach/Grushin argument should be more efficient than paying for
two complete L2 resolvents.

## Floating sparse audit

The row-normalized eight-sigma sparse family was diagonalized at nine noise
levels with n sigma approximately 20.48, reaching:

| quantity at sigma = 1e-4 | value |
|---|---:|
| dimension | 204800 |
| Perron projector norm | 1.4009681515362922 |
| parity projector norm | 1.3558346334547398 |
| rank-two weighted Frobenius norm | 1.9575799632322384 |
| Perron contour-resolvent lower | 28.01936303072584 |
| parity contour-resolvent lower | 27.116692669094792 |
| stationary endpoint coefficient | 0.24178227476953104 |
| parity endpoint coefficient | 0.2454905228634945 |

The endpoint coefficients drift toward the analytic value
0.22642358926050635. These eigensolver values and fitted slopes are floating
diagnostics, not validated enclosures.

## Theorem boundary

- The fixed-contour result is a resolvent lower bound, not a reduced-resolvent
  upper.
- The anchored bulk uses the compressed continuum Riesz kernel, not the
  finite matrix's actual Riesz term.
- The intrinsic identification defect remains open.
- Normalized power ledgers set unknown theorem constants to one and display
  exponents only.
- Sparse eigenfactors are binary64 diagnostics.
- No arithmetic trace formula, prime-power identity, zeta-zero
  identification, self-adjoint Hilbert--Polya operator, T log T counting
  law, or Riemann-hypothesis conclusion is made.

## Complete replay

From this directory:

~~~bash
OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
  PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_peripheral_factor_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_conditioning_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf logarithmic-peripheral-conditioning.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~

The full sparse factor pilot takes about one minute on the reference server;
all remaining steps take seconds.

## Layout

- main.tex and references.bib: manuscript sources.
- logarithmic-peripheral-conditioning.pdf: publication PDF.
- src/peripheral_conditioning/: logarithmic clocks, anchored ledgers, and
  low-rank utilities.
- experiments/run_peripheral_factor_pilot.py: nine-level sparse
  Perron/parity factor audit.
- experiments/build_conditioning_certificate.py: theorem and exponent
  certificate.
- experiments/make_figures.py: publication figure.
- experiments/build_archive.py and experiments/verify_archive.py: hashed
  archive construction and theorem-gate verification.
- tests/: low-rank identities, exponent checks, and archived result gates.
- results/: factor pilot, theorem certificate, summary, dependency manifest,
  and archive verification.
