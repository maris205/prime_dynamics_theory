# Bridge B V92: Brun--Titchmarsh primitive-bucket envelope

Date: 2026-08-24

Status: `PROVED_SOURCE_BACKED_PRIME_DENSITY_L1 / LOGARITHMIC_ONLY`.

TPC-239 follows the obstruction isolated by TPC-238: after cross-frequency
signs are ruled out as a source of a uniform fixed-power saving, move the
arithmetic input inside one literal primitive prime-shell bucket.  A direct
Brun--Titchmarsh count improves the TPC-237 collision factor by
`log x / loglog x`.  The fixed-power exponent is unchanged.

## Registry and claim firewall

```text
TPC239_MAXIMUM_CLAIM = SOURCE_BACKED_PRIME_DENSITY_L1_LOGARITHMIC_IMPROVEMENT
TPC239_ROUTE_ADVANCE = YES_LOGARITHMIC_ONLY
TPC239_PRIMITIVE_AP_REDUCTION = PROVED_EXACT_UPPER_COMPILER
TPC239_BRUN_TITCHMARSH_INPUT = SOURCE_BACKED
TPC239_BUCKET_MULTIPLICITY = PROVED_LE_16_Q_SQUARED_OVER_H_TIMES_H_OVER_PHI_H_OVER_LOG_2Q_OVER_H
TPC239_V59_BUCKET_MULTIPLICITY = PROVED_X_1_OVER_96_LOGLOG_X_OVER_LOG_X
TPC239_FINITE_WINDOW_PACKET_TRACE = PROVED_X_1_OVER_48_LOG_FOUR_LOGLOG
TPC239_UNNORMALIZED_FIXED_POWER_EXPONENT = PROVED_49_OVER_48
TPC239_IMPROVEMENT_OVER_TPC237 = PROVED_FACTOR_LOG_X_OVER_LOGLOG_X
TPC239_FIXED_POWER_IMPROVEMENT = NONE
TPC239_C_H_SIGNED_CANCELLATION = NONE
TPC239_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC239_ARITHMETIC_ADVANCE = NO
TPC239_FIXED_ATOM_CREDIT = 0
TPC239_L2 = NONE
TPC239_FULL_GATE_B = OPEN
TPC239_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC239_STATUS = PROVED_SOURCE_BACKED_PRIME_DENSITY_L1
TPC239_ROUND2_CLUE = TEST_THE_EXACT_TOP_BAND_C_H_BEFORE_SEEKING_FURTHER_UNIFORM_BUCKET_SAVINGS
```

Here `ARITHMETIC_ADVANCE = NO` uses the program's strict meaning: no signed
arithmetic `L2` estimate on the physical four-packet scalar has been proved.
Brun--Titchmarsh is a genuine arithmetic theorem, but here it supplies only a
coefficient-blind `L1` prime-density input.

## 1. Frozen common-source object

Keep the V59 scales and the TPC-237 kernel:

```text
H=x^(21/32),  Q=x^(1/3),  U=x^(133/400),
Q_x={q prime: Q<q<=2Q},
D_x={d: H/(4Q)<d<=U, mu(d)^2=1},
C_h=sum_(d in D_x,h|d) mu(d)log(d)/d,

B_(h,q)^(j)(a)
 = sum_(0<|m|<=floor(hq/H))
     psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h),

K_j(n)
 = sum_(h<=U) sum_((a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h).
```

The outer `q` weight is one.  The profile family is fixed and finite, with
`M=max_j ||psi_j||_infty`.  No sign, profile value, cutoff, or packet label is
changed.

For a primitive residue `a mod h`, let

```text
R_h(a)=#{q in Q_x: a belongs to the support of B_(h,q)^(j)},
M_h=floor(2hQ/H),
M_h^x={m in Z: 0<|m|<=M_h, (m,h)=1}.
```

The support incidence is independent of `j`; a profile may delete an
amplitude, but never creates an additional row.

## 2. Primitive residue to prime progression

Assume first `h>=2`.  Since `h<=U<Q<q`, every shell prime is a unit modulo
`h`.  If row `q` reaches primitive bucket `a`, its multiplier satisfies

```text
m q^(-1) = a (mod h),
q = a^(-1)m (mod h),
(m,h)=1.
```

TPC-236 internal row injectivity shows that one fixed `q` contributes at most
one multiplier to one bucket.  Dropping only the `q`-dependent cutoff
`|m|<=floor(hq/H)` and retaining the global bound `|m|<=M_h` gives

