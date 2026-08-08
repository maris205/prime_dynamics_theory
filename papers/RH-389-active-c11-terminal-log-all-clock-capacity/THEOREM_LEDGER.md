# RH-389 theorem ledger

## Domain and normalization

For every individually fixed integer `q>=1`, let `A_q` be the finite set
of universally distance-two-safe `q`-periodic lag-two table families.  Put

    mu_0(m)=mu(m) for m>=1, and mu_0(m)=0 for m<=0,
    1<=omega(X)<=X, omega(X)->infinity,
    S_X^omega(q,f)
      =(log omega(X))^-1
       sum_(X/omega(X)<n<=X)
       mu(n)f_(n mod q)(mu_0(n-2),mu(n))/n.

The clock `q`, the family `f`, and the admissible `omega` are fixed before
`X` tends to infinity.

## Terminal Abel ledger

If `A(T)=sum_(n<=T)a_n=o(T)`, partial summation gives

    (log omega(X))^-1 sum_(X/omega(X)<n<=X) a_n/n ->0.

The proof covers both lower-endpoint regimes.  If `Y=X/omega(X)>=T`, the
uniform tail bound for `A(t)/t` applies.  If `Y<T`, the lower part has
bounded harmonic mass while `log X/log omega(X)->1`; the remaining upper
part is controlled after the fixed cutoff.  No assumption
`X/omega(X)->infinity` is inserted.

The RH-379 proof supplies the independently valid prefix cancellations for
the `c01`, `c12`, and `c21` channels.  Abel transfer also removes the
corresponding zero-mean decompositions.  This extraction does not invoke
RH-379's phase-limit proposition outside its stated `c11=0` domain.

## Active determinant-two ledger

TPC-137 applies to primitive determinant-two data

    (d,s)=(u,a)=(a,s)=1, su-ad=2,
    (d,s,u,a)=(-2,1,0,1),
    D(n)=n-2, V(n)=n.

After deleting the finite `n<=2` endpoint, both affine forms are positive.
For every fixed periodic residue weight `rho`, the theorem gives

    (log omega(X))^-1
    sum_(X/omega(X)<n<=X) mu(n-2)mu(n)rho(n)/n ->0.

Tao's Theorem 2, equation (3), is upstream Liouville provenance for
TPC-137; TPC-137 itself is the full Mobius-correlation theorem used here.

## Density limit

For each phase `r mod q`,

    delta_(q,r)=lim X^-1 sum_(n<=X,n=r mod q) mu(n)^2,
    theta_(q,r)=lim X^-1 sum_(n<=X,n=r mod q)
                        mu_0(n-2)^2 mu(n)^2.

The cone and totals are

    0<=theta_(q,r)<=delta_(q,r),
    0<=theta_(q,r)<=delta_(q,r-2),
    sum_r delta_(q,r)=6/pi^2,
    sum_r theta_(q,r)=kappa_2=prod_p(1-2/p^2).

Thus every fixed table has the exact limit

    L_q(f)=sum_r[c02(r)delta_(q,r)+c22(r)theta_(q,r)].

## Projection ledger

For a truth set `E`, define

    E^+=E intersect (T x {+1}).

Then `E^+` is a subset of `E`, preserves universal compatibility, and
has nonnegative pointwise finite-`X` gain `z(f^+-f)` at all nine inputs.
The 512 tables project to the eight masks

    0, 4, 32, 36, 256, 260, 288, 292,

with exactly 64 preimages each.  Their `(delta,theta)` weight pairs are

    (0,0), (0,1/2), (1,-1), (1,-1/2),
    (0,1/2), (0,1), (1,-1/2), (1,0).

Directed compatibility is computed from the underlying edge triples:
empty left action allows all eight targets, and a nonempty left action
allows exactly the four targets not containing `+1`.

## Predecessor-charge ledger

The baseline action is `{-1,0}` with phase weight

    H_r=delta_(q,r)-theta_(q,r)/2.

If phase `r` uses an action containing `+1`, compatibility forces phase
`r-2` to be empty.  The density cone gives the exact decomposition

    H_(r-2)-theta_(q,r)/2
      =[delta_(q,r-2)-theta_(q,r-2)]/2
       +[delta_(q,r-2)-theta_(q,r)]/2 >=0.

Translation `r -> r-2` is a permutation of `Z/qZ`; the charged empty
phases are disjoint and the predecessor map is injective.  For `q=1,2`,
the translation is a self-loop and no `+1` action can occur.  Summing the
charge gives

    sum_r phase_weight_r
      <=sum_r[delta_(q,r)-theta_(q,r)/2]
      =6/pi^2-kappa_2/2.

The constant baseline action attains equality for every fixed `q`.

## Reflection and absolute capacity

Input reflection is an involution preserving compatibility.  Its exact
coefficient parity in the order `(c01,c02,c11,c12,c21,c22)` is

    (+,-,-,+,+,-).

Only `c02`, `c11`, and `c22` negate; the invariant `c01`, `c12`, and
`c21` channels have zero terminal limits.  Table 36 reflects to table 72.
Consequently

    G_log(q):=max_(f in A_q)|L_q(f)|
             =6/pi^2-kappa_2/2

for every fixed `q`, and

    sup_(fixed q>=1)G_log(q)=6/pi^2-kappa_2/2

only after the individual fixed-clock limits have been formed.

## Scope and epistemic status

The 602 finite rows have role `finite_reproduction_not_analytic_proof`.
They check interpolation, projection, compatibility, charge, reflection,
and exact interface declarations; they do not prove Davenport, Mirsky,
TPC-137, or Tao.  Fixed-`q` maximization is legitimate because `A_q` is
finite.  No unbounded-`q`/adaptive max-before-limit, ordinary Cesaro,
growing clock, `K_N`, quantitative rate, operator, trace, zeros, or RH
conclusion is claimed.  Gates A--E are false.
