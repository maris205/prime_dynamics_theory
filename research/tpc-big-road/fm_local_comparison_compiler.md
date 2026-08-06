# TPC big road: tensor-local Ford--Maynard redesign

Status:

```text
UNNUMBERED_WORKING_ARTIFACT
COARSE_COMPARISON_TYPE_I_ADVANCE_RETAINED
COARSE_COMPARISON_UNIVERSAL_TYPE_II_FALSE_LOCAL_RANK_ONE
TENSOR_LOCAL_HYBRID_COMPARISON_EXACT_LOCAL_PROFILE_CONSTRUCTED
HYBRID_COMPARISON_b1_w_AND_SUBHALF_TYPE_I_PROVED
HB4_QUARTER_COLLECTIVE_MAIN_PROVED_SOURCE_BACKED_ALL_D
HB4_QUARTER_OFFDIAGONAL_1_4_LT_DELTA_LT_3_8_PROVED_WEIL_PLUS_PASCADI
HB4_QUARTER_OFFDIAGONAL_1_4_LT_DELTA_LT_1_2_PROVED_CONDUCTOR_PROJECTOR
HB4_EXACT_HALF_ENDPOINT_OPEN_LOG_POWER_GATE
BP2607_FIXED_UNIT_LOCAL_ENGINE_ATTACHED_BUT_OUTER_SUM_INSUFFICIENT
BP2607_ARBITRARY_UNIT_VECTOR_LIFT_STOP_SCOPED_FALSE_CHARACTER_EIGENMODE
HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION_SELECTED_PRIMARY_OPEN
LARGE_D_HB2_SWITCH_PROVED_EXACT_ANALYTIC_HB4xHB2_GATE_OPEN
HB4xHB2_NAIVE_RESIDUE_COMPRESSION_STOP_SCOPED_KERNEL_NORM_Q
HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI_INDEPENDENT_OPEN
HB4xHB2_PAIRED_VORONOI_FIRST_TRANSFORM_DERIVED_SOURCE_BACKED
HB4xHB2_COLLECTIVE_POLAR_MAIN_ATTACHMENT_OPEN
DIRECT_DFI_ROW_BY_ROW_STOP_SCOPED_F7_VERSUS_F4
CURRENT_UMBRELLA_GATE = TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE
CURRENT_PRIMARY_ROUTE = HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION
CURRENT_INDEPENDENT_RESERVE = HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI
TPC_THEOREM = NO
TPC207_TRIGGER = false
```

This file is not a paper and is not TPC-207.  It turns the four channels in
`TPC_review3.md` into one literal prime-producing compiler.  The point is not
to rename an old `STOP_SCOPED` cell.  The point is to remove every local and
one-sided obstruction first, and then adversarially test the resulting formula
on the existing physical exponents `J=133/400` and `Q=267/400`.  That test
found a fatal rank-one residue mode for the first comparison.  The artifact
therefore retains the valid Type-I advance, closes that comparison's direct
route, and constructs the exact local profile required by the replacement.

