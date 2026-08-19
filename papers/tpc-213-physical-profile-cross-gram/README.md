# TPC-213: Physical Profile Pullback and the Cross-Divisor Gram

## Result

TPC-212 showed that the reciprocal emitter has a block-diagonal Gram only when
the divisor residuals are placed in a natural direct sum.  TPC-213 constructs
the missing physical map before Cauchy: a common sequence on a finite support
is lifted to every residue space, Fourier transformed, and paired with the
corresponding emitter.

For a finite support `U`, define

```text
(C_d f)(a) = sum_(u in U, u == a mod d) f(u)
K_d(u)     = sum_(r mod d) A_d(r) exp(2*pi*i*r*u/d)
```

The V46 residual pairing then has the exact pullback form

```text
sum_d sum_r A_d(r) Rhat_d(r)
 = sum_u v(u) K(u) - sum_d sum_u b_d(u) K_d(u),
K(u)=sum_d K_d(u),
```

where `v` is the common physical sequence and `b_d` is the divisor-dependent
Euler profile correction.  Thus the physical residuals cannot be replaced by
independent direct-sum vectors without changing the operator.

Two exact Gram identities make the coupling explicit.  On a complete period
`L=lcm(d,e)`, the residue lifts satisfy

```text
(C_d C_e^*)(a,b) = 1_(a == b mod gcd(d,e)),
```

and the emitter pullbacks satisfy

```text
sum_(u mod L) K_d(u) conjugate(K_e(u))
 = L sum_(r/d == s/e mod 1) A_d(r) conjugate(A_e(s)).
```

The finite fixture `d={5,7,35}`, `q={11,13,17}`, `H=40`, `U={0,...,34}`
has nonzero cross-Gram values `560` for `5,35` and `770` for `7,35`, while
`5,7` has no nonzero common frequency.  These are exact finite structural
certificates.  They do not prove a saving for the literal smooth V46 emitter.

## Claim firewall

```text
TPC213_ROUTE_ADVANCE = YES
TPC213_STRUCTURAL_THRESHOLD_A = PASS
TPC213_PHYSICAL_PROFILE_EMITTER_PULLBACK = PROVED_EXACT
TPC213_RESIDUE_LIFT_GCD_ALIASING = PROVED_EXACT
TPC213_CROSS_DIVISOR_FREQUENCY_GRAM = PROVED_EXACT_FINITE
TPC213_PHYSICAL_DIRECT_SUM_REPLACEMENT = REFUTED_SCOPED
TPC213_LITERAL_V46_ASYMPTOTIC_GRAM_BOUND = OPEN
TPC213_PRIME_SHELL_REASSEMBLY = OPEN
TPC213_ARITHMETIC_ADVANCE = NO
TPC213_FIXED_ATOM_CREDIT = 0
TPC213_L2 = NONE
TPC213_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

The scoped negative result says that the physical coupling map is nontrivial;
it does not say that the coupling is useless.  The next theorem must estimate
the joint pullback kernel with the smooth `psi`, the four-packet signs, the
zero-axis normalization, and the prime shell retained.

## Project layout

```text
README.md
PAPER_PLAN.md
PROOF_PACKAGE.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/profile_cross_gram.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/coupling_sanity.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-213-physical-profile-cross-gram/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-213-physical-profile-cross-gram/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-213-physical-profile-cross-gram/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-213-physical-profile-cross-gram/experiments/coupling_sanity.py
```

The certificate uses exact integer/rational arithmetic.  Its emitter geometry
uses unit reciprocal weights and omits the `log(d)` prefactor, explicitly as a
finite modeling choice.

Author: Liang Wang, Huazhong University of Science and Technology.
