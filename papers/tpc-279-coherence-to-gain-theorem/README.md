# TPC-279 — A minimal coherence-to-gain criterion for four-packet reassembly

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For four Hilbert-space packets, the exact normalized deficit
`Delta=(D-G)/D=-2E/D` is the necessary-and-sufficient source input for a
power gain: `D/G >= b X^gamma` if and only if
`G/D <= b^(-1) X^(-gamma)`.  Pairwise absolute coherence gives only the sharp
constant envelope `G/D <= min(4,1+3 mu)`, while orthogonal packets attain
`D/G=1`, so pairwise coherence alone cannot pay a positive power.

The twelve TPC-278 rows were transferred into the `(r,q,Delta)` coordinates
with exact reciprocal interval arithmetic: 8 positive-deficit and 4
negative-deficit rows.  This is a finite structural theorem and transfer,
not an arithmetic `L2` estimate or a twin-prime result.

## Claim ceiling

```text
PROVED_EXACT = minimal four-packet deficit criterion
PROVED_EXACT = sharp pairwise-coherence envelope and reciprocal floor
REFUTED_EXACT = pairwise absolute coherence as a positive-power mechanism
NUMERICALLY_CERTIFIED_FINITE = exact transfer of all 12 TPC-278 rows
OPEN = source-level asymptotic deficit bound
FIXED_POWER_CREDIT = 0
ARITHMETIC_ADVANCE = NO
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc279_coherence_to_gain_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc279_coherence_to_gain_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc279_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc279_coherence_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The parent TPC-278
certificate is hash-locked; no floating-point classification is used by the
producer or independent transfer checker.
