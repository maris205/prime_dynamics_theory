# Bridge B V20: terminal innovation floor and the end of the automatic-smoothing bypass

This unnumbered big-road artifact audits the route selected after V19.  It is
not TPC-207, a paper, an arithmetic estimate, or a dynamical proof of the twin
prime conjecture.  Its purpose is to decide whether the canonical source
innovation

```text
eta_p(V)=(I-alpha_p^(-1)R_pR_p^*)V
```

is a genuinely smaller object than the combined raw MASTER residual.  The
answer is **no at the terminal physical stage**.  In the no-wrap regime the
last innovation retains essentially the whole physical state and the whole
signed raw-row evaluation.  An affine/path-space carrier is exact and useful
for typing, but it is an isometric re-coordinatization, not a source of
cancellation.

## 1. Decision first

The V20 verdict is

```text
TERMINAL_SOURCE_INNOVATION_FIBER_FORMULA
  = PROVED_EXACT,

TERMINAL_NO_WRAP_INNOVATION_NORM_FLOOR
  = PROVED_EXACT_RATIO_(p-3)/(p-2),

TERMINAL_INNOVATION_RAW_EVALUATION
  = ORIGINAL_COMBINED_RAW_TARGET
    + O_K(x^(1/2+o(1))),

GROWING_HORIZON_DUHAMEL_WEIGHTS
  = PROVED_EXACT_NONNEGATIVE_PARTITION_OF_ONE,

ABSTRACT_AFFINE_PATH_SPACE
  = PROVED_EXACT_WEIGHTED_ISOMETRIC_RECOORDINATIZATION,

INNOVATION_AS_AUTOMATIC_SMALL_ERROR_OR_TELESCOPING_SAVING
  = STOP_SCOPED_TERMINAL_NEAR_IDENTITY,

COMBINED_RAW_MASTER_SIGNED_PHYSICAL_SAVING
  = OPEN_NEW_ARITHMETIC_THEOREM.
```

Thus V19 did identify the correct missing source port, but the port does not
soften the arithmetic wall.  A dynamical carrier can only succeed by proving
the same signed physical estimate in a new representation; it cannot receive
credit merely for encoding the innovations.

## 2. Frozen physical object and exact fiber projection

The object is unchanged from V19:

```text
h0=2,
x=2X,
z=(log x)^K,

w_x^(z)(t)=Lambda(t+2)-b_x^(z)(t),

beta_x^raw(t)
 =1_(x/2<t<=x)
  sum_(MASTER occurrences o over t)
   c_(j(o)) product_i mu(e_i(o)) log(f_1(o))/log t,

c_1=+2, c_2=-1.                                      (2.1)
```

All source slots, unit multiplicities, MASTER routing, Möbius signs, physical
shells and the `log(f_1)/log t` normalization remain literal.

Fix a parent modulus `P` and a new odd prime `p` with `gcd(P,p)=1`.  On the
fiber over `r mod P`, put

```text
q_(r,j)=r+jP,
m_(r,j)=1_(p does not divide q_(r,j)(q_(r,j)+2)),

S_r={j:m_(r,j)=1},
D_r={j:m_(r,j)=0}.                                    (2.2)
```

There are `p-2` survivors and two deleted copies.  With normalized Haar
inner products,

```text
(R_p^*V)(r)=p^(-1)sum_(j in S_r)V(q_(r,j)),
alpha_p=(p-2)/p,

(Pi_pV)(q_(r,j))
 =m_(r,j)/(p-2) sum_(ell in S_r)V(q_(r,ell)).          (2.3)
```

Writing

```text
Vbar_r=(p-2)^(-1)sum_(ell in S_r)V(q_(r,ell)),
```

gives the exact innovation formula

```text
eta_p(V)(q_(r,j))
 =V(q_(r,j)),                 j in D_r,
 =V(q_(r,j))-Vbar_r,          j in S_r.               (2.4)
```

The deleted values are retained, not damped.  On survivors the operation is
fiber centering, not a small scalar perturbation.

## 3. Exact physical evaluation formula

Let the algebraic raw covector be

```text
L_beta(V)=sum_(q mod pP)beta(q)V(q).
```

Define the survivor mean `betabar_r` in the same way as `Vbar_r`.  Direct
expansion of (2.4) gives

```text
L_beta(eta_p(V))
 =sum_r [
    sum_(j in D_r)beta(q_(r,j))V(q_(r,j))
   +sum_(j in S_r)
      (beta(q_(r,j))-betabar_r)
      (V(q_(r,j))-Vbar_r)
  ].                                                   (3.1)
```

Equivalently,

```text
L_beta(eta_p(V))
 =sum_r [
    sum_(j in D_r)beta_jV_j
   +sum_(j in S_r)beta_jV_j
   -(p-2)^(-1)(sum_(j in S_r)beta_j)(sum_(j in S_r)V_j)
  ].                                                   (3.2)
```

There is no missing Haar scalar.  The normalized-Haar Riesz vector is
`pP conjugate(beta)`, so its inner product with `eta_p(V)` is exactly (3.1).
Neither complete-frequency Parseval nor an averaged covariance can replace
this prescribed physical scalar.

