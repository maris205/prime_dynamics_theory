# RH-383: exact Euler-tail partition normal form

RH-383 proves an exact all-order power-sum expansion of the square-clock gap
inside the unchanged RH-379 class: each clock `q` is fixed before
`N -> infinity`, the phasewise lag-two tables are universally
distance-two-safe, and `c11(r)=0` at every phase. It is not an
unrestricted-memory, growing-clock, or adaptive-capacity theorem.

For

```text
a_(j+1) = 1/(p_(j+1)^2-1),
P_r(y)  = sum_(j>=y) a_(j+1)^r,
Phi_c(y)= sum_(r>=1) c^r P_r(y)/r,
```

the exact ratios are

```text
U_m^(y)=u_m exp(Phi_(m-1)(y)),
H_y=(4/pi^2)exp(-Phi_1(y)).
```

With

```text
C(V)=1-2V2+2V3-2V4+2V5-2V6+2V7-2V8,
W(V)=V2-2V3+2V4-2V5+2V6-2V7+2V8,
```

the paper proves

```text
pi^2(B_infinity-G(q_y))
 =2(C(u)-C(U^(y)))-4W(U^(y))(1-exp(-Phi_1(y))).
```

For a partition `lambda=1^k1...d^kd`, define

```text
P_lambda=product_r P_r^k_r,
z_lambda=product_r r^k_r*k_r!,
alpha=(-2,2,-2,2,-2,2,-2),
beta=(1,-2,2,-2,2,-2,2),
```

where `alpha,beta` are indexed by `m=2,...,8`. Then

```text
pi^2(B_infinity-G(q_y))
 =sum_(d>=1) sum_(lambda partition d) gamma_lambda P_lambda(y),

gamma_lambda
 =-(2/z_lambda)sum_(m=2)^8 alpha_m*u_m*(m-1)^d
  -(4/z_lambda)sum_(m=2)^8 beta_m*u_m*
    ((m-1)^d-product_r((m-1)^r-1)^k_r).
```

The series is absolutely convergent. The `m=2` contribution cancels
exactly for every nonempty partition. The loss coefficient uses
`(-1)^(length(lambda)+1)`, not total-degree parity.

## Low orders and arbitrary-order tail

Let

```text
X = 2u4-4u5+6u6-8u7+10u8,
Y = 6u4-16u5+30u6-48u7+70u8,
m = 2u3-4u4+6u5-8u6+10u7-12u8.
```

The first layers are

```text
gamma_(1)   = 2X,
gamma_(1,1) = Y+2m,
gamma_(2)   = Y-2m.
```

Thus the RH-381 and RH-382 coefficient layers are recovered exactly,
including the independent `P_2(y)` memory sign. The new cubic block is
printed in `main.tex` and
frozen in the exact certificate.

For `rho_y=7P_1(y)<=7/8` and every exact integer `D>=1`, the remainder in
`B_infinity-G(q_y)` after total degree `D` satisfies

```text
abs(R_(D,y)) <= 92*rho_y^(D+1)/(3*pi^2)
             < 31*rho_y^(D+1)/pi^2.
```

The proof uses the original increment arrays

```text
XI =(2,-4,6,-8,10),       m=4,...,8,
ETA=(2,-4,6,-8,10,-12),  m=3,...,8.
```

Their absolute ledgers are `35/4` and `14`, leading to homogeneous bounds
`5/2` and `4/3`, then geometric tail costs `20` and `32/3`. These constants
belong only to `XI/ETA`; they are not sums of the endpoint arrays
`alpha/beta`. The general bound does not inherit RH-381's `342` or
RH-382's `3301/6` special-purpose constants.

## Exact artifact

The standard-library core compares three independent oracles:

1. endpoint `C/W` canonical partition coefficients;
2. ordered increment `Gamma/h/e/Phi` coefficients, using the strict
   successor tail `j+1`;
3. direct `A_c/F_c` telescope coefficients and finite gaps.

The frozen grid is:

| Check | Rows |
|---|---:|
| endpoint normal form | 67 |
| `A/F` coefficients | 864 |
| `Q` length-sign oracle | 432 |
| gamma equivalence | 1084 |
| increment-channel equivalence | 144 |
| low-order recovery | 33 |
| cubic direct + labeled symbolic | 67 + 12 |
| `m=2` cancellation | 1151 |
| arbitrary-order remainder | 804 |
| terminal + successor-tail | 4 + 7 |
| rejected real mutations | 20/20 |

The label redundancy is explicit:

- `432 = 72` unique tail/degree `Q` identities repeated under six inert
  `c` labels;
- `1084 = 271` unique symbolic partitions through degree 12 under four
  endpoint labels;
- `1151 = 4*271 + 67`, namely the labeled symbolic `m=2` rows plus 67
  direct finite telescopes.
- `33` low-order rows are endpoint-labeled bundles of the same three
  symbolic coefficient identities, not 33 different theorems.

These are exact reproduction and adversarial rows, not that many distinct
theorems and not finite evidence for the infinite result.

The certificate has `12245` canonical bytes and SHA-256

```text
9e2742fcdb2f626909eeb528c5081c9ace5414a1e6466c15b8b6800f427b6f16
```

Exactly 41 immutable predecessor files are locked in groups
`7/8/8/8/8/2`; mutable root `AGENTS.md` and `RH_HANDOFF.md` are excluded.
Every live input must equal its declared release blob. The aggregate digest
is

```text
492100fe3b6b823a39b58cec25b0dcddf6d52c02bd1941f0978611f01a2b8db9
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make schema
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

## Boundaries

Route A is `GO`; Route B is `STOP_SCOPED`. RH-383 uses no prime number
theorem or `p_y` rewrite, introduces no `q(N)`, does not cover active
nonzero `c11`, and does not prove the RH-377 adaptive envelope or capacity
limit. It constructs no intrinsic operator, determinant, scattering
completion, self-adjoint generator, von Mangoldt weighted prime-power
trace, completed-zeta divisor equality, Riemann-zero identification,
Hilbert--Polya object, or proof of RH. Gates A--E remain false/open.
