# RH-391 theorem ledger

## Fixed repeated consecutive-prime gap

Maynard Theorem 1.3, printed page 385/PDF page 3, gives

    liminf_(n->infinity)(p_(n+1)-p_n)<=600.

Since prime gaps are positive integers, infinitely many consecutive gaps
are at most 600.  Finite pigeonhole extraction gives one fixed positive
integer `h_*<=600` and infinitely many edges

    x=p_y, q=p_(y+1)=x+h_*.

No nonconsecutive prime-pair input is substituted.

## Exact same-rank tails and errors

At `x=p_y`, for exact `j>=1`,

    P_j(y)=sum_(p>x)(p^2-1)^(-j),
    I_(2j)(x)=integral_x^infinity t^(-2j)dt/log t,
    J_j(x)=integral_x^infinity dt/((t^2-1)^j log t).

The endpoint is strict.  For the same exact rank `r` at both endpoints,

    E^I_r=P_r-I_(2r), E^J_r=P_r-J_r.

The retained-head coordinates keep `P_j` for `j<r` and use the complete
`I` or `J` tail for `j>=r`.  With the RH-383 endpoint map `F`,

    Delta^I_r=pi^2(GapP-GapI_(<r)),
    Delta^J_r=pi^2(GapP-GapJ_(<r)).

## Linear moving-rank edge

Fix `C>0`.  Along the extracted edges, take exact integers

    r=r_y->infinity, r<=C*x,

and use this identical `r` at `x` and `q`.  Set

    a=(x^2/(q^2-1))^r, rho=(x/q)^(2r).

The exact successor and smooth intervals give

    P_r(y)-P_r(y+1)=(q^2-1)^(-r),
    x^(2r) integral_x^q t^(-2r)dt/log t <= h_*/log x,
    x^(2r) integral_x^q dt/((t^2-1)^r log t)
      <= h_*(1-x^-2)^(-r)/log x=o(1).

Therefore both scalar edge jumps equal `a+o(1)`.  Moreover

    rho/a=(1-q^-2)^r->1,
    log a=-r log(1+2h_*/x+(h_*^2-1)/x^2).

If `r/x->lambda<infinity`, then `a,rho->exp(-2*lambda*h_*)`.
Without that optional limit, `liminf a>=exp(-1200*C)`.

## Uniform gamma direction

For `v_r=(c^r/r)_(c=1)^7`, put `gamma_r=grad F(0) dot v_r`.  Exact
differentiation gives

    gamma_r=(4/r)[3^r u4-2^r u3+5^r u6-4^r u5
                    +7^r u8-6^r u7
                    +2(u3-u4+u5-u6+u7-u8)].

RH-384 outward rational intervals prove

    u4/u3>2/3, u6/u5>(4/5)^2, u8/u7>(6/7)^6,
    u3>u4, u5>u6, u7>u8.

For exact `r>=7`, the last power pair is at least
`7^r*u8_lower/7`; all remaining terms are positive.  Thus

    gamma_r>=kappa_gamma*7^r/r,
    kappa_gamma=4*u8_lower/7>0.0347017856545.

## Integer-tail and Taylor payments

For each fixed `C`, once `x>=x0(C)`, `r>=7`, `r<=C*x`, and `c<=7`,

    P_(r+1)<=4*x^(-2r-1)/(2r+1),
    sum_(j>r)c^jP_j/j
      <=4*c^(r+1)*x^(-2r-1)/((r+1)(2r+1)),
    sum_(j>r)c^jI_(2j)/j
      <=2*c^(r+1)*x^(-2r-1)/((r+1)(2r+1)log x),
    sum_(j>=r)c^j(J_j-I_(2j))/j
      <=4*c^r*x^(-2r-1)/((2r+1)log x),
    ||H||_infinity<=14/x.

The constants are paid by geometric denominators, the eventual bound
`(1-x^-2)^(-r-1)<=2`, and the exact telescope
`sum_(n>x)1/(n^2-1)=(1/2)(1/x+1/(x+1))`.  No prime-number-theorem
estimate and no linear-rank asymptotic `P_r~K_r` is used.

The coordinate jumps satisfy

    x^(2r)(D^S(y)-D^S(y+1))=a*v_r+eta^S,
    r||eta^S||_infinity/7^r->0, S in {I,J}.

On the eventual cube `[0,1/2]^7`, the Hessian ledger is `<224`, and

    |F(H+A)-F(H+B)-grad F(0) dot (A-B)|
      <=224||H||_infinity||A-B||_infinity
        +112(||A||_infinity^2+||B||_infinity^2).

After division by `gamma_r*x^(-2r)`, the cross and square remainders are
bounded by

    18816/(kappa_gamma(2r-1)),
    (2240/kappa_gamma)7^r*x^(2-2r)/(r(2r-1)^2),

and both vanish.  This proves the two gamma-normalized endpoint jumps.

## Natural pair profile and next rank

For any of `E^I`, `E^J`, `Delta^I/gamma_r`, or
`Delta^J/gamma_r`, put

    L=x^(2r)|Q(y)|, R=q^(2r)|Q(y+1)|.

The edge jump gives the exact two-scale mechanism

    a+o(1)<=L+rho*R<=(1+rho)max{L,R}.

Consequently the natural normalized liminf is at least one.  Under
`r/x->lambda`, its unnormalized profile is

    exp(-2*lambda*h_*)/(1+exp(-2*lambda*h_*)).

The coarse linear and sublinear bounds are `exp(-1200*C)/2` and `1/2`.
The one-sided integer upper bound for `P_(r+1)` then makes every raw pair
error divided by `P_(r+1)` tend to infinity.

## Epistemic and claim boundary

The 60 exact rows have role `finite_exact_algebra_not_analytic_proof`.
They check exact algebraic interfaces and mutations; they do not prove
Maynard's theorem, integer/integral comparisons, Taylor's theorem, or an
asymptotic limit.  The result is same-rank and pairwise in the displayed
`P/J/I` hierarchy.  It excludes arbitrary single-vertex schedules,
different endpoint ranks, arbitrary surrogates, `r/x->infinity`,
linear-rank `P~K`, RH-389/TPC-137/Tao, operators, zeros, and RH.  Gates
A--E are false.
