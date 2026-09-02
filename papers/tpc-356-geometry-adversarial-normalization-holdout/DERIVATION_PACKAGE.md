# TPC-356 derivation package

Let $I=[x,x+N-1]\cap\mathbb Z$, let $S_Q$ be the primes in $(Q,2Q]$, and
write

\[
B_p(u,t)=p\,\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\]

The unsigned geometry energy is

\[
 G_u=\sum_{p\in S_Q}\sum_{t\in I}B_p(u,t)^2.
\]

TPC-355 defines $D_G=\operatorname{diag}(G_u)$ and
$A^\#=D_G^{-1/2}AD_G^{-1/2}$ whenever the finite diagonal is positive.
TPC-356 does not alter this operator.  It changes only the origin-selection
protocol, selecting origins from unsigned pilot geometry before any source
response is evaluated.

For the finite source residual $\beta=\Lambda-b$, either $T=A$ or
$T=A^\#$ satisfies the exact expansion

\[
 \|T\beta\|_2^2=\|T\Lambda\|_2^2+\|Tb\|_2^2
 -2\langle T\Lambda,Tb\rangle.
\]

The reported coefficient is
$\kappa(T)=2\langle T\Lambda,Tb\rangle/
(\|T\Lambda\|_2^2+\|Tb\|_2^2)$.
All remaining statements are finite computations under the inherited V59
source model.