## 4. Terminal no-wrap floor

Let the terminal prime clock satisfy

```text
p_s^2<=x+2<p_(s+1)^2,
p=p_s,
P=P_(s-1).                                            (4.1)
```

For every sufficiently large terminal stage, V19 proved

```text
P_(s-1)>p_(s+1)^2>x.                                  (4.2)
```

Hence the physical shell occupies at most one child in each parent fiber.
For a shell-supported state `V`, (2.4) now yields the exact identity

```text
||eta_p(V)||_(pP)^2
 =1/(pP) [
    sum_(t deleted)|V(t)|^2
   +(p-3)/(p-2) sum_(t survivor)|V(t)|^2
  ].                                                   (4.3)
```

Consequently

```text
||eta_p(V)||_(pP)^2
 >=(p-3)/(p-2)||V||_(pP)^2.                           (4.4)
```

The support also expands rather than shrinks:

```text
#supp(eta_p(V))
 =#deleted active coordinates
  +(p-2)#surviving active coordinates.                (4.5)
```

Since `p asymp sqrt(x)`, the lower-bound ratio in (4.4) tends to one.  Ambient
Haar dilution from increasing `pP` is not an arithmetic saving and cannot be
used to pay the physical coordinate-sum normalization.

## 5. Near-identity of the actual combined raw evaluation

Periodize both `beta_x^raw` and `w_x^(z)` at the terminal modulus.  Condition
(4.2) makes this an ordinary no-wrap embedding, so (3.2) becomes

```text
L_(beta_x^raw)(eta_p(w_x^(z)))
 =S_x
  -(p-2)^(-1)
    sum_(x/2<t<=x, p does not divide t(t+2))
      beta_x^raw(t)w_x^(z)(t),                        (5.1)

S_x=sum_(x/2<t<=x)beta_x^raw(t)w_x^(z)(t).
```

The two source-locked HB2 types give the elementary pointwise bound

```text
|beta_x^raw(t)|<=2d_2(t)+d_4(t)<=3d_4(t).             (5.2)
```

The committed hybrid residual bound and fixed divisor moments give

```text
sum_t |beta_x^raw(t)w_x^(z)(t)|<<_K x log^C(x).       (5.3)
```

Bertrand's postulate applied to (4.1) gives `p>sqrt(x+2)/2`.  Therefore

```text
L_(beta_x^raw)(eta_p(w_x^(z)))
 =S_x+O_K(x^(1/2)log^C(x)).                           (5.4)
```

For every fixed `A,K`, the error in (5.4) is smaller than
`x/log^A(x)`.  Thus

```text
L_(beta_x^raw)(eta_p(w_x^(z)))<<_(A,K)x/log^A(x)

if and only if

S_x<<_(A,K)x/log^A(x).                                (5.5)
```

This equivalence is only for the V19 combined physical raw MASTER row.  It
does not materialize the missing separated `Xi,Kappa` registry or its
transform tails.

## 6. The growing-horizon telescope has nonnegative weights

Assume a no-wrap prime horizon `a<s<=b`, as occurs for fixed `K>1` and
`z=(log x)^K` once `x` is sufficiently large.  Put

```text
q_s(t)
 =1_(p_s does not divide t(t+2))/(p_s-2).             (6.1)
```

Backward pseudoinverse recursion and algebraic dual pullback give a base term
with weight

```text
omega_base(t)=product_(a<u<=b)q_u(t),                 (6.2)
```

and the stage-`s` innovation weight

```text
omega_s(t)
 =[1-q_s(t)]product_(s<u<=b)q_u(t).                  (6.3)
```

For every physical coordinate,

```text
omega_base(t)+sum_(a<s<=b)omega_s(t)=1,
omega_base(t)>=0,
omega_s(t)>=0.                                        (6.4)
```

If the terminal coordinate is deleted, `omega_b=1`.  If it survives,

```text
omega_b=(p_b-3)/(p_b-2),
omega_base+sum_(s<b)omega_s=1/(p_b-2).                (6.5)
```

The Duhamel expansion is therefore an exact partition of the original
scalar, not an alternating or cancellative telescope.  Arithmetic signs in
different coordinates may still cancel, but a new theorem must prove that
cancellation; stage bookkeeping does not create it.

## 7. Exact affine/path state: useful typing, no compression

Let

```text
E_s=ker(R_(s-1)^*)=ran(R_(s-1))^perp.
```

For a fixed terminal state `W_b`, recursively define

```text
W_(s-1)=R_(s-1)^dagger W_s,
eta_s=(I-Pi_s)W_s in E_s.                             (7.1)
```

Then

```text
W_b
 =R_(b:a)W_a+sum_(a<s<=b)R_(b:s)eta_s.               (7.2)
```

The summands are pairwise orthogonal.  With
`alpha_(b:s)=product_(s<u<=b)alpha_u`,

```text
||W_b||_b^2
 =alpha_(b:a)||W_a||_a^2
  +sum_(a<s<=b)alpha_(b:s)||eta_s||_s^2.              (7.3)
```

Thus the weighted synthesis map from

```text
V_a direct_sum E_(a+1) direct_sum ... direct_sum E_b
```

