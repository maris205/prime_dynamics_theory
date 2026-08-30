# TPC-313 derivation package

Let `U_k` be the first `k` columns of the literal source-profile matrix and
let `W_k=A^T U_k` be its image in the shell coordinates.  Put

\[
 M_k=U_k^{\mathsf T}U_k,\qquad
 B_{k,\tau}(b)=\min_c\{c^{\mathsf T}M_kc:
       \|W_kc-b\|_2^2\le R^2\},
 \quad R^2=\tau^2\|b\|_2^2.
\]

For the finite rows in this paper `M_k` is positive definite on every scanned
prefix.  Fix `rho>0` and define

\[
 c_\rho=(W_k^{\mathsf T}W_k+\rho M_k)^{-1}W_k^{\mathsf T}b.
 \tag{1}
\]

The Lagrangian with multiplier `mu>=0` is

\[
 L(c,\mu)=c^{\mathsf T}M_kc+
 \mu(\|W_kc-b\|_2^2-R^2).
\]

Setting `mu=1/rho` makes its stationarity equation exactly (1).  Completing
the square therefore gives the dual value

\[
 D_\rho(b)=
 \frac{\|b\|_2^2-R^2-b^{\mathsf T}W_kc_\rho}{\rho}.
 \tag{2}
\]

For every feasible `c`, weak duality gives
`D_rho(b)<=c^T M_k c`; hence `D_rho(b)<=B_{k,tau}(b)`.  The paper does
not need to invoke strong duality: its lower bound is a directly checked
rational witness, and its upper bound is a directly checked feasible vector.

## Prefix rule

For each TPC-312 minimum label `b^-`, exact rational least squares is solved
on prefixes `k=1,...`.  The first `k` with residual square at most `R^2` is
`k*`; every earlier residual is checked to be strictly larger.  The positive
control is evaluated on the same `k*`, so the two budget bounds use a common
profile prefix.

## Outward enclosure

Every exact scalar `z` is enclosed by

\[
 [\lfloor z10^{36}\rfloor 10^{-36},
   \lceil z10^{36}\rceil 10^{-36}].
\]

For interval operands, addition, subtraction, multiplication, squaring, and
division use the extrema of the endpoint products/quotients and then apply
the same floor/ceiling operation.  Division is used only when the denominator
interval is strictly positive (or strictly negative).  Thus interval
containment follows by induction on the expression tree.

The producer and independent checker both compute the exact rational
expression and independently repeat this endpoint propagation.  Decimal
strings in the certificate are therefore audit outputs, not unverified
floating-point approximations.
