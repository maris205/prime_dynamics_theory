# TPC-357 proof and scope package

## Proposition 1: finite Schur/Frobenius envelope

For every finite real symmetric matrix `T`,
`||T||_2 <= max_u sum_t |T(u,t)|` and `||T||_2 <= ||T||_F`.  The first
statement follows from the standard induced-norm inequality and symmetry;
the second follows because the squared Frobenius norm is the sum of squared
singular values.  This proposition is exact and independent of the numerical
certificate.

## Proposition 2: finite normalized operator

On every declared row `G_u>0`, so the diagonal square root is a well-defined
positive real number.  Since the raw matrix is symmetric, the congruence is
also symmetric and the proposition applies to it.

## Proposition 3: finite replay certificate

The canonical certificate has 288 unique keys.  It records Schur and
Frobenius values for all four laws, and exact extreme-eigenvalue values for
all 72 all-plus rows.  A reverse-shell implementation independently rebuilds
the matrices and agrees within the declared tolerance.  The exact anchor
checks rational symmetry, positive geometry, and the two-prime shell.

## Proposition 4: scoped obstruction

The normalized all-plus spectral transition census contains 15 increases and
35 decreases (4 flats under the guard).  Therefore the statement “every
declared transition is nonincreasing” is false for this finite ladder.  This
does not imply that a different ladder, a different sign law, or an asymptotic
sequence is nonmonotone.

## Scope firewall

`NUMERICALLY_CERTIFIED_FINITE` is the maximum status.  There is no source
attachment in this paper, no arithmetic reassembly, no fixed-power credit,
no source-uniform masked `L2` theorem, no Route-A/Route-B official evaluator
pass, and no twin-prime conclusion.
