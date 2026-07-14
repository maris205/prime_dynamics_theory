# Endpoint-centered Gaussian resolution rank

This directory contains the sixteenth-layer paper in the quadratic
prime-dynamics program:

> *Endpoint-Centered Gaussian Resolution at a Quadratic Band-Merging Map: A
> Singular-Value Theorem for the Half-Logarithmic Rank*

The distinguished boundary cycles have clearances

```text
delta_k = 1 - p_{2k} = C_b lambda**(-2*k) (1 + o(1)).
```

For a Gaussian transition row with endpoint clearance `delta`, the code uses
its unit Hellinger fingerprint `psi_(sigma,delta)`. After orthogonally
removing the limiting endpoint fingerprint, these rows define a compact
resolution operator

```text
R_sigma e_k = (I - |psi_(sigma,0)><psi_(sigma,0)|)
              psi_(sigma,delta_k).
```

The paper proves analytically that

```text
||R_sigma||_S2**2
    = log(1/sigma)/(2*log(lambda)) + O(1),

#{j : s_j(R_sigma) > eta}
    = log(1/sigma)/(2*log(lambda)) + O_eta(1)
```

for every fixed `0 < eta < 1`. Thus the half-logarithmic effective-rank clock
is a singular-value theorem for the endpoint Gaussian row family, not merely
a fit to resonance counts.

The theorem is power-universal. The default `power=1/2` gives Hellinger
fingerprints, while `power=1` gives the `L2`-normalized linear Gaussian kernel
rows. Both have the same leading rank law.

This does **not** prove that the number of noisy Markov resonances equals the
rank above. That identification still requires the Feshbach/Grushin
shift-block reduction proposed in RH-15. Numerically, the parameter-free
half-energy count `s_j**2 > 1/2` agrees with the archived RH-15 cloud degree at
six of seven noise levels and differs by one at the coarsest level. This is a
floating-point comparison, not part of the theorem.

## Reproduction

Run the tests and audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_endpoint_rank_audit.py
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The boundary asymptotic, exact conditioned-Gaussian affinity,
Hilbert--Schmidt law, and threshold-rank theorem are analytic. Boundary
decimals, Gram spectra, and the RH-15 cloud comparison are numerical audits.
