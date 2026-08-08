# RH-387 theorem ledger

## Domain and source

    x = p_y,
    L = log x >= 512,
    c in {1,...,7},
    V(L) = L^(3/5)(log L)^(-1/5),
    epsilon_x = (27/1000)L^(1801/1000)exp(-(1853/10000)V).

Johnston--Yang Theorem 1.4, equation (1.8), printed page 2, supplies

    |theta(t)-t| <= t epsilon_t  (t>=23).

On L>=512, epsilon_t decreases, so the right side may be frozen at
epsilon_x for t>=x. The source constants remain exact fractions in the
certificate.

## Strict endpoint and all-order source transfer

    P_r = sum_(p>x)(p^2-1)^(-r),
    h_r(t) = (t^2-1)^(-r)/log t,
    J_r = integral_x^infinity h_r(t)dt.

The endpoint is strict:

    P_r = integral_(x,infinity) h_r dtheta
        = -theta(x)h_r(x)-integral_x^infinity theta(t)h'_r(t)dt.

Writing E=theta-id and integrating J_r by parts gives

    P_r-J_r = -E(x)h_r(x)-integral_x^infinity E(t)h'_r(t)dt,
    |P_r-J_r| <= epsilon_x(2xh_r(x)+J_r).

This absolute bound is summed before any relative logarithm. Tonelli and
-log(1-z)=sum z^r/r give

    PhiP_c = sum_(p>x)-log(1-c/(p^2-1)),
    PhiJ_c = integral_x^infinity -log(1-c/(t^2-1))/log t dt,
    |PhiP_c-PhiJ_c|
      <= 3c epsilon_x/[xL(1-(1+c)/x^2)]
      < 4c epsilon_x/(xL).

The maximum over c<=7 is 28 epsilon_x/(xL).

## Power-kernel transfer

With I_2r=integral_x^infinity t^(-2r)/log(t)dt, Tonelli gives

    PhiI_c = integral_x^infinity -log(1-c/t^2)/log t dt.

The exact integrand identity and log(1+u)<=u give

    log[(1-c/t^2)/(1-c/(t^2-1))]
      = log[1+c/{t^2(t^2-1-c)}],

    0 <= PhiJ_c-PhiI_c
      <= c/[3x^3L(1-(1+c)/x^2)]
      < 2c/(3x^3L).

The maximum over c<=7 is 14/(3x^3L).

## Cube bridge

    L>=512 => x=e^L>2^L>=2^512>256.
    sum_(n>x)1/(n^2-1) = (1/x+1/(x+1))/2.

The prime logarithmic coordinate is less than 2c/x<1/2; the two integral
coordinates obey even smaller direct bounds. All three vectors and their
joining segments lie in [0,1/2]^7. No x=23 cube claim is made.

## Endpoint map

For m=2,...,8,

    alpha=(-2,2,-2,2,-2,2,-2),
    beta =(1,-2,2,-2,2,-2,2),
    0<u_m<=(9-m)/8,
    C(V)=1+sum alpha_m V_m,
    W(V)=sum beta_m V_m,
    F(z)=2(C(u)-C(u_m exp z_(m-1)))
         -4W(u_m exp z)(1-exp(-z_1)).

The deficits in the defining product for u_m are summable, so u_m>0. The
exact RH-383 endpoint identity defines

    GapP = B_infinity-G(q_y)=F(PhiP)/pi^2,
    GapJ = F(PhiJ)/pi^2,
    GapI = F(PhiI)/pi^2.

The coefficient ledgers are

    sum |alpha_m|u_m <= 7,
    sum |beta_m|u_m <= 49/8.

The three derivative contributions have coefficients 2,4,4. Therefore

    ||grad F||_1
      <= exp(1/2)[2*7+4*(49/8)+4*(49/8)]
      = 63exp(1/2) < 126.

The input norm is l_infinity; its dual gradient norm is l_1.

## Master bounds

    pi^2|GapP-GapJ| <= 126*28 epsilon_x/(xL)
                     = 3528 epsilon_x/(xL),
    pi^2|GapJ-GapI| <= 126*(14/3)/(x^3L)
                     = 588/(x^3L),
    pi^2|GapP-GapI| <= 3528 epsilon_x/(xL)+588/(x^3L).

## Novelty and firewall

RH-386's relative per-order logarithmic estimate requires a finite largest
order. RH-387 instead sums the absolute Stieltjes bound across all orders,
then passes the complete resummation through F. This closes an r-infinite
and partition-infinite interface rather than applying a finite-partition
corollary.

Since

    log(epsilon_x x^2)=2L+O(log L)-0.1853V(L) -> infinity,

the theorem has no P_2-scale, second-order, or cubic coefficient precision.
Complex c, active c11, growing clocks, joint prefix/prime limits,
operators, traces, zeros, and RH are outside scope. Gates A--E are false.
The 42 finite rows have role reproduction_not_analytic_proof.
