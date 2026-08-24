# TPC-240: A Top-Prime Direct-Energy Floor for the Frozen Common Profile

Author: Liang Wang, Huazhong University of Science and Technology, Wuhan 430074,
P.R. China; `liang.wang@hust.edu.cn`.

Status: `PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR`

TPC-240 evaluates one exact source-backed factor left open by the preceding
finite-window papers.  Keep

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
```

and fix a real profile `psi` in `C_c^infty(R)` with
`0<=psi<=1`, support in `[-1,1]`, and integral one.  For top-shell primes
`U/2<p<=U` and shell primes `Q<q<=2Q`, define

```text
B^psi_(p,q)(a)
 = sum_(0<|m|<=floor(pq/H))
     psi(Hm/(pq)) 1_(m q^(-1)=a mod p),
C_p=-log(p)/p.
```

The exact q-split unsigned direct residue-row energy is

```text
D_top^psi
 = sum_(U/2<p<=U) |C_p|^2
     sum_(Q<q<=2Q) sum_((a,p)=1) |B^psi_(p,q)(a)|^2.
```

Writing `kappa_psi=int_{-1}^1 psi(t)^2 dt`, the main theorem proves, for
every fixed admissible profile,

```text
1/2 <= kappa_psi <= 1,
D_top^psi
 = [1197*kappa_psi*log(2)/800 + o_psi(1)] Q^2/H
 = x^(1/96+o_psi(1)).
```

The quantifier is profilewise: for every fixed `psi` and every `epsilon>0`,
there is `x_0(psi,epsilon)`.  No class-uniform threshold is claimed.  The
aggregate lattice error is relatively
`O_psi(H/(UQ))=O_psi(x^(-23/2400))`.

This result is a matching floor for the exact unsigned q-split direct factor.
It rules out `o(Q^2/H)` and every fixed-power saving for that factor.  It is
not the q-collapsed coefficient energy, the signed `C_h` scalar, or the signed
four-packet Gate-B object.  The optional finite-window corollary only gives
`(1/2-o(1))D_top^psi`, hence still has exponent `1/96`; it does not prove the
`1/48` collision exponent sharp.

## Reproduction

From this project directory:

```bash
python -B code/tpc240_top_prime_energy_certificate.py --check
python -O -B code/tpc240_top_prime_energy_certificate.py --check
python -B experiments/tpc240_independent_checker.py --check
python -O -B experiments/tpc240_independent_checker.py --check
python -B experiments/tpc240_profile_stress.py --check
python -O -B experiments/tpc240_profile_stress.py --check
```

The producer and independent checker use strict runtime guards, canonical JSON,
and exact `Fraction` ledgers.  The stress program tests fixed-row injectivity,
row-energy equality, and lattice Riemann convergence for two legitimate
nonnegative smooth bump shapes.  Those finite calculations are labeled
`NUMERICAL_FINITE_ILLUSTRATION_ONLY` and are not theorem evidence.

The compiled manuscript is `paper/paper.pdf`.

## Route extraction

- Strongest positive result: the exact leading constant and the
  `x^(1/96)` direct-energy floor.
- Strongest obstruction: no `o(Q^2/H)` or fixed-power saving can hold for this
  unsigned q-split factor.
- Open theorem: determine the top-prime q-collapsed collision energy and whether
  it contributes another `x^(1/96)` factor; signed `C_h` and four-packet
  cancellation remain open.
- Reusable structure: fixed-q signed-interval injectivity, endpoint-safe lattice
  Riemann summation, and factorized weighted-prime averaging.
- `ROUND2_CLUE`:
  `TEST_THE_TOP_PRIME_Q_COLLAPSED_COLLISION_EXCESS_OVER_THE_EXACT_DIRECT_FLOOR_BEFORE_CLAIMING_X_1_OVER_48_SHARPNESS`.
