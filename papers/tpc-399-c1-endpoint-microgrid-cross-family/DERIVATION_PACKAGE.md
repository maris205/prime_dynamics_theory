# TPC-399 derivation package

For a prime (pin(Q,2Q]), set (Q=8192), (H=66), exponent one, and
(eta=2). The finite component used by the code is

```text
K_p(u,v) = p (p/Q)^2 H^2/(H^2+(u-v)^2)
            (1_{p | u-v} - 1/(p-1))
            1_{u != v} 1_{p not|u} 1_{p not|v}.
```

Define the finite geometry

```text
G(u) = sum_{p in (Q,2Q]} sum_v K_p(u,v)^2.
```

With the prime shell indexed increasingly, define the two endpoint matrices

```text
M_all_plus          = sum_p K_p
M_alternating_index = sum_p (-1)^index(p) K_p.
```

For each declared rational coefficient,

```text
M_lambda = (1-lambda) M_all_plus + lambda M_alternating_index,
lambda in {7/8, 15/16, 31/32, 1}.
```

This is an exact finite linear-algebra identity. The fractional probes are
modeling probes, not asserted arithmetic characters or sign laws.

At each of the six selected origins, coordinates are divided into eight
blocks of length 128. The fixed `c=3` band retains block pairs whose block
indices differ by at most three. If (S_lambda(o)) is the resulting spectral
diagnostic, the origin spread is

```text
R_lambda = (max_o S_lambda(o) - min_o S_lambda(o)) /
           mean_o S_lambda(o).
```

The local normalization divides entries by (sqrt{G(u)G(v)}). The other
normalizations divide the masked base metrics by the pooled calibration mean,
the current-origin mean, or the first calibration-origin mean.

TPC-399 imports, by hash, the TPC-398 all-origin mean (B_{lambda}^{(398)})
for the same law and normalization. The cross-family errors are

```text
E_cal(lambda)  = mean_calibration(S_lambda) / B_lambda^(398) - 1
E_hold(lambda) = mean_holdout(S_lambda) / B_lambda^(398) - 1.
```

This direct same-law baseline is frozen before the current readout; no scalar
fit or segment interpolation is performed. The within-family transfer is

```text
T(lambda) = mean_holdout(S_lambda) / mean_calibration(S_lambda) - 1.
```

All formulas are finite and scoped to the declared proxy. They do not imply a
growing operator bound, source-uniformity, an arithmetic `L2` estimate, or a
twin-prime theorem.
