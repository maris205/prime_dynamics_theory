# RH-382: Two-scale prime-square tail expansion

RH-382 proves a second-order expansion of the RH-381 square-clock gap. Its
scope is unchanged: `q` is fixed before `N -> infinity`, the phasewise
lag-two tables are universally distance-two-safe, and `c11(r)=0` at every
phase. It is not an unrestricted-memory or adaptive-clock theorem.

Let

```text
a_(j+1) = 1/(p_(j+1)^2-1),
T_y     = sum_(j>=y) a_(j+1),
S_y     = sum_(j>=y) a_(j+1)^2,
u_m     = e_m/e_1,
e_m     = product_(p odd) (1-m/p^2),
```

and define

```text
X_infinity = 2u_4-4u_5+6u_6-8u_7+10u_8,
Y_infinity = 6u_4-16u_5+30u_6-48u_7+70u_8,
m_infinity = 2u_3-4u_4+6u_5-8u_6+10u_7-12u_8.
```

For every `y>=1`, the paper proves

```text
B_infinity-G(q_y)
 = 2X_infinity*T_y/pi^2
   +(Y_infinity+2m_infinity)*T_y^2/pi^2
   +(Y_infinity-2m_infinity)*S_y/pi^2
   +R_y,

abs(R_y) <= 3301*T_y^3/(6*pi^2) < 551*T_y^3/pi^2.
```

The stronger explicit ledger is

```text
X channel      931/2
memory channel 254/3
total          3301/6 = 550+1/6 < 551.
```

## Proof ingredients

For the exact finite ratio `U_m^(j)=E_m^(j)/E_1^(j)`, write

```text
P_(m,j) = u_m/U_m^(j)
        = product_(k>=j) (1-(m-1)a_(k+1)).
```

Bonferroni and inverse-product inequalities imply

```text
0 <= U_m^(j)-u_m-(m-1)u_m*T_j
   <= U_m^(j)(m-1)^2*T_j^2
   <= (9-m)(m-1)^2*T_j^2/8.
```

The resulting numerator constant is `931/4`. The memory Euler form gives
`abs(M_j/A_j-m_infinity)<=63T_j`. The exact normalized `H` loss differs
from `T_(j+1)` by at most `T_(j+1)^2/2`. Two quadratic tail identities
produce `T_y^2+S_y` and `T_y^2-S_y`, while cube telescopes bound the memory
error by `254/3`.

The terminal run is always

```text
R_8^(j) = P_j E_8^(j).
```

Second differences are used only for `1<=ell<=7`. The memory derivation
contains `E_9`, which is exactly zero because the `p=3` factor is `1-9/9`.
No `E_10` is constructed or used.

## Exact artifact

The standard-library certificate uses exact `Fraction` arithmetic. It
contains:

- 24 finite product-expansion rows;
- four Bonferroni rows, four quadratic/cubic telescope rows, and four finite
  endpoint gap rows;
- the exact `931/4`, `63`, `931/2`, `254/3`, and `3301/6` ledgers;
- a terminal `R8/E9/no-E10` ledger;
- a reproduction-only `p=71` mutation that changes only the memory
  `-2mS` term to `+2mS` while leaving `+YS` unchanged.

For that one-tail mutation, the exact rational residual ratios have decimal
displays

```text
correct sign  0.042746686479386  PASS
wrong sign    7.335622869337969  FAIL.
```

The difference is exactly `4mS`. These finite rows reproduce and attack the
formulas; they do not prove the all-`y` theorem by fitting.

Exactly 33 immutable predecessor inputs are locked: 7 from RH-374, 8 each
from RH-379, RH-380, and RH-381, and 2 from RH-MVP2. Every live file must be
byte-identical to its declared release blob. The aggregate source digest is

```text
7b62b7e77ad313a52a07851e700aff197c2cc4bc3d910c6a464cd3cec0b55cb6
```

The result and its recursively closed Draft 2020-12 schema fully
regenerate. Duplicate keys, non-finite JSON, numeric-type aliases, unsafe
paths, duplicate membership, release rebinding, source drift, and semantic
PDF drift fail closed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make schema
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

## Boundaries

RH-382 does not use a prime number theorem, rewrite the result on a `p_y`
scale, introduce `q(N)`, cover active nonzero `c11`, prove adaptive-capacity
convergence, or infer a geometrically selected measure or deterministic
strong-space Ulam theorem. It constructs no intrinsic operator,
determinant, prime-power trace identity, zero model, Hilbert--Polya operator,
or proof of RH. Gates A--E remain false/open.
