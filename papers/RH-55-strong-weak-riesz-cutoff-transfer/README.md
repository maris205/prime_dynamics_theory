# RH-55: strong--weak Riesz cutoff transfer

This directory contains the fifty-fifth-layer paper in the quadratic
small-noise spectral program:

> *Strong--Weak Adaptive Cutoff Transfer for Intrinsic Riesz Factors:
> Sandwiched Functional Calculus, Midpoint--Ulam Contour Inheritance, and a
> Fixed-Window Route No-Go*

## Main result

RH-55 closes the analytic Riesz-conditioning premise left by RH-54.  If a
peripheral contour avoids zero, then

```text
Pi(T;Gamma) = (2 pi i)^-1 integral z^-2 T(z-T)^-1 T dz,
W(T;Gamma)  = (2 pi i)^-1 integral z^-1 T(z-T)^-1 T dz.
```

The outer transfer factors allow strong-space contour resolvents to be
combined with Gaussian `L1 -> L2` smoothing.  The sandwich defect is

```text
D <= rho M R + S M Mtilde tau_1 R + S Mtilde tau_0.
```

No uniform global `L2` contour bound is used; RH-47 proved that such a bound
cannot be `O(1)` as noise vanishes.

## Midpoint--Ulam bridge

For the conditioned folded-Gaussian kernel,

```text
sup_x integral (|k_xx| + |k_yy|) dy = O(sigma^-2).
```

The full discretely normalized midpoint lift and exact Ulam lift therefore
differ by

```text
row L1       O(h^2 sigma^-2),
piecewise BV O(h sigma^-2).
```

Thus fixed strong-space peripheral contours pass to the midpoint family on
every `h=o(sigma^2)` schedule and then to the adaptive sparse family.

## Two adaptive thresholds

A distribution-free use of the exact twice-the-tail row identity gives

```text
projector + weighted-Riesz defect
    = O(Q_h/(h sigma^(3/2))).
```

For `L_kappa(h)=sqrt(2 kappa log(1/h))`, this route preserves every strict
`h=o(sigma^2)` schedule when `kappa>=7/4`.

Using the actual Gaussian tail variation removes the artificial `1/h` loss:

```text
projector + weighted-Riesz defect
    = O(h^kappa sigma^(-5/2)).
```

The sufficient threshold improves to `kappa>=5/4`.  RH-39 already uses
`kappa=2`, giving `o(sigma^(3/2))`.  These are sufficient proof thresholds,
not necessary thresholds for actual Riesz stability.

Fixed `L` fails to vanish through this strong-BV route.  This does not prove
that the actual fixed-window projectors diverge.

## Numerical audit

- Four midpoint--Ulam grids give maximum row error divided by
  `h^2 sigma^-2` below `0.424`.
- The inherited RH-54 five-sigma projector-plus-weighted defect is at most
  `6.49e-8`.
- The largest actual defect divided by the shape-aware unit-constant
  envelope is `1.35e-3`.
- A 256-bit Arb run audits the tail and sandwich scalar formulas.

The matrix quadrature and intrinsic factors are binary64 diagnostics.  The
Arb run is not a production intrinsic Riesz interval eigensolver.

## Exact boundary

Closed analytically:

- midpoint-to-Ulam strong contour inheritance;
- adaptive sparse/full unweighted projector transfer;
- adaptive sparse/full weighted-Riesz transfer;
- RH-54's factor-aware cutoff premise;
- the analytic factor-transfer component of Stage A3.

Still open:

- a dyadically uniform Hardy/Stein trace budget (Stage A1);
- production-scale interval execution combining all-column traces and
  intrinsic factors;
- unconditional Stage A4 intrinsic identification.

No arithmetic trace formula, prime-power identity, zeta-zero spectral
identity, self-adjoint Hilbert--Polya operator, `T log T` law, Riemann
hypothesis, or twin-prime conclusion is claimed.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_riesz_cutoff_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_arb_riesz_ledger.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_riesz_cutoff_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf strong-weak-riesz-cutoff-transfer.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The formal manuscript is `strong-weak-riesz-cutoff-transfer.pdf`.
