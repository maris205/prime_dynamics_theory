# TPC-215: Short-Quotient Mobius Tails and the No-Power-Loss Majorant

## Result

TPC-214 reduced the complete-period physical Gram to Mobius-log tails

```text
C_h = sum_(Y0 < d <= U, mu(d)^2=1, h|d) mu(d) log(d) / d.
```

TPC-215 source-locks the actual V46 scales

```text
H=x^(21/32),  Q=x^(1/3),  Y0=H/(4Q),  U=x^(133/400),
Q < q <= 2Q.
```

If the reduced emitter row at denominator `h` is nonzero, its integer cutoff
forces

```text
h >= H/q_max >= H/(2Q) = 2Y0.
```

Thus `h` itself lies in the full squarefree transition band.  Writing `d=hk`
gives the exact short-quotient normal form

```text
C_h = mu(h)/h
      sum_(Y0/h < k <= U/h, (k,h)=1)
      mu(k)(log(h)+log(k))/k,

k <= U q_max/H <= 2UQ/H = 2x^(23/2400+o(1)).
```

With

```text
D_h = sum_(d in D_x, h|d) |mu(d)log(d)/d|^2,
N_h = sum_((a,h)=1) |B_h(a)|^2,
```

the exact row decomposition and a deterministic harmonic estimate imply

```text
sum_h N_h |C_h|^2
 <= A_x sum_h N_h D_h
  = A_x sum_d |c_d|^2 sum_(r mod d)|B_d(r)|^2,

A_x <= [log(U)/log(H/q_max)]^2
       Harmonic(floor(U q_max/H))^2
     = O((log x)^2) = x^(o(1)).
```

This is a genuine asymptotic structural advance: reduced-frequency clustering
cannot amplify the divisor direct-sum energy by a fixed power of `x`.
It is not a saving theorem.  Indeed, for every active `U/2 < h <= U`, the only
multiple in the band is `d=h`, so `C_h=c_h` and `|C_h|^2/D_h=1` exactly.

## Claim firewall

```text
TPC215_ROUTE_ADVANCE = YES
TPC215_STRUCTURAL_THRESHOLD_A = PASS
TPC215_ACTIVATION_FLOOR = PROVED_EXACT
TPC215_SHORT_QUOTIENT_NORMAL_FORM = PROVED_EXACT
TPC215_QUOTIENT_LENGTH_EXPONENT = PROVED_23_OVER_2400
TPC215_ROW_NORM_DIVISOR_DECOMPOSITION = PROVED_EXACT
TPC215_CLUSTER_TO_DIRECT_MAJORANT = PROVED_O_LOG_X_SQUARED
TPC215_FIXED_POWER_CLUSTER_AMPLIFICATION = EXCLUDED
TPC215_UNIFORM_ROWWISE_POWER_SAVING = REFUTED_SCOPED
TPC215_FINITE_RATIOS = NUMERICAL_OBSERVATION
TPC215_DIRECT_SUM_ARITHMETIC_ENERGY_BOUND = OPEN
TPC215_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC215_PRIME_SHELL_REASSEMBLY = OPEN
TPC215_ARITHMETIC_ADVANCE = NO
TPC215_FIXED_ATOM_CREDIT = 0
TPC215_L2 = NONE
TPC215_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

## Project layout

```text
README.md
PAPER_PLAN.md
PROOF_PACKAGE.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/short_quotient_majorant.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/majorant_sanity.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-215-short-quotient-mobius-majorant/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-215-short-quotient-mobius-majorant/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-215-short-quotient-mobius-majorant/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-215-short-quotient-mobius-majorant/experiments/majorant_sanity.py --check
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_short_quotient_mobius_majorant_checker.py --check
```

The finite fixture uses exact rational emitter rows with
`Q={11,13,17}`, `H=40`, `Y0=2`, `U=35`, and
`psi(t)=(1+t^2)^(-2)`.  Decimal energy and tail ratios remain
`NUMERICAL_OBSERVATION`; they are not theorem evidence.

Author: Liang Wang, Huazhong University of Science and Technology.
