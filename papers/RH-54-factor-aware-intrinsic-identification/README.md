# RH-54: factor-aware intrinsic identification transfer

This directory contains the fifty-fourth-layer paper in the quadratic
small-noise spectral program:

> *Factor-Aware Sparse-to-Full Transfer for Intrinsic Riesz Identification:
> Growing-Horizon Hardy Robustness, a Conditional Closure Theorem, and a
> Nonnormal No-Go*

## Main result

RH-54 closes the finite-dimensional interface left between RH-53's sparse
Hardy certificate and RH-48/49's intrinsic identification theorem.

For a nonzero Hilbert--Schmidt coupling,

```text
||B/||B||_S2 - Btilde/||Btilde||_S2||_S2
    <= 2 ||B-Btilde||_S2 / ||B||_S2.
```

Together with `||B||_S2,||C||_S2 = Theta(h sigma^(-3/2))`, the adaptive
Gaussian cutoff gives normalized-coupling error

```text
O(h sigma^(3/2) / log(1/h)^(1/4)).
```

The recomputed intrinsic factors enter through explicit projector and
weighted-Riesz defects. For the left Hardy triple,

```text
delta_A <= (delta_T + epsilon_W,f)/r,
delta_X <= epsilon_P,f + ||Qtilde_f|| 2 delta_B/||B||_S2,
delta_Y = 0,
```

with the symmetric right formulas. A common-contour resolvent ledger is one
rigorous way to bound `epsilon_P` and `epsilon_W`.

## Growing horizon

Using actual finite-time norms

```text
a_j = ||A^j||,  atilde_j = ||Atilde^j||,
d_M = delta_A sum_(j=0)^(M-1) a_(M-1-j) atilde_j,
```

the sparse contracting block transfers whenever `q_M+d_M<1`. The theorem
also gives a complete perturbed Hardy upper. No replacement by `||A||^j` or
spectral-radius decay is used.

## Identification composition

If the dyadic left/right Hardy energies satisfy

```text
E_B = O(sigma^(-alpha_B)),
E_C = O(sigma^(-alpha_C)),
```

and the range-restricted residues are bounded, then

```text
||I_(n,sigma)||_S2
    = O(n^(-2) sigma^(-13/4-alpha_B-alpha_C)).
```

Every strict `n sigma^2 -> infinity` schedule survives when
`alpha_B+alpha_C <= 1/4`. Polylogarithmic energies yield
`O(n^(-2) sigma^(-13/4) polylog(1/sigma))`.

This is a rigorous conditional composition theorem. It does not prove the
uniform Hardy or Riesz-conditioning premises.

## Nonnormal no-go

For

```text
T_K = [[0,K],[0,1]],
E_K = [[0,0],[c/K,0]],
```

the input defect tends to zero, while the selected Riesz projector changes
by at least a fixed positive amount and in fact becomes highly conditioned.
Therefore the adaptive cutoff norm alone cannot control recomputed intrinsic
factors; a contour or strong--weak stability ledger is indispensable.

## Numerical audit

The dense audit uses `N*sigma=5.12`, `r=0.85`, dimensions
`32,64,128,256,512`, horizons `4,8,16,24,32`, and cutoff multiples
`L=5,6,8`. The five-sigma family deliberately amplifies the perturbation.

- Maximum five-sigma Markov spectral defect: `6.61e-8`.
- Maximum fine weighted-Riesz defect: `3.72e-8`.
- Maximum normalized outgoing-coupling defect: `4.12e-7`.
- Maximum fraction of a contraction margin consumed: `3.34e-7`.
- All factor-aware bounds dominate the actual recomputed triple defects.
- All sparse/full block powers remain contracting.

At `N=512,L=5`, the actual left/right full Hardy-energy-squared changes are
`1.70e-7` and `4.93e-7`; finite-time theorem uppers are `5.14e-4` and
`5.81e-4`. The bounds are conservative but valid. At `L=6`, matrix defects
are about `1e-10`; at `L=8`, they are at binary64 roundoff.

A separate 256-bit Arb run certifies the normalization, factor composition,
and block-transfer arithmetic on a small abstract interval ledger. It is not
a production folded-Gaussian Riesz enclosure.

## Exact boundary

Closed:

- normalized coupling stability;
- factor-aware finite-matrix sparse/full transfer;
- growing-horizon contraction and full-energy robustness;
- the conditional RH-48 through RH-53 exponent composition.

Still open:

- a dyadically uniform analytic Hardy/Stein trace budget (Stage A1);
- a uniform intrinsic Riesz-conditioning modulus or production interval
  enclosure;
- full Stage A3 and unconditional Stage A4 identification.

No arithmetic trace formula, prime-power identity, zeta-zero spectral
identity, self-adjoint Hilbert--Polya operator, `T log T` counting law, or
Riemann-hypothesis conclusion is claimed. The TPC twin-prime branch remains
independent.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_factor_aware_pilot.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_arb_transfer_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_closure_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf factor-aware-intrinsic-riesz-identification.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The formal manuscript is `factor-aware-intrinsic-riesz-identification.pdf`.
