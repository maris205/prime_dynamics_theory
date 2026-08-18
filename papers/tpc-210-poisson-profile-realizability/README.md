# TPC-210: Poisson Profile Realizability and the Mobius Alignment Obstruction

## Result

TPC-210 tests whether the Schwartz/Poisson admissibility conditions left in
TPC-209 already restrict the divisor-dependent dual profiles. They do not, at
finite modulus: every vector in `C^(F_q^*)` is exactly realizable as a residue
profile of a compactly supported smooth Fourier packet. The construction uses
isolated dual nodes `n_s/q` and a standard `C_c^infty` bump.

Putting the literal Mobius weights back into this realizable class gives an
exact aligned family. For squarefree unit divisors `D`, set

```text
c_D = mu(D),
B_D = mu(D) U_D^* z,
```

with a centered witness `z`. Then

```text
P sum_D c_D U_D B_D = (#D) z,
sum_D |c_D|^2 ||P U_D B_D||^2 = (#D) ||z||^2,
||P sum_D c_D U_D B_D||^2 = (#D)^2 ||z||^2.
```

The coherent-to-diagonal energy ratio is therefore exactly `#D`. This is a
genuine admissible Poisson-profile obstruction, stronger than an abstract
vector fixture, but it is still scoped: the independent profiles are not
claimed to be the literal coupled TPC physical coefficient family.

## Claim firewall

```text
TPC210_ROUTE_ADVANCE = YES
TPC210_STRUCTURAL_THRESHOLD_A = PASS
TPC210_FINITE_PROFILE_INTERPOLATION = PROVED_EXACT
TPC210_MOBIUS_WEIGHTED_ALIGNED_FAMILY = PROVED_EXACT
TPC210_CROSS_DIVISOR_GRAM_REDUCTION = PROVED_EXACT
TPC210_PROFILE_CLASS_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC210_ACTUAL_PHYSICAL_PROFILE_BOUND = OPEN
TPC210_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC210_ARITHMETIC_ADVANCE = NO
TPC210_FIXED_ATOM_CREDIT = 0
TPC210_L2 = NONE
TPC210_TPC_TRIGGER = true
```

The strongest reusable object is the cross-divisor Gram matrix

```text
G_(D,E) = <P U_D B_D, P U_E B_E>.
```

The remaining open theorem is a bound for this matrix on the literal physical
Möbius/Poisson packets, retaining the exact `(q-2)` diagonal, prime shell,
kernel localization, four-packet signs, and block reassembly.

## Project layout

```text
README.md
PAPER_PLAN.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/profile_realization.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/profile_interpolation_sanity.py
results/certificate.json
notes/theorem_ledger.md
notes/route_evaluation.md
notes/source_lock.md
```

## Reproduce

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-210-poisson-profile-realizability/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-210-poisson-profile-realizability/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-210-poisson-profile-realizability/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-210-poisson-profile-realizability/experiments/profile_interpolation_sanity.py
```

The finite certificate covers `q=3,5,7,11,13`, 20 exact divisor-profile rows
and 178 residue-coordinate rows, together with the Mobius-aligned Gram
matrices. These are finite QA checks, not asymptotic evidence.

Author: Liang Wang, Huazhong University of Science and Technology.
