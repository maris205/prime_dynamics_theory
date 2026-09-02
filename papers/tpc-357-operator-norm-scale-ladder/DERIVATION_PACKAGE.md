# TPC-357 derivation package

## Operator

For an interval `I` and shell `S_Q={p:Q<p<=2Q}`, inherit the literal finite
component `B_p` and signed matrix `A_epsilon` from TPC-355.  The frozen
position-aware matrix is

`A# = D_G^(-1/2) A_epsilon D_G^(-1/2)`,

where `G_u=sum_(p in S_Q,t in I) B_p(u,t)^2`.  Every audited diagonal entry is
positive by the producer and reverse-shell replay.

## Finite inequalities

For a real symmetric finite matrix `T`, the induced Euclidean operator norm is
the largest absolute eigenvalue.  The row-sum inequality gives

`||T||_2 <= ||T||_infty = max_u sum_t |T(u,t)|`,

because `||T||_1=||T||_infty` for a symmetric matrix and
`||T||_2^2 <= ||T||_1||T||_infty`.  The singular-value/Frobenius inequality
also gives `||T||_2 <= ||T||_F`.

These are finite algebraic inequalities; they do not provide a uniform bound
when the interval, origin, shell, or normalization changes.

## Scale audit

For each fixed `(origin,Q,exponent)` the four counts form a sequence.  The
producer labels a transition as increase, decrease, or flat using an absolute
guard `10^-6`.  The declared replay has 54 transitions.  The normalized
all-plus spectral sequence has 15 increases, 35 decreases, and 4 flats.  Thus
the finite monotone-decay hypothesis is rejected on this ladder, while the
operator-uniform theorem remains open.
