# Bridge B V17: physical-dual rank barrier and the growing-rank highway

This is an unnumbered route artifact.  It is not TPC-207, a paper, a proof of
the twin-prime conjecture, or an arithmetic `L2` advance.  It continues the
V16 physical-observable gate by asking how much linear state a common stage
carrier must retain before mixing or error estimates are even considered.

The current claim ceiling is

```text
EXACT_ACTUAL_PHYSICAL_DUAL_RANK_GEOMETRY
+ COMMON_FIXED_RANK_CARRIER_STOP_SCOPED
+ GROWING_RANK_SPARSE_CARRIER_SELECTED_OPEN
+ NO_ARITHMETIC_ADVANCE.
```

The physical shift remains fixed at `h0=2`.  Fixed-atom credit is `0`, the
strict `1/400` is unpaid, `L2=NONE`, and `TPC_207_TRIGGER=false`.

## 1. Source lock and quantifier order

Let

```text
p_1=2<p_2<...,
P_k=product_(j<=k)p_j,
G_k=Z/P_k Z,
V_k=C^(G_k).
```

For a physical scale `X`, V16 fixes `k_X` and the interval functional by

```text
p_(k_X) <= sqrt(2X+2) < p_(k_X+1),
ell_X(f)=sum_(X<n<=2X) f(n mod P_(k_X)).                 (1.1)
```

The selected Bridge B theorem has the quantifier order

```text
there exist common stage maps (J_k,Q_k,Err_k)_(k>=j_0)
such that for every sufficiently large X, every active A,
and every declared physical ell, the return and loss ledger hold. (1.2)
```

In particular, `J_k` is chosen before `X`, `A`, and `ell`; it is not a family
`J_(k,X)` fitted separately to each window.  For each declared physical
functional, exact return holds on every `f in V_k`:

```text
ell(f)=Lambda_(X,A,ell)^dyn(J_k f).                     (1.3)
```

This common-map and forall-`f` contract is what makes a rank question
mathematically meaningful.  The historical scale-dependent PBAPT symbol
`J_X` is a different operator and cannot discharge (1.2).

## 2. Exact integer stage band

Fix `k>=2`, put `p=p_k` and `q=p_(k+1)`, and restrict to the integer-scale
subfamily.  Squaring the cutoff in (1.1) gives

```text
p^2 <= 2X+2 < q^2.
```

Because `p,q` are odd, the exact band is

```text
X_k^int
 = {X in Z:
      (p^2-1)/2 <= X <= (q^2-3)/2},                    (2.1)

BANDCOUNT_k
 = cardinality(X_k^int)
 = (q^2-p^2)/2.                                        (2.2)
```

The integer restriction is essential.  For arbitrary real `X`, different
values can define the same set of integers; for example two nearby reals may
give identical `(X,2X] intersect Z`.  The integer subfamily alone is already
sufficient for the lower bound below.

No prime number theorem is needed for growth.  Consecutive odd primes differ
by at least two, hence

```text
BANDCOUNT_k
 = (q-p)(q+p)/2
 >= p+q
 >= 2p_k+2 -> infinity.                                (2.3)
```

The notation `BANDCOUNT_k` is deliberate: the big-road archive already uses
`M_k` for a different divisor-incidence operator.

## 3. No-wrap theorem for `k>=4`

The whole band (2.1) is ordinary rather than cyclic whenever

```text
2 max(X_k^int)=q^2-3<P_k.                              (3.1)
```

For `k=4`, `P_4=210>11^2`.  If `P_k>p_(k+1)^2`, then Bertrand's theorem gives
`p_(k+2)<2p_(k+1)` and, since `p_(k+1)>4`,

```text
P_(k+1)=P_k p_(k+1)
        >p_(k+1)^3
        >4p_(k+1)^2
        >p_(k+2)^2.
```

Thus (3.1) holds for every `k>=4`.  In this range, the coefficient row of
`ell_X` is the literal interval indicator

