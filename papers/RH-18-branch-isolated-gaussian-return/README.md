# Branch-isolated Gaussian return blocks

This directory contains the eighteenth-layer paper in the quadratic
prime-dynamics program:

> *Branch-Isolated Gaussian Return Blocks at a Quadratic Band-Merging Map:
> Riccati Packet Monodromy, Critical Closure, and the Bulk Spectral Edge*

For the time-ordered boundary cycle from RH-17, the affine two-step Gaussian
channels admit unique periodic packet widths

```text
m_j**2 * t_j**2 = t_(j+1)**2 + beta_j**2.
```

Peak-normalized Gaussian observables are then transported exactly with
coefficients

```text
c_j = t_(j+1) / sqrt(t_(j+1)**2 + beta_j**2),
product(c_j) = 1 / abs(M_k).
```

The construction removes the single exponentially large RH-17 weight, but
the balanced packet basis still has asymptotic condition exponent `1/2` in
component period. At the half-logarithmic noise clock this is a
`sigma**(-1/4+o(1))` barrier.

At the final critical return, the affine Gaussian packet fails. The paper
derives an explicit conditioned Gaussian--quadratic profile. Its two lobes
are exchanged across the canonical partition `b=u_c**(-1/2)`; retaining the
left lobe selects the boundary word without a fitted cutoff.

The time-labeled local channels

```text
A_j = chi_j K_sigma**2 chi_(j+1)
```

form an exact block-cyclic auxiliary operator. Every nonzero return
eigenvalue generates an exact roots-of-unity ring. Numerically, the principal
branch-isolated ring selected by the RH-16 Hellinger rank predicts the
archived bulk spectral radius to within `5.7e-4` at `sigma=1e-4`.

This is not yet a theorem identifying the auxiliary block with the full
Feshbach block of the Markov operator. Controlling the coupling to the
complement remains the next gate.

Run the tests and audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_gaussian_return_audit.py
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
