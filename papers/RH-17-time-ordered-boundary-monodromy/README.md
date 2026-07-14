# Time-ordered boundary monodromy

This directory contains the seventeenth-layer paper in the quadratic
prime-dynamics program:

> *Time-Ordered Boundary Monodromy at a Quadratic Band-Merging Map: Exact
> Geometric Cycle Determinants and a Nonuniform-Conditioning Barrier*

The distinguished point `p_(2k)` does not move to another member of the
cross-cycle endpoint dictionary under `S=f^2`.  Instead, its own period-`k`
orbit is an exact closed time chain.  The paper proves the new multiplier law

```text
(S^k)'(p_(2k)) = -C_M lambda^k (1 + o(1)),  C_M > 0,
```

and assigns the inverse-Jacobian weights `omega_j=1/|S'(x_j)|` along that
chain.  The resulting weighted cyclic shift has radius

```text
rho_k = |(S^k)'(p_(2k))|^(-1/k) -> lambda^(-1).
```

After a bipartite one-step lift and removal of the distinguished edge pair,
its determinant is exactly

```text
Pi_(k-1)(rho_k z^2) = 1 + rho_k z^2 + ... + (rho_k z^2)^(k-1).
```

Thus the roots-of-unity phases and the limiting radius `lambda^(-1/2)` have
an exact time-ordered deterministic realization.  This is a cyclic return
shift, not a bare unilateral shift (whose finite determinant is one).

The result is not yet a Feshbach theorem for the noisy Gaussian Markov
operator.  In fact, the diagonal similarity balancing the weighted cycle has
condition number at least `c lambda^k`; at the RH-16 rank scale this is
`Omega(sigma^(-1/2))`.  A successful noisy reduction therefore needs an
adapted norm or a structured Grushin normalization.

In the archived seven-noise comparison, the intrinsic Hellinger half-energy
degree agrees with the RH-15 cloud degree at six points, while the normalized
linear-row degree agrees at four; every discrepancy is one.  Both independent
integer choices nevertheless give finite-cycle radii closer to every cloud
mean than the limiting radius.  These are floating-point diagnostics, not
rank-identification theorems.

Run the tests and audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_time_ordered_monodromy_audit.py
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
