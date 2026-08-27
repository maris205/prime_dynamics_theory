# TPC-281 proof package

## The typed `L2` interface

Let `S=sum_j V_j`.  By the definition of the operator norm,

`||A_X S||_2 <= ||A_X||_(2->2)||S||`
`<= K X^(-sigma) sqrt(G)`.

Squaring and using `G=qD` proves

`||A_X S||_2^2 <= K^2 X^(-2sigma) qD`.

Substitution of `q<=Q_X` proves the two-term interface.  If
`Q_X<=C X^(-kappa)` and `D<=d_+X^a`, substitution proves the collapsed
interface

`||A_X S||_2^2 <= K^2d_+C X^(a-2sigma-kappa)`.

No reverse implication is asserted: an output bound does not manufacture the
operator estimate or a source-level cancellation theorem.

## Scalar readout

For `||lambda||<=1`, Cauchy--Schwarz gives
`|lambda(A_XS)|<=||lambda|| ||A_XS||_2<=||A_XS||_2`.  The scalar lane cannot
exceed the typed output norm, but it can be zero if the readout is orthogonal.

## Exact attachment obstruction

Take a nonzero `S=(S_1,S_2)` in the real plane.  The Riesz representatives
`u_parallel=S` and `u_perp=(-S_2,S_1)` satisfy
`||u_parallel||^2=||u_perp||^2=||S||^2=G`.  Their rank-one functional values
are respectively `G` and zero.  The same packet tuple therefore has identical
`D`, `G`, `q`, `r`, and operator norm, while the squared attachments are
`G^2` and zero.  Any positive lower attachment statement needs an additional
typed nondegeneracy or source-identification hypothesis.

## Finite arithmetic status

The producer uses `Fraction` and canonical JSON.  The independent checker
reconstructs packet sums, energies, operator budgets, attachments, and the
TPC-280 parent rows without importing the producer.  A hostile stress checker
mutates theorem text, vectors, operator budgets, attachment values, parent
binding, and transfer rows; all mutations must be rejected.  These checks are
finite certificate checks, not a proof of the literal growing-source `L2`
estimate.
