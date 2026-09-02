# TPC-358 derivation package

For the inherited literal component `B_p`, define the signed finite operator
`A_epsilon=sum_p epsilon_p B_p` and the unsigned geometry
`G_u=sum_(p,t) B_p(u,t)^2`.  The frozen normalized operator is

`A#=D_G^(-1/2) A_epsilon D_G^(-1/2)`.

Every fresh row has positive `G_u`, so the congruence is a finite real
symmetric matrix.  For any finite real symmetric matrix `T`,

The two valid inequalities are separately
`||T||_2 <= max_u sum_t |T(u,t)|` and `||T||_2 <= ||T||_F`.  The producer and
reverse-shell checker test both against the explicitly computed all-plus
spectrum.

The fresh origins are not selected from spectral data.  Their only rule is
the fixed arithmetic spacing `52001+100000j`, which makes the comparison a
disjoint origin-scale holdout.  Parent compatibility means closeness to the
TPC-357 finite maxima within tolerance `0.001`; it is not a uniform limit.
