# TPC-281 derivation package

Let `H_X` be a Hilbert space, let `I_X` be a finite or countable index set,
and let

`A_X : H_X -> ell^2(I_X)`

be a linear arithmetic operator.  For four source packets
`V_0,...,V_3 in H_X`, put

`S=sum_j V_j`, `D=sum_j ||V_j||^2`, `G=||S||^2`, and `q=G/D` when `D>0`.

Assume the typed operator hypothesis

`||A_X||_(2->2) <= K X^(-sigma)`

and the source-side bounds

`D <= d_+ X^a`,

`q <= Q_X = B X^(-gamma)+(ell/d)X^(-delta)`.

The Hilbert-space contraction gives

`||A_X S||_2^2 <= K^2 X^(-2sigma)||S||^2`
`= K^2 X^(-2sigma)qD`
`<= K^2 X^(-2sigma)Q_XD`.

Using `Q_X <= (B+ell/d)X^(-kappa)`, where
`kappa=min(gamma,delta)`, and the upper source envelope gives

`||A_X S||_2^2 <= K^2 d_+(B+ell/d)X^(a-2sigma-kappa)`.

For a scalar functional `lambda` on `ell^2(I_X)` with norm at most one,

`|lambda(A_X S)|^2 <= ||A_X S||_2^2`.

This is a typed conditional interface: it becomes an arithmetic theorem only
after the displayed operator bound and the packet attachment are proved for
the literal source.

The attachment issue is independent.  In `R^2`, for any nonzero `S=(S_1,S_2)`
define the rank-one functionals represented by

`u_parallel=S`, `u_perp=(-S_2,S_1)`.

They have equal squared operator norm `G`, but
`<u_parallel,S>=G` and `<u_perp,S>=0`.  Thus neither `(D,G)` nor the operator
norm identifies a positive arithmetic attachment lower bound.
