# RH-56: growing-horizon strong-space barriers

This directory contains the fifty-sixth RH-layer paper:

> *Growing-Horizon Strong-Space Barriers for Directional Hardy Energies: An
> Optimized Exponent No-Go and a Mixed Haar-Channel Overlap Route*

## Main result

RH-50 reduced the remaining intrinsic-identification problem to two
Perron/parity-deflated directional Hardy energies. RH-56 analyzes the natural
two-stage proof attempt: an initial weak/Hilbert segment followed by a
postcritical strong-space decay estimate after a growing horizon.

If the strong-space prefactor is `sigma^-p` and the global tail rate is
`theta`, optimizing the switch gives

```text
alpha = p log(1/r) / log(1/theta).
```

The standard isotropic strong-space estimate has `p=1` per direction. Since
RH-54 allows total Hardy power at most `1/4`, the common rate at `r=0.85`
would have to satisfy

```text
theta <= r^8 = 0.2724905250390625...
```

This is a rigorous route obstruction, not a claim that the actual directional
Hardy energies diverge.

## Certified deterministic-sector input

The old RH-13 number `0.329642...` is only a spectral-radius upper and cannot
by itself prove a no-go. RH-56 adds a separate 512-bit Arb contour certificate:
the deterministic reduced even analytic sector has exactly one resonance in

```text
|w - 0.2078803| < 0.05,
```

so its modulus is greater than `0.1578803` and the compatible one-step rate is
greater than `0.3973415407`, already above `r^8`. The full 50-coordinate Taylor
matrix is used for the contour resolvent bound; the active 25-coordinate block
is used only to isolate the nonzero finite eigenvalue. The full-circle tail
perturbation product is below `0.077271` (the conservative full-matrix
resolvent bound is `147.5271`; the active-block value is not used for this
margin).

This is a deterministic component-square theorem. It is not a noisy-bulk
eigenvalue theorem and does not assume the RH-15 noisy resonance-cloud
conjecture.

## Surviving route

For a modal bulk `N = sum(mu_j P_j)`, normalized source `X`, and observation
`Y`, RH-56 proves the sufficient bound

```text
E(r) <= sum_j ||Y P_j X||_S2 / sqrt(1 - |mu_j/r|^2).
```

The next positive target is therefore a dyadically uniform mixed
source--resonance--observation overlap budget, preferably formulated with
Riesz blocks rather than individual ill-conditioned eigenvectors.

## Numerical evidence

- The deterministic five-scale all-column audit has maximum energy `1.76031`.
- Energy divided by the radial Hardy clock is at most `1.09463`.
- Production-resolution truncated RH-50 evidence remains below `2.35829`.
- The deterministic RH-53 block-tail relative excess is below `4.94e-4`.

These are binary64 diagnostics; the production RH-50 values use probes and a
finite time horizon. They do not prove a uniform small-noise Hardy bound.

## Exact boundary

Closed analytically or by the stated computer-assisted certificate:

- the two-stage exponent ledger;
- the `r^8` critical-rate criterion;
- the deterministic analytic-sector resonance inclusion;
- the modal mixed-overlap Hardy upper;
- the inherited finite-matrix tail and overlap-route audits.

Still open:

- a dyadically uniform mixed-overlap or Hardy/Stein budget for the physical
  small-noise family;
- RH-54 Stage A1 and unconditional Stage A4 intrinsic identification;
- any self-adjoint Hilbert--Polya operator, `T log T` law, arithmetic
  prime-power trace formula, zeta-zero identity, Riemann-hypothesis result, or
  TPC twin-prime conclusion.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_hardy_barrier_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_arb_exponent_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_arb_sector_resonance.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_hardy_barrier_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf growing-horizon-hard-space-barrier.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```
