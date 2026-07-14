# TPC-9 reproducibility package

The package separates exact algebraic checks from a finite floating
diagnostic.

## Exact certificate

Run from the paper directory:

```bash
python experiments/exact_zero_mellin_certificate.py \
  --output experiments/data/exact-zero-mellin-certificate.json
python experiments/test_exact_zero_mellin_certificate.py
```

The exact program uses the Python standard library only. It represents
`log(p)` and `log(p)*log(q)` as formal basis symbols and verifies:

- `sum_{d|r} (Lambda(d)-1) = log(r)-tau(r)` for every retained `r`;
- equality of the direct factor-pair sum and the collapsed product sum;
- the exact split into `d <= D` and `d > D`;
- target arithmetic-progression reindexing for every `d <= D`;
- the local Euler factors at `s=0` entering `C_h(s)`.

The canonical payload SHA-256 is

```text
6686C9E926CCB05F4DB0BF56A6A8F2811D5DED9A020FB905AC8DC54D350EDAEE
```

The committed JSON file SHA-256 is

```text
A0D6303B26118D756406677A748D74160065390E5B4A55F70FDD2F1549E2BE43
```

These hashes certify the finite conventions and data, not the analytic
Titchmarsh or Bombieri--Vinogradov theorems. The finite reference product
for `C_2` is stored as an exact rational number; its decimal field is marked
display-only.

## Floating sharp-box diagnostic

The optional script also uses the standard library only:

```bash
python experiments/zero_mellin_diagnostic.py \
  --powers 14,16,18,20 --h 2 \
  --output experiments/data/zero-mellin-diagnostic.json
python experiments/test_zero_mellin_diagnostic.py
```

It uses the nonsmooth box `X < r <= 2X`, floating logarithms, and the cutoff
`D = floor(sqrt(X))`, which lies outside the theorem's unspecified
logarithmically shortened range. It reports complete, small-factor, and large-factor
sums normalized by `X*log(X)`. The generated JSON is ignored by Git. This is
a finite implementation diagnostic, not a verification of the asymptotic
theorem or of its non-explicit logarithmic cutoff.