```text
R_h(a)
 <= sum_(m in M_h^x)
      [pi(2Q;h,a^(-1)m)-pi(Q;h,a^(-1)m)].            (2.1)
```

Every displayed residue class is reduced.  Formula (2.1) is an upper
compiler, not an identity: the same shell prime may be counted for more than
one global multiplier after the physical cutoff is dropped.

For `h<2Q`, the standard Brun--Titchmarsh theorem gives, uniformly in every
reduced class `b mod h`,

```text
pi(2Q;h,b)
 <= 4Q/[phi(h) log(2Q/h)].                            (2.2)
```

Moreover,

```text
#M_h^x <= 2M_h <= 4hQ/H.                              (2.3)
```

Combining (2.1)--(2.3) proves

```text
R_h(a)
 <= 16 (Q^2/H) (h/phi(h))/log(2Q/h).                 (2.4)
```

The case `h=1` is empty because `floor(q/H)=0` when `q<=2Q<H`.

## 3. V59 logarithmic saving

The exact scale separation is

```text
Q/U=x^(1/1200).
```

Therefore, uniformly for `h<=U`,

```text
log(2Q/h) >= log(2Q/U)
            = (1/1200)log x+log 2.
```

The standard maximal-order estimate
`h/phi(h) << loglog(3h)` then turns (2.4) into

```text
max_(h<=U,(a,h)=1) R_h(a)
 << (Q^2/H) loglog x/log x
 = x^(1/96) loglog x/log x.                           (3.1)
```

This is smaller by `log x/loglog x` than the coefficient-blind fixed-power
collision envelope used in TPC-237.  It supplies no new negative power of
`x`.

## 4. Transfer through the TPC-237 composition

Coordinatewise Cauchy with (3.1) gives

```text
sum_(h,a,j) |C_h|^2 |sum_q B_(h,q)^(j)(a)|^2
 << x^(1/96) loglog x/log x
    sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2.             (4.1)
```

TPC-237 proves on the same common-source object

```text
sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2
 << J M^2 x^(1/96)(log x)^5.                          (4.2)
```

Distinct primitive fractions have circular spacing at least `U^(-2)`, so the
same reduced-frequency large sieve on a consecutive interval `I` of `N`
integers yields

```text
sum_(n in I) sum_j |K_j(n)|^2
 << (N-1+U^2) J M^2 x^(1/48)(log x)^4 loglog x.       (4.3)
```

For `I=I_x=(x/2,x] intersect Z`, `N` is comparable to `x` and
`U^2/N=x^(-67/200+o(1))`.  Hence

```text
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
 << J M^2 x^(1/48)(log x)^4 loglog x.                 (4.4)
```

The leading unnormalized fixed-power exponent remains `49/48+o(1)`.

## 5. Scope boundary and next theorem

The theorem counts prime rows one residue class at a time and then uses
Cauchy--Schwarz.  It neither uses the signs of `C_h` nor the signed
four-packet polarization.  The maximal-order bound on `h/phi(h)` is also a
uniform worst-case envelope.  Thus (4.4) is a source-backed logarithmic
improvement, not an arithmetic `L2` promotion and not evidence that exponent
`1/48` is sharp.

The next minimal question is whether the literal divisor coefficient itself
can provide a uniform saving in the active top denominator band.  That must be
tested before another abstract bucket optimization is attempted.

```text
STRONGEST_POSITIVE_RESULT = FINITE_WINDOW_COMMON_SOURCE_PACKET_TRACE_AT_X_1_OVER_48_LOG_FOUR_LOGLOG
STRONGEST_OBSTRUCTION = PRIME_DENSITY_SAVES_ONLY_A_LOGARITHM_AND_LEAVES_THE_FIXED_POWER_1_OVER_48
OPEN_THEOREM = LITERAL_WEIGHTED_OR_SIGNED_WITHIN_BUCKET_CANCELLATION_BEYOND_COEFFICIENT_BLIND_PRIME_COUNTING
REUSABLE_STRUCTURE = PRIMITIVE_RESIDUE_TO_REDUCED_PRIME_AP_COMPILER
ROUND2_CLUE = TEST_THE_EXACT_TOP_BAND_C_H_BEFORE_SEEKING_FURTHER_UNIFORM_BUCKET_SAVINGS
```

No fixed-atom credit, signed `C_h` cancellation, arithmetic `L2`, strict
`1/400` payment, full Gate B, or twin-prime theorem is claimed.
