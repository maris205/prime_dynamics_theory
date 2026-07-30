# RH-272: Resolution-clocked monodromy counterloop bridge

This paper extracts a deterministic, operator-derived counterloop from the
weighted boundary cycle.  If `k` is the cycle length and `rho_k` is its
single-value multiplier radius, the edge-deflated factor is

```text
C_k(z) = Pi_{k-1}(rho_k z^2),   Pi_N(q)=1+...+q^N.
```

After Hardy scaling, its `2(k-1)` roots have power moments
`beta_k^n (2k 1_{2k|n}-1-(-1)^n)`.  Since `rho_k -> lambda^{-1}`, the
counterloop subtracts exactly the deterministic pole contribution at every
fixed order before its first alias.  This is an exact graded/superloop
bridge, not a claim that the roots are a spectral submultiset of the noisy
operator.

The noisy spectral-cloud ledger and Gates A--E therefore remain open.

Reproduce with:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
```
