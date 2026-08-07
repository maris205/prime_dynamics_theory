# RH-385 Theorem Ledger

## Frozen inputs

| ID | Input | Immutable origin | Status |
|---|---|---|---|
| I1 | Uniform Davenport estimate `D(X)<<_A X(log X)^(-A)` for every fixed `A>0` | RH-366 release `0396fab9...` and classical sources | locked |
| I2 | Exact six-term ternary interpolation and universal safety interface | RH-378 | locked |
| I3 | Phasewise `c11(r)=0` fixed-clock limit, max-plus optimizer `G(q)`, all-clock endpoint `B_infinity`, and positive square-clock optimizers | RH-379 | locked |
| I4 | One-site squarefree progression densities | RH-375 | locked |
| I5 | RH-384 immutable 51-file closure plus RH-384 and RH-366 standard-eight sets | 67 release blobs, never mutable root policy files | PASS |

## Exact definitions

```text
mu_0(m) = mu(m) for m>=1, and 0 for m<=0,
S_N(q,f) = N^-1 sum_{n<=N} mu(n) f_{n mod q}(mu_0(n-2),mu(n)),
L_q(f) = sum_{r mod q} [c02(r) delta_{q,r}+c22(r) theta_{q,r}].
```

The family `F_q` consists exactly of universally distance-two-safe,
`q`-periodic lag-two tables with `c11(r)=0` separately at every phase.

## New theorem edges

| ID | Claim | Proof edge | Status |
|---|---|---|---|
| T1 | Exact conservative bound `4 sqrt(Q)D_*/N+13 tau_P+6Q/N+4/N` | periodic cutoff, normalized DFT, squarefree tails, period discrepancy, zero-padding endpoints | proved |
| T2 | `sup_{q<=floor(log^B N),f}|S_N-L_q|->0` for every fixed `B>0` | `P=floor(sqrt(log log N))`, `M_P=log^{o(1)}N`, fixed `A>B/2` in Davenport | proved |
| T3 | `sup_{q<=floor(log^B N)}|G_N(q)-G(q)|->0` | finite-family max inequality applied to T2 | proved |
| T4 | `max_{q<=floor(log^B N)}G_N(q)->B_infinity` | T3 plus fixed-clock approximation to the RH-379 supremum | proved |
| T5 | Nonempty square-clock diagonal tends to `B_infinity` | `y_B(N)->infinity`, RH-379 positive optimizer, T2 | proved |

## Conservative ledger

For `N>=3`, `P>=2`, set

```text
eta_P(m)=prod_{p<=P}(1-1_{p^2|m}),
M_P=(prod_{p<=P}p)^2,
Q=lcm(q,M_P),
tau_P=sum_{p>P}p^-2,
D_*(N)=max_{X in {N,N-2}} sup_alpha |sum_{n<=X}mu(n)e(alpha n)|.
```

`Q` is a valid common period, never asserted minimal. The five channels pay:

| Channel | Fourier | Tail | Period | Padding |
|---|---:|---:|---:|---:|
| `c01` | 1 | 0 | 0 | 0 |
| `c12` | 1 | 1 | 0 | 0 |
| `c21` | 2 | 2 | 0 | 2 |
| `c02` | 0 | 2 | 2 | 0 |
| `c22` | 0 | 8 | 4 | 2 |
| **Total** | **4** | **13** | **6** | **4** |

The tail total is `8+5`: finite-to-mask costs `1+1+2+4`, and comparison of
the two limiting means costs `1+4`. For positive `m`,

```text
0 <= eta_P(m)-mu(m)^2 <= sum_{p>P} 1_{p^2|m},
sum_{m<=X}(eta_P(m)-mu(m)^2) <= X*tau_P.
```

Thus no `sqrt(N)`, `pi(sqrt(N))`, or `N^-1/2` term occurs. The normalized
DFT estimate retains its necessary sup norm:

```text
sum_a |hat w(a)| <= sqrt(Q)*(Q^-1 sum_r |w(r)|^2)^(1/2)
                 <= sqrt(Q)*||w||_infinity.
```

## Endpoint and diagonal contract

Only `n=1` contributes the two padding costs: `eta_P(-1)=1` whereas
`mu_0(-1)=0`; at `n=2`, `eta_P(0)=mu_0(0)=0`. For
`q_y=4 prod_{i<=y}p_i^2`, the first square clock is `q_1=36`. Before the
clock budget reaches 36 the exact sentinel is `no_square_clock_available`.
Only afterward is `y_B(N)=max{y:q_y<=floor(log^B N)}` defined.

## Nonclaims

No unrestricted `q`, `q=N^epsilon`, varying `B(N)`, active phasewise `c11`,
effective threshold, adaptive `K_N/N`, projectively compatible selector,
operator, trace, zero identification, or RH assertion is made. The cubic
corollary inherited from RH-383/RH-384 is context, not an RH-385 discovery.