The prime-producing source is Ford--Maynard,
[*On the theory of prime-producing sieves*](https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf),
arXiv:2407.14368.  The maximal one-sided input below is the classical
Bombieri--Vinogradov theorem; primary references include
[Bombieri, *On the large sieve*](https://doi.org/10.1112/S0025579300005313)
and
[Vinogradov, *The density hypothesis for Dirichlet L-series*](https://www.mathnet.ru/eng/im3080).

## 1. Bold conclusion, after the rank-one correction

Put

```text
J = 133/400,
Q = 267/400 = 1-J,
nu = 67/400 = 1/2-J.
```

There is a nonnegative coarse comparison `b_x^(2)(n)` for the shifted-prime
sequence `a_x(n)=Lambda(n+2)` such that:

1. all multiplier-slice main terms agree exactly, including every even
   multiplier;
2. the Ford--Maynard comparison hypotheses `(b.1)` and `(b.2)` hold;
3. maximal Type I holds throughout every fixed power range below `1/2`;
4. however, the universal Type II estimate on

   ```text
   (x/2)^J < m <= x^(1/2)
   ```

   is **false** for this comparison: fixed selectors
   `m=n=1 (mod 6)` expose a linear mod-3 discrepancy.

The `J -> sqrt(x) -> Q` exponent compiler remains exact, but it can only be
used after replacing the coarse comparison by a tensor-locally matched one.
For `z>=2`, Section 8 constructs

```text
b_x^(z)(n)
 = 1_(x/2<n<=x) C_(2,>z)
   product_(p<=z) [p/(p-1) 1_(p does not divide n+2)]
   product_(p|n,p>z) (p-1)/(p-2).
```

It satisfies `b_x^(2)=b_x`, preserves every multiplier-slice local mean, and
matches the full residue factor of `Lambda(n+2)` at every prime `p<=z`.
Taking `z=(log x)^K` therefore moves every fixed local tensor obstruction
below the requested logarithmic error scale.  Sections 8.3--8.4 close its
Ford--Maynard `(b.1)/(w)` package and maximal Type I for every fixed exponent
below `1/2`.  The high-conductor Type II estimate is the remaining analytic
proof gate; it is not claimed here.

If those replacement gates hold at

   ```text
   P_TPC = (gamma,theta,nu) = (1/2,133/400,67/400),
   ```

then Ford--Maynard yields infinitely many twin primes (indeed the expected
dyadic order and constant).

Thus the direct compiler is

```text
exact shifted-prime sequence
  -> tensor-local hybrid comparison b^(z), z=log^K(x)
  -> fundamental-lemma/BV comparison compiler               [proved]
  -> high-conductor arbitrary-coefficient Type II [J,1/2]
  -> Ford--Maynard Theorem 2.2
  -> weighted twin-prime asymptotic
  -> twin primes.
```

The first arrow is exact local algebra and the second is now a source-backed
classical compiler.  The final Type II is the genuine global wall.
Existing additive orbit covariance, Haar-a.e. recurrence, O161 special atoms,
packet Gram bounds, or complete-frequency means prove neither arrow.

## 2. Literal sequences and normalization

Let

```text
C2 = product over primes p>2 of (1-1/(p-1)^2).
```

For `x/2<n<=x`, define

```text
a_x(n) = Lambda(n+2),

b_x(n) = 2 C2 1_(2 does not divide n)
         product over p|n, p>2 of (p-1)/(p-2),

w_x(n) = a_x(n)-b_x(n).
```

All three sequences are zero outside `(x/2,x]`.  Both `a_x` and `b_x` are
nonnegative.  No change of prime index occurs: for prime `r` in the support,

```text
a_x(r)=Lambda(r+2).
```

Therefore the Ford--Maynard prime sum is precisely the shifted target,
apart from the explicitly negligible case in which `r+2` is a higher prime
power.

For `p>2`, the comparison has the local-factor form

```text
v_p = p(p-2)/(p-1)^2     if p does not divide n,
u_p = p/(p-1)            if p divides n.
```

At `p=2`, the factor is `2` on odd `n` and `0` on even `n`.  Consequently

```text
(1-1/p)v_p + (1/p)u_p = 1                  (p>2),
(1/2)2 + (1/2)0 = 1                        (p=2).
```

This is the reason the comparison is centered on every multiplier slice,
not merely on the unconditioned mean.

## 3. Exact multiplier-slice matching

Define the squarefree multiplicative function

```text
g(d) = product over p|d of 1/(p-2)          (d odd and squarefree).
```

The exact divisor expansion is

```text
b_x(n)=2 C2 1_(n odd) sum_(d|n, d odd) mu^2(d) g(d).
```

If `m` is even, then

```text
b_x(mr)=0.
```

If `m` is odd, put

```text
A(m)=product over p|m (p-1)/(p-2).
```

Then

```text
b_x(mr)
 = 2 C2 A(m) 1_(r odd)
   sum_(d|r, (d,2m)=1) mu^2(d) g(d).
```

For every integer interval `I` contained in the active quotient support
`{r in N:x/2<mr<=x}`, elementary counting of odd multiples gives

```text
sum_(r in I) b_x(mr)
 = (m/phi(m)) |I| + O(A(m) log^K(2+max I))       (m odd),
```

with one absolute fixed `K` (for example a nonoptimized `K=4` is enough).
The main constant is exact because

```text
C2 A(m)
 product_(p does not divide 2m) (1+1/(p(p-2)))
 = m/phi(m).
```

Indeed

```text
1+1/(p(p-2))=(p-1)^2/(p(p-2)),
```

which cancels the corresponding Euler factor in `C2`; a prime forced to
divide `m` leaves exactly `p/(p-1)`.

For the real sequence, the same slice has prime main term

```text
sum_(r in I) Lambda(mr+2)
       main = (m/phi(m)) |I|                    (m odd),
```

because `mr+2` is in the reduced residue class `2 mod m`.  When `m` is even,
`mr+2` is even, and only powers of two survive; their total contribution over
all relevant rows is `x^o(1)` and is absorbable in every fixed power margin.
Thus the old `b=1`, `m=2` fatal discrepancy is removed
exactly, and no fixed-`W` truncation leaves an unmodelled prime factor.

## 4. Ford--Maynard comparison regularity

### 4.1 `(b.1)`

For a prime `r` in `(x/2,x]`,

```text
b_x(r)=2 C2 (r-1)/(r-2)=2 C2+O(1/x).
```

The prime number theorem therefore gives

```text
sum_(x/2<r<=x, r prime) b_x(r)
  ~ C2 x/log x,
```

For any one fixed sufficiently large `varpi_0>1`, this implies the
Ford--Maynard lower bound `(b.1)`.  We use the same `varpi_0` large enough to
absorb the divisor moments in `(w)`; no claim is made at the sharp
normalization `varpi=1`, where the constant `C2<1` matters.

### 4.2 `(b.2)`

In Ford--Maynard `(b.2)`, every prime factor in the relevant vector region
satisfies `p_i >= n^nu`, and the number of factors is bounded in terms of
`nu`.  Uniformly on that domain,

```text
b_x(p_1...p_k)=2 C2(1+O_nu(x^(-nu))).
```

Repeated prime factors only reduce the number of distinct local factors and
do not spoil the bound.  Also `b_x(r)=2C2+O(1/x)` on the prime reference sum.
It follows that `(b.2)` is the constant-comparison generalized PNT, multiplied
by `2C2`, plus `o(x/log x)` uniformly over the prescribed convex `T` and
bounded Lipschitz `f`.  Ford--Maynard explicitly records that the constant
comparison satisfies `(b.1)` and `(b.2)`.  Hence this `b_x` satisfies both
comparison hypotheses.

### 4.3 Growth `(w)`

The elementary bounds

```text
b_x(n) << tau(n),
a_x(n) <= log(2x)
```

and standard fixed moments of the divisor function give

```text
sum_n |w_x(n)| tau(n) << x log^K x.
```

Moreover `w_x(n)>=-b_x(n)>=-x^(nu/10)` for sufficiently large `x`, since
`tau(n)=x^o(1)`.  Thus the Ford--Maynard growth hypothesis holds for a fixed
sufficiently large `varpi`.

## 5. Source-backed maximal Type I below one half

Fix `gamma<1/2`.  For every demanded log power, the maximal
Bombieri--Vinogradov theorem applies to moduli

```text
m <= x^gamma <= x^(1/2)/log^L x
```

for sufficiently large `x`.  For odd `m`, subtract the exact comparison
average from Section 3 from the arithmetic-progression formula for
`Lambda(mr+2)`.  For even `m`, both the comparison and all non-power-of-two
Mangoldt terms vanish.  This gives

```text
sum_(m<=x^gamma) tau(m)^B max_I
 | sum_(x/2<mr<=x, r in I) w_x(mr) |
 << x/log^B x.
```

The divisor weight does not require a stronger distribution theorem.  Split
the moduli according to whether `tau(m)^B<=log^L x`.  The first part is
absorbed by asking maximal Bombieri--Vinogradov for a larger log saving.  On
the complementary set, use the trivial row bound, Markov's inequality, and a
higher fixed moment of `tau`; choosing `L` and the moment large makes the
tail `O(x/log^B x)`.  Quantitatively, for any fixed auxiliary `R>0`,

```text
1_(tau(m)^B>log^L x) tau(m)^(B+1)
 <= tau(m)^(B+1+R)/log^(LR/B) x,
```

and the required harmonic fixed-divisor moment is polylogarithmic; first
choose `R`, then `L`.  The polylogarithmic comparison error sums to
`O(x^gamma log^K x)` and is smaller still.

Hence

```text
FM_COARSE_DIVISIBILITY_COMPARISON = CONSTRUCTED
FM_COARSE_COMPARISON_b1_b2_w_FOR_FIXED_VARPI0 = PROVED
FM_COARSE_MAXIMAL_TYPE_I_EVERY_FIXED_GAMMA_LT_1_2 = PROVED_SOURCE_BACKED
```

This is a genuine one-sided arithmetic interface advance.  It does not use
the dynamical recurrence theorem and does not claim Type II.  Section 7 shows
that it is not tensor-local enough for universal Type II.

## 6. Why the old `J/Q` exponents form the compiler

Take

```text
P_TPC=(gamma,theta,nu)=(1/2,133/400,67/400).
```

The parameter identities are

```text
theta+nu = 1/2,
1-theta-nu = 1/2,
1-theta = 267/400 = Q.
```

Ford--Maynard Proposition 4.11 says that Type II on `[theta,theta+nu]`
also supplies the complementary window `[1-theta-nu,1-theta]` and supplies
the corresponding maximal Type I rows (with one harmless log-power loss).
Thus Type II on

```text
[133/400,1/2]
```

automatically supplies its mirror (with the literal fixed endpoint factors)

```text
[1/2,267/400],

that is `x^(1/2)<=m<=(x/2)^Q`.  The notation `[1/2,Q]` records
exponents only; it does not discard the factor `2^(-Q)`.
```

It also fills the logarithmic top gap between classical
`sqrt(x)/log^L x` and exact `sqrt(x)`, so the literal Ford--Maynard Type I
hypothesis holds at `gamma=1/2`.

For Theorem 2.2, `M=floor(1/(1-gamma))=2`.  Condition `(A1)` holds because,
for every `n>=3`, there is an integer `a` with

```text
133/400 <= a/n <= 1/2;
```

the tight case is `n=3`, where `a/n=1/3` and

```text
1/3-133/400=1/1200>0.
```

Condition `(A2)` holds with `h=1`, since `1-gamma=1/2` is the upper endpoint
of the Type II interval.  Therefore Ford--Maynard Theorem 2.2 gives, for
every fixed `A`,

```text
sum_(x/2<r<=x, r prime) w_x(r) <<_A x/log^A x.
```

No numerical optimization of `C_minus` is needed: this parameter is in the
asymptotic region.

### 6.1 The strict `1/400` finally has a payment formula

There is a second, exponent-equivalent way to read the same mirrored window.
After the lower-half Type II interval is reflected, its full exponent span is

```text
[J,Q],  width Q-J=134/400.
```

The corresponding full-window parameter ledger is

```text
gamma_sharp = Q = 267/400,
theta_sharp = J = 133/400,
nu_sharp = Q-J = 134/400.
```

It has the exact surplus

```text
gamma_sharp+nu_sharp
  = 267/400+134/400
  = 401/400
  = 1+1/400.
```

Ford--Maynard records in its introduction that Type I and Type II give the
prime-weighted asymptotic directly by Vaughan's identity when
`gamma+nu>1`.  Thus the long-standing TPC `strict 1/400` is no longer an
unlocated loss: in this compiler it is exactly the surplus by which the
mirrored `J/Q` window crosses the Vaughan threshold.

This is a conditional loss ledger, not present proof credit.  Proposition
4.11 gives the literal complementary interval only up to the fixed endpoint
`(x/2)^Q`; invoking the full-window Vaughan shortcut also requires a finite
rescaling/reblocking argument for the constant-factor fringe up to `x^Q`.
Alternatively, the exact-half-window parameter avoids that presentation issue
once a valid Type II comparison is supplied.  Section 7 proves that the coarse
comparison does not supply one: its universal Type II claim is false before
the endpoint is reached.  The exponent identity remains a conditional compass,
and no physical packet has paid the `1/400` charge.

## 7. Fatal audit of the coarse comparison

The tempting statement was the following, for every fixed
log power `B` and all arbitrary complex coefficients satisfying
`|xi_m|<=tau(m)^B`, `|kappa_n|<=tau(n)^B`:

```text
TPC_J_TO_SQRT_UNIVERSAL_MULTIPLICATIVE_TYPE_II:

sup_(xi,kappa)
| sum_((x/2)^(133/400)<m<=x^(1/2), x/2<mn<=x)
    xi_m kappa_n
    [ Lambda(mn+2)
      - 2 C2 1_(mn odd)
        product_(p|mn,p>2) (p-1)/(p-2) ] |
  <<_B x/log^B x.
```

It is not merely open; it is false.  Put `M=x^(1/3)`, choose fixed short
constant-ratio intervals `M<m<(1+eta)M` and
`c_1 x/M<n<c_2 x/M` whose products all lie in `(x/2,x]`, and take

```text
xi_m    = 1_(m=1 mod 6) on the m interval,
kappa_n = 1_(n=1 mod 6) on the n interval.
```

For large `x`, the `m` interval lies inside the literal Type II range because
`J<1/3<1/2`.  There are `c_eta x+o(x)` selected pairs.  Every selected product
is odd and satisfies

```text
mn+2=0 mod 3.
```

Hence `Lambda(mn+2)` vanishes unless `mn+2=3^j`; the total exceptional
Mangoldt mass is `x^o(1)` by the divisor bound.  On the other hand,
`b_x(mn)>=2C2` for every selected pair.  The bilinear sum is therefore
`-c x+o(x)`, contradicting every logarithmic saving.

```text
DECLARED_COARSE_SINGULAR_SERIES_COMPARISON_UNIVERSAL_TYPE_II_
MOD3_RANK_ONE_V1 = STOP_SCOPED_FALSE
```

The failure has a precise type.  Multiplier-slice matching tests only the
conditional average after fixing `m`; arbitrary Type II coefficients can
simultaneously select residue classes of both `m` and `n`, and therefore see
the tensor mode `mn=-2 (mod p)`.  A viable comparison must match this full
local product-residue factor for every prime above the requested error scale.

The original target remains the correct contract against which a replacement
must be tested:

- it is multiplicative in the product `mn`, not additive in `n-m`;
- it is uniform over arbitrary divisor-bounded coefficients, not one selected
  packet coefficient;
- it retains the literal physical shift `+2`;
- its lower endpoint is the actual `J=133/400`;
- its upper endpoint is the exact square-root boundary, not
  `1/2-epsilon`;
- its complementary upper scale is the actual `Q=267/400`;
- it contains no averaged-phase, density-one, Parseval, or orbit-Poisson
  substitution.

Losing the upper endpoint by a fixed power is fatal for any replacement
compiler:
Ford--Maynard's `gamma=1/2` boundary is discontinuous for general unbounded
sequences.  Likewise moving the lower endpoint above `1/3` loses the `n=3`
case of `(A1)`.  The margins `J<1/3` and `Q>2/3` are therefore structural,
not cosmetic.

### 7.1 The coarse comparison is the projected Ramanujan major arc

Define the untruncated profile

```text
b^(2,circ)(n)=2C2 1_(n odd) product_(p|n,p>2)(p-1)/(p-2).
```

It is the standard pair singular series evaluated at the moving even shift
`2n`:

```text
b^(2,circ)(n)=S(2n),
b_x^(2)(n)=1_(x/2<n<=x)b^(2,circ)(n).
```

Equivalently, with the usual Euler/Ramanujan limiting convention,

```text
b^(2,circ)(n)
 = sum_(q>=1) mu(q)^2/phi(q)^2 c_q(2n),
```

where `c_q` is the Ramanujan sum.  This follows prime by prime from

```text
1+c_p(2n)/(p-1)^2
 = p/(p-1)                         if p divides 2n,
 = 1-1/(p-1)^2                     otherwise.
```

Thus the subtraction is not an ad hoc scalar centering, but it is only the
projection of the local prime condition onto the divisibility data of `n`.
The mod-3 witness shows that this projection is not the complete local model
for arbitrary factored tests.  A dispersion proof must first restore the
missing product-residue modes; the formal Ramanujan expansion alone is not
Type II.

### 7.2 The shifted prime has an exact determinant-two lift

The two equivalent elementary identities

```text
Lambda(N)= sum_(d r=N) mu(d) log r
         =-sum_(d|N) mu(d) log d
```

give the exact four-variable lift

```text
Lambda(mn+2)
 =  sum_(d r-m n=2) mu(d) log r
 = -sum_(d r-m n=2) mu(d) log d.
```

On the non-negligible odd sector, `m,n,d,r` are odd.  The equation forces
`gcd(d,m)|2`, hence `gcd(d,m)=1`.  For fixed coprime odd `(d,m)`, choose one
solution `(n_0,r_0)` of

```text
d r_0-m n_0=2.
```

All solutions are then

```text
n=n_0+d z,
r=r_0+m z,
```

and the affine determinant stays exactly

```text
d(r_0+mz)-m(n_0+dz)=2.
```

This is the first exact, source-forward explanation for why the abstract O161
geometry `s u-a d=2` is relevant to the FM wall: expanding the shifted
Mangoldt weight creates a primitive determinant-two affine family before any
`TT*` step.  More sharply, the first version has the literal core coefficient
`mu(d) log r` requested in the committed TPC-31 next-gate formula
`mu(d)(log ell) omega_D(d) psi_L(ell/L)`.  Thus, after the variable rename
`r=ell`, the shifted-prime lift and the TPC-31 prime--Mobius core agree
coefficientwise before the physical cutoffs and masks are installed.

It is not yet an O161 or TPC-31 theorem attachment.  The factors
`omega_D(d)`, `psi_L(r/L)`, the fixed residue factors, pair mask, three-channel
reassembly, and all physical weights are absent; the FM coefficients are
arbitrary, while the committed O161 corridors have their own two-Mobius
coefficient, scale restrictions, prefix normalization, and packet provenance.
A legitimate next proof must install those factors without changing the
product domain and derive any second Mobius factor through the outer-prime
Vaughan/Heath--Brown decomposition.  The determinant identity opens a typed
pre-`TT*` bridge; it does not cross it.

### 7.3 Source coverage stops at fixed Mobius plus two arbitrary rough coordinates

Substituting the exact lift into the universal Type II target produces the
prime part

```text
sum_(d r-m n=2) mu(d) (log r) xi_m kappa_n.
```

This exposes a later theorem-level obstruction after local tensor modes are
removed: one fixed rough Mobius coordinate `mu(d)` and two arbitrary rough
coordinates `xi_m,kappa_n`.  The checked primary-source landscape has
complementary but strictly weaker quantifiers:

* [Assing--Blomer--Li](https://arxiv.org/abs/2005.13915) and the BFI
  arithmetic-progression theorems cover fixed shifts and arbitrary
  logarithmic savings, but only unweighted, fixed-character, or
  well-factorable modulus structures;
* [Duke--Friedlander--Iwaniec](https://www.math.ucla.edu/~wdduke/preprints/bilinear.pdf)
  bilinear/Kuznetsov estimates allow two arbitrary coefficient sequences only
  after dispersion has produced a reciprocal-exponential kernel;
* the [Bettin--Chandee](https://arxiv.org/abs/1502.00769)
  fixed-determinant corollary provides two arbitrary-weight slots while its
  remaining coordinate weights are smooth;
* the [Friedlander--Iwaniec asymptotic sieve](https://arxiv.org/abs/math/9811186)
  assumes a dedicated Mobius bilinear axiom and therefore cannot be used to
  prove that axiom here.

Consequently no theorem in this bounded primary-source scan literally gives
the required product-domain norm for two arbitrary divisor-bounded
`xi,kappa`.  Once local tensor matching is installed, the next missing
statement is the fixed-Mobius-plus-two-arbitrary-rough determinant dispersion
bridge; uniformity through the closed endpoint `M=sqrt(x)` is a later gap.
This is a scoped source-lock verdict, not a global literature no-go theorem:
a fresh Vaughan/Heath--Brown plus dispersion proof may still exploit the
structured coefficient families actually emitted by the prime detector.

## 8. Tensor-local hybrid comparison

Let `z>=2` and set

```text
C_(2,>z)=product_(p>z) (1-1/(p-1)^2),

b^(z,circ)(n)
 = C_(2,>z)
   product_(p<=z) [p/(p-1) 1_(p does not divide n+2)]
   product_(p|n,p>z) (p-1)/(p-2),

b_x^(z)(n)=1_(x/2<n<=x)b^(z,circ)(n).
```

The prime `2` is included in the first product.  At `z=2` this reduces
exactly to the coarse comparison in Sections 2--7.

### 8.1 Exact local identities

For `p<=z`, the local factor as a function of `t=n mod p` is

```text
F_p(t)=p/(p-1) 1_(t!=-2 mod p).
```

For `p>z`, it is the projected factor

```text
G_p(t)=p/(p-1)                    if t=0,
       p(p-2)/(p-1)^2            otherwise.
```

Both have uniform mean one.  If a multiplier `m` is divisible by an odd
prime `p`, then `t=mr=0` and either factor equals `p/(p-1)`; if `p` does not
divide `m`, averaging over `r mod p` gives one.  At `p=2`, an even multiplier
gives zero and an odd multiplier gives the correct parity mean.  Therefore
the hybrid retains the exact multiplier-slice local constant

```text
m/phi(m)   for odd m,
0          for even m,
```

while additionally matching the full forbidden residue `mn=-2 mod p` for
every `p<=z`.  These are finite Euler identities, not a distribution theorem.

### 8.2 Why `z` must grow with the requested saving

For an unmodelled odd prime `p>z`, restrict to nonzero residues.  The difference
between the exact residue factor and the projected one is

```text
D_p(a,b)=p/(p-1)^2 [1-(p-1)1_(ab=-2 mod p)].
```

Its bilinear `l_infinity -> l_1` norm on `F_p^*` is comparable with `p`:
a nontrivial real character gives the lower bound `p`, while the row `l_1`
bound gives `O(p)`.  Since each residue cell in an `MN asymp x` box has size
`asymp x/p^2`, a single unmodelled local mode can contribute `asymp x/p`.
Thus a target `x/log^B x` requires at least

```text
z >= log^(B+O(1)) x.
```

This calculation explains why a fixed `W` cannot work and why the old
`z=2` comparison failed.  Taking `z=log^K x`, with `K` chosen after the
Ford--Maynard saving parameter, removes every fixed local selector at the
target scale.  It is necessary local preconditioning, not yet sufficient
high-conductor cancellation.

### 8.3 The replacement proof package

For one fixed large Ford--Maynard input exponent `B`, choose a still larger
fixed `K=K(B)` and `z=log^K x`.  The sequences in the Ford--Maynard class are
allowed to depend on `x` and on the fixed class parameters, so this dependence
does not itself violate the quantifiers.  The legal order is

```text
target A,varpi -> Ford--Maynard B -> fixed K=K(B) -> x>=x_0(A,varpi,B,K).
```

One fixed finite `K` is not an all-`B` object.  With that quantifier fixed, the
gate ledger is

```text
H0  hybrid finite Euler profile and old b=b^(2)       PROVED_EXACT
H1  hybrid (b.1), for each fixed K                    PROVED_FUNDAMENTAL_LEMMA_PLUS_BV
    hybrid (w), for each fixed K                      PROVED_ELEMENTARY
    hybrid (b.2) at P_TPC                             VACUOUS_PROVED_R(P_TPC)=EMPTY
H2  hybrid maximal Type I, every fixed gamma<1/2     PROVED_FUNDAMENTAL_LEMMA_PLUS_MAXIMAL_BV
    hybrid maximal Type I at gamma=1/2                NOT_PROVED_BY_BV
H3  hybrid universal Type II on [J,1/2]              OPEN_HIGH_CONDUCTOR_WALL
```

Here is the literal classical compiler.  Put

```text
W_z=product_(p<=z)p/(p-1).
```

Since

```text
0<=b_x^(z)(n)<=C W_z 2^omega(n)<=C(log z)tau(n),
```

fixed divisor moments give

```text
sum_n |Lambda(n+2)-b_x^(z)(n)|tau(n)<<_K x log^C x,
b_x^(z)(n)=x^o(1)<x^(nu/10).
```

Thus `(w)` holds for one fixed sufficiently large `varpi`.  On a prime index
`r` in the dyadic support,

```text
b_x^(z)(r)
 = C_(2,>z) W_z 1_((r+2,P_odd(z))=1) (r-1)/(r-2).
```

For squarefree odd `e|P(z)`, the prime row `r=-2 mod e` has density
`1/phi(e)`.  Apply Rosser--Iwaniec upper and lower fundamental-lemma weights
at any fixed positive power level and use Bombieri--Vinogradov for the total
prime-progression remainder.  Since

```text
s=log D/log z -> infinity
```

for fixed `K`, the sieve relative error beats every fixed log power, while

```text
C_(2,>z) W_z product_(3<=p<=z)(1-1/(p-1))=2C2.
```

Consequently

```text
sum_(x/2<r<=x, r prime)b_x^(z)(r)~C2 x/log x,
```

which proves `(b.1)`.  At the exact parameter `P_TPC`, `(A1)/(A2)` imply
`R(P_TPC)=empty`; Ford--Maynard `(b.2)` quantifies over subsets of
`C(R(P_TPC))`, so it is literally vacuous.

For maximal Type I, define

```text
g_z(d)=mu^2(d)1_(P^-(d)>z) product_(p|d)1/(p-2),
A_z(m)=product_(p|m,p>z)(p-1)/(p-2),
h_(m,z)(r)=sum_(d|r,(d,m)=1)g_z(d).
```

For odd `m` the exact slice identity is

```text
b_x^(z)(mr)
 =C_(2,>z)W_z A_z(m)h_(m,z)(r)
  1_((mr+2,P(z))=1)
```

inside the active support.  For squarefree `e|P(z)`, `(e,m)=1`, elementary
CRT counting gives, uniformly for every active interval `I`,

```text
sum_(r in I, mr=-2 mod e)h_(m,z)(r)
 =|I|H_(m,z)/e+O(log^C x),

H_(m,z)=product_(p>z,p does not divide m)(1+1/(p(p-2))).
```

The endpoint error follows from

```text
sum_(d<=R)g_z(d)<<log^C R,
R sum_(d>R)g_z(d)/d<<log^C R.
```

The small-prime sieve density is

```text
V_(m,z)=product_(p<=z,p does not divide m)(1-1/p),
```

and exact multiplication of the local factors gives

```text
C_(2,>z)W_z A_z(m)H_(m,z)V_(m,z)=m/phi(m).
```

For a fully uniform maximal-interval ledger, fix

```text
E=log^L_E x,       D=x^delta,       0<delta<1-gamma.
```

Truncate the `d`-sum in `h_(m,z)` at `E` and write `r=ds`.  Since every
prime of `d` exceeds `z`, all small-prime congruences are reduced and have
one residue class in `s`; Rosser weights at level `D` therefore incur only
integer-lattice remainders.  Uniformly in the interval,

```text
sum_(r in I)b_x^(z)(mr)
 = (m/phi(m))|I|
   +O(tau(m)[epsilon_x |I|m/phi(m)
             +D log^C x+x/(mE)log^C x]),
epsilon_x<<_(A,K,delta)log^(-A)x.
```

Here the last term pays both the actual divisor tail and the Euler main-term
tail; one may use `g_z(d)<=3^omega(d)/d` and
`sum_(d|r)3^omega(d)<=tau(r)^2`.  After multiplying by `tau(m)^B` and summing
over `m<=x^gamma`, the three errors are respectively

```text
epsilon_x x log^C x,
x^(gamma+delta)log^C x,
x log^C x/E.
```

First choose `delta<1-gamma`, then `L_E` and the fundamental-lemma saving.
This gives every requested log power without counting or union-bounding the
set of intervals.

On the real side, maximal Bombieri--Vinogradov applies to the reduced class
`2 mod m` for odd `m`.  Insert the outer `tau(m)^B` by splitting at
`tau(m)^B<=log^L x`; the low part uses a larger BV saving and the high part
uses the trivial row bound plus an arbitrarily high fixed divisor moment.
Even `m` contributes only `mr+2=2^j`, hence `x^o(1)` after the same divisor
weight.  This proves H2 for every fixed `gamma<1/2`; the constants are not
uniform as `gamma` approaches `1/2`.

After H0--H2, H3 has no fixed-prime rank-one counterexample.  Expanding its
prime part still gives the determinant form in Section 7.2, while the hybrid
comparison subtracts all conductors up to `z`.  The remaining analytic task is
therefore a genuinely high-conductor determinant/dispersion estimate, not an
unpaid local congruence.

### 8.4 Two honest analytic forks

The published Ford--Maynard hypothesis `(II)` cannot simply be relabelled
"structured."  In its direct Vaughan branch, Lemma 7.14 takes a supremum over
`ell=6 ceil(1/(1-gamma))=12` arbitrary one-bounded sequences, removes the box
conditions, and groups them into two divisor-bounded convolutions before
calling `(II)`.  Because unused factors may be `delta_1`, that envelope already
contains arbitrary two-sided coefficients.

Before this supremum, however, the modified Heath--Brown identity emits only
finite-complexity atoms: truncated Mobius factors, at most one normalized log
factor, constants/interval or Mellin factors, bounded-depth convolutions, and
perfect-power remainders.  This leaves two honest forks:

```text
U: prove H3 exactly as stated for the hybrid comparison;

S: reprove the Ford--Maynard extraction before the arbitrary-beta supremum,
   retain only the actual Mobius/log/truncation atoms,
   and prove the resulting structured determinant estimates plus the
   exact-square-root Type-I fringe.
```

Fork S is strictly a new compiler lemma, not a consequence already contained
in Ford--Maynard.  Using the mirrored parameter `P^#=(Q,J,Q-J)` makes the
Vaughan surplus `1/400` explicit, but it also asks for maximal Type I through
`x^Q`, which ordinary Bombieri--Vinogradov does not provide.  The primary
structured redesign should therefore remain at the exact-half parameter
`P_TPC` and carry its own top-fringe ledger.  The formula-level TPC-31 bridge
in Section 7.2 supplies a natural determinant atom for fork S; it does not
discharge that new lemma.

### 8.5 Fork decision: direct modified-Heath--Brown extractor `S-HB2`

The universal fork `U` remains mathematically open: after choosing `K=K(B)`,
no surviving local-character counterexample is known.  It is nevertheless the
wrong primary target.  It asks for the raw shifted-prime operator norm against
every pair of divisor-bounded coefficient sequences.  No checked source
compiles that norm from a Kloosterman or determinant estimate.

A first structured design followed the general Ford--Maynard
Proposition 7.22/Lemmas 7.17--7.14 machinery.  That route is sufficient only
after retaining largest-prime block selectors, rough-factor fragmentation,
Mellin/Perron phases, perfect powers, and their full convolution closure.  It
is also unnecessarily broad for this one sequence.  In that generic route,
Lemma 7.14 has

```text
ell=6 ceil(1/(1-gamma))=12
```

at `gamma=1/2`, not `24`; moreover the supremum contains `k ell` slots, not
merely `ell`.  The selected route bypasses this arbitraryization completely.

Put `w_x^(z)(n)=Lambda(n+2)-b_x^(z)(n)`.  Ford--Maynard Lemma 5.2 is valid
for every positive integer `h`.  The smallest fail-closed choice for the
present Type-I/Type-II window is `h=2`: multiply that identity by
`w_x^(z)(n)/log n` and sum over the dyadic support.  This is an exact identity
for

```text
sum_(x/2<p<=x)w_x^(z)(p).
```

The identity has a root index `r`.  When `r>=2`, its support consists only of
perfect powers.  For fixed `K`,

```text
|w_x^(z)(n)|<=log(2x)+C(log z)tau(n)=x^o(1),
```

and the bounded-depth factorization multiplicity is also `x^o(1)`.  Therefore
all `r>=2` terms together are `x^(1/2+o(1))` and are negligible.  This disposal
uses the literal shifted-prime sequence; it is not a consequence of the
abstract Ford--Maynard `(w)` hypothesis for an arbitrary sequence.

For `r=1`, each term has `1<=j<=2`,

```text
n=e_1...e_j f_1...f_j,       e_i<=sqrt(x),

coefficient
 =mu(e_1)...mu(e_j) log(f_1)/log(n),
```

up to a fixed combinatorial constant.  Thus there are at most four literal
variables and at most two HB Mobius slots.

Choose the first component `u>=sqrt(n)`, if one exists.  If it is an `f_q`,
its complement `D=n/f_q` is at most `sqrt(n)`.  The subrange `D<=x^J` is paid
by the proved H2 at `gamma=J`; the rest is assigned to the structured master.
The large `f_q` has only a constant/log weight, so the Type-I use is legitimate
after partial summation and divisor-bounded outer reassembly.  If the first
large component is an `e_i`, then `e_i<=sqrt(x)` and `n>x/2` force both `e_i`
and `n/e_i` into a constant-factor square-root corridor.  This is not Type I,
but both orientations lie in the same closed structured master window.

On tuples with no large component, discard unit slots.  A component equal to
`1/2` is itself an admissible group.  Otherwise the vector

```text
(log u_i/log n)_i
```

has components in `(0,1/2)`, sum one, and therefore cannot lie in
`R(P_TPC)=empty`.  Some nonempty proper subset `E` consequently satisfies

```text
J<=sum_(i in E)log(u_i)/log(n)<=1/2.
```

Because `n>x/2`, its product obeys the literal window

```text
(x/2)^J < M_E<=sqrt(x).
```

Choose the first admissible `E` in a fixed ordering.  This existential cover
does not by itself give separated Type-II coefficients: the failures of all
earlier subsets are joint multiplicative cutoffs.  The canonical exact object
is therefore the original at-most-four-variable sum with its finite region
indicator.  Its separated presentation uses at most `2^4` selectors and
Perron/Mellin transforms (or an equivalent bounded polytope partition), with
the transform `L^1` norm and tails retained in the analytic master.  Likewise
the literal factor `1/log n` is retained through

```text
rho_x(n)=log x/log n,
```

or expanded to any requested fixed order on the dyadic shell, with all bounded
log powers and the remainder recorded.  It is never silently replaced by
`1/log x`.

The choice `h=1` is not safe.  It permits a Mobius-bearing factor `e` far above
`sqrt(x)` while its complement lies below `x^J`; the large variable is then
rough, so the term is neither the proved unweighted-inner Type I nor the
`[J,1/2]` structured master.  Choices `h=3,4` also give exact extractors, but
have more literal slots; they remain factorized analytic lifts rather than the
minimal obstruction normal form.

Define `C_HB2` to be the resulting finite source-emitted closure of the atoms

```text
delta_1, 1, mu(e)1_(e<=sqrt(x)), log(f)/log x,
hard interval/product selectors, and real power twists u^(it),
```

under at most four-variable grouping and bounded-depth convolution.  It is
independent of future prime outcomes.  The selected analytic master gate is

```text
(SHB-D2)

sup_((Xi,Kappa) emitted by C_HB2)
| sum_((x/2)^J<m<=sqrt(x), x/2<mn<=x)
    rho_x(mn) Xi(m)Kappa(n)
    [ sum_(d r-m n=2)mu(d)log r-b_x^(z)(mn) ] |
 <<_(A,K) x/log^A x,

rho_x(t)=log x/log t.
```

Here the display denotes the separated versions of the literal finite-region
templates; uniform transform norms and tails are part of the quantifiers.  The
supremum is not over arbitrary divisor-bounded sequences.  It includes the
closed `m=sqrt(x)` endpoint.  A theorem ending at
`sqrt(x)/log^L x` cannot be repaired by taking a nonuniform BV limit, and
calling the published Proposition 4.11 or Theorem 2.2 would reintroduce
universal `(II)` and be circular.

The exact reduction above gives

```text
H3-U      OPEN_RESERVE_NO_COUNTEREXAMPLE_BUT_OVERSTRONG
S-PROP722 DEPRIORITIZED_BROADER_THAN_NEEDED
S-HB2     PROVED_EXACT_REDUCTION_TO_SHB_D2
S-HB3/HB4 EXACT_ALTERNATE_FACTORIZED_LIFTS
SHB-D2    SELECTED_PRIMARY_OPEN_NEW_THEOREM.
```

The remaining arithmetic work is to split `(SHB-D2)` into comparison main,
small-divisor/degenerate, and high-conductor determinant-dispersion ranges.
Bettin--Chandee/DFI-type Kloosterman fractions and later unbalanced-convolution
estimates are candidate engines only after this exact reduction; none is
currently a black-box proof.

## 9. Conditional endpoint theorem

For each requested output saving, choose the associated `B`, then the fixed
`K(B)` above.  Either assume universal H3-U for that parameterized hybrid
  family, or prove `(SHB-D2)` for the direct `S-HB2` compiler.  The proved H0--H2
package and the exact extractor above then give

```text
sum_(x/2<r<=x, r prime) Lambda(r+2)
  ~ C2 x/log x.
```

If `r+2=q^j` with `j>=2`, its total Mangoldt contribution is
`O(sqrt(x) log x)`, hence negligible.  Since
`log(r+2)=(1+o(1))log x` on the dyadic interval,

```text
#{x/2<r<=x : r and r+2 are prime}
  ~ C2 x/log^2 x.
```

In particular, the replacement package implies TPC.  This is a conditional
compiler theorem, not a claim that H3 has been proved.

## 10. Typed crosswalk to the four review3 routes

```text
analytic far-copy / dispersion
    possible engine for the Section 8 high-conductor Type II norm

determinant-two O161 fixed atom
    possible local summand after an exact identity decomposition
    but current coefficientwise packet-to-FM map is absent

pair-native / H1 architecture
    possible reassembly and exactly-once provenance layer
    but it does not weaken the universal FM quantifier by declaration

nonautonomous rare-event dynamics
    organizes recurrence once arithmetic covariance is supplied
    but H3_METRIC does not imply the prescribed arithmetic seed or Type II
```

The direct linear crosslink from an existing O161 packet to the Ford--Maynard
sum remains `STOP_SCOPED`.  A future bridge must literally expand the same
`w_x(mn)`, preserve every coefficient and product domain, and reproduce the
full `[J,1/2]` operator norm.  Until then, the two engines are aligned by
their exponents and endpoint, not identified as the same object.

## 11. State ledger

| gate | state |
|---|---|
| coarse divisibility comparison `b^(2)` | `PROVED_EXACT` |
| coarse Ramanujan profile `b^(2,circ)(n)=S(2n)` | `PROVED_EXACT_ON_UNTRUNCATED_PROFILE` |
| coarse universal Type II | `STOP_SCOPED_FALSE_MOD3_RANK_ONE` |
| hybrid tensor-local Euler profile `b^(z)` | `PROVED_EXACT` |
| hybrid Ford--Maynard `(b.1)` | `PROVED_SOURCE_BACKED_FUNDAMENTAL_LEMMA_PLUS_BV` |
| hybrid Ford--Maynard `(w)` | `PROVED_ELEMENTARY_FOR_EACH_FIXED_K` |
| hybrid Ford--Maynard `(b.2)` at `P_TPC` | `VACUOUS_PROVED_R_EMPTY` |
| hybrid maximal Type I, every fixed `gamma<1/2` | `PROVED_SOURCE_BACKED_FUNDAMENTAL_LEMMA_PLUS_MAXIMAL_BV` |
| hybrid maximal Type I at `gamma=1/2` | `NOT_PROVED_BY_BV` |
| hybrid universal Type II `[J,1/2]` | `OPEN_HIGH_CONDUCTOR_WALL` |
| universal fork H3-U | `OPEN_RESERVE_NO_COUNTEREXAMPLE_BUT_OVERSTRONG` |
| generic Proposition 7.22 structured fork | `DEPRIORITIZED_BROADER_THAN_NEEDED` |
| direct modified-HB2 prime extractor | `PROVED_EXACT_REDUCTION_TO_SHB_D2` |
| structured atom closure `C_HB2` | `PROVED_FINITE_SOURCE_EMITTED_LANGUAGE` |
| modified-HB3/HB4 extractors | `EXACT_ALTERNATE_FACTORIZED_LIFTS` |
| direct determinant gate `(SHB-D2)` | `SELECTED_PRIMARY_OPEN_NEW_THEOREM` |
| minimal central `(HB2-B3)` three-Mobius cell | `SELECTED_PROVISIONAL_OPEN_NEW_THEOREM` |
| BC Corollary 1 direct attachment to `(HB2-B3)` | `STOP_SCOPED_GROUPED_COR1_SCALE_NO_SAVING` |
| one-Poisson BC Theorem 1 quarter lift | `STOP_SCOPED_FIRST_SUMMAND_NO_NEW_RANGE` |
| HB4 quarter collective `h=0` hybrid-main attachment | `PROVED_SOURCE_BACKED_ALL_D_ATTACHMENT` |
| HB4 quarter Ramanujan axes | `PROVED_ELEMENTARY_X3_OVER_4_POWER_SAVING` |
| HB4 quarter nonzero off-diagonal, `1/4<delta<3/8` | `PROVED_SOURCE_BACKED_WEIL_PLUS_PASCADI` |
| HB4 quarter high-conductor ratio-character component, `3/8<=delta<1/2` | `PROVED_PRIMITIVE_LARGE_SIEVE_PLUS_PASCADI` |
| HB4 quarter low-conductor Gauss--Ramanujan projector | `PROVED_CRT_PLUS_PRIMITIVE_LARGE_SIEVE` |
| HB4 quarter exact half endpoint | `OPEN_LOG_POWER_ENDPOINT` |
| HB2 Cauchy zero mode | `OPEN_MOBIUS_WEIGHTED_CRT_BDH_COVARIANCE` |
| HB4 second Cauchy | `OPEN_RANK2_RECIPROCAL_PHASE` |
| large-divisor HB2 switch | `PROVED_EXACT_COEFFICIENTWISE` |
| switched `HB4xHB2` divisor-log determinant | `OPEN_NEW_THEOREM` |
| shifted-Mangoldt determinant-two lift `dr-mn=2` | `PROVED_EXACT` |
| TPC-31 prime--Mobius core `mu(d) log ell` | `PROVED_FORMULA_LEVEL` |
| coarse multiplier main terms | `PROVED_EXACT` |
| coarse Ford--Maynard `(b.1)/(b.2)/(w)` | `PROVED_FOR_FIXED_VARPI0` |
| coarse maximal Type I for every fixed `gamma<1/2` | `PROVED_SOURCE_BACKED` |
| exponent compiler `J -> 1/2 -> Q` | `PROVED_EXACT` |
| conditional Vaughan surplus `Q+(Q-J)-1` | `EXACTLY_1/400; UNPAID_UNTIL_TYPE_II` |
| literal theorem for fixed Mobius plus two arbitrary rough coordinates | `NONE_IN_BOUNDED_SCAN` |
| existing O161-to-FM coefficientwise attachment | `ABSENT` |
| fixed arithmetic seed from Haar metric theorem | `OPEN` |
| strict physical `1/400` credit | `UNPAID` |
| TPC theorem | `NO` |
| TPC-207 trigger | `false` |

This checkpoint changes the route, not the final theorem state.  The coarse
comparison closed the one-sided local and Type-I gates but failed the stronger
tensor-local test.  The hybrid profile removes that exact failure and its
fundamental-lemma regularity package is proved.  The first remaining bridge is
the single structured high-conductor determinant norm `(SHB-D2)` on the
physical `J/Q` scales.

## 12. Source-locked determinant range atlas

This section applies the complete published error terms, not only their
favourable summands.  Write

```text
D=x^delta,  R asymp x/D,
M=x^mu,     N asymp x/M,
```

on a smoothed dyadic cell of `dr-mn=2`.  A power-saving determinant error is
only a candidate contribution to `(SHB-D2)`: its explicit main term must still
be proved equal to the same-cell contribution of `b_x^(z)`.

### 12.1 The neighbouring two-rough cells really touch existing theory

For the `h=2,j=1` cell `dr-ef=2`, assign the two smooth variables `r,f` and
the two arbitrary variables

```text
alpha_e=mu(e),       beta_d=mu(d)
```

to [Bettin--Chandee Corollary 1](https://arxiv.org/pdf/1502.00769).  If
`E=x^a,D=x^delta`, its error, up to fixed log powers, is

```text
x^(Gamma(a,delta)+o(1)),
Gamma(a,delta)=17(a+delta)/20+max(a,delta)/4.
```

Thus `a,delta<=1/2` has worst exponent `39/40`; the coefficient interface and
error have a genuine power saving on the half-hyperbola.  The same calculation
for the `h=3` thin cell `J<a<=1/3` gives worst exponent `5/6` when
`delta<=1/2`, and more generally covers

```text
delta < (20-17a)/22.
```

This is an important positive control: determinant technology reaches the
road immediately adjacent to the TPC cell.  It does not identify the BC main
term with the hybrid comparison, and it does not truncate the literal Mobius
divisor to `D<=sqrt(x)`.

### 12.2 Minimal central obstruction: the bare three-Mobius cell

The first scale-degenerate central obstruction already occurs in the source-emitted
`h=2,j=2` language.  Fix an odd integer `c>1`, take `f_1=c,f_2=1`, and put
`e_1,e_2` in constant-factor square-root intervals.  One literal prime-side
cell is, up to fixed smooth shell and log factors,

```text
(HB2-B3)
sum_(d r-c e_1 e_2=2)
  mu(d)mu(e_1)mu(e_2)log(r) W(d,r,e_1,e_2)
  - the same hybrid-comparison cell.
```

It has three primitive rough coordinates `d,e_1,e_2` and only one genuinely
long smooth coordinate `r`.  This is **not** a literal slot-count mismatch in
Bettin--Chandee Corollary 1: one may group

```text
alpha_n=sum_(e_1e_2=n)mu(e_1)mu(e_2)W,
beta_d=mu(d)W_D(d),
```

put `r` in one smooth slot, and put the fixed `c` in a compact smooth bump in
the other.  The determinant interface then matches.  It fails numerically.
Here `N_1 asymp x,N_2=D`; the `L^2` norms and the complete Corollary-1 error
give

```text
x^(11/10+o(1))D^(17/20),
```

which exceeds the `x` main scale even for bounded `D`.  Thus the correct
direct black-box verdict is

```text
BC_COROLLARY_1_TO_HB2_B3
 = STOP_SCOPED_GROUPED_COR1_SCALE_NO_SAVING.
```

The failure persists well before the bare limit.  If the largest smooth
`f`-slot has exponent `b` and the other three HB factors are grouped into a
rough coordinate of exponent `1-b`, the formal Corollary-1 error at
`delta=1/2` is power-saving only when

```text
b>21/44.
```

The symmetric quarter cell has `b=1/4`, and `(HB2-B3)` has `b=0`; neither is
covered.  This error test is still prior to comparison-main attachment.

Consequently `h=2` is only the **minimal-slot obstruction normal form**.  It
is selected provisionally for stating the missing theorem; it is not proved
analytically superior to the more factorized `h=3,4` identities:

```text
HB_H_OPTIMIZATION = OPEN_THREE_ROUGH_CELL_COMPARISON.
```

### 12.3 One Poisson plus Bettin--Chandee does not open the quarter cell

The factorized `h=4,j=2` quarter lift has

```text
e_1,e_2,f_1,f_2 asymp x^(1/4).
```

It is tempting to Poisson-sum one smooth `f` variable and apply
Bettin--Chandee Theorem 1, which does accept three arbitrary coefficients in a
reciprocal phase.  Let `D=x^delta`.  The nonzero Poisson range begins at
`D>x^(1/4)`.  After the literal Poisson prefactor, the two terms in the
published BC bound contribute respectively

```text
E_1=x^(69/80+7delta/10+o(1)),
E_2=x^(3/4+7delta/8+o(1)).
```

The second term alone would save for `delta<2/7`, but the theorem gives their
sum.  The first term saves only for `delta<11/56<1/4`, disjoint from the new
nonzero range.  It is therefore illegal to quote only `E_2`:

```text
ONE_POISSON_BC1_QUARTER
 = STOP_SCOPED_FIRST_SUMMAND_NO_NEW_RANGE.
```

This does not prove the quarter cell false.  It proves that a second
dispersion/Cauchy step, or a genuine strengthening that removes the first BC
summand, is necessary.

### 12.4 Primary-source interface table

| source | literal useful object | current verdict for `(SHB-D2)` |
|---|---|---|
| [Ford--Maynard](https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf), Lemma 5.2 | exact prime extractor for any `h` | supplies HB2/HB3/HB4 identities; Theorem 2.2 and Proposition 4.11 cannot prove the input `(II)` without circularity |
| [Duke--Friedlander--Iwaniec](https://www.math.ucla.edu/~wdduke/preprints/bilinear.pdf) | two arbitrary sequences after a reciprocal-exponential kernel exists | candidate only after dispersion; no direct determinant or comparison-main interface |
| [Bettin--Chandee](https://arxiv.org/abs/1502.00769), Corollary 1 | determinant asymptotic with two arbitrary plus two smooth slots | proves adjacent two-rough cells; grouped `(HB2-B3)` matches the slots but its full error has no saving |
| Bettin--Chandee, Theorem 1 | reciprocal phase with three arbitrary sequences | shape-compatible only after Poisson/dispersion; the complete one-Poisson bound gives no new quarter range |
| [Fouvry--Radziwill](https://arxiv.org/abs/1811.08672) and [Wright](https://arxiv.org/html/2604.25177v1) | average AP discrepancy for unbalanced convolutions with a Siegel--Walfisz input | conditional small/unbalanced strips only; no balanced three-rough cell and no automatic hybrid-main identification |
| [Assing--Blomer--Li](https://arxiv.org/abs/2005.13915) | unweighted/fixed-character Titchmarsh and specialised multilinear forms | no literal `C_HB2` coefficient and normalization interface |

The claimed improvement in arXiv:2601.00292 is excluded: its current author
comment records a missing `L^2` factor and withdraws the improved bound.  No
exponent ledger here uses it.

### 12.5 Historical attack gate: native two-stage determinant dispersion

At this checkpoint the range atlas replaced the broad request “prove Type II”
by one construction problem:

```text
TPC_FM_NATIVE_TWO_STAGE_D2_DISPERSION_GATE
 = SUPERSEDED_BY_SECTIONS_12_6_12_7.
```

A valid theorem must perform all of the following in one ledger.

1. Start from either the minimal `(HB2-B3)` normal form or an exactly equivalent
   factorized HB3/HB4 lift; do not arbitraryize its Mobius tensors.
2. Apply Cauchy/dispersion before destructive `m/n` convolution, then produce a
   separated reciprocal phase to which the complete DFI/BC bound applies.
3. Identify the zero frequency coefficientwise with the same tensor-local
   `b_x^(z)` main.  “A main term of the right size” is insufficient.
4. Split low conductor and high conductor using the actual `z=log^K x` local
   factors, and retain all diagonal, gcd, transform-tail, and `K(B)` losses.
5. Obtain a saving from every summand in the invoked source bound; the rejected
   `E_2`-only `2/7` calculation may not reappear.
6. Cover the full `d/r` hyperbola.  The range `d>sqrt(x)` needs an explicit
   outer-Lambda dual or switching identity; exchanging the names `d,r` changes
   `mu(d)log r` and is not a proof.

The exact direct-HB reduction and this source atlas are genuine route advances,
but the two-stage estimate is a new theorem.  Current status remains

```text
HB2_B3_MINIMAL_CORE = SELECTED_PROVISIONAL_OPEN_NEW_THEOREM
HB3_HB4_FACTORIZED_ATTACK_LIFTS = OPEN
NATIVE_TWO_STAGE_D2_DISPERSION = SUPERSEDED_BY_SECTION_12_6_12_7_AUDIT
STRICT_1_OVER_400 = UNPAID
TPC_207_TRIGGER = false.
```

### 12.6 Two-stage audit: one true Weil window and two new central objects

Retaining both smooth quarter variables in the `h=4,j=2` lift does produce a
genuine partial off-diagonal range.  Put

```text
F_1 asymp F_2 asymp x^(1/4),
a=e_1e_2 asymp x^(1/2),
D=x^delta.
```

Poisson summation in `f_2` modulo `d` has prefactor `F_2/D` and dual length
`H=D/F_2`.  Completing `f_1` has prefactor `F_1/D`, dual length `L=D/F_1`,
and produces a Kloosterman sum

```text
S(ell,-2h conjugate(a);d).
```

Weil's bound, with gcd losses absorbed by a fixed divisor sum, gives for each
`(e_1,e_2,d)`

```text
(F_2/D)(F_1/D) H L D^(1/2+o(1))=D^(1/2+o(1)).
```

Absolute summation over `e_1,e_2,d` is therefore

```text
x^(1/2+o(1))D^(3/2).
```

Consequently

```text
HB4_DOUBLE_SMOOTH_OFFDIAGONAL_1/4<delta<1/3
 = PROVED_SOURCE_BACKED_WEIL_POWER_SAVING,
```

with no saving at `delta=1/3`.  This verdict is only for the nonzero
off-diagonal.  The `h=0` linear main, the `ell=0` Ramanujan term, the two-adic
sector, and their coefficientwise identification with the dyadic
`b_x^(z)` cell remain a separate attachment gate.

The naive second Cauchy step does not extend this range.  For the minimal
`(HB2-B3)` cell, Cauchy in `e_2` and expansion introduce `d_1,d_2`,

```text
g=(d_1,d_2),       q=[d_1,d_2].
```

The CRT zero mode has density

```text
E_2/q=E_2 g/(d_1d_2)
```

and the compatibility condition `e_1=e'_1 (mod g)` in the odd sector.  This
is a quadratic signed covariance of the two Mobius rows.  It is not the
linear Poisson zero mode and is not centered by the first-moment comparison
`b_x^(z)`.  Absolute summation returns the original square scale; a saving
requires a new Mobius-weighted CRT/Barban--Davenport--Halberstam covariance
theorem.

The nonzero generic-`g=1` phase has modulus about `D^2`.  If all outer
variables are frozen and only their sizes are inserted into a DFI-shaped
envelope, the optimistic formal count is

```text
E^(149/96)D^(119/96),       E=x^(1/2),
```

which would require `delta<43/238<1/4`, before the nonzero range starts.  This
is **not** a literal source map: the outer variables and the resulting phase
have not been fitted to one published DFI theorem, so the number receives no
theorem credit.  In
the HB4 quarter lift, a second Cauchy produces a rank-two reduced-fraction
phase whose numerator depends jointly on
`d_1,d_2,h_1,h_2,e_i,f_i`; it is not a rank-one BC/DFI coefficient array.
Taking a spectral supremum at that point destroys the source-emitted tensor
and returns an overstrong U-like envelope.

Finally, `D>sqrt(x)` is independent of the central covariance problem.
Divisor switching gives

```text
mu((mn+2)/r)log r,       r<sqrt(x),
```

not `mu(r)log d`.  None of the checked sources controls this quotient-Mobius
cell.  The honest refined ledger is

```text
HB4_DOUBLE_SMOOTH_OFFDIAGONAL_D_LT_X1/3 = PROVED_POWER_SAVING
HB4_DOUBLE_SMOOTH_MAIN_ATTACHMENT = SUPERSEDED_BY_12_7_COLLECTIVE_ALL_D_PROOF
HB2_CAUCHY_ZERO_MODE = OPEN_MOBIUS_WEIGHTED_CRT_BDH_COVARIANCE
HB4_SECOND_CAUCHY = OPEN_RANK2_RECIPROCAL_PHASE
LARGE_D_DUAL_V5_SNAPSHOT = SUPERSEDED_BY_EXACT_HB2_SWITCH_IN_12_9
NAIVE_NATIVE_TWO_STAGE_CLOSURE = STOP_SCOPED_AT_QUADRATIC_DIAGONAL.
```

Thus the HB2 branch target is no longer a generic second dispersion.  It would
need the signed CRT covariance estimate that controls the Cauchy zero mode
without absolute values, together with a separate legal large-divisor
switching identity.  Section 12.7 makes the final route choice in favour of
the more factorized HB4 lift after its principal and first off-diagonal window
are closed.  None of these objects may be relabelled as the linear hybrid main.

### 12.7 Collective principal attachment and the surviving signed-modulus wall

The HB4 quarter lift becomes substantially cleaner if the two smooth variables
are kept until after Poisson summation.  Write

```text
F_1 asymp F_2 asymp F=x^(1/4),
a=e_1e_2 asymp x^(1/2),
u=a f_1 asymp x^(3/4).
```

Poisson summation in `f_2` modulo `d` first produces a dual index `h`.  The
`h=0` term must be summed over **all signed `d`-dyads** before it is compared
with `b_x^(z)`.  For odd `u`, the physical `f_2` lattice is odd and has density
`1/2`; the admissible divisors satisfy `(d,2u)=1`.  Put

```text
F_(2u)(s)=sum_((d,2u)=1) mu(d)d^(-s)
         =zeta(s)^(-1) product_(p|2u)(1-p^(-s))^(-1).
```

The zero of `1/zeta(s)` at `s=1` gives, by Perron with the logarithmic kernel,

```text
G_q(Y)=sum_(d<=Y,(d,q)=1) mu(d)/d log(Y/d),

(1/2)G_(2u)(Y)
 =u/phi(u)+O_(A,C)(tau(u)^C log^(-A)Y),                 (12.7.1)
```

uniformly for the emitted `u<=Y^(3/4+o(1))`.  The arbitrary logarithmic
saving follows by moving the contour through a Vinogradov--Korobov zero-free
region; the finite Euler factors and the bounded number of Mellin derivatives
cost only fixed log powers.  See [Ford, *Zero-free regions for the Riemann
zeta function*](https://arxiv.org/abs/1910.08205) for a modern source for the
zero-free input.  Ramaré's explicit coprime Möbius bound by itself supplies
only one logarithm and is not being promoted to `(12.7.1)`.

For even `u=2^v u_o`, squarefreeness pairs the odd row `d'` with `2d'`.
Their zero frequencies have the same density and opposite Möbius signs.  With
the truncation retained exactly, their sum is

```text
G_(2u_o)(Y)-G_(2u_o)(Y/2).
```

The two principal constants are equal and cancel; both remainders are swallowed
by the same zero-free estimate.  The collective principal is therefore zero,
as is `b_x^(z)(u f_2)` outside the negligible power-of-two sector.  This parity
cancellation is destroyed by a per-`D` triangle inequality.

On the comparison side, the exact slice expansion of Section 8.3 can be used
on the short `f_2` interval without Bombieri--Vinogradov.  Choose a small-prime
sieve level `F^eta`, `0<eta<1`, and truncate the rough-divisor expansion at
`log^L x`.  The Rosser--Iwaniec fundamental lemma (see
[Iwaniec, *Rosser's sieve*](https://doi.org/10.4064/aa-36-2-171-202)) applies
because `log(F^eta)/log z` tends to infinity.  Uniformly in the emitted `u`, it
gives the same `u/phi(u)` weighted integral.  Summing the lattice remainders over the
source-emitted outer representations costs

```text
x^(3/4+eta/4+o(1))=o_A(x/log^A x),
```

and the divisor tail is `O_A(x/log^A x)` after choosing `L`.  Fixed-log
partition/Mellin norms are included in that choice.  Together with `(12.7.1)`
and an exactly-once partition of unity over all `d/r` dyads, this proves

```text
HB4_QUARTER_COLLECTIVE_H0_TO_HYBRID_MAIN
 = PROVED_SOURCE_BACKED_ALL_D_ATTACHMENT.               (12.7.2)
```

It does **not** construct objects `b_(z,D)`.  The statement that a single
dyadic `D` main equals a comparison cell remains false-object bookkeeping:

```text
HB4_PER_D_H0_TO_bz = STOP_SCOPED_NO_NATURAL_D_LABEL.
```

For `h!=0`, Poisson/completion in `f_1` produces a second dual index `ell`.
The `ell=0` Ramanujan axis is bounded, after reducing the gcd strata, by

```text
sum_(h<=D/F)|c_d(2h)| << (D/F)d^o.
```

The two Poisson prefactors then give `F/D` per `(e_1,e_2,d)`; summing the
`d`-shell and the `x^(1/2+o(1))` outer pairs yields

```text
HB4_QUARTER_RAMANUJAN_AXIS = O(x^(3/4+o(1))).            (12.7.3)
```

When `h ell !=0`, Weil gives the already recorded
`x^(1/2+o(1))D^(3/2)`.  Thus the complete HB4 quarter transform now has a
proved principal, proved axes, and a genuine off-diagonal power-saving window

```text
x^(1/4+epsilon) <= D <= x^(1/3-epsilon).                (12.7.4)
```

The first literal substitution into
[Pascadi, Theorem 10.3](https://arxiv.org/abs/2304.11696) puts `e_1` in the
source's `r` slot.  It is valid but nonoptimal.  The source permits a stronger
coefficient compression: convolve `a=e_1e_2 asymp F^2` first and define, on
each dyadic `n` interval,

```text
b_(n,d)=mu(d)
 sum_(a,h: n=-4h conjugate(a) mod d) alpha_a Gamma(a,d;h).
```

Expanding its square gives `h_1a_2=h_2a_1 (mod d)`.  For nonzero difference,
each quadruple has only `x^o(1)` possible divisors `d`; for zero difference,
the multiplicative energy is `FD x^o(1)` and the free `d`-sum costs `D`.
Since `a` has length `F^2` and `h` has length `D/F`, both cases give

```text
||b||_2^2 << F^2 D^2 x^o(1),
||b||_2   << F D x^o(1).                                (12.7.5)
```

The source-map also retains the transform weights.  Split the signs and
dyadic ranges of `ell` and the least positive residue `n`, reduce the odd
coprime gcd strata, and apply a bounded Fourier/Mellin separation on each
smooth shell:

```text
Gamma(a,d;h,ell)
 = integral_(|t|<=log^B x)
     A_t(a,d;h) g_t(ell/M,n/N,d/D) dt
   +O_A(x^(-A)).
```

The total transform `L^1` norm is `log^O(1)x`; choosing `B` after the target
saving absorbs it, and smooth tails are rapid.  Put `A_t` into `b_(n,d)` and
`g_t` into the theorem's smooth test function.  The finitely many gcd strata
are reduced before this step.  The target condition `(d,2e_1e_2)=1` already
makes the active `d` odd, so there is no off-diagonal two-adic stratum inside
`K_D`; any finite two-adic separation belongs to the earlier outer reduction.
In the source convention `r_src asymp R_src` means
`R_src<r_src<=2R_src`; hence `R_src=1` is the literal singleton `r_src=2`,
not `r_src=1`.  The source kernel is
`S(m conjugate(r_src),+n;sc)`.  Isolate `c=1`
with the first smooth coordinate and use, for odd `d`,

```text
S(ell conjugate(2),-4h conjugate(a);d)
 =S(ell,-2h conjugate(a);d).
```

Thus `m=ell,r_src=2,n=-4h conjugate(a),s=d,c=1` is the exact source kernel.
The coefficient compression is literal, not merely an exponent substitution.

Take `C=R_src=1,S=D,M=D/F,N<=D` in the complete theorem.  Its base factor is
`D^2 sqrt(F)`; after multiplication by the physical `F^2/D^2` prefactor, all
five terms are bounded respectively by

```text
F^(5/2)D,  F^2D,  F^2D,  F^(5/2)D,  F^2D.
```

Every term has a fixed power saving for `D<=x^(3/8-epsilon)`, while the first
and fourth terms have no saving at the endpoint.  Hence

```text
HB4_QUARTER_PASCADI_OFFDIAGONAL_1/3<=delta<3/8
 = PROVED_SOURCE_BACKED_POWER_SAVING.                    (12.7.6)

HB4_QUARTER_OFFDIAGONAL_1/4<delta<3/8
 = PROVED_SOURCE_BACKED_POWER_SAVING.                    (12.7.7)
```

Quoting only the favourable `F^2D` terms would falsely extend the range to
`delta<1/2`; the complete-bound endpoint is `3/8`.

This is the decisive route advance.  Generic second Cauchy is stopped, but a
modulus-dependent coefficient compression followed by the complete spectral
large sieve opens a real second window.  After pulling out the double-Poisson
factor `F^2/D^2`, define the literal remaining family

```text
K_D = sum_(e_1,e_2 asymp F) mu(e_1)mu(e_2)
      sum_(d asymp D,(d,2e_1e_2)=1) mu(d)
      sum_(0<|h|,|ell| << D/F)
        Gamma(e_1,e_2,d;h,ell)
        S(ell,-2h conjugate(e_1e_2);d).
```

Here `Gamma` ranges only over the source-emitted smooth shells and their
fixed-log Mellin derivatives.  The minimal sufficient central theorem is

```text
|K_D| <<_A F^2 D^2/log^A x,
x^(3/8) <= D <= F^2=x^(1/2).                            (12.7.8)
```

Multiplication by `F^2/D^2` then gives the required `x/log^A x`.  Relative to
the Pascadi bound, `(12.7.8)` asks for the additional gain `D/F^(3/2)`, at
worst only `F^(1/2)=x^(1/8)`.  A convenient stronger sufficient
form is square-root cancellation in the `a=e_1e_2` direction,

```text
|K_D| <<_A D^(7/2)/(F log^A x),
```

which covers the whole stated range after the physical prefactor.  This is a
new signed-modulus theorem, not a restatement of Pascadi or Kuznetsov.

The selected central target must therefore retain the literal
`mu(d)mu(e_1)mu(e_2)` tensor in the modulus-averaged Kloosterman family.
Sections 12.8--12.9 split its first missing by conductor and replace the old
large-divisor quotient-Mobius object by an exact HB2 switch.  Neither operation
reopens the HB2 absolute CRT diagonal, the stopped one-Poisson/BC route, or any
legacy Section 6 method cell.

### 12.8 Ratio-character split: the false shortcut and the real central gate

There is useful extra structure in the incidence coefficient, but it must be
extracted conductor by conductor.  Put

```text
g=(h,d),  d=gq,  h=gk,  Q=D/g,  U=Q/F.
```

Then `(k,q)=1`, `(e_1e_2,gq)=1`, and the Pascadi residue reduces on the unit
group modulo `q` to

```text
u=-4k conjugate(e_1e_2) (mod q).                        (12.8.1)
```

The projection is performed on this complete gcd stratum.  Lift each least
residue `n_0 (mod d)` to `n=d+n_0 in [d,2d)` first, and only then split the
result into the bounded number of `N asymp D` source blocks.  Pascadi's smooth
test is taken constant in `n`; every physical `n` dependence belongs to its
arbitrary coefficient.  Thus no weighted or partial-residue sum is being
declared to have zero mean.

After the already required fixed-log Mellin/Fourier separation, write

```text
E_i(chi)=sum_(e_i asymp F,(e_i,gq)=1) mu(e_i)W_i(e_i)chi(e_i),
H_g(chi)=sum_(k asymp Q/F,(k,q)=1) W_H(k)chi(k).
```

More explicitly, on a conductor/cofactor dyad
`cond(chi)=r_chi asymp R_chi`, `q=r_chi s_chi`, and
`s_chi asymp S_chi=Q/R_chi`, every frozen atom has the form

```text
Gamma
 = integral_(t in T) A_t^P(e_1,e_2;g) A_t^U(k;g)
     W_t^ell(ell/H) W_t^q(q/Q) W_t^s(s_chi/S_chi)
     dmu(t) + O_A(x^(-A)),                              (12.8.1a)

integral_(t in T)|dmu(t)| <= log^C x.
```

Signs, gcd strata, and all dyadic ranges are fixed before `(12.8.1a)`; the
display is a product atom, not a placeholder for a coupled weight.  After the
coprimality divisor expansion, the arithmetic character-polynomial arrays at
fixed `(g,s_chi,t)` are independent of the primitive modulus `r_chi`.
The remaining smooth scalar `W_t^q(r_chi s_chi/Q)` is removed by ordinary
partial summation, whose total variation is included in the displayed
`log^C x` budget.  Thus all other `r_chi` dependence is through character
evaluation.  Conductor projection is made on the complete residue group
before the bounded `N`-block restriction, which can only decrease the
coefficient `L^2` norm.  For the low part the complete residue group is
reassembled before applying the projector; no partial or weighted residue
sum is assigned zero mean.

The nonprincipal Fourier coefficient of `(12.8.1)` is, up to a unit phase and
the harmless choice of conjugates,

```text
E_1(conjugate chi) E_2(conjugate chi) H_g(chi).          (12.8.2)
```

Conjugating the two `E_i` coefficient arrays converts `(12.8.2)` into one
ordinary character polynomial of length `FQ`; its coefficient square norm is
`O(FQ log^C x)`.  For characters of primitive conductor `r>=F`, conductor
reduction, the coprimality divisor expansion, and the classical primitive
multiplicative large sieve (as stated in
[Pascadi, Lemma 3.4](https://doi.org/10.1112/S0010437X2500747X), ultimately
the primitive-character inequality of
[Montgomery--Vaughan](https://doi.org/10.1112/S0025579300004708)) give

```text
sum_g sum_(q asymp D/g) 1/phi(q)
 sum_(chi mod q, cond(chi)>=F) |E_1 E_2 H_g|^2
 << F D^2 log^C x.                                     (12.8.3)
```

Thus the genuinely high-conductor part has coefficient norm
`sqrt(F)D log^C x`; in the complete Pascadi bound it is power-saving for every
fixed `D<=x^(1/2-epsilon)`.  This does not include the exact half endpoint.

The tempting replacement of `cond(chi)>=F` by every nonprincipal character is
false.  Fix the real primitive character `psi (mod 3)`, put
`c_t=conjugate(psi(t))` on an interval of length `N=FQ`, and induce `psi` to
each `q=3p asymp Q`.  Its character sum has size comparable with `N`, so the
claimed all-character large-sieve left side is

```text
asymp F^2 Q^2/log Q,
```

whereas the proposed right side is only `O(FQ^2)`.  The ratio `F/log Q`
diverges.  Unit centering removes the principal character, not these repeated
proper-conductor characters.

Trying to prove the corresponding low-conductor coefficient norm would still
be an unnecessary new theorem:

```text
HB4_LOW_CONDUCTOR_RATIO_CHARACTER_SECOND_MOMENT:

sum_(g<=D/F) sum_(q asymp D/g) 1/phi(q)
 sum_(chi mod q, cond(chi)<F)
 |E_1(conjugate chi)E_2(conjugate chi)H_g(chi)|^2
 << F D^2 log^C x.                                     (12.8.4)
```

No checked theorem supplies `(12.8.4)`, and it is not needed.  Keep the
Kloosterman transform instead.  Since `mu(d)!=0`, the active `d` are
squarefree; hence `(g,q)=1`.  Kloosterman multiplicativity gives, up to the
displayed unit scalings,

```text
S(ell,gv;gq)=c_g(ell)S(ell conjugate(g),v;q).            (12.8.5)
```

For a character modulo `q` define its exact projector

```text
T_q(chi;ell)=sum_(u in (Z/qZ)^*) conjugate(chi(u))S(ell,u;q).
```

Expanding the Kloosterman sum and interchanging the two finite sums gives,
with the present conjugation convention,

```text
tau_q(eta,a)=sum_(v mod q)^* eta(v)e(av/q),
T_q(chi;ell)
 =tau_q(conjugate(chi),1)tau_q(conjugate(chi),ell),      (12.8.5a)
```

up to the already displayed unit scaling of `ell`; reversing the character
convention conjugates both Gauss factors simultaneously and changes only a
unit phase.  When squarefree
`q=r_chi s_chi` and `chi` is induced by a primitive
`psi (mod r_chi)`, elementary CRT factors `(12.8.5a)` into a primitive Gauss
square and a Ramanujan factor, giving the exact absolute identity

```text
|T_q(chi;ell)| = r_chi |c_(s_chi)(ell)| 1_((ell,r_chi)=1)
                <= r_chi(s_chi,ell).                     (12.8.6)
```

The equality is this elementary finite CRT/Gauss derivation;
[Pascadi, Lemmas 3.7--3.8](https://doi.org/10.1112/S0010437X2500747X)
pay the generalized Gauss and Weil--Ramanujan bounds used after it, rather
than being cited as the statement of the exact projector.

This projector closes the low conductors by classical means.  Put `H=D/F`.
For a conductor dyad `r_chi asymp R_chi<F`, the reduced `h/g` length is
`U=H/g=Q/F`, while `ell` retains length `H`.  For each separated smooth atom,
convolve the two `e_i` rows and the `h/g,ell` rows respectively.  Their lengths
and square norms are

```text
P_psi=E_1E_2:       length F^2,  ||P||_2^2 << F^2 x^o(1),
U_psi L_psi:        length UH,   ||UL||_2^2 << U S_(g,s_chi)x^o(1),

S_(g,s_chi)=sum_(|ell|<<H)|c_g(ell)c_(s_chi)(ell)W(ell)|^2.
```

The primitive large sieve applied to a fixed `R_chi` shell gives

```text
sum_(r_chi asymp R_chi) r_chi/phi(r_chi)
 sum_(psi mod r_chi)^* |P_psi|^2
 << (R_chi^2+F^2)F^2 x^o(1) << F^4x^o(1),

sum_(r_chi asymp R_chi) r_chi/phi(r_chi)
 sum_(psi mod r_chi)^* |U_psi L_psi|^2
 << (R_chi^2+UH)U S_(g,s_chi)x^o(1).                   (12.8.7)
```

Here conjugating a character is absorbed by conjugating its coefficient
array.  The cofactor lift has precisely the weight
`r_chi/phi(r_chi s_chi)=(r_chi/phi(r_chi))/phi(s_chi)`.
Divisor expansion and squarefree
multiplicativity give

```text
sum_(s_chi asymp Q/R_chi) S_(g,s_chi)/phi(s_chi)
 << H^2 g x^o(1).                                      (12.8.8)
```

Indeed `|c_m(ell)|<=(m,ell)`, the dyadic average of `(s,ell)^2` is
`O(ell x^o(1))`, and
`sum_(ell<=H)ell(g,ell)^2<<H^2g x^o(1)`.  Cauchy in the primitive
characters and then the cofactor therefore bounds a fixed `(g,R_chi)` by

```text
F^2 sqrt((R_chi^2+UH) U H^2g) x^o(1)
 =F^2 H^(3/2)sqrt(R_chi^2+H^2/g)x^o(1)
 <=F^3H^(3/2)x^o(1).                                  (12.8.9)
```

The conductor dyads cost logarithms.  Summing the permitted `g<=H` crudely
and restoring the physical double-Poisson prefactor
`F^2/D^2=H^(-2)` yields

```text
(F^2/D^2)|K_D^(cond<F)|
 << F^3 H^(1/2)x^o(1)
 <=F^(7/2)x^o(1)=x^(7/8+o(1)).                         (12.8.10)
```

The conductor-one character satisfies the same estimate directly and is
included; no zero-free region, Burgess estimate, or generic Mobius randomness
is being assumed.  The target condition `(d,2e_1e_2)=1` makes `d`, hence
`g,q,r_chi,s_chi`, odd on `K_D`; any finite two-adic cases separated in the
earlier outer identity are outside this off-diagonal family.

For `cond(chi)>=F`, `(12.8.3)` gives
`||b^(hi)||_2^2<<FD^2x^o(1)`.  Substitution into **all five** terms of
Pascadi's theorem, rather than only its favourable terms, gives respectively

```text
F^2D, F^(3/2)D, F^(3/2)D, F^2D, F^(3/2)D.              (12.8.11)
```

Thus `(F^2/D^2)|K_D^(cond>=F)| << F^2D x^o(1)`; the first and fourth
entries are the worst terms and become exactly order `x` at `D=F^2`.

Equations `(12.8.10)--(12.8.11)` are uniform for the source-emitted finite
gcd shells and fixed-log separation parameters.  The multivariable
Mellin/Fourier expansion from Section 12.7 has total `L^1=log^O(1)x`, so it is
absorbed by the fixed power saving.  Consequently

```text
HB4_QTR_CONDUCTOR_PROJECTED_INCIDENCE_THEOREM
 = PROVED_ELEMENTARY_GAUSS_CRT_PLUS_PRIMITIVE_LARGE_SIEVE,

HB4_QUARTER_OFFDIAGONAL_3/8<=delta<1/2
 = PROVED_SOURCE_BACKED_POWER_SAVING,

HB4_QUARTER_OFFDIAGONAL_1/4<delta<1/2
 = PROVED_SOURCE_BACKED_POWER_SAVING,

HB4_EXACT_HALF_ENDPOINT = OPEN_LOG_POWER_ENDPOINT.     (12.8.12)
```

At `D=F^2=x^(1/2)`, the high-conductor term `(12.8.11)` is only `x^(1+o(1))`;
there is no logarithmic saving.  Thus the strict endpoint remains a real gate,
not a limit of the fixed-`delta` theorem.  Also, `(12.8.12)` concerns this
factorized HB4 quarter family only; it is not an all-shape proof of `(SHB-D2)`.

### 12.9 Exact HB2 large-divisor switch and the new bilateral determinant

The old statement that `D>sqrt(x)` requires a theorem for the quotient weight
`mu((mn+2)/r)log r` was too pessimistic.  There is an exact coefficientwise
switch.  Fix a dyadic top `Z`, put `Y=floor(sqrt(Z))`, and for every `N<=Z`
define

```text
A_1(N)=sum_(ef=N,e<=Y) mu(e)log f,

A_2(N)=sum_(e_1,e_2<=Y, e_1e_2f_1f_2=N)
         mu(e_1)mu(e_2)log f_1.                         (12.9.1)
```

The `h=2`, `r=1` precursor in the proof of the modified Heath--Brown identity
of [Ford--Maynard, Lemma 5.2](https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf)
has the exact binomial signs `+2,-1` and gives

```text
Lambda(N)=2A_1(N)-A_2(N).                               (12.9.2)
```

The statement of Lemma 5.2 also sums power indices `r`; it would be incorrect
to call its isolated `r=1` term the prime indicator.  Equation `(12.9.2)` is
the standard `-zeta'/zeta` identity used inside its proof.  Since

```text
Lambda(N)=A_1(N)+L_>(N),
L_>(N)=sum_(d|N,d>Y)mu(d)log(N/d),
```

we obtain the exact switch

```text
L_>(N)=A_1(N)-A_2(N).                                   (12.9.3)
```

The closed endpoint `d=Y` belongs only to `A_1`; there is no half weight.
Moving `sqrt(N)` cutoffs are equally legal, while replacing them by a fixed
dyadic cutoff requires retaining the entire constant-factor square-root
corridor.  Prime powers are already included in `(12.9.2)`.

Now insert `(12.9.3)` into the outer HB4 `h=4,j=2,r=1` quarter cell.  Rename
its variables so that

```text
t=a_1a_2b_1b_2,
outer coefficient=-6 mu(a_1)mu(a_2) log(b_1)/log(t).
```

The switched `A_1` cell has determinant and coefficient

```text
ef-a_1a_2b_1b_2=2,
-6 mu(a_1)mu(a_2)mu(e) [log(b_1)/log(t)] log f.
```

The correction has

```text
e_1e_2f_1f_2-a_1a_2b_1b_2=2,                           (12.9.4)

+6 mu(a_1)mu(a_2)mu(e_1)mu(e_2)
   [log(b_1)/log(t)] log f_1.                           (12.9.5)
```

The symmetric hard cell has all eight literal variables of quarter scale:
four Mobius slots `a_1,a_2,e_1,e_2` and four smooth/log slots
`b_1,b_2,f_1,f_2`.  With `A=a_1a_2`, `B=b_1b_2`, `E=e_1e_2`, `R=f_1f_2`, its
determinant is `ER-AB=2`.

Two coefficient firewalls are essential.  First,

```text
c_Y(E)=(mu 1_([1,Y]) * mu 1_([1,Y]))(E)
```

is not `mu(E)`: for `e_1=e_2=p`, the literal coefficient is `+1` while
`mu(p^2)=0`.  Second, the identity

```text
sum_(f_1f_2=R) log f_1 = (1/2)tau(R)log R              (12.9.6)
```

holds for the complete ordered factorization sum.  On unequal dyadic/smooth
shells define instead the literal truncated ordered convolution

```text
c_Eis^(I,J)(R)
 =sum_(f_1f_2=R) W_I(f_1)W_J(f_2)log f_1.
```

It may be symmetrized only after pairing a shell with its exactly swapped
shell and swapping the weights.  Then
`c_Eis^(I,J)+c_Eis^(J,I)=log(R)c_div^(I,J)` for the paired off-diagonal
shells, while a diagonal shell has the corresponding factor `1/2`.  Neither
identity turns a truncated shell into the full `tau(R)` coefficient.

After the fixed-log separation, the `A_2` correction contribution has the
exact compact normal form

```text
(6/log x) sum_(ER-AB=2)
 c_mu(E)c_mu(A)c_Eis^in(R)c_Eis^out(B)
 rho_x(AB) W(A,B,E,R),                                   (12.9.6a)

c_mu = truncated weighted mu_F * mu_F,
c_Eis = truncated ordered (log W_I) * W_J,
A,B,E,R asymp sqrt(x).
```

Thus the new object is not a generic eight-variable sum: it is two explicit
truncated weighted two-fold Mobius-convolution rows against two
Eisenstein/divisor-log columns at fixed determinant two.  The factor `6/log x` is forced by
`rho_x(AB)=log x/log(AB)` and the literal coefficient `(12.9.5)`.  Exact
swapped-shell pairing can simplify the two `c_Eis` columns, but the literal
ordered form `(12.9.4)--(12.9.5)` controls all bookkeeping.

The full switched error is the coefficientwise combination `A_1-A_2`, not
an independently centred `A_2` term.  It must be combined before any triangle
inequality.  The preassigned comparison contribution, whose all-`D` sum is
the collective hybrid main, is subtracted exactly once from that combined
error.

This switch is a real route improvement: it removes the quotient-Mobius
object and exposes a divisor-log/Eisenstein weight eligible for a joint
Voronoi--Estermann/Kuznetsov treatment.  It does not by itself close the
large-divisor range.  Bettin--Chandee cannot accept both divisor convolutions
as smooth slots; after literal expansion its balanced-quarter error gives no
saving.  Pascadi's coefficient may depend on all three of its displayed
indices, but the literal source map in Section 12.7 compresses only one row;
no simultaneous second-row incidence/range/`L^2` map has been attached.  The
exact state is

```text
LARGE_D_HB2_SWITCH = PROVED_EXACT_COEFFICIENTWISE
LARGE_D_QUOTIENT_MOBIUS_GATE = SUPERSEDED
LARGE_D_TO_CURRENT_BETTIN_CHANDEE
 = STOP_SCOPED_NONSMOOTH_COLUMNS_OR_EXPANDED_SCALE_NO_SAVING
LARGE_D_TO_CURRENT_PASCADI
 = NOT_ATTACHED_SECOND_ROW_INCIDENCE_MAP
HB4xHB2_SIGNED_DIVISOR_VORONOI_DETERMINANT_GATE
 = OPEN_NEW_THEOREM.                                   (12.9.7)
```

The current umbrella gate is

```text
TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE.
```

It has two genuine construction targets, not a list of small repairs:
the exact-half logarithmic endpoint for the conductor-projected HB4 family,
and the bilateral divisor-log determinant beyond the square-root switch.  Neither one
changes the all-shape physical cover, normalization, tail/A/B, actual packet,
or provenance gates, so neither alone triggers TPC-207.

### 12.10 V8 source screen: fixed-unit engine, character obstruction, and route pivot

This section separates three levels which must not be merged: a published
fixed-unit estimate, exact finite algebra showing that its generic moving-unit
lift is false, and two genuinely new structured theorem targets.

#### 12.10.1 What the new fixed-unit theorem really gives

[Blomer--Pascadi, Theorem 1.1](https://arxiv.org/abs/2607.24311) bounds a
critical-length Kloosterman bilinear form at a fixed modulus `c` and fixed unit
parameter by

```text
||alpha||_2 ||beta||_2 c^(31/32+o(1)).                  (12.10.1)
```

At the exact-half scale `D=F^2`, fixing the physical product unit
`A=e_1e_2` and modulus `d` makes the target kernel a literal instance after
unit scaling.  The local saving is therefore

```text
d^(-1/32)=F^(-1/16)=X^(-1/64).                         (12.10.2)
```

This is a real analytic engine, but not an endpoint theorem.  A fixed cell has
scale `F D^(31/32)=F^(47/16)`.  Freezing and taking absolute values over the
`F^2` product units and `F^2` moduli gives `F^(111/16)`, while the raw endpoint
target is `F^6`.  It still misses by `F^(15/16)`.  The same conclusion survives
the exact `g=(h,d)` stratification; it does not supply the lost outer signed
compression.

The critical moving-unit lift is not merely unproved.  With

```text
e_p(t)=exp(2 pi i t/p),
S(m,n;p)=sum_(x mod p)^* e_p(mx+n x^(-1)),
tau(psi)=sum_(y mod p)^* psi(y)e_p(y),
```

every nontrivial multiplicative character satisfies the exact identity

```text
sum_(A mod p)^* chi(A) S(ell,-2h A^(-1);p)
 =tau(conjugate(chi))^2 chi(-2h ell).                   (12.10.3)
```

Thus the unit variable contains a rank-one character eigenmode of magnitude
`p`.  On intervals `H=L=sqrt(p)`, take `P(A)=chi(A)` and character-matched
`h,ell` coefficients.  The trilinear form has size `pHL=p^2`, whereas a
no-cost `L_A^2`-valued version of `(12.10.1)` would give only

```text
p^(1/2) p^(1/4) p^(1/4) p^(31/32)=p^(63/32).
```

It is false by the exact factor `p^(1/32)`.  The independent checker verifies
`(12.10.3)` in `Z[i][Z/13Z]` for a quartic character without floating point.
Consequently

```text
BP2607_FIXED_UNIT_EXACT_HALF_LOCAL_ENGINE
 = SOURCE_ATTACHED_LOCAL_F^(-1/16)_SAVING,

BP2607_AFTER_FREEZE_AND_OUTER_TRIANGLE
 = STOP_SCOPED_F^(15/16)_DEFICIT,

BP2607_ARBITRARY_UNIT_VECTOR_LIFT
 = STOP_SCOPED_FALSE_CHARACTER_EIGENMODE.               (12.10.4)
```

[Pascadi's frequency-concentrated large sieve](https://arxiv.org/abs/2404.04239)
does not repair this: its coefficient uses a fixed-multiplier integer equality,
whereas the physical incidence has moving products and a modular inverse; its
improvement is also in the exceptional spectral slot, not the regular first
and fourth majorants which saturate `(12.8.11)`.
[Pascadi's non-abelian amplification](https://arxiv.org/abs/2511.08445) again
has fixed-unit bilinear inputs, and its modulus average takes an absolute value
before the physical `mu(d)` cancellation can be used.  These are supporting
engines, not direct attachments.

#### 12.10.2 Selected exact-half theorem contract

The physical product-unit coefficient does not have a formal orthogonality to
the bad mode.  On a separated source atom,

```text
P_p(A)=sum_(e_1e_2=A mod p) mu(e_1)mu(e_2)W_1(e_1)W_2(e_2),

P_hat_p(chi)=E_1(chi)E_2(chi),
E_i(chi)=sum_(e_i asymp F)mu(e_i)W_i(e_i)chi(e_i).       (12.10.5)
```

The natural norm of `P_p` is already the norm of a bad character vector.
Pointwise nonconcentration of `(12.10.5)` is therefore insufficient; the new
estimate must exploit a joint signed correlation before the Pascadi
triangle/Cauchy step.

The prime-modulus `g=1` model makes the missing geometry more precise.  For a
single frozen atom put

```text
H(chi)=sum_(|h|<<F)U(h)chi(h),
L(chi)=sum_(|ell|<<F)V(ell)chi(ell).
```

The exact complete-character inversion, before Cauchy, is

```text
G_p=mu(p)/(p-1) sum_(chi mod p)
 tau(chi)^2 conjugate(chi)(-2)
 E_1(chi)E_2(chi)H(conjugate chi)L(conjugate chi).       (12.10.5a)
```

The principal contribution is `O(p^(-1)F^4)=O(F^2)`.  For nonprincipal
characters write `epsilon_p(chi)=p^(-1/2)tau(chi)`.  Then

```text
G_p^hi=mu(p)p/(p-1) sum_(chi!=1)
 epsilon_p(chi)^2 conjugate(chi)(-2)
 E_1(chi)E_2(chi)H(conjugate chi)L(conjugate chi).       (12.10.5b)
```

Define the two literal ratio-incidence vectors

```text
C_1(r)=sum_(e conjugate(h)=r)mu(e)W_1(e)U(h),
C_2(r)=sum_(e conjugate(ell)=r)mu(e)W_2(e)V(ell).
```

Their multiplicative Fourier transforms are `E_1(chi)H(conjugate chi)` and
`E_2(chi)L(conjugate chi)`.  The Gauss multiplier

```text
m_p(chi)=epsilon_p(chi)^2 conjugate(chi)(-2)             (12.10.5c)
```

has absolute value one.  Thus an estimate for arbitrary ratio vectors is
impossible.  Orthogonality and the critical determinant incidence give
`||C_hat_i||_2<<F^(2+o(1))`; plain Cauchy is exactly `F^(4+o(1))` per prime,
which is the known endpoint after the `F^2` moduli and physical `F^(-2)`
prefactor.

The arbitrary character fixture does not supply a fatal actual-class
counterexample.  For source-smooth intervals of length `F=sqrt(p)`, the
Burgess `r=2` estimate, in the form discussed by
[Heath--Brown](https://arxiv.org/abs/1203.5219), gives

```text
H(chi),L(chi)<<F^(7/8+o(1)).                            (12.10.5d)
```

Even the trivial `|E_1E_2|<=F^2` then bounds one character by
`F^(15/4+o(1))=o(F^4)`.  Hence no single character can saturate the actual
prime cell; the unresolved obstruction is broad-spectrum alignment of the two
Mobius ratio vectors under `(12.10.5c)`.  Unsigned fourth moments already have
an `F^4` diagonal floor, so the gain must use the Gauss phase rather than a
smaller unsigned norm.

For every source-emitted product atom, retain the notation of Section 12.8 and
put

```text
C_(g,q)(chi)=E_1(conjugate chi)E_2(conjugate chi)H_g(chi),

L_(g,q)(chi)=tau_q(conjugate chi,1)
 sum_ell W^ell(ell/F)c_g(ell)tau_q(conjugate chi,ell).
```

The selected new theorem is the source-class statement that, at `D=F^2`, for
some fixed `eta>0`,

```text
|sum_(g<=F) sum_(q asymp F^2/g) mu(gq)/phi(q)
  sum_(chi mod q, cond(chi)>=F) C_(g,q)(chi)L_(g,q)(chi)|
 << F^2 D^2 D^(-eta) X^o(1).                           (12.10.6)
```

It must be uniform in every gcd/conductor/cofactor dyad, transform parameter,
actual mask, and source product atom.  Projectors are taken on the complete
residue group; the principal/low-conductor branch remains the already proved
Gauss--CRT route.  The signed `mu(gq)`, Gauss-square phase, fixed physical
shift `2`, and moving unit remain present until the saving in `(12.10.6)` is
created.  No arbitrary unit coefficient is quantified.

Any fixed `eta>0` is enough for the endpoint.  If the fixed-unit
`eta=1/32` survived in this restricted signed family, the physical scale would
be `X D^(-1/32)=X^(63/64+o(1))`; this is a target ledger, not a claim that the
theorem is known.  The frozen status is

```text
HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION
 = SELECTED_PRIMARY_OPEN_NEW_THEOREM.                   (12.10.7)
```

The first proof-or-refutation subgate is therefore

```text
HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE:

|sum_(chi!=1)m_p(chi)C_hat_1(chi)C_hat_2(chi)|
 <<F^(-eta)||C_hat_1||_2||C_hat_2||_2                  (12.10.5e)
```

for the literal source-emitted ratio vectors only.  Per prime this gives
`F^(4-eta+o(1))`; summing `O(F^2)` prime moduli and restoring `F^(-2)` gives
`F^(4-eta+o(1))=X^(1-eta/4+o(1))`.  Since `mu(p)=-1` on this subfamily, the
prime-stage gain cannot be credited to modulus-Mobius cancellation.  It must
come from the inner Mobius ratio structure and the Gauss root-number phase.
No checked source proves `(12.10.5e)`, and no actual-class counterexample was
found.  Its status is

```text
HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE
 = FIRST_SUBGATE_OPEN_NEW_THEOREM_PLAUSIBLE.             (12.10.5f)
```

The construction attempt is now specific.  Parameterize each reduced ratio by
`e=ak, h=bk`.  Long common-`k` fibers are the only place where classical
smooth Mobius cancellation can be harvested after removing `(k,a)=1`;
primitive or short fibers must instead retain both quotient-incidence vectors
inside the quadratic-character fourth-moment mechanism behind
Blomer--Pascadi.  The missing step is a power-saving principal angle between
those two restricted incidence manifolds under the Gauss multiplier.  Results
on Mobius against trace functions just above the critical length, such as
[Korolev--Shparlinski](https://arxiv.org/abs/1804.01337), do not include
`N=sqrt(p)` or this four-factor Gauss correlation, so they are evidence for a
mechanism rather than an attachment.

#### 12.10.3 Independent bilateral road and its own firewall

The exact HB2 switch in Section 12.9 remains an independent parent.  Its first
transform is source-backed, but it is not symmetric between `A_2` and `A_1`.
For one exactly-swapped shell cell, the literal joint object is

```text
H_sigma=(6/log X) sum_(ER-AB=2)
 C_A^(2)(A)D_B^(2)(B)rho_X(AB)Omega_sigma(A,B,E,R)
 [C_E^(2)(E)D_R^(2)(R)-C_E^(1)(E)D_R^(1)(R)],          (12.10.8a)
```

where `C_A^(2),C_E^(2)` are the two literal weighted `mu_F*mu_F` rows,
`D_B^(2),D_R^(2)` are ordered truncated divisor-log columns, while

```text
C_E^(1)(E)=mu(E)W_E(E),
D_R^(1)(R)=W_R(R)log R.                                (12.10.8b)
```

Thus `A_2` has two Estermann/Voronoi columns, but `A_1` has one such column
and one untransformed smooth-log column.  Inventing a second divisor column
for `A_1` changes the physical coefficient and is forbidden.

The ordered column has a legal generalized Estermann compiler.  Put

```text
tau_(u,v)(n)=sum_(rs=n)r^(-u)s^(-v).
```

Mellin inversion writes `c_Eis^(I,J)` as a double integral of
`(-partial_u)tau_(u,v)`.  Pairing the exactly-swapped shell replaces this by
`-(partial_u+partial_v)tau_(u,v)`; the diagonal shell has the corresponding
factor `1/2`.  This preserves the truncated factor weights.  The generalized
functional equation in
[Kaneko, Theorem 2.6](https://arxiv.org/abs/2110.08974) has two polar residues
and two Bessel signs.  At `u=v=0` its polar term is

```text
q^(-1) integral G(x)(log x+2 gamma-2log q)dx.           (12.10.8c)
```

Every Mellin derivative must act on the polar residues, `q` powers,
Gamma/Bessel kernels, and dual coefficients together; appending only a
`log m` to the dual coefficient is not the source formula.

The determinant itself sharply controls the gcd branches:

```text
(A,E)|2,
A=gA_0, E=gE_0, (A_0,E_0)=1, g in {1,2},
E_0R-A_0B=h_g, h_g=2/g.                                (12.10.8d)
```

Hence `g=1` has physical shift `2`, while `g=2` is the unique two-adic common
row and has reduced shift `1`; there is no odd common-row branch.  For
`g_A=(A_0,q)` define the reduced-and-lifted inverse

```text
A_q^sharp=g_A conjugate(A_0/g_A) (mod q),               (12.10.8e)
```

where the inverse is first taken modulo `q/g_A`; define `E_q^sharp`
similarly.  This is the reduced-inverse convention in
[Duke--Friedlander--Iwaniec](https://www.math.ucla.edu/~wdduke/preprints/quadraticdiv.pdf).

With every delta weight, Mellin derivative, gcd power, and Bessel transform
kept inside the displayed `I` weights, the `A_2` first transform has exactly
the following branch skeleton:

```text
c_q(h_g) I^(00)
+sum_(eta_B,b*) S(h_g,-eta_B A_q^sharp b*;q) I^(eta_B,0)
+sum_(eta_R,r*) S(h_g, eta_R E_q^sharp r*;q) I^(0,eta_R)
+sum_(eta_B,eta_R,b*,r*)
 S(h_g,eta_R E_q^sharp r*-eta_B A_q^sharp b*;q)
 I^(eta_B,eta_R).                                      (12.10.8f)
```

These are polar x polar, both one-polar families, and all four dual x dual
families.  The `Y_0Y_0` branch contains the previously displayed kernel

```text
S(h_g,E_q^sharp r* - A_q^sharp b*;q).                   (12.10.8g)
```

The other three Bessel-sign branches and every one-polar branch remain.  In
the complete zero-shift divisor specialization this agrees with DFI equations
(22)--(24), including the extra `K_0` terms.

For `A_1`, only the `B` column is transformed; `R` stays literal:

```text
sum_R c_q(E_0R-h_g)J^0(R)
+sum_(eta_B,b*,R)
 S(E_0R-h_g,eta_B A_q^sharp b*;q)J^(eta_B)(b*,R).       (12.10.8h)
```

Let `Z_2` be the `A_2` polar x polar branch and `Z_1` the `A_1`
Ramanujan/progression zero column.  The only legal main ownership statement is

```text
Z_joint=sum_(sigma,D)(Z_(2,sigma)-Z_(1,sigma))
        -M_cmp^(all-D).                                 (12.10.8i)
```

Neither `Z_2`, `Z_1`, nor a single shell/`D` contribution is independently the
hybrid main.  Therefore

```text
HB4xHB2_PAIRED_VORONOI_FIRST_TRANSFORM
 = DERIVED_SOURCE_BACKED,
HB4xHB2_PAIRED_VORONOI_COLLECTIVE_POLAR_MAIN_IDENTITY
 = OPEN_NEW_ATTACHMENT.                                (12.10.8j)
```

The scale audit identifies the next estimate.  In the balanced cell
`q asymp D_0=F^2`, the generic dual lengths are
`b*,r* asymp q^2/D_0 asymp F^2`.  DFI gives `F^(3+o(1))` for a fixed pair of
complete divisor rows, while the two literal Mobius-row `L^1` ledgers have
product `F^(4+o(1))`.  Row-by-row application therefore gives `F^7`, against
the physical `F^4 log^(-A)X` target.  The first genuinely new family estimate
must jointly recover `F^3`:

```text
sum_(sigma,D)[O_(2,sigma)-O_(1,sigma)]
 <<_A F^4/log^A X,                                     (12.10.8k)
```

where `O_2` contains both one-polar and all four dual x dual branches, and
`O_1` contains the complete one-Voronoi branch.  Consequently

```text
DIRECT_DFI_ROW_BY_ROW = STOP_SCOPED_F7_VERSUS_F4,
HB4xHB2_STRUCTURED_TWO_ROW_KLOOSTERMAN_FAMILY
 = OPEN_NEW_THEOREM.                                   (12.10.8l)
```

This family saving must use the two original factorized Mobius rows.  If the
rows are first compressed into arbitrary residue sequences, the next exact
firewall applies.

If the two rows are first compressed into arbitrary residue sequences, the
kernel becomes `K_q(u,v)=S(-2,u-v;q)`.  Its additive Fourier eigenvalues are
exactly

```text
lambda_k=q e_q(-2k^(-1))  for k in (Z/qZ)^*,
lambda_k=0                 otherwise,                  (12.10.9)
```

so its `L^2` operator norm is `q`.  The checker verifies `(12.10.9)` exactly
for four prime moduli.  Hence generic residue compression destroys the only
structure from which a saving could come:

```text
BP2607_AFTER_NAIVE_RESIDUE_COMPRESSION
 = STOP_SCOPED_ADDITIVE_DIFFERENCE_KERNEL_NORM_Q.
```

The surviving theorem must act before that compression and keep four literal
Mobius slots, both reciprocal-incidence rows, both ordered Voronoi columns,
exactly-swapped shell pairing, shift `2`, and the physical `A_2-A_1`
combination forced by the outer `-6` times the source switch `A_1-A_2`.
For paired shell tuples `sigma`, with the collective main subtracted once, its
minimal contract is

```text
E_sigma=(A_(2,sigma)-A_(1,sigma))-M_(cmp,sigma),

sum_sigma E_sigma << X^(1-eta)(log X)^C.                (12.10.10)
```

The estimate must be uniform over the moving/fixed square-root corridor,
gcd/two-adic branches, Estermann poles and zero modes, Bessel tails, Mellin
losses, and the original `6/log X` normalization.  Thus

```text
HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI
 = OPEN_NEW_THEOREM_PLAUSIBLE_INDEPENDENT_PARENT.       (12.10.11)
```

Equations `(12.10.7)` and `(12.10.11)` have different source locks and cannot
be spliced.  The scheduling decision is to attack `(12.10.6)` first because
its physical source map and saturating terms are already complete, while
developing `(12.10.10)` as the independent fallback.  This is a route pivot,
not an arithmetic advance: fixed-atom credit remains `0`, strict `1/400`
remains unpaid, `L2=NONE`, and `TPC207_TRIGGER=false`.
