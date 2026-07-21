# RH-58: time-ordered Schur cross-Gramians

This directory contains the fifty-eighth RH-layer paper:

> *Time-Ordered Schur Cross-Gramians for Directional Hardy Fusion: Removing
> Radial Riesz Obliqueness*

## Main result

For a stable finite matrix `A = Q T Q*`, RH-58 partitions the unitary Schur
coordinates into radial packets. It proves two exact positive Gram identities:

```text
input packets:  K_in[i,j]  = tr(X_j^* O X_i)
output blocks:  K_out[i,j] = tr(Y_i G_ij Y_j^*)
E^2 = 1^* K_in 1 = 1^* K_out 1
```

Here `G` and `O` are the controllability and observability Gramians. The
coordinate projections have norm one, so no oblique Riesz projector appears.

Upper triangularity also gives the exact reverse recursion

```text
G_ij = L_ij^{-1}(X_i X_j^* + later feed-forward blocks)
L_ij(Z) = Z - D_i Z D_j^*.
```

If every diagonal block contracts after `M` steps, the Stein inverse has the
explicit upper

```text
sum_(s=0)^(M-1) ||D_i^s|| ||D_j^s||
------------------------------------------------.
               1 - ||D_i^M|| ||D_j^M||
```

## Five-scale result

The all-column binary64 audit uses the same `N*sigma=5.12` family and radial
cuts as RH-57.

- The largest input-packet coherence upper is `1.90086`.
- The largest output-block coherence upper is `1.76120`.
- Every diagonal Schur block has eight-step norm below `0.290`.
- The largest observed block-Stein gain is below `2.793`.
- Schur reconstruction and cross-Stein residuals remain below `7.1e-15`.

At `sigma=0.01`, RH-57's fixed radial Riesz uppers were `81.68` and `672.41`.
Thus unitary Schur packets remove the radial-projector obliqueness seen there.

## New route boundary

The straightforward scalar proof is still unusable. Replacing every
feed-forward block by an independent spectral/Frobenius norm gives smallest-
scale uppers `1922.40` and `380.40`, despite the exact energies `1.4681` and
`1.7603`.

This is a no-go for the scalar absolute-path ledger, not for Schur packets or
for Stage A1. The next analytic target must preserve packet square sums,
phases, or a positive anisotropic block metric.

## Evidence boundary

Analytic finite-dimensional results:

- dual input-packet and output-state Gram identities;
- reverse time-ordered cross-Stein recursion;
- block-power Stein inverse upper;
- scalar absolute Schur-path majorant.

Computer evidence:

- five-scale ordered Schur forms, Gramians, gains, and fitted powers are
  binary64 diagnostics;
- the 256-bit Arb certificate covers only a two-scalar-block model;
- no continuum regularity of the noise-dependent Schur packets is proved.

Stage A1, unconditional Stage A4, a self-adjoint Hilbert-Polya operator,
`T log T` counting law, arithmetic prime-power trace formula, zeta-zero
identity, and Riemann-hypothesis conclusion remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_schur_fusion_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_schur_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf time-ordered-schur-cross-gramian.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
