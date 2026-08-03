# Roadmap after RH-349

RH-349 proves a fixed two-coordinate incompatibility law.  At

    m_j=k-j,  j=2,3,

the parity/demand ratios have limits

    gamma_j(eta)=C_* C_M lambda^(eta-j).

Hence `gamma_3=gamma_2/lambda`, and no scalar phase balances both.  If the
two actual signed remainders separately satisfy

    Y_j=o(H_(m_j)),  j=2,3,

then the two-order direct subprefix has the exact asymptotic

    (W_2+W_3)/x^(k-3)
      -> [x|a-1|+|a/lambda-1|]/C_M,

where `a=gamma_2(eta)`.  The coefficient is uniformly positive because

    inf_(a>0)[x|a-1|+|a/lambda-1|]=1-1/lambda.

If the physical phase is bounded but does not converge, the same fixed-depth
calculation gives the conditional liminf lower bound

    liminf (W_2+W_3)/x^(k-3)
      >= (1-1/lambda)/C_M.

The route remains conditional: neither actual remainder estimate is proved.
No unconditional full-`E_off` verdict follows from this paper alone.

RH-350 may ask whether the phase-incompatibility law extends to

    j=2,...,J

for fixed `J`, and then whether any slowly growing depth `J=J_k` is legal.
For fixed `J`, the scalar minimax candidate is

    inf_(a>0) max_(2<=j<=J)|a lambda^(2-j)-1|
      =(lambda^(J-2)-1)/(lambda^(J-2)+1).

A growing-depth theorem cannot be copied from RH-349.  It requires a genuine
uniform audit of the parity Taylor remainder, multiplier asymptotic, radial
suppression, `m_j/k->1`, and simultaneous actual-remainder assumptions.
Failure of any uniform source lock must produce a scoped fixed-`J` endpoint,
not an advertised growing-depth result.

Odd orders, upper off-alias orders, actual remainder control, head transport,
unconditional full-direct-prefix behavior, RH-288, and Gates A--E remain
open.
