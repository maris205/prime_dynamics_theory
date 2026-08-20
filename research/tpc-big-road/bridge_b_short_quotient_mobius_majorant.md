# Bridge B / Gate B TPC-215: short-quotient Möbius tails and the no-power-loss cluster majorant

Date: 2026-08-20

Status: `PROVED_STRUCTURAL_L1 / SHORT_QUOTIENT_CLUSTER_MAJORANT`.

TPC-214 proved that the complete-period common-source Gram is controlled by
the reduced-denominator coefficients

```text
C_h = sum_(d in D, h|d) mu(d)log(d)/d.
```

TPC-215 answers its literal next question on the V46 transition band: how long
is this tail for an emitter row that can actually occur, and how large can the
cluster energy be relative to the divisor direct-sum energy?

## Registry and claim firewall

```text
TPC215_MAXIMUM_CLAIM = SOURCE_LOCKED_SHORT_QUOTIENT_MOBIUS_TAIL_NORMAL_FORM_AND_O_LOG_X_SQUARED_COMPLETE_PERIOD_CLUSTER_TO_DIRECT_MAJORANT_WITH_TOP_SHELL_NO_SAVING_OBSTRUCTION
TPC215_ROUTE_ADVANCE = YES
TPC215_STRUCTURAL_THRESHOLD_A = PASS
TPC215_ACTIVATION_FLOOR = PROVED_EXACT
TPC215_ACTIVE_DENOMINATOR_IN_FULL_BAND = PROVED_EXACT
TPC215_SHORT_QUOTIENT_NORMAL_FORM = PROVED_EXACT
TPC215_QUOTIENT_LENGTH_EXPONENT = PROVED_23_OVER_2400
TPC215_ROW_NORM_DIVISOR_DECOMPOSITION = PROVED_EXACT
TPC215_CLUSTER_TO_DIRECT_MAJORANT = PROVED_O_LOG_X_SQUARED
TPC215_FIXED_POWER_CLUSTER_AMPLIFICATION = EXCLUDED
TPC215_TOP_SHELL_RATIO_ONE = PROVED_EXACT
TPC215_UNIFORM_ROWWISE_POWER_SAVING = REFUTED_SCOPED
TPC215_FINITE_RATIOS = NUMERICAL_OBSERVATION
TPC215_DIRECT_SUM_ARITHMETIC_ENERGY_BOUND = OPEN
TPC215_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC215_PRIME_SHELL_REASSEMBLY = OPEN
TPC215_ARITHMETIC_ADVANCE = NO
TPC215_FIXED_ATOM_CREDIT = 0
TPC215_L2 = NONE
TPC215_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC215_TPC_TRIGGER = true
```

The result is an asymptotic structural comparison.  It rules out fixed-power
amplification by reduced-frequency clustering, but does not prove a saving,
bound the direct-sum arithmetic energy, or close any arithmetic `L2` gate.

## 1. Literal V46 source lock

Keep the exact V46 scales

```text
H = x^(21/32),       Q = x^(1/3),
Y0 = H/(4Q) = x^(31/96+o(1)),
U = x^(133/400),     Q < q <= 2Q.
```

Let

```text
D_x = {d in Z : Y0<d<=U, mu(d)^2=1},
c_d = mu(d)log(d)/d.
```

The source records `d<U<Q<q`; every `q` is therefore a unit modulo every
active divisor.  Strip the coefficient from the literal reciprocal occupancy:

```text
B_d(r) = sum_(q in Q-shell) sum_(0<|m|<=dq/H)
         psi(Hm/(dq)) 1_(m q^(-1)=r mod d).
```

All cutoffs are integer cutoffs.  TPC-214 proves

```text
B_d((d/h)a)=B_h(a),  h|d,
```

and on `L=lcm(D_x)` it proves

```text
E_cluster
 = sum_(u mod L)|sum_d c_d sum_r B_d(r)e(ru/d)|^2
 = L sum_h |C_h|^2 N_h,

C_h = sum_(d in D_x,h|d)c_d,
N_h = sum_(a mod h,(a,h)=1)|B_h(a)|^2.
```

The full squarefree band matters.  An arbitrary subfamily need not contain
`d=h` and is outside the diagonal-anchor theorem below.

## 2. The activation floor

### Theorem: activation floor

If `B_h` is nonzero, then

```text
h >= H/q_max >= H/(2Q) = 2Y0,
q_max = max(Q-shell).
```

Indeed, a nonzero row contains a summand with a nonzero integer `m`.  For its
prime `q`,

```text
1 <= |m| <= hq/H <= hq_max/H.
```

The stated inequality follows.  If this `h` occurs as a reduced denominator,
then `h|d` for a squarefree `d in D_x`; hence `h` is squarefree and `h<=U`.
The lower bound gives `h>Y0`, so `h` itself belongs to `D_x`.

This last conclusion is the key diagonal anchor.  It is not obtained merely
from `h|d`; it uses the literal emitter cutoff and the full V46 band together.

## 3. Exact short-quotient normal form

For active `h`, write every multiple as `d=hk`.  Since `d` is squarefree,
`(h,k)=1` and `mu(hk)=mu(h)mu(k)`.  Therefore

```text
C_h = mu(h)/h
      sum_(Y0/h<k<=U/h, (k,h)=1)
      mu(k)(log h+log k)/k.
```

The `k=1` term is present because `h in D_x`.  Every quotient satisfies

```text
k <= U/h <= Uq_max/H <= 2UQ/H.
```

The exponent is exact:

```text
133/400 + 1/3 - 21/32 = 23/2400.
```

Thus

```text
k <= 2x^(23/2400+o(1)).
```

The original divisor band has width on the scale `x^(133/400)`, but every row
that can emit sees only this very short quotient band.

