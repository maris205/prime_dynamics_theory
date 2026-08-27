# TPC-282 — Literal source attachment and finite source-lock audit

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On the frozen literal V59 operator and the six registered growing-cutoff rows
of TPC-275, the actual projected source attachment
`C=<w_perp,S>` is separated from zero on all 12 `(scale, kernel exponent)`
rows: 11 negative and 1 positive.  The weakest normalized attachment is only
about `3.36e-5`, so this finite source lock supplies no uniform asymptotic
nondegeneracy or fixed-power credit.

## What advances

- evaluates the actual comparison-weight readout, rather than an arbitrary
  equal-norm functional;
- locks `w_perp=(I-P_3)w`, `S=A_perp beta`, and `C=<w_perp,S>` to the physical
  prime-shell source;
- independently replays all 12 rows with outward interval arithmetic and
  exact rational projected output energy;
- records the sign change at `(256,38,6,2)` and the weakest squared cosine;
- makes the finite-to-asymptotic boundary explicit: a nonzero table is not a
  growing lower-bound theorem.

## Claim ceiling

```text
NUMERICALLY_CERTIFIED_FINITE = literal source attachment separated from zero on 12 rows
NUMERICALLY_CERTIFIED_FINITE = 11 negative signs and 1 positive sign
OPEN = uniform asymptotic source nondegeneracy
OPEN = literal arithmetic L2 estimate
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc282_literal_source_attachment_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc282_literal_source_attachment_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc282_literal_source_attachment_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc282_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc282_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc282_attachment_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The certificate is a
finite, source-locked audit; it does not promote the observed attachment to a
uniform estimate in the growing parameter.
