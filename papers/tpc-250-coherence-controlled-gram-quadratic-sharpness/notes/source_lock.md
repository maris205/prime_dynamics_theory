# Source Lock

Observed handoff SHA-256:

```text
75fe9219197b41a54271df2ce4d1f15d20cd5fccd500c0a4cf4527f43c8f7357
```

TPC-249 supplies only the literal shared-lane identities

```text
g_c=sum_b lambda_cb v_cb,
||g_c||^2=lambda_c^* G_c lambda_c.
```

With the inner product conjugate-linear first, the expansion is
`sum_(b,b') conjugate(lambda_cb) lambda_cb' <v_cb,v_cb'>`; the weights in
`g_c` are not conjugated.  TPC-250 derives a finite coherence envelope from
this quadratic.  It imports no estimate for actual V59 coherence or Gram
asymptotics.

The task supplied baseline HEAD
`1e68dd6df622f7f9b715d3b967474541c1f86ad2`.  It is recorded but not queried
through Git because all Git actions were forbidden by the write envelope.
