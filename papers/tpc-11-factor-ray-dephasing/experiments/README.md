# Finite factor-ray certificate

This directory checks the exact finite identities used before the analytic
estimates in TPC-11. It verifies primitive-ray compression, the hyperbolic
log-spacing bound, hard-kernel compression, exact Fejér diagonalization,
compact-Fourier support-allowed determinant layers and their geometric
bound, and the endpoint selector geometry.

It deliberately does **not** estimate a fixed-shift prime-pair asymptotic and
is not numerical evidence for the twin-prime conjecture.

From the paper directory, run:

```powershell
python experiments/factor_ray_certificate.py
python -m unittest experiments.test_factor_ray_certificate
```

The first command regenerates
`experiments/data/factor-ray-certificate.json`. Only the Python standard
library is required.