```text
w_(k,X)(r)=1_(X<r<=2X),  0<=r<P_k.                    (3.2)
```

For all stages, including wrap controls, the exact coefficient is

```text
w_(k,X)(r)
 = floor((2X-r)/P_k)-floor((X-r)/P_k).                 (3.3)
```

## 4. Exact physical-dual rank theorem

Order the scales `X,Y in X_k^int` increasingly and form the endpoint minor

```text
C_(X,Y)=w_(k,X)(2Y).                                   (4.1)
```

For `k>=4`, no wrap applies.  If `Y>X`, then `2Y>2X`, so `C_(X,Y)=0`; while
`C_(X,X)=1`.  Hence `C` is lower triangular with unit diagonal.  Therefore

```text
rank span{ell_X:X in X_k^int}=BANDCOUNT_k.             (4.2)
```

The V16 physical dual family also contains Haar mean.  Every row in (3.2)
vanishes at residue `0`, whereas the constant mean row does not.  Consequently

```text
rank span{mean,ell_X:X in X_k^int}=BANDCOUNT_k+1.       (4.3)
```

This growing family has an exact positive structural feature.  Consecutive
rows differ by only three atoms:

```text
w_(k,X)-w_(k,X-1)
  = -e_X+e_(2X-1)+e_(2X).                              (4.4)
```

Thus (4.3) does not say that all `P_k` residue states must be retained.  It
says that fixed rank is impossible, while a sparse growing basis is available
for the next construction.

Small-stage controls are typed separately.  At `k=2`, the eight wrapped rows
have rank five; at `k=3`, the twelve rows happen to have rank twelve despite
partial wrap.  The asymptotic theorem uses only the uniform no-wrap range
`k>=4`.

## 5. Common-`J_k` rank obstruction

Suppose one linear map

```text
J_k:V_k -> B_k^dyn
```

has exact physical returns for every integer `X` in the same stage band:

```text
ell_X=Lambda_X^dyn composed with J_k.                  (5.1)
```

Then every `ell_X` lies in `range(J_k^*)`.  If mean is also preserved, (4.3)
gives

```text
rank(J_k)>=BANDCOUNT_k+1.                              (5.2)
```

Since the right side tends to infinity,

```text
UNIFORMLY_BOUNDED_RANK_COMMON_EXACT_PHYSICAL_OBSERVABLE_QUOTIENT
  = STOP_SCOPED_STAGE_BAND_DUAL_RANK_OBSTRUCTION.       (5.3)
```

The first quantifier fatal is equally exact:

```text
FOR_EACH_X_THERE_EXISTS_A_FITTED_J_(k,X)
  != THERE_EXISTS_ONE_COMMON_J_k_FOR_ALL_STAGE_X.       (5.4)
```

A rank-one map can trivially fit one functional.  Such a fit is not a common
cocycle, does not transport deletion forcing, and receives no Bridge B credit.
A separately predeclared scale-dependent triangular family remains a reserve
only if it rebuilds a common formula, uniform constants, stage transition, and
the full physical-loss ledger.

## 6. Stronger conditional theorem for all translations

This section is a falsifier for an additional symmetry claim, not an extra
assumption in the current gate.  On `Z/PZ`, let

```text
(T_(P,L)f)(a)=sum_(1<=j<=L)f(a+j mod P),  L>=1.         (6.1)
```

The `m`-th Fourier multiplier is

```text
H_L(m)=sum_(1<=j<=L)exp(2 pi i m j/P).
```

The constant multiplier is `L`, hence nonzero.  For `m!=0`, the multiplier
vanishes exactly when `P` divides `mL`.  There are `gcd(P,L)-1` such nonzero
frequencies, so over `R` or `C`

```text
rank(T_(P,L))=P-gcd(P,L)+1.                            (6.2)
```

Equivalently, over `Q`, multiplication by
`1+z+...+z^(L-1)` in `Q[z]/(z^P-1)` has the same rank.  If all `P` translations
of a length-`L` interval must factor through one `J`, then its rank is at least
(6.2).  For `0<L<P/2`, this exceeds `P/2`; when `gcd(P,L)=1`, `J` must be
injective.

