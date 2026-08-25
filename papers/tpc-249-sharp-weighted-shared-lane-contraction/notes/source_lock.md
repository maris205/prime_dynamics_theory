# Source lock

TPC-248 explicitly leaves the contraction
`g_c=sum_b lambda_cbv_cb` as the next problem, with
`v_cb=A_cb beta_b` from TPC-247.  Because the physical covariance is
`<W_c,v_cb>` and the inner product is linear in its second slot, the same
weights enter `g_c` without conjugation.

Centered lane balls are the exact TPC-248 geometry.  An affine nominal lane
plus a ball is separately labeled `MODELING_CHOICE`; it is not asserted to be
the literal V59 uncertainty family.
