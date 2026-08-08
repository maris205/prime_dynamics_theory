# RH-388 theorem ledger

## Domain and kernels

    x=p_y, L=log x>=512,
    epsilon_x=(27/1000)L^(1801/1000)
              exp(-(1853/10000)L^(3/5)(log L)^(-1/5)),
    c in {1,...,7},
    1<=K<=floor(3L).

For `r>=2`,

    K_r=x^(1-2r)/((2r-1)L),
    a_r=1/((2r-1)L),
    S_K(a)=sum_(j=0)^(K-1)(-1)^j j!a^j,
    I^[K]_(2r)=K_r S_K(a_r).

The rank-one coordinate is kept exact:

    Psi^[K]_c=cP_1+sum_(r>=2)c^r I^[K]_(2r)/r.

## Strict higher-rank source ledger

For `h_r(t)=(t^2-1)^(-r)/log t` and `E=theta-t`, strict `p>x`
Stieltjes integration gives

    P_r-J_r=-E(x)h_r(x)-integral_x^infinity E(t)h'_r(t)dt,
    |P_r-J_r|<=epsilon_x(2xh_r(x)+J_r).

The bound is used only for `r>=2`.  With
`R(z)=-log(1-z)-z`,

    0<=R(z)<=z^2/[2(1-z)],  R'(z)=z/(1-z).

Tonelli and the exact common denominator imply, for all seven channels,

    |sum_(r>=2)c^r(P_r-J_r)/r| < 60 epsilon_x/(x^3L),
    0<=sum_(r>=2)c^r(J_r-I_(2r))/r < 13/(x^5L).

The constants use

    D_c(x)^-1
      =[(1-x^-2)^2(1-c/(x^2-1))]^-1
      =[(1-x^-2)(1-(1+c)/x^2)]^-1,
    D_c(x)^-1 < 536870912/536797185 <36/35<5/4,
    (7/6)c^2D_c^-1 <294/5<60,
    c^2D_c^-1/5 <49/4<13.

## Exact factorial ledger

With `G(a)=integral_0^infinity e^-v/(1+av)dv`,

    I_(2r)=K_rG(a_r),
    G(a)-S_K(a)=(-a)^K integral_0^infinity
                e^-v v^K/(1+av)dv,
    (-1)^K(I_(2r)-I^[K]_(2r))>=0,
    |I_(2r)-I^[K]_(2r)|<=K_r a_r^K K!.

Summing every `r>=2` gives

    max_c |sum_(r>=2)c^r(I_(2r)-I^[K]_(2r))/r|
      <=(28/3)x^-3/L K!/(3L)^K.

The alternating terms decrease throughout the stated integer window,
so `0<S_K(a_r)<=1`; consequently `Psi^[K]` lies in the real cube
`[0,1/2]^7`.  For

    b_K=K!/(3L)^K,
    b_(K+1)/b_K=(K+1)/(3L)<=1,

induction over the complete window gives `b_K<=b_1=1/(3L)`.
The twelve finite `K` rows are regression fixtures, not this proof.

## Endpoint ledger

For the RH-383 endpoint map `F` on the real cube,

    sum |alpha_m|u_m<=7,  sum |beta_m|u_m<=49/8.

The gradient contributions have coefficients `2,4,4`, hence

    ||grad F||_1<=63 exp(1/2)<126.

The entrywise Hessian contributions have coefficients `2` and
`4+8+4`, hence

    sum_(i,j)|partial_ij F|<=112 exp(1/2)<224,
    |F(z)-grad F(0).z|<=112||z||_infinity^2.

The input norm is `l_infinity`; the dual gradient norm is `l_1`.

## Sufficiency theorem

Define

    GapP=B_infinity-G(q_y)=F(PhiP)/pi^2,
    GapJ=F(PhiJ)/pi^2,
    GapI=F(PhiI)/pi^2,
    GapK=F(Psi^[K])/pi^2.

Then

    max_c |PhiP_c-Psi^[K]_c|
      <=x^-3/L[60 epsilon_x+13/x^2+(28/3)K!/(3L)^K],

and multiplication by the exact endpoint bound gives

    pi^2|GapP-GapK|
      <=x^-3/L[7560 epsilon_x+1638/x^2
               +1176K!/(3L)^K].

Since `P_2(y)~1/(3x^3L)` and `b_K<=1/(3L)`,

    lim_(y->infinity) max_(1<=K<=floor(3log p_y))
      |GapP-GapK|/P_2(y)=0.

This quantifies over every fixed or moving integer `K_y` in the window.

## Bounded-gap necessity

Maynard's Theorem 1.3 implies infinitely many consecutive prime pairs
`x=p_y`, `q=p_(y+1)=x+h`, `h<=600`.  For
`E_y=P_1(y)-I_2(p_y)`, exact succession gives

    E_y-E_(y+1)=1/(q^2-1)-integral_x^q dt/(t^2 log t),
    x^2(E_y-E_(y+1))->1,
    limsup_y p_y^2|E_y|>=1/2.

Also `J_1-I_2=O(1/(x^3L))=o(x^-2)`.  The seven-coordinate jump is

    x^2[(PhiP-PhiI)_y-(PhiP-PhiI)_(y+1)]
      ->(1,2,3,4,5,6,7).

The exact endpoint direction is

    grad F(0).(1,2,3,4,5,6,7)=2X_infinity,
    X_infinity=2u_4-4u_5+6u_6-8u_7+10u_8>0.

Since `PhiP,PhiI=O(1/(xL))`, the Taylor remainder is `o(x^-2)`.
Therefore

    limsup p_y^2 pi^2|GapP-GapI|>=X_infinity,
    limsup p_y^2 pi^2|GapP-GapJ|>=X_infinity,

and both errors divided by `P_2` have infinite limsup.  The artifact's
`1/16` finite witness is eventual and nonsharp; the theorem constants
are `1/2` and `X_infinity`.

## Scope and epistemic status

The necessity result applies only to this frozen `P/J/I` hierarchy.
The finite certificate has role `reproduction_not_analytic_proof`.
It does not prove the source theorems, Stieltjes integration, Tonelli,
the asymptotic limits, or a convergent factorial series.  There is no
`P_3`/cubic precision, complex channel, growing clock, active `c11`,
`K_N`, operator, trace, zeros, or RH conclusion.  Gates A--E are false.
