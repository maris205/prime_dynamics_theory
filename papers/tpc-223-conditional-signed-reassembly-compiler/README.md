# TPC-223: Conditional Signed-Reassembly Compiler

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`CONDITIONAL_THEOREM / FULL_GATE_B_OPEN`

TPC-220 supplies the literal prime-AP/collision coordinate and TPC-222 supplies
the exact polarized four-packet interface.  TPC-223 makes their required joint
statement explicit.  If

```text
A_x << x^(E0-delta_AP+o(1))
P_x << x^(E0-kappa_pol+o(1))
S_x << x^lambda_struct (A_x+P_x)
```

then the exact compiled saving is

```text
sigma = min(delta_AP,kappa_pol) - lambda_struct.
```

The strict endpoint condition is `sigma > 1/400`.  The canonical exact ledger
uses `E0=5/3`, `delta_AP=1/100`, `kappa_pol=1/80`, and
`lambda_struct=1/1200`, giving effective saving `11/1200`, strict margin `1/150`,
and compiled exponent `663/400` below the target `1997/1200`.

This is a conditional compiler theorem, not a proof of the input estimates.
The certificate deliberately includes a borderline equality, failed and
zero-channel cases, and a loss-dominated case.  Arithmetic `L2`, fixed-atom
credit, strict Gate B, and the twin-prime endpoint remain open.

## Claim firewall

```text
TPC223_ROUTE_ADVANCE = YES
TPC223_TWO_CHANNEL_COMPILER = PROVED_CONDITIONAL_ALGEBRA
TPC223_AP_DISPERSION = OPEN_CONDITIONAL_INPUT
TPC223_POLARIZED_CROSS_CORRELATION = OPEN_CONDITIONAL_INPUT
TPC223_LITERAL_REASSEMBLY_INTERFACE = OPEN_CONDITIONAL_INPUT
TPC223_EFFECTIVE_SAVING = CERTIFIED_EXACT_MIN_MINUS_LOSS
TPC223_STRICT_1_OVER_400 = CONDITIONAL_ONLY
TPC223_ARITHMETIC_ADVANCE = NO
TPC223_FIXED_ATOM_CREDIT = 0
TPC223_L2 = NONE
TPC223_FULL_GATE_B = OPEN
TPC223_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC223_STATUS = CONDITIONAL_THEOREM
TPC223_ROUND2_CLUE = PROVE_OR_REFUTE_THE_COMMON_LITERAL_TWO_CHANNEL_INTERFACE
```

## Layout

```text
paper/paper.pdf
paper/main.tex
code/reassembly_compiler.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/borderline_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
