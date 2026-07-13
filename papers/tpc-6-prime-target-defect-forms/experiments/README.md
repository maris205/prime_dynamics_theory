# Exact finite prime-target defect certificate

This experiment gives a finite, exact nullspace witness for the information
lost by one fixed CRT window.  For

```text
Q = 5 * 7 * 11 = 385,  h = 2,
```

the nonnegative unit point masses at

```text
(m,n) = (1,148994),  mn+h = 148996 = 386^2,
(m,n) = (1,149379),  mn+h = 149381 (prime)
```

have the same residue pushforward modulo `Q`.  Consequently they have the
same divisibility signatures at every window prime, the same finite character
data, and the same centered target-rough-kernel value `7/9`.  Their prime
indicators differ by one and their Liouville values are `+1` and `-1`.

The primality of `149381` is accompanied by a full-factorization Lucas
certificate.  All calculations use standard-library integers and
`fractions.Fraction`; there is no floating-point or randomized computation.

Run from this directory:

```bash
python exact_defect_certificate.py --output data/exact-certificate.json
python -m unittest -v test_exact_defect_certificate.py
```

The checked JSON is rendered with sorted keys and a fixed final newline.  The
test suite regenerates it and compares the result byte for byte.

This is a fixed-finite-window information-loss certificate.  It does not claim
that growing sieve windows, bilinear/dispersion input, or other analytic data
cannot distinguish primes, and it is not a proof of a twin-prime statement.
