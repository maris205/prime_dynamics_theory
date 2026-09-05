# TPC-401: C1 diagonal-deletion decomposition

TPC-401 isolates an exact finite identity behind the TPC-400 production panel.
For `N=1024`, `Q=8192`, and primes `Q<p<=2Q`, every off-diagonal difference
has size below `p`.  Thus the divisibility indicator vanishes off diagonal and

```text
K_p = -a_p (D_p T D_p - D_p),
a_p = p(p/Q)^2/(p-1),  T_uv = H^2/(H^2+(u-v)^2).
```

The producer checks 104640 prime/component rows over six origins and five
sampled positions, with exact `Fraction` arithmetic, and all rows agree with
the decomposition.  The exact anchor deliberately records the boundary
counterexample `N=13,Q=8,p=11,u-v=-11`: the simplification is not valid there.

This is `PROVED_EXACT_FINITE` structural evidence.  It does not provide a
source sign law, arithmetic `L2`, a growing estimate, fixed-power credit, a
Route-B closure, or a twin-prime result.  The next clue audits the signed
diagonal-deletion contribution rather than repeating another affine family.

## Contents

The project contains `README.md`, `paper/`, `code/`, `experiments/`,
`results/`, and `notes/`, with `paper/paper.pdf` as the reproducible manuscript.

```bash
python -B papers/tpc-401-c1-diagonal-deletion-decomposition/code/tpc401_c1_diagonal_deletion_decomposition.py --check
python -B papers/tpc-401-c1-diagonal-deletion-decomposition/experiments/tpc401_independent_checker.py --check
python -B papers/tpc-401-c1-diagonal-deletion-decomposition/experiments/tpc401_adversarial_certificate_stress.py --check
```

## Claim firewall

```text
TPC401_ANALYTIC_STRUCTURE = PROVED_EXACT_FINITE
TPC401_NUMERICAL_CERTIFICATION = NONE_NEEDED
TPC401_ARITHMETIC_ADVANCE = NO
TPC401_FIXED_POWER_CREDIT = 0
TPC401_SOURCE_UNIFORM_L2 = OPEN
TPC401_FULL_GATE_B = OPEN
TPC401_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_DIAGONAL_DELETION_SIGNED_TERM_AUDIT
```
