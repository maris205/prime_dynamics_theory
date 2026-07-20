# RH-53: deterministic Hardy tails and Gaussian cutoff transfer

This directory contains the fifty-third-layer paper in the quadratic
small-noise spectral program:

> *Deterministic Block-Tail Certificates for Directional Hardy Energies:
> All-Column Trace Sums, Adaptive Gaussian Cutoff Transfer, and the Remaining
> Production-Interval Gap*

## Main result

For a stable scaled bulk matrix `A`, source `X`, observation `Y`, and

```text
S_M = sum_(m=0)^(M-1) A^m X X^* (A^*)^m,
q_M = ||A^M||_2 < 1,
```

the complete directional Hardy energy satisfies

```text
sum_(m>=0) ||Y A^m X||_S2^2
 <= sum_(m=0)^(M-1) ||Y A^m X||_S2^2
    + ||A^M S_M (A^*)^M||_2 ||Y||_S2^2/(1-q_M^2).
```

The finite sum is accumulated over every source column. It is a deterministic
Frobenius trace identity: no Hutchinson probes and no fitted tail decay are
used. A second block-geometric upper is also available and the smaller valid
tail can be retained.

## Cutoff verdict

The sparse/full transfer has two different answers:

- Fixed eight sigma is harmless on every stored RH-50 grid. The RH-39
  analytic two-norm upper is at most `5.60e-13` through `N=40960`.
- Fixed eight sigma is not a canonical all-grid limit. At fixed positive
  noise it leaves a strictly positive continuum row defect.
- The honest full-Gaussian route uses
  `L(h)=max(5,2 sqrt(log(1/h)))`, giving a cutoff defect
  `O(h^2/(log(1/h))^(1/4))`.

A finite-time telescoping theorem propagates operator, source, and observation
defects through the deterministic main sum and transfers a contracting block
when the remaining margin is positive.

## Numerical evidence

The dense five-scale audit uses `N*sigma=5.12`, `r=0.85`, and dimensions
`32,64,128,256,512`. The horizons are `4,8,16,24,32`.

| sigma | N | M | left exact | left upper | right exact | right upper |
|---:|---:|---:|---:|---:|---:|---:|
| 0.16 | 32 | 4 | 0.90396 | 0.90414 | 1.00265 | 1.00289 |
| 0.08 | 64 | 8 | 1.16256 | 1.16307 | 1.26528 | 1.26591 |
| 0.04 | 128 | 16 | 1.33383 | 1.33396 | 1.48454 | 1.48477 |
| 0.02 | 256 | 24 | 1.40958 | 1.40968 | 1.63399 | 1.63415 |
| 0.01 | 512 | 32 | 1.46807 | 1.46809 | 1.76031 | 1.76036 |

The worst relative energy excess is `4.94e-4`. These values are binary64
all-column diagnostics, not interval enclosures. A separate 256-bit Arb run
executes the complete outward-rounded algorithm on a small abstract matrix.

## Exact boundary

RH-53 closes the deterministic finite-matrix tail mechanism and the
exact-real adaptive cutoff route. It does **not** claim full Stage A3 closure:

- the `N=40960` all-column Hardy trace has not been executed in interval
  arithmetic;
- the complete cutoff perturbation has not yet been propagated through
  recomputed intrinsic factors and normalized coupling ranges;
- no uniform/polylogarithmic small-noise Hardy bound is proved, so Stage A1
  remains open;
- Stage A4 intrinsic Riesz identification remains unproved.

No arithmetic trace formula, prime-power identity, zeta-zero spectral
identity, self-adjoint Hilbert--Polya operator, `T log T` law, or Riemann
hypothesis conclusion is claimed. The TPC twin-prime branch remains
independent.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q

OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_deterministic_tail_pilot.py

PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_arb_tail_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_arb_cutoff_ledger.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_tail_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf deterministic-block-tail-hardy-cutoff.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The formal manuscript is `deterministic-block-tail-hardy-cutoff.pdf`.
