# Derivation package

For `N=4H`, the production divisibility condition gives
`M_{0r}=P_minus T_r` and `M_{rs}=-A T_{r-s}` for interior `r,s`, where
`A=P_plus-P_minus`.  The exact diagonal energies are
`D_0=V_minus S_0` and
`D_r=V_minus S_r+V_plus(S_r-T_r^2)` for `r>=1`.

Writing the locally normalized matrix as `Z=[[0,q^T],[q,C]]`,
`||q||^2<=4/(a_min^2 H)` follows from `S_r>=H/4`,
`sum T_r^2<=S_0`, `P_minus^2<=m_minus V_minus`, and
`V_minus>=m_minus a_min^2`.  The interior row sum is at most
`16|A|/V_minus`, because `D_r>=V_minus H/4` and the two-sided kernel sum is
at most `4H`.  The triangle inequality gives the stated full finite bound.