## 4. Coefficient majorant

Define the direct coefficient mass above `h` by

```text
D_h = sum_(d in D_x,h|d)|c_d|^2.
```

Because `d=h` occurs,

```text
D_h >= (log h/h)^2.
```

The triangle inequality, with `d=hk`, gives

```text
|C_h|
 <= sum_(k<=U/h) log(hk)/(hk)
 <= (log U/h) Harmonic(floor(U/h)).
```

Consequently

```text
|C_h|^2
 <= [log U/log h]^2 Harmonic(floor(U/h))^2 D_h.
```

For every active row, monotonicity and the activation floor yield the uniform
factor

```text
A_x = [log U/log(H/q_max)]^2
      Harmonic(floor(Uq_max/H))^2,

|C_h|^2 <= A_x D_h.
```

Since `q_max<=2Q`,

```text
A_x
 <= [log U/log(H/(2Q))]^2
    Harmonic(floor(2UQ/H))^2
 = O((log x)^2)
 = x^(o(1)).
```

No cancellation in `mu(k)` is used.  The conclusion is therefore
deterministic and unconditional after the source lock.

## 5. Exact row-norm decomposition

### Theorem: row-norm divisor decomposition

For every `d in D_x`,

```text
sum_(r mod d)|B_d(r)|^2 = sum_(h|d)N_h.
```

Every residue `r mod d` determines a unique reduced fraction
`r/d=a/h`, where `h|d` and `(a,h)=1`.  Its representative is
`r=(d/h)a`.  TPC-214 dilation covariance gives

```text
B_d(r)=B_h(a).
```

The reduced-denominator classes form a disjoint partition of the entire
residue row, proving the identity.  The `h=1` class is the additive zero axis;
it vanishes in the source range because `q_max<H`.

## 6. Complete-period no-power-loss theorem

### Theorem: cluster-to-direct majorant

Let

```text
E_direct = L sum_(d in D_x)|c_d|^2
             sum_(r mod d)|B_d(r)|^2.
```

Then

```text
E_cluster <= A_x E_direct,
A_x = O((log x)^2)=x^(o(1)).
```

Indeed,

```text
E_cluster/L
 = sum_h N_h|C_h|^2
 <= A_x sum_h N_hD_h
  = A_x sum_d |c_d|^2 sum_(h|d)N_h
  = A_x E_direct/L.
```

The middle equality is a finite rearrangement of nonnegative terms, and the
last equality is the row-norm divisor decomposition.

This proves that reduced-frequency collisions introduce no fixed power of
`x` beyond the direct-sum row energy.  It does not estimate that direct-sum
energy and is not called an arithmetic saving.

## 7. Sharp scoped obstruction

### Proposition: top-shell ratio one

If an active denominator satisfies

```text
U/2 < h <= U,
```

then

```text
C_h=c_h,       D_h=|c_h|^2,
|C_h|^2/D_h=1.
```

Any distinct multiple of `h` is at least `2h>U`, so `d=h` is the only band
multiple.  Therefore cluster algebra alone cannot produce a uniform rowwise
fixed-power saving.  This obstruction is deliberately scoped: a global
physical-interval saving could still arise from the arithmetic row norms,
off-frequency interactions, prime-shell averaging, or signed four-packet
reassembly.

## 8. Finite release fixture

The executable fixture freezes

```text
Q = {11,13,17},  H=40,  Y0=2,  U=35,
psi(t)=(1+t^2)^(-2),
D = squarefree d in (Y0,U] coprime to Q.
```

The activation floor is `ceil(40/17)=3`.  Every nonzero reduced row lies in
the band; dilation covariance and the row decomposition hold exactly over
rational emitter rows.  Every active `h>17.5` has exact top-shell ratio one.
The recorded tail and whole-energy ratios use real logarithms and are labeled
`NUMERICAL_OBSERVATION`.

The independent checker reconstructs the fixture without importing the
producer module.  The sanity checker also tests the harmonic bound,
full-band requirement, and top-shell equality across several source-shaped
finite configurations.

## 9. Route-B evaluation

The strongest positive result is the explicit
`O((log x)^2)=x^(o(1))` complete-period cluster/direct comparison.  The
strongest obstruction is exact top-shell ratio one.  The next genuine theorem
must control the direct-sum physical row energy, after which finite-window
off-frequency and prime-shell/four-packet reassembly still have to be paid.

```text
STRONGEST_POSITIVE_RESULT = SOURCE_LOCKED_COMPLETE_PERIOD_CLUSTER_GRAM_IS_AT_MOST_O_LOG_X_SQUARED_TIMES_DIVISOR_DIRECT_SUM_ENERGY
STRONGEST_OBSTRUCTION = EVERY_ACTIVE_TOP_SHELL_DENOMINATOR_HAS_EXACT_CLUSTER_TO_DIRECT_COEFFICIENT_RATIO_ONE
OPEN_THEOREM = PHYSICAL_INTERVAL_DIRECT_SUM_ROW_ENERGY_BOUND_WITH_FINITE_WINDOW_AND_PRIME_SHELL_REASSEMBLY
REUSABLE_STRUCTURE = ACTIVATION_FLOOR_PLUS_SHORT_QUOTIENT_TAIL_PLUS_DIAGONAL_ANCHOR_PLUS_ROW_NORM_DIVISOR_DECOMPOSITION
ROUND2_CLUE = BOUND_THE_DIRECT_SUM_PHYSICAL_ROW_ENERGY_BEFORE_REINTRODUCING_CROSS_FREQUENCIES
```

Route A is not applicable.  Route B passes structural threshold A, but
arithmetic `L2`, fixed-atom credit, full Gate B, strict `1/400`, and the
twin-prime endpoint remain unchanged.