The current Bridge B gate requires anchored actual intervals, not all their
translations.  Therefore

```text
ALL_TRANSLATIONS_CURRENT_GATE = NO.                    (6.3)
```

Equation (6.2) stops only a proposed translation-equivariant low-rank upgrade.
It cannot be used to strengthen the current theorem target after the fact.

## 7. Exact versus approximate return

The rank obstruction uses exact forall-`f` factorization.  Approximate return
is not automatically stopped.  A quantitative version must freeze the
physical dual norm and compare its error with the least positive singular
value

```text
sigma_min^+(T_(P,L))
 = min_(H_L(m)!=0)|H_L(m)|,                             (7.1)
```

or with the appropriate Kolmogorov width of the actual anchored family.
Qualitative `o(1)`, a single fitted trajectory, a modular rank calculation,
or an unfrozen normalization does not supply this stability theorem.

Thus

```text
APPROXIMATE_LOW_RANK_RETURN
  = OPEN_REQUIRES_WIDTH_AND_PHYSICAL_NORM.              (7.2)
```

## 8. Architecture retype

The selected surviving gate is

```text
BRIDGE_B_COMMON_STAGE_GROWING_RANK_SPARSE_CARRIER
  = SELECTED_OPEN_NEW_THEOREM.                          (8.1)
```

Its first candidate dual skeleton is the mean, one base interval row, and the
three-sparse differences (4.4).  It must then close under deletion forcing,
the additive-Fourier functionals, the PBAPT Type-II tests, and backward source
evolution.  For a finite horizon `b>=k`, the canonical falsifier is the dual
hull

```text
H_(k,b)^dual
 = span{
     R_(j:k)^* ell:
     k<=j<=b, ell in declared physical dual family at stage j
   }.                                                   (8.2)
```

The next construction must prove that this hull has controlled growing
dimension, sparse transitions, and physical dual norms.  If one or two
backward-closure steps expand it to rank comparable with `P_k`, the sparse
highway is stopped and Bridge B returns to A1/A2 reserves.

The architecture consequences are deliberately scoped:

- a fixed finite Markov/Ulam dictionary with common exact return is stopped;
- Logistic transfer spaces are normally infinite-dimensional, so Logistic
  itself is not stopped;
- a fixed symbolic alphabet can retain unbounded path memory and is not the
  same thing as fixed linear rank;
- a finite-vertex Bratteli diagram is stopped only if the physical return
  factors through its finite-dimensional level-state vector;
- two-dimensional Hénon phase space is not two-dimensional observable rank;
  only a fixed finite dictionary is stopped;
- Hénon still needs the V16 exact factor/event/measure/functional diagram.

## 9. Canonical V17 status registry

The checker freezes 24 rows, sorted by key with final-LF canonical rows
`key<TAB>value<LF>`:

