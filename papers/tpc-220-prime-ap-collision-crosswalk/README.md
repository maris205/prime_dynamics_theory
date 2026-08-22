# TPC-220: Prime-AP Collision Crosswalk for the Literal Shell

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / EXACT_PRIME_AP_MULTIPLICATIVE_CROSSWALK`

TPC-219 将改善 `P` collapse 精确化为 q-transverse energy。TPC-220 把该 transverse
quantity 重新接回 literal rows。对

```text
B_(h,q)^(j)(a)
 = sum_m psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h)
```

以及 primitive residue `a`, unit condition gives the exact identity

```text
sum_q lambda_q B_(h,q)^(j)(a)
 = sum_(m != 0) Pi_(h,m)^(j)(a^(-1)m; lambda),
```

where `Pi_(h,m)` is a weighted prime-AP sum over
`q = a^(-1)m (mod h)` with the original cutoff and profile weight retained.

The corresponding row Gram has the exact collision form

```text
Gamma_h(q,q')
 = sum_(m,m') w_(m,q) conjugate(w_(m',q'))
     1_(m q' = m' q mod h),
```

with primitive `m,m'`. For `q=q'`, TPC-218 injectivity reduces this to the diagonal
`sum_m |w_(m,q)|^2`; for `q!=q'`, the remaining multiplicative congruence is the precise
new arithmetic interface.

## Claim firewall

```text
TPC220_ROUTE_ADVANCE = YES
TPC220_PRIME_AP_CROSSWALK = PROVED_EXACT
TPC220_MULTIPLICATIVE_COLLISION_GRAM = PROVED_EXACT
TPC220_DIAGONAL_REDUCTION = PROVED_EXACT
TPC220_ARITHMETIC_ADVANCE = NO
TPC220_FIXED_ATOM_CREDIT = 0
TPC220_L2 = NONE
TPC220_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC220_FULL_GATE_B = OPEN
TPC220_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC220_STATUS = PROVED_STRUCTURAL_L1
TPC220_ROUND2_CLUE = QUANTIFY_THE_OFF_DIAGONAL_COLLISION_GRAPH_BEYOND_SCHUR
```

The finite certificate checks exact rational equality for constant and affine profiles;
it is not a PNT or asymptotic AP estimate.

## Layout

```text
paper/paper.pdf
paper/main.tex
code/prime_ap_crosswalk.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/collision_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
