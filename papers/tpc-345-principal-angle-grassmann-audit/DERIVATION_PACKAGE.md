# TPC-345 derivation package

Let `N_1,N_2` be the two finite nuisance matrices after stacking the three
rows of TPC-341 and TPC-342.  For either declared weighting, take positive-SVD
orthonormal bases

`text
N_i = Q_i Sigma_i V_i^T,       P_i = Q_i Q_i^T.
`

The nonzero singular values of `Q_1^T Q_2` are the principal cosines
`c_1 >= c_2 >= 0`; the principal angles are
`theta_i = arccos(c_i)`.  Because the observed ranks are 3 and 2, exactly
two angles are reported and one direction is panel-specific.

For a target `Y`, the cross-panel residual is

`text
R(Y,N_i) = ||(I-P_i)Y||_2^2 / ||Y||_2^2.
`

Equal-row weighting replaces every row block `(y_r,n_{r,j})` by
`(y_r/||y_r||, n_{r,j}/||y_r||)` before stacking.  This is a finite
sensitivity transform, not an arithmetic normalization theorem.

If `S_1,S_2` are nonsingular coefficient changes, then
`col(N_i S_i)=col(N_i)`, hence their orthogonal projectors and principal
angles agree exactly.  The implementation checks this numerically with the
fixed upper-triangular shear

`text
S = [[1,1,0],[0,1,1],[0,0,1]].
`

For leave-one-control-out index `k`, replace each nuisance row mean by the
mean over the other eight controls and use the omitted twin output as the
target block.  The same SVD and angle definitions then produce nine
adversarial finite angle pairs per weighting.
