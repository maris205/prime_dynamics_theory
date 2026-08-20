# Bridge B / Gate B TPC-214: Möbius-weighted shared-frequency clusters

Date: 2026-08-20

Status: `PROVED_STRUCTURAL_L1 / MOBIUS_CLUSTER_REDUCTION`.

TPC-213 constructed the common physical pullback and identified the
frequency-intersection Gram.  TPC-214 restores the literal V46 coefficient and
answers the smallest next question: what is the exact object obtained when
divisors sharing a rational frequency are collected before the physical square
is taken?

## Registry and claim firewall

```text
TPC214_MAXIMUM_CLAIM = EXACT_MOBIUS_LOG_SHARED_FREQUENCY_CLUSTER_FACTORIZATION_WITH_ZERO_AXIS_AND_FOUR_PACKET_COMPATIBILITY
TPC214_ROUTE_ADVANCE = YES
TPC214_STRUCTURAL_THRESHOLD_A = PASS
TPC214_EMITTER_DILATION_COVARIANCE = PROVED_EXACT
TPC214_REDUCED_DENOMINATOR_CLUSTER_FACTOR = PROVED_EXACT
TPC214_ZERO_AXIS_SCOPE = PROVED_EXACT
TPC214_FOUR_PACKET_POLARIZATION = PROVED_EXACT_LINEAR_EXTENSION
TPC214_NESTED_CLUSTER_CANCELLATION = PROVED_EXACT_FINITE_SIGN
TPC214_COMPOSITE_QUOTIENT_ENHANCEMENT = PROVED_EXACT_FINITE_SIGN
TPC214_FINITE_ENERGY_RATIOS = NUMERICAL_OBSERVATION
TPC214_UNIVERSAL_CLUSTER_SAVING_SIGN = REFUTED_SCOPED
TPC214_LITERAL_V46_ASYMPTOTIC_CLUSTER_BOUND = OPEN
TPC214_PRIME_SHELL_REASSEMBLY = OPEN
TPC214_ARITHMETIC_ADVANCE = NO
TPC214_FIXED_ATOM_CREDIT = 0
TPC214_L2 = NONE
TPC214_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC214_TPC_TRIGGER = true
```

The release maximum is an exact finite structural theorem.  The two displayed
energy ratios are numerical evaluations of exact rational row data followed by
real logarithms; they are not asymptotic evidence.

## Literal emitter and dilation covariance

Let `D` be a finite squarefree divisor family, let `Q` be a finite set of
integers coprime to all active divisors, and let `H >= 1`.  For a function
`psi` define

```text
B_d(r) = sum_(q in Q) sum_(0 < |m| <= d q/H)
         psi(H m/(d q)) 1_(m q^(-1) = r mod d).
```

The cutoff is integer-valued (`floor(dq/H)`).  Keep the literal coefficient

```text
c_d = mu(d) log(d) / d.
```

### Theorem: dilation covariance

If `h | d` and `d = k h`, then for every `a mod h`,

```text
B_d(k a) = B_h(a).
```

Indeed, because `q` is a unit modulo `kh`, the congruence
`m q^(-1) = k a mod kh` forces `m = k n`.  The cutoff becomes
`|n| <= hq/H`, and `Hm/(dq) = Hn/(hq)`.  The summands therefore agree
term by term.  This proof uses the actual cutoff and does not replace it by a
continuous approximation.

## Reduced-denominator cluster factorization

Let `L = lcm(D)`, and let `h` range over all nonzero reduced denominators that
divide at least one active divisor.  Define the Möbius-log tail

```text
C_h = sum_(d in D, h | d) c_d.
```

The exact common-source kernel is

```text
K_d(u) = c_d sum_(r mod d) B_d(r) exp(2*pi*i*r*u/d),
K(u) = sum_(d in D) K_d(u).
```

### Theorem: reduced-denominator cluster factorization

On one complete physical period,

```text
sum_(u mod L) |K(u)|^2
 = L sum_(h) |C_h|^2
       sum_(a mod h, gcd(a,h)=1) |B_h(a)|^2.
```

For a frequency `a/h` in lowest terms, its representative in the `d`-row is
`(d/h)a`.  Dilation covariance makes every such row amplitude equal to
`B_h(a)`, so the coefficients add to `C_h` before squaring.  Complete-period
orthogonality removes distinct rational frequencies.  Equivalently, the
pairwise **frequency-intersection** Gram is exactly the expansion of this
cluster sum.  Every pair must be lifted to the common family period `L`; using
only `lcm(d,e)` in a family sum loses period multiplicity.

### Zero axis

If `max(Q) < H`, then `B_d(0)=0`: the zero residue would require `d | m`,
whereas the nonzero cutoff gives `|m| < d`.  This is a statement about the
additive reciprocal-emitter zero axis only.  It does not remove a multiplicative
principal character or a later Euler exception.

## Four-packet compatibility

For `a^(j)=beta+i^j w`,

```text
1/4 sum_(j=0)^3 i^j |beta + i^j w|^2 = beta conjugate(w).
```

Cluster formation is linear before the Hermitian square, so the same identity
holds cluster by cluster.  The resulting polarized scalar remains signed and
is not a positive energy theorem.

## Finite certificates and obstruction

The reproducible fixture is

```text
Q = {11, 13, 17},  H = 40,  psi(t) = (1+t^2)^(-2).
```

All row entries and primitive cluster norms are exact rationals.  The family
`{5,7,35}` has exact negative cross-energy sign and numerical
physical/direct-sum ratio `0.59634355565371822`.  The family
`{3,5,7,105}` has exact positive cross-energy sign and ratio
`1.2119952512624363`.  The first is a finite cancellation direction; the
second is a finite composite-quotient enhancement direction.  Together they
refute, at this scoped finite level, any universal favorable cluster-saving
sign based only on shared-frequency coupling.

The independent checker reconstructs the rational emitter rows without
importing the producer module.  Normal and optimized Python modes both pass,
and an exact Gaussian-rational check verifies the four-packet identity.

## Route-B evaluation and next theorem

The exact factorization identifies the correct arithmetic object: a
Möbius-log tail over multiples of each reduced denominator.  It does not bound
those tails uniformly in the V46 transition band `Y0 < d <= U`, does not
reassemble the prime shell, and does not attach a collective four-packet
prime-BDH theorem.  Therefore:

```text
STRONGEST_POSITIVE_RESULT = EXACT_REDUCED_DENOMINATOR_CLUSTER_FACTOR_OF_THE_COMMON_SOURCE_GRAM
STRONGEST_OBSTRUCTION = FINITE_COMPOSITE_QUOTIENT_ENHANCEMENT_REFUTES_UNIVERSAL_CLUSTER_SAVING_SIGN
OPEN_THEOREM = UNIFORM_LITERAL_V46_MOBIUS_LOG_CLUSTER_BOUND_WITH_PRIME_SHELL_REASSEMBLY
REUSABLE_STRUCTURE = DILATION_COVARIANCE_PLUS_REDUCED_FREQUENCY_CLUSTER_TAIL
ROUND2_CLUE = ESTIMATE_THE_MOBIUS_LOG_TAILS_C_h_BEFORE_ANY_PRIME_SHELL_OR_Q_TRIANGLE
```

Route A is not applicable to this analytic twin-prime session.  Route B gains a
structural threshold-A pass only; arithmetic `L2`, fixed-atom credit, the
strict `1/400` endpoint, and a twin-prime conclusion remain unpaid.
