# Computational protocol

All theorem-facing arithmetic in the executable artifacts uses
`fractions.Fraction` and Gaussian pairs of exact fractions. No floating-point
comparison is used as theorem evidence.

## Generation and checks

Run from the paper directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc242_phase_fourier_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc242_phase_fourier_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O code/tpc242_phase_fourier_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc242_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc242_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc242_phase_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc242_phase_stress.py --check
```

Normal and optimized stdout are compared byte-for-byte for each checker. No
validation relies on `assert`, so `python -O` does not bypass a gate.

## Trust boundaries

- The producer exposes mutually exclusive, required `--write` and `--check`
  modes.
- The stored document is one-line, sorted-key, compact ASCII JSON with one
  trailing newline and a SHA-256 over the payload excluding the digest field.
- Strict parsing rejects duplicate keys and `NaN`/infinite constants.
- Fraction records must be reduced and have a positive denominator.
- The independent checker does not import the producer.
- The independent checker binds every nested theorem, source-lock, scope,
  status, task, and mutation-manifest field; no uninspected schema key is
  accepted merely because the payload digest was recomputed.
- Semantic mutation documents have their payload digest recomputed before
  rejection, preventing the digest from being the only firewall.
- Four additional hostile rebound controls replace the full source lock,
  promote strict `1/400`, promote a twin-prime result, and fabricate an
  arithmetic route breakthrough; all must be rejected after digest renewal.
- The stress census is exhaustive only over two-dimensional vectors whose
  Gaussian-integer components have real and imaginary parts in `[-1,1]`.
  Its status is `NUMERICAL_FINITE_ILLUSTRATION_ONLY`.
