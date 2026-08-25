# Derivation package

For each output group `c`, define

```text
g_c=sum_b lambda_cb v_cb,
s_c=lambda_c*G_c lambda_c=||g_c||^2,
r_c=rho_c sqrt(s_c).
```

Linearity in the second slot gives the literal contraction

```text
sum_b lambda_cb<W_c,v_cb>=<W_c,g_c>.
```

The radius-`rho_c` ball maps under this scalar functional to `r_c Dbar`.  If
`g_c!=0`, a desired `d_c` is realized by

```text
W_c=(conjugate(d_c)/||g_c||^2)g_c.
```

For `R=sum_c r_c>0`, a target `d`, `|d|<=R`, is realized with
`d_c=(r_c/R)d`; if `R=0`, every `g_c` on an active group vanishes and the only
output is zero.

For affine declared lanes `W_c=W_c^0+U_c`, add the fixed center
`C=sum_c<W_c^0,g_c>`.  For one global direct-sum budget, contract to
`g_ext=direct_sum_c g_c` and use radius `rho||g_ext||`.

Finally,

```text
||g_c||<=sum_b |lambda_cb|||v_cb||.
```

Triangle equality holds exactly when all nonzero vectors `lambda_cb v_cb`
belong to one common nonnegative real ray.  Zero-radius groups are omitted
from the global equality test.
