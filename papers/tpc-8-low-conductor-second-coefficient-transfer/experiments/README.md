# TPC-8 reproducibility package

This directory deliberately separates two kinds of computation.

## Exact certificate

`exact_transfer_certificate.py` uses only standard-library integers and
`fractions.Fraction`. At the reference modulus

```text
q = 5 * 7 * 11 = 385,  h = 2,
```

it verifies:

1. the pointwise inclusion-exclusion resolution of the survivor operator;
2. the arithmetic involutions `J_(h,d)(x) = -h*x^(-1) mod d` for every
   squarefree divisor `d` of `q`, including their exact `+/-` dimensions;
3. the CRT-fiber identity
   `K = sum_(d|q) mu(d)/phi(d) U_(h,d) E_(q,d)`;
4. the principal mode, all seven nonprincipal real quadratic conductor
   modes, and the normalized TPC-5 multipliers;
5. the exact normalization of the Bombieri--Vinogradov row main term;
6. progression reindexing for an arbitrary integer target weight and for
   von Mangoldt sums represented exactly in the formal basis `{log(p)}`.

Regenerate the committed canonical JSON and run the fast tests from this
directory:

```bash
python exact_transfer_certificate.py --output data/exact-certificate.json
python test_exact_transfer_certificate.py
```

The test file is also pytest-compatible:

```bash
pytest -q test_exact_transfer_certificate.py
```

## Optional floating diagnostic

`lambda_transfer_diagnostics.py` requires NumPy. It sieves the genuine von
Mangoldt function, computes each weighted row both directly and through
target progressions modulo `m*q`, and compares it with the exact rational
local main term. A reference-scale run is:

```bash
python lambda_transfer_diagnostics.py \
  --m 32 --n 524288 --q 35 --conductors 1,5,7,35 \
  --output data/lambda-diagnostic.json
python test_lambda_transfer_diagnostics.py
```

The floating output is intentionally not the exact certificate. In
particular, it cannot instantiate the non-explicit logarithmic constant in
Bombieri--Vinogradov and is not evidence that a fixed-shift prime-pair defect
is small. The `l1_row_error_over_X` field is merely the finite supremum over
coefficients of modulus at most one for the displayed collection of rows.
