# TPC-216: Direct-Sum Row-Energy Envelope and the Cauchy Bottleneck

## Result

TPC-215 reduced the complete-period shared-frequency cluster Gram to the
source-locked divisor direct-sum row energy up to `O((log x)^2)`.  TPC-216 now
proves the deterministic envelope

```text
L^(-1) E_direct <= C_psi (Q^3/H) (log U)^3
                     = x^(11/32+o(1))
```

for the literal V46 emitter, where

```text
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400),
Q<q<=2Q, Y0<d<=U, mu(d)^2=1.
```

The proof uses `4Q<H` for sufficiently large `x`, which makes the fixed-q
integer cutoff injective modulo `d`.  One Cauchy inequality across the prime
shell then gives the row bound; `P<=2Q` is the only shell cardinality input.

## Adversarial result

The exact rational fixture `d=5`, `H=500`, `Q-scale=100`,
`q={101,131,151,181}`, and `psi(t)=(1+t^2)^(-2)` has every fixed-q row
supported on `{1,4}` modulo 5.  The combined/direct row-norm ratio is exactly
recorded in `results/certificate.json` and is approximately `3.70568607565`.
This is finite structural evidence that shell rows cannot be assumed orthogonal.

## Claim firewall

```text
TPC216_ROUTE_ADVANCE = YES
TPC216_STRUCTURAL_THRESHOLD_A = PASS
TPC216_FIXED_Q_NO_COLLISION = PROVED_EXACT
TPC216_FIXED_Q_ROW_ENERGY = PROVED_EXACT
TPC216_SHELL_CAUCHY_ENVELOPE = PROVED_EXACT
TPC216_PRIME_SHELL_CARDINALITY = PROVED_P_LE_2Q
TPC216_NORMALIZED_EXPONENT = PROVED_11_OVER_32
TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE = PROVED_X_11_OVER_32_LOG_CUBED
TPC216_ARITHMETIC_CANCELLATION = NONE
TPC216_ALIGNED_SUPPORT_ADVERSARY = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC216_FREE_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC216_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC216_PRIME_SHELL_REASSEMBLY = OPEN
TPC216_FULL_GATE_B = OPEN
TPC216_ARITHMETIC_ADVANCE = NO
TPC216_FIXED_ATOM_CREDIT = 0
TPC216_L2 = NONE
TPC216_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

This is a complete-period structural result.  It is not an arithmetic saving,
not a finite-window theorem, and not a twin-prime result.

## Layout

```text
README.md
PAPER_PLAN.md
PROOF_PACKAGE.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/direct_sum_row_energy.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/adversarial_shell_alignment.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-216-direct-sum-row-energy-envelope/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-216-direct-sum-row-energy-envelope/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-216-direct-sum-row-energy-envelope/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-216-direct-sum-row-energy-envelope/experiments/adversarial_shell_alignment.py --check
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_direct_sum_row_energy_envelope_checker.py --check
```

Author: Liang Wang, Huazhong University of Science and Technology.