```text
BRIDGE_B_ACTUAL_INTERVAL_PLUS_MEAN_RANK	PROVED_EXACT_GROWING_BANDCOUNT_K_PLUS_1
BRIDGE_B_ACTUAL_STAGE_BAND_INTERVAL_RANK	PROVED_EXACT_GROWING_BANDCOUNT_K
BRIDGE_B_ALL_TRANSLATIONS_CURRENT_GATE	NO
BRIDGE_B_ALL_TRANSLATIONS_FIXED_RANK_RETURN	STOP_SCOPED_NEAR_PRIMORIAL_RANK
BRIDGE_B_APPROXIMATE_LOW_RANK_RETURN	OPEN_REQUIRES_WIDTH_AND_PHYSICAL_NORM
BRIDGE_B_ARITHMETIC_ADVANCE	NO
BRIDGE_B_BRATTELI_FIXED_VERTEX_RANK	NOT_STOPPED_WITHOUT_LEVEL_STATE_FACTORIZATION
BRIDGE_B_COMMON_STAGE_FIXED_RANK_EXACT_RETURN	STOP_SCOPED_STAGE_BAND_RANK_GROWTH
BRIDGE_B_COMMON_STAGE_GROWING_SPARSE_CARRIER	SELECTED_OPEN_NEW_THEOREM
BRIDGE_B_HENON_FIXED_FINITE_DICTIONARY_EXACT_RETURN	STOP_SCOPED_IF_COMMON_STAGE_RETURN
BRIDGE_B_HENON_GROWING_OBSERVABLE_FAMILY	OPTIONAL_OPEN_EXACT_FACTOR_REQUIRED
BRIDGE_B_INTERVAL_DIFFERENCE_BASIS	PROVED_EXACT_THREE_SPARSE
BRIDGE_B_LOGISTIC_FIXED_FINITE_DICTIONARY_EXACT_RETURN	STOP_SCOPED_IF_COMMON_STAGE_RETURN
BRIDGE_B_LOGISTIC_GROWING_FUNCTION_SPACE	OPEN_REQUIRES_FORCING_AND_LOSS_LEDGER
BRIDGE_B_STAGE_BAND_CARDINALITY	PROVED_EXACT_BANDCOUNT_K
BRIDGE_B_STAGE_BAND_NO_WRAP_K_GE_4	PROVED_EXACT
BRIDGE_B_S_ADIC_FIXED_ALPHABET	NOT_STOPPED_WITHOUT_LEVEL_STATE_FACTORIZATION
BRIDGE_B_TRANSLATED_INTERVAL_CIRCULANT_RANK	PROVED_EXACT_P_MINUS_GCD_PLUS_1
BRIDGE_B_X_SPECIFIC_ONE_SCALE_FIT	STOP_SCOPED_NO_COMMON_COCYCLE
BRIDGE_B_X_SPECIFIC_UNIFORM_TRIANGULAR_FAMILY	OPEN_RESERVE_REQUIRES_UNIFORM_LEDGER
FIXED_ATOM_CREDIT	0
L2	NONE
STRICT_1_OVER_400	UNPAID
TPC_207_TRIGGER	false
```

The final-LF SHA-256 is

```text
8edf44c0af0146acfe9f0cb7e9c1a72f53bc2a05dc852cac11e547db478f2aac
```

Run the exact read-only checker with

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -B research/tpc-big-road/tpc_bridge_b_rank_growth_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_rank_growth_checker.py --check
```

It checks three no-wrap stages, two wrap controls, exact interval and
mean-augmented ranks, the three-sparse difference, 304 small translated
circulants, larger closed-form fixtures, and eight semantic mutations.  These
checks support finite algebra only; (8.1) remains an open new theorem.

## 10. Route verdict

```text
COMMON_STAGE_FIXED_RANK_EXACT_RETURN = STOP_SCOPED
COMMON_STAGE_GROWING_RANK_SPARSE_CARRIER = SELECTED_OPEN_NEW_THEOREM
X_SPECIFIC_ONE_SCALE_FIT = STOP_SCOPED_NO_COMMON_COCYCLE
APPROXIMATE_LOW_RANK_RETURN = OPEN_STABILITY_THEOREM_REQUIRED
ALL_TRANSLATIONS_CURRENT_GATE = NO
TRANSLATION_UNIFORM_LOW_RANK_UPGRADE = STOP_SCOPED
LOGISTIC_GROWING_FUNCTION_SPACE = OPEN
BRATTELI_AND_FIXED_ALPHABET = SCOPE_DEPENDS_ON_LEVEL_STATE_FACTORIZATION
HENON_GROWING_OBSERVABLE_FAMILY = OPTIONAL_OPEN
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
```

The immediate finite gate is to compute the first backward-closed hulls in
(8.2), with the V16 deletion forcing and actual Fourier/Type-II dual family
attached.  Controlled sparse growth is a construction signal; primorial-rank
explosion is a broad falsifier.  Neither finite outcome is arithmetic credit.
