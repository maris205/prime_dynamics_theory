# TPC-214: Mobius-Weighted Shared-Frequency Clusters

## Result

TPC-213 identified the exact common-source Gram, but left the shared-frequency
clusters as a general finite intersection sum.  TPC-214 restores the actual
V46 coefficient

```text
c_d = mu(d) log(d) / d
```

and proves an additional exact covariance: if `h|d` and `d=k h`, then the
smooth reciprocal emitter satisfies

```text
B_d(k r) = B_h(r).
```

Every common rational frequency therefore carries one reduced-denominator row,
multiplied by the Mobius-log tail

```text
C_h = sum_(d in D, h|d) c_d.
```

On a complete `lcm(D)` period, the physical Gram is exactly

```text
L sum_(h|L) |C_h|^2
  sum_(u mod h, gcd(u,h)=1) |B_h(u)|^2.
```

The zero axis is absent when the prime shell lies below `H`.

## What this establishes

```text
TPC214_ROUTE_ADVANCE = YES
TPC214_STRUCTURAL_THRESHOLD_A = PASS
TPC214_EMITTER_DILATION_COVARIANCE = PROVED_EXACT
TPC214_REDUCED_DENOMINATOR_CLUSTER_FACTOR = PROVED_EXACT
TPC214_ZERO_AXIS_SCOPE = PROVED_EXACT
TPC214_FOUR_PACKET_POLARIZATION = PROVED_EXACT_LINEAR_EXTENSION
TPC214_NESTED_CLUSTER_CANCELLATION = PROVED_EXACT_FINITE_SIGN
TPC214_COMPOSITE_QUOTIENT_ENHANCEMENT = PROVED_EXACT_FINITE_SIGN
TPC214_FINITE_ENERGY_RATIOS = NUMERICAL_OBSERVATION
TPC214_UNIVERSAL_CLUSTER_SAVING_SIGN = REFUTED_SCOPED
TPC214_LITERAL_V46_ASYMPTOTIC_CLUSTER_BOUND = OPEN
TPC214_PRIME_SHELL_REASSEMBLY = OPEN
TPC214_ARITHMETIC_ADVANCE = NO
TPC214_FIXED_ATOM_CREDIT = 0
TPC214_L2 = NONE
TPC214_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

The `{5,7,35}` fixture has physical/direct-sum weighted energy ratio about
`0.5963435557`; the adversarial `{3,5,7,105}` fixture has ratio about
`1.2119952513`.  These are finite certificates, not asymptotic evidence.

## Project layout

```text
README.md
PAPER_PLAN.md
PROOF_PACKAGE.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/shared_frequency_clusters.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/packet_sanity.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-214-mobius-frequency-clusters/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-214-mobius-frequency-clusters/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-214-mobius-frequency-clusters/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-214-mobius-frequency-clusters/experiments/packet_sanity.py --check
```

The finite emitter uses the exact rational Schwartz profile
`psi(t)=(1+t^2)^(-2)`.  The logarithms are retained in the coefficient ledger;
finite energy ratios are reported with high-precision decimal evaluation.

## Interpretation

The new result is an analytic structure, not arithmetic `L2` credit.  Nested
Mobius signs can reduce the physical Gram, but composite quotient families can
also increase it.  A future theorem must control the actual cluster tails in
the V46 divisor band rather than assume a favorable sign.

Author: Liang Wang, Huazhong University of Science and Technology.
