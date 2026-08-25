# Source Lock

Observed repository baseline:

```text
2654b470d2ba3d62c09a8cf1923254886dd92ead
```

Observed `TPC_HANDOFF.md` SHA-256:

```text
c0460de36fb09655078b6040f501539a63515eebe4667b65e666995b7810912f
```

Frozen source object:

```text
H=C^I, I finite nonempty,
I=disjoint_union_d J_d with every J_d nonempty,
beta_b=P_b beta,
A_cb=P_c A_x P_b,
v_cb=A_cb beta_b,
w_c=P_c w,
lambda_cb=1,
g_c=sum_b v_cb=P_c A_x beta,
C_x=<w,A_x beta>=sum_c <w_c,g_c>.
```

The same complete declared partition indexes `b` and `c`.  The flat direction
`u_c=|J_c|^(-1/2)1_(J_c)` is relative only to that declared block.  It is not
V59-canonical and not the TPC-219 object.  TPC-250 is applied only after
projection and with its `mu=0` empty-pair convention.  An external `E` is an
independent conditional input.

No Git mutation, staging, commit, rebase, or push is authorized.  All writes
are confined to the new TPC-251 project directory.
