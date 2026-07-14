# Finite certificate

This package checks only the finite algebra used in TPC-12:

- factor-pair versus primitive-ray compression;
- product-center regrouping of the source diagonal;
- the finite Cauchy--Schwarz exceptional-mass bound;
- the sign-coherent obstruction ray;
- the exact `6 k^2 + 1` quadratic embedding;
- the Euclidean radial-minimax identity.

Run from the paper directory:

```powershell
python experiments/short_shift_certificate.py
python -m unittest experiments.test_short_shift_certificate
```

The script uses only the Python standard library. It does not test the
Guth--Maynard theorem, a fixed quadratic-prime asymptotic, or any
fixed-shift prime-pair assertion.
