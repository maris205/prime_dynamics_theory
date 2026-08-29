# TPC-298 proof package

## Proposition 1 — projection and angle identity

For each declared row and each prefix with full column rank, the normal
equations give `V_k^T V_k c_k=V_k^T b`.  Hence `V_k c_k=P_k b`, the residual is
orthogonal to `range(V_k)`, and Pythagoras gives

```text
||b||^2 = ||P_k b||^2 + ||(I-P_k)b||^2.
```

Dividing by `||b||^2` proves `r_k^2+cos^2(theta_k)=1` and the stated
principal-angle formula.

## Proposition 2 — nested-prefix monotonicity

The columns of `V_k` are the first `k` columns of `V_{k+1}`.  Therefore
`range(V_k) subseteq range(V_{k+1})`.  The orthogonal projection is the best
approximation in each subspace, so the residual norm cannot increase.  Since
`arcsin` is increasing on `[0,1]`, the principal angle cannot increase either.

## Proposition 3 — finite dimension certificate

The producer computes the exact rational entries of `V_k` before converting to
70-digit arithmetic.  Gaussian elimination over each declared prime modulus
certifies the rank of every prefix.  Agreement of the two moduli is a
redundant finite check, not an asymptotic proof.  The independent checker
reconstructs physical columns source-first and recomputes all threshold
indices and intervals.

## Boundary of the proof

The rank checks are finite numerical certificates.  They do not establish rank
or angle bounds for moving `x`, a growing cutoff family, or the arithmetic
prime-shell reassembly.  In particular, reaching zero residual at the last
finite prefix is not a twin-prime result: it is the consequence of a finite
surjective map when the number of source directions reaches the shell size.