onto `V_b` is an exact isometry.  It has the full dimension

```text
dim V_a+sum_(a<s<=b)(dim V_s-dim V_(s-1))
 =dim V_b=P_b.                                        (7.4)
```

For a fixed terminal covector, the dual Duhamel sum telescopes only to its
endpoint evaluation.  Cauchy--Schwarz in this path norm reproduces the
original source norm and gives no new logarithmic factor.

A legal physical quotient at a declared horizon must annihilate only the
intersection of kernels of the complete backward physical hull.  It cannot
delete the whole innovation space.  The actual V19 row at `x=168,t=90` has

```text
beta_168^raw(90)=2,

L_(beta_168)((I-Pi_13)e_90)=20/11.                    (7.5)
```

Hence an actual physical row detects a canonical innovation direction.

## 8. Two exact coherence/rank falsifiers

Changing-scale raw rows are not one pullback orbit.  At

```text
x=166, t=84:
  beta_166^raw(84)=1,
  84 survives p=13,

x=168:
  84 is excluded by the strict shell (84,168].        (8.1)
```

Therefore

```text
beta_166^raw != R_13^vee beta_168^raw.                (8.2)
```

No cross-scale coboundary identity may be inferred from the single-terminal
Duhamel telescope.

The V19 `k=5,b=7` source rows give a second exact falsifier after their common
nonzero prime-log column scalars are removed:

| family | rows | exact rank |
|---|---:|---:|
| raw source rows | 120 | 65 |
| base components | 120 | 56 |
| terminal eta components | 96 | 50 |
| all eta components | 132 | 54 |
| all eta plus all base components | 252 | 76 |

There are 110 raw source coordinates and 3984 exact nonzero row-coordinate
partitions.  The component union expands from raw rank 65 to rank 76; it does
not collapse automatically.  These finite ranks are a falsifier, not an
all-horizon asymptotic theorem.

## 9. The scoped stop and the only honest surviving theorem

V20 adds the broad cell

```text
DECLARED_TPC_BRIDGE_B_20260807_SHBD2_LONG_HORIZON_SOURCE_INNOVATION_
SMALL_NORM_AUTOMATIC_TELESCOPE_OR_LOW_RANK_BYPASS_V1
  = STOP_SCOPED_EXACT_TERMINAL_NEAR_IDENTITY.          (9.1)
```

It stops only the claim that canonical innovations automatically produce a
small norm, a stagewise cancellation, a low-rank family, or an independently
easier dynamical error.  It does not stop an enlarged source state, a
noncoercive physical quotient, a genuine signed dynamical theorem, the
separated analytic proof, or the independent A1/A2 routes.

The surviving Bridge B theorem is

```text
BRIDGE_B_SHBD2_TERMINAL_INNOVATION_SIGNED_PHYSICAL_EVALUATION
  = OPEN_NEW_ARITHMETIC_THEOREM.                      (9.2)
```

It must directly prove

```text
sup_(actual source-locked raw MASTER rows)
|sum_(x/2<t<=x)
  beta_x^raw(t)
  [Lambda(t+2)-b_x^((log x)^K)(t)]|
 <<_(A,K)x/log^A(x),                                  (9.3)
```

or the equivalent terminal-innovation form.  It must retain fixed physical
`h0=2`, `x=2X`, all ordered coefficients and masks, uniform `A,K`, the
separated-transform/reassembly ledger, and strict endpoint losses.

An actual Logistic or symbolic carrier would additionally need a common
all-horizon physical quotient, target-independent affine input maps, an exact
stage/event coding, and deterministic return of (9.3).  Positive measure,
a.e. genericity, complete-frequency mean square, or an abstract direct-sum
coding does not meet this contract.

## 10. Claim firewall

The checker freezes the exact fiber formulas, norm floor, nonnegative
partition, path isometry, two raw-row witnesses and the rank table.  The
maximum claim is

```text
EXACT_L0_TERMINAL_INNOVATION_EQUIVALENCE_AND_BYPASS_STOP.
```

In particular,

```text
SEPARATED_SHB_D2_TEMPLATE_REGISTRY = ABSENT,
SIGNED_TERMINAL_INNOVATION_SAVING = OPEN,
LOGISTIC_AFFINE_RETURN = OPEN,
ARITHMETIC_ADVANCE = NO,
FIXED_ATOM_CREDIT = 0,
STRICT_1_OVER_400 = UNPAID,
L2 = NONE,
TPC_207_TRIGGER = false.                              (10.1)
```

The frozen proof/checker pair is

```text
research/tpc-big-road/bridge_b_terminal_innovation_floor.md
research/tpc-big-road/tpc_bridge_b_terminal_innovation_checker.py
```

The checker registry has 37 exact rows and final-LF SHA-256

```text
0408cb3e4fd0bbfb7815df0df24902d4cc9fa1b75875e66f41482c30768652ee.
```

A release run must reject all 19 contract mutations and all 39 registry
mutations under both normal and optimized Python.  The checker is a finite
identity/falsifier certificate; it is not evidence for (9.3).

No numbered paper, PDF, build artifact or TPC-207 is created by this gate.
