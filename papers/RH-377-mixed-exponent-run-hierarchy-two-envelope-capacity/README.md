# RH-377: Mixed-exponent run hierarchy and the two-envelope capacity boundary

RH-377 expands every RH-371 same-sign run window on its native odd-start
endpoint.  For `I_k={0,...,k-1}` and
`1<=n<=N-2(k-1), n odd`, define

```text
T_(k,S) = sum_n product_(j in S) mu(n+2j)
                  product_(j not in S) mu(n+2j)^2,
H_(k,r) = sum_(|S|=r) T_(k,S).
```

Let `A_k` sum the even layers `r>=2` and `B_k` sum the odd layers
`r>=3`.  Then, exactly at every prefix,

```text
2^k C_(sigma,k) = H_(k,0) + A_k + sigma (H_(k,1) + B_k),
1 <= k <= 8.
```

The deterministic layers are unconditional:

```text
H_(k,0)/N -> Delta_k = e_k/2,
e_k = product_(p odd) (1-k/p^2),
H_(k,1) = o(N).
```

The factor `1/2` is the odd-start density.  It is not an additional local
factor inside `e_k`.  The `H_(k,1)` proof fixes a bounded periodic
prime-square mask, expands it into finitely many fixed residue classes,
uses Davenport cancellation there, and only then removes the cutoff by a
large-prime-square union bound.  It does not use a growing modulus.

All sixteen signed run densities exist simultaneously if and only if the
following thirteen aggregate limits exist:

```text
A_k/N, 2 <= k <= 8,
B_k/N, 3 <= k <= 8.
```

There are 466 formal `|S|>=2` coordinates.  Their thirteen block sums have
formal rank 13 and kernel dimension 453.  This is only a formal linear-map
statement; it does not show that thirteen is the arithmetic minimal
dimension of actual Möbius correlations.  A single sign at one `k>=3`
controls only `A_k+sigma B_k`, not the two aggregates separately.

For the frozen RH-371 capacity, define

```text
U_N = sum_(k=2)^8 (-1)^(k+1) A_k/2^k,
V_N = sum_(k=3)^8 (-1)^(k+1) B_k/2^k,
r_0 = 1/pi^2 + sum_(k=1)^8 (-1)^(k+1) Delta_k/2^k.
```

The exact `P_N,Q_N,U_N,V_N` ledger gives

```text
R_sigma = r_0 N + U_N + sigma V_N + o(N),
K_N/N = 2 r_0 + 2 (U_N + |V_N|)/N + o(1).
```

Thus `K_N/N` converges exactly when the two-envelope quantity
`(U_N+|V_N|)/N` converges.  This criterion is not proved to hold.  Full
mixed-exponent cancellation is sufficient for the conditional constant

```text
2/pi^2 + sum_(k=1)^8 (-1)^(k+1) e_k/2^k,
```

but is not necessary and is not established.

The paper also constructs a second-order stationary ternary chain with
uniform pair law.  It has zero raw moments, iid-uniform square-only moments,
and zero exactly-one-sign masked moments, while one directional two-sign
masked moment equals `8 epsilon/81`.  The witness is synthetic, not Möbius,
and its squarefree marginal does not match Möbius.  It proves only that the
missing layer is not forced by stationarity and ternary algebra alone.

Route A is `GO`; Route B is `STOP_SCOPED`.  No capacity limit, intrinsic
operator, trace formula, Riemann-zero identification, Hilbert--Pólya
construction, or proof of RH is claimed.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The artifact checks 19,680 Boolean cases, the `466 -> 13` exact rank,
1,048,548 odd-window updates, 4,194,304 cumulative signed identities,
262,144 path/capacity prefixes, the rational stationary witness, and a
finite Euler diagnostic.  These finite rows reproduce identities only and
are not asymptotic evidence.
