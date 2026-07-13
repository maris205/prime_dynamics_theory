# Exact finite diagnostics

The reference program verifies three finite statements using only integer and
rational arithmetic:

1. the inclusion--exclusion fiber bound and its quadratic-character
   consequence;
2. the `Q = 5 * 7 * 11` shifted-divisor Selberg-form certificate which
   annihilates every one-prime Fourier mode;
3. exact conductor-by-conductor decompositions for a fixed `h = 2` box and
   for the complete fully-active shift mean square, followed by separate
   checks of the elementary low- and high-conductor bounds.

Run from this directory:

```bash
python exact_diagnostics.py --output data/exact-certificate.json
python -m unittest -v test_exact_diagnostics.py
```

The output is a finite consistency certificate. It does not contain von
Mangoldt weights, detect twin primes, or supply evidence for a prime-pair
asymptotic.
