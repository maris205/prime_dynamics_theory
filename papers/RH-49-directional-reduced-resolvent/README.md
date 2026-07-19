# RH-49: residue-deflated directional resolvents

This directory contains the forty-ninth-layer paper in the quadratic
small-noise spectral program:

> *Residue-Deflated Directional Resolvents at a Quadratic Critical Fold: A
> Quarter-Power Stable-Rank Bridge for Intrinsic Riesz Identification*

## Main result

RH-48 left a mixed directional gain

\[
\mathcal L_{n,\sigma}
=\sum_s\min\{\ell_{B,s}^{(2)}\ell_{C,s}^{(\infty)},
\ell_{B,s}^{(\infty)}\ell_{C,s}^{(2)}\}.
\]

RH-49 proves the exact stable-rank reduction

\[
\mathcal L_{n,\sigma}
\le
\mathcal F_{n,\sigma}
\min\left\{
\frac{\|B\|_{S_2}}{\|B\|},
\frac{\|C\|_{S_2}}{\|C\|}
\right\},
\qquad
\mathcal F_{n,\sigma}
=\sum_s\ell_{B,s}^{(2)}\ell_{C,s}^{(2)}.
\]

For the canonical cell-average folded-Gaussian family, an endpoint Haar
packet gives

\[
\|B\|_{S_2}=O(h\sigma^{-3/2}),
\qquad
\|B\|\ge c h\sigma^{-5/4},
\]

and hence

\[
\frac{\|B\|_{S_2}}{\|B\|}=O(\sigma^{-1/4}).
\]

Therefore, if the purely Hilbert--Schmidt directional product is
`O(sigma**(-delta))`, then the RH-48 mixed exponent is

```text
gamma = 1/4 + delta.
```

Every strict `n*sigma**2 -> infinity` schedule remains sufficient when
`delta <= 1/4`. Uniform or polylogarithmic Hilbert--Schmidt gains are more
than sufficient.

The paper also proves the exact rank-one deflation identity

\[
R^\circ(z)
=(z-T)^{-1}-\frac{P}{z-\lambda}
=(z-T+\lambda P)^{-1}(I-P)
\]

and gives primal/adjoint residual uppers for finite-matrix certification.

## Five-scale audit

The full audit uses exact Haar nesting with finest `N*sigma = 20.48`, eight
nodes on each Perron/parity contour, exact rank-one branch deflation, and
GMRES tolerance `2e-10`.

| sigma | dimension | B sqrt stable rank | full HS sum | transferred candidate | direct mixed sum |
|---:|---:|---:|---:|---:|---:|
| 0.01 | 2048 | 2.9203 | 4.4076 | 12.8714 | 4.5434 |
| 0.004 | 5120 | 3.6474 | 4.6473 | 16.9507 | 6.0494 |
| 0.002 | 10240 | 4.3227 | 4.2154 | 18.2220 | 6.9431 |
| 0.001 | 20480 | 5.1280 | 4.1833 | 21.4524 | 7.6162 |
| 0.0005 | 40960 | 6.0878 | 3.9630 | 24.1260 | 8.1287 |

Fitted growth exponents:

```text
||B||_S2                         0.4952635
||B|| operator candidate        0.2500047
B sqrt stable rank candidate    0.2452588
full Hilbert--Schmidt gain sum  0.0000000
transferred full candidate      0.2037100
direct mixed branch sum         0.1916177
```

The last-three-level direct mixed exponent is `0.11373`. Maximum GMRES
iterations are 41, relative residuals remain below `2e-10`, and deflated
branch leakage remains below `3e-13`.

## Exact theorem boundary

RH-49 does **not** prove:

- a uniform small-noise upper for the Hilbert--Schmidt directional gains;
- transfer of the endpoint lower theorem to the hard eight-sigma sparse
  cutoff with interval validation;
- that power-iteration or Hutchinson candidates are certified norm uppers;
- an arithmetic trace formula, prime-power identity, zeta-zero
  identification, self-adjoint Hilbert--Polya operator, `T log T` counting
  law, or the Riemann hypothesis.

The next analytic target is now the Hilbert--Schmidt gate

\[
\sup_{j\ge0}\mathcal F_{2^j n,\sigma}
=O((\log(1/\sigma))^m)
\]

or, more generally, `O(sigma**(-delta))` with `delta <= 1/4`, followed by a
validated hard-cutoff transfer.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_coupling_stable_rank_pilot.py

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_reduced_directional_pilot.py

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_mixed_operator_gain_pilot.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_directional_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The complete mixed audit is the expensive step; the finest 40960-dimensional
level performs both primal and adjoint deflated GMRES singular iterations.
