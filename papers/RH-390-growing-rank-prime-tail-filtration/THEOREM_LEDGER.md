# RH-390 theorem ledger

## Domain and exact tails

Put

    x=p_y, L=log x>=512,
    V=L^(3/5)(log L)^(-1/5),
    epsilon_x=(27/1000)L^(1801/1000)exp(-(1853/10000)V).

For every exact integer `r>=1`,

    P_r=sum_(p>x)(p^2-1)^(-r),
    J_r=integral_x^infinity dt/((t^2-1)^r log t),
    I_(2r)=integral_x^infinity t^(-2r)dt/log t.

The endpoint is strict: `p=x` is excluded.  The strict Stieltjes and
successor identities are

    P_r-J_r=-E(x)h_r(x)-integral_x^infinity E(t)h'_r(t)dt,
    P_r(y)=(p_(y+1)^2-1)^(-r)+P_r(y+1).

They imply `|P_r-J_r|<=epsilon_x(2x h_r(x)+J_r)`.

## Rank-tail replacement

For exact integers `s>=2`, `K>=1`, and `c in {1,...,7}`, define

    K_r=x^(1-2r)/((2r-1)L), a_r=((2r-1)L)^(-1),
    S_K(a)=sum_(j=0)^(K-1)(-1)^j j!a^j,
    Psi_(c;s,K)=sum_(r<s)c^rP_r/r+sum_(r>=s)c^rK_rS_K(a_r)/r.

The three safe denominator factors are

    A_(s,c)=[(1-x^-2)^s(1-c/(x^2-1))]^-1,
    B_(s,c)=[(1-x^-2)^(s+1)(1-c/(x^2-1))]^-1,
    C_c=(1-c/x^2)^-1.

Tonelli, the strict boundary, the power-kernel mean inequality, and the
exact Laplace remainder give

    |PhiP_c-Psi_(c;s,K)|/K_s
      <=c^s[(4-1/s)A_(s,c)epsilon_x
            +((2s-1)/(2s+1))B_(s,c)/x^2
            +C_c K!/{s((2s-1)L)^K}].

The exponent `s+1` in `B_(s,c)` and the factors `x^2-1` versus `x^2`
are part of the sealed result.

## Full factorial window and endpoint

Let `D=(2s-1)L`, a positive real, and `b_K=K!/D^K`.  For exact integers
`1<=k<floor D`,

    b_(k+1)/b_k=(k+1)/D<=1,

so `K!/D^K<=1/D` throughout `1<=K<=floor D`.  Alternating pairs give
`0<S_K(a_r)<=1` for every `r>=s` in the same window.  The bridge
`L>=512 => x=e^L>2^512>256` puts both prime and surrogate coordinates in
`[0,1/2]^7`.

The endpoint arrays satisfy

    sum |alpha_m|u_m<=7, sum |beta_m|u_m<=49/8,
    ||grad F||_1<126

on the cube.  Hence

    pi^2|GapP-Gap_(s,K)|
      <=126 K_s max_(1<=c<=7){the normalized coordinate bound}.

## Growing-rank theorem

For fixed `0<delta<1`, put

    S_y=floor((1-delta)log L/log 7).

Eventually `S_y>=2`.  Uniformly for exact `2<=s<=S_y`,

    7^S_y<=L^(1-delta), log S_y=o(V), 7S_y epsilon_x<=1/2,
    P_s/K_s->1.

Since `s+1<=L+1<x`, Bernoulli gives a common positive denominator floor;
therefore `A_(s,c)<4`, `B_(s,c)<4`, and `C_c<2`.  The source, power, and
factorial ledgers vanish uniformly, yielding

    as y->infinity,
    max_(2<=s<=S_y,1<=K<=floor((2s-1)L))
      |GapP-Gap_(s,K)|/P_s -> 0.

## All-rank endpoint positivity

For `v_r=(c^r/r)_(c=1)^7`, put `gamma_r=grad F(0) dot v_r`.  Exact
differentiation and the cancellation of the `m=2` term give

    gamma_r=(4/r)[3^r u4-2^r u3+5^r u6-4^r u5
                    +7^r u8-6^r u7
                    +2(u3-u4+u5-u6+u7-u8)].

RH-384 outward rational intervals give positive lower endpoints for
`r=1,...,5`.  Exact cross-products give

    u4/u3>2/3, u6/u5>(4/5)^2, u8/u7>(6/7)^6,

together with `u3>u4`, `u5>u6`, `u7>u8`.  These inequalities prove
`gamma_r>0` for every exact integer `r>=1`.

## Fixed-rank necessity

Fix exact `s>=2` and put `r=s-1`.  Along infinitely many Maynard
consecutive gaps `q-x<=600`,

    x^(2r)[(P_r-I_(2r))_y-(P_r-I_(2r))_(y+1)] -> 1,

and consequently `limsup x^(2r)|P_r-I_(2r)|>=1/2`.  For the common exact
head `H`, the endpoint Hessian ledger is `<224` and

    |F(H+A)-F(H+B)-grad F(0) dot (A-B)|
      <=224||H||_infinity||A-B||_infinity
        +112(||A||_infinity^2+||B||_infinity^2).

The remainder is `o(x^(-2r))`; higher ranks and the full `J-I` tail are
also `o(x^(-2r))`.  Since `gamma_r>0`,

    limsup x^(2r)pi^2|GapP-GapI_(<r)|>=gamma_r/2,
    limsup x^(2r)pi^2|GapP-GapJ_(<r)|>=gamma_r/2.

Because `P_s~x^(1-2s)/((2s-1)L)`, both ratios to `P_s` have infinite
limsup.  This is a fixed-rank statement only in the displayed `P/J/I`
hierarchy.

## Epistemic and claim boundary

The 72 exact rows have role `finite_exact_algebra_not_analytic_proof`.
They check exact algebraic interfaces and mutations; they do not prove
the Johnston--Yang or Maynard inputs, Stieltjes/Tonelli analysis, or an
asymptotic limit.  No growing-`s` necessity, arbitrary surrogate theorem,
convergent factorial series, complex `c`, active `c11`, growing clock,
`K_N`, operator, trace, zeros, or RH conclusion is claimed.  Gates A--E
are false.
