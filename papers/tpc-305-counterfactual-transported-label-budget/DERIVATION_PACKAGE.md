# TPC-305 derivation package

Let `S_L,S_R` be adjacent finite prime shells and let `a_L,a_R` be the locked
source-first binary labels.  On `O=S_L cap S_R`, put

```text
sigma = sign(sum_{p in O} a_L(p)a_R(p)), with sigma=+1 at a zero tie.
```

The two full-shell counterfactual targets are

```text
t_L(p) = sigma*a_R(p) on O, and a_L(p) off O,
t_R(p) = sigma*a_L(p) on O, and a_R(p) off O.
```

Thus the left physical operator is evaluated with `(a_L,t_L)` and the right
physical operator with `(a_R,t_R)`.  The native and transported targets are
compared at `k=max(k_native,k_transport)` where `k_*` is the first source
profile prefix whose least-squares relative RMS is at most the declared tau.

For a fixed operator matrix `V` and source Gram `M`, the finite native budget is

```text
B_(V,k,tau)(b) = min c^T M c
                   subject to ||V_k c-b||_2 <= tau ||b||_2.
```

The TPC-302 ridge/KKT frontier computes this value numerically with an
enclosure.  TPC-305 stores the three normalized ratios
`B(t_transport)/B(t_native)` for each operator.  A ratio below one means the
transported target is cheaper on that fixed operator; a ratio above one means
the native/home target is cheaper.  The orientation rule combines the left and
right statuses into four descriptive classes.

The protocol isolates a target swap inside each operator row, but it does not
hold the two physical operators equal.  Consequently it is a partial
counterfactual control, not a causal decomposition.
