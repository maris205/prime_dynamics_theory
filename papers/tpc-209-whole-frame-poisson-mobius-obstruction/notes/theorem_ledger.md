# Theorem ledger

## PROVED

`T209.1` — For a Schwartz component (F_D) and ((D,q)=1), Poisson gives

```text
sum_m F_D(m)e_q(-kDm)
 = sum_(n = kD mod q) Fhat_D(n/q).
```

The map (n=qr+kD) is a bijection from (k\ne0,r\in\mathbb Z) to
(q\nmid n).

`T209.2` — The complete edge frame applied to a divisor sum is exactly

```text
E_q(Y,Z) = <P_q sum_D c_D U_D B_D,
             P_q sum_E d_E U_E C_E>.
```

`T209.3` — Multiplicative Fourier diagonalizes (U_D), giving the shared
character profile expression

```text
sum_(chi != chi_0)
 (sum_D c_D chi(D) M B_D(chi))
 conjugate(sum_E d_E chi(E) M C_E(chi)).
```

`T209.4` — For a physical additive Fourier vector, the nonprincipal
multiplicative coordinate is the explicit Gauss factor times the V59
nonprincipal Dirichlet transform.

`T209.5` — The vector map

```text
L_c((B_D)) = P_q sum_D c_D U_D B_D
```

has exact operator norm (|c|_2), and the bound is attained by aligned
profiles.

`T209.6` — In the common-profile model, (q=5,D=2,3,c_2=c_3=-1) has a
quadratic-character multiplier (2), equal to the coefficient (ell^1)
mass.

## REFUTED_SCOPED

`T209.R1` — Poisson plus complete-frame algebra does not imply a single scalar
dual packet independent of (D).

`T209.R2` — Literal Möbius signs do not, by themselves, force nonprincipal
character cancellation.

## NUMERICALLY_CERTIFIED

The Gaussian Poisson experiment reports errors below (10^{-12}) for three
test configurations.  This validates implementation only.

## STOP_SCOPED

`T209.S1` — No frame-only power saving or direct Blomer--Pascadi attachment is
claimed.  A profile-aware theorem on the actual packets remains open.

## OPEN

Carry the exact (q-2) diagonal subtraction, prime-only shell, kernel
localization, four-packet signs, and physical block reassembly through the
shared-character profile expression.

## Status registry

```text
CLAIM_LEVEL = PROVED_STRUCTURAL_L1_STOP_SCOPED_FRAME_ONLY_SAVING
TPC209_ROUTE_ADVANCE = YES
TPC209_STRUCTURAL_THRESHOLD_A = PASS
TPC209_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC209_ARITHMETIC_ADVANCE = NO
TPC209_FIXED_ATOM_CREDIT = 0
TPC209_L2 = NONE
TPC209_TPC_TRIGGER = true
```
