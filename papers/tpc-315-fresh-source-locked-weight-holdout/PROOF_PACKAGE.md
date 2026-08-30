# TPC-315 proof package

## Proposition 1: rational fresh-panel construction

For every declared `(Q,s)`, the vectors `g_p` and Gram entries `G_(p,q)` are
rational, and the Gram matrix is positive semidefinite.

**Proof.**  The source coefficients, kernel values, congruence indicators,
and denominators in the physical formula are rational.  Finite sums and
products preserve rationality.  For any real vector `a`,
`a^T G a = ||sum_p a_p g_p||_2^2 >= 0`.  The producer computes these finite
sums exactly with `Fraction`.  ∎

## Proposition 2: exact sign enumeration

Fixing the first sign to `+1` represents every sign vector modulo global sign.
The Gray traversal visits exactly `2^(m-1)` states for a shell of size `m`,
and its one-bit update maintains the exact quadratic form value.

**Proof.**  The map from the binary reflected Gray code on `m-1` bits to the
last `m-1` signs is bijective.  Flipping coordinate `i` changes
`c^T A c` by `-4 c_i sum_{j != i} A_(i,j)c_j`; the maintained fields update
by the corresponding two-term change.  Induction over the traversal proves
the stored value equals the direct quadratic form at every state.  The
independent checker repeats this enumeration and checks uniqueness of both
extrema.  ∎

## Proposition 3: weighted Gram identity and normalizer

For every finite sign vector `c` and positive weight vector `w`,

    E_w(c)=||sum_p c_p w_p g_p||_2^2,
    D_w=sum_p w_p^2 ||g_p||_2^2>0

whenever one physical component is nonzero.  Moreover `R_(a w)(c)=R_w(c)` for
`a>0`.

**Proof.**  Expand the finite squared norm and substitute the Gram entries.
The diagonal summands are nonnegative and at least one is positive.  A common
positive scale multiplies numerator and denominator by the same square.  ∎

## Proposition 4: rational enclosure for the logarithm

For `0<=z<1`, the 120-term atanh partial sum is below `2 atanh(z)` and the
tail bound in the derivation package is above the remainder.  Range reduction
therefore encloses every `log(p)` used by the declared shells.

**Proof.**  The power series has positive terms.  After the first `N` terms,
each denominator is at least `2N+1`, while the remaining powers form a
geometric series with ratio `z^2`.  Since `y in [1,2)`, `z<=1/3`; adding the
same enclosure for `log(2)` proves the claim.  ∎

## Proposition 5: directed interval soundness

If interval inputs contain their exact values, the stored numerator,
denominator, and ratio intervals contain the exact weighted quantities.

**Proof.**  Four-endpoint multiplication, endpoint addition/subtraction,
and quotienting by an interval avoiding zero are inclusion-preserving.
Outward rounding on `10^-36` preserves inclusion after each operation.
Induction over the finite expression tree proves the statement.  ∎

## Proposition 6: certified finite result

On the fresh panel there are 8 rows, 3 laws, and 2 targets per law.  The
certificate and independent replay establish 24/24 minimum cases strictly
below one and 24/24 all-positive cases strictly above one.  Every adjacent
law interval is disjoint.  The minimum order census is

    VON_MANGOLDT < COUNTING < REDUCED_RESIDUE : 6
    REDUCED_RESIDUE < COUNTING < VON_MANGOLDT : 1
    COUNTING < VON_MANGOLDT < REDUCED_RESIDUE : 1,

and the positive-control census is

    REDUCED_RESIDUE < COUNTING < VON_MANGOLDT : 6
    VON_MANGOLDT < REDUCED_RESIDUE < COUNTING : 2.

These are finite, same-engine statements.  They do not identify a canonical
weight, remove Gram-target dependence, or imply an asymptotic arithmetic or
twin-prime theorem.  ∎
