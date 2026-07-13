# Exact weighted-kernel diagnostics

The reference program verifies the finite weighted identities with integer and
rational arithmetic:

1. direct weighted centering and exact-conductor reconstruction at `h = 2`;
2. complete fully-active-shift Parseval conductor by conductor;
3. the exact-conductor second-moment bound used before the multiplicative
   large-sieve aggregation;
4. deterministic short-shift completion for signed integer coefficients.

Run from this directory:

```bash
python exact_weighted_diagnostics.py --output data/exact-certificate.json
python -m unittest -v test_exact_weighted_diagnostics.py
```

The certificate is finite normalization evidence only. It contains no von
Mangoldt data, no floating-point Fourier transform, and no evidence for a
twin-prime assertion.
