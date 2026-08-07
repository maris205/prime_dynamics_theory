# RH-376: The shift-two Chowla boundary for two-site Möbius intervals

RH-376 isolates the first genuinely correlation-hard term inside the RH-371
run hierarchy.  For `sigma` in `{-1,+1}`, the RH-371 count
`C_(sigma,2)(N)` records overlapping odd starts `1<=n<=N-2` for which
`mu(n)=mu(n+2)=sigma`.  It is a two-site same-sign interval count.  It is not
the count of maximal runs of exact length two.

With every sum taken over the same endpoint `1<=n<=N-2`, put

```text
Q2 = sum mu(n)^2 mu(n+2)^2,
U2 = sum mu(n)   mu(n+2)^2,
V2 = sum mu(n)^2 mu(n+2),
D2 = sum mu(n)   mu(n+2).
```

Even starts contribute zero because one of `n,n+2` is divisible by four.
The Boolean identity is therefore exact for every prefix:

```text
4 C_(sigma,2) = Q2 + sigma U2 + sigma V2 + D2.
```

An elementary squarefree-pair sieve gives

```text
Q2/N -> kappa2 = product_p (1-2/p^2).
```

Expanding one squarefree mask and fixing a divisor cutoff before taking
`N->infinity`, Davenport cancellation in each fixed arithmetic progression
gives `U2=o(N)` and `V2=o(N)`.  The tail is
`O(N/R+sqrt(N))`; only after the `N`-limit is taken is `R` sent to infinity.
No growing modulus is used.

The frozen Teräväinen--Walker affine theorem gives logarithmic cancellation
for `mu(m+1)mu(m+3)`.  Abel summation is used in one direction only: if
`D2(N)/N` has a Cesàro limit, that limit must be zero.  Consequently, for
either fixed sign,

```text
C_(sigma,2)(N)/N converges
  iff D2(N)=o(N),
```

and the interval density is then `kappa2/4`.  Thus existence of even one
signed two-site interval density is equivalent to ordinary shift-two Cesàro
Chowla and forces both signs to converge to the same value.

This is a scoped hardness equivalence, not a proof of shift-two Chowla and
not a nonconvergence theorem.  It does not settle any `k>=3` run density, the
RH-371 alternating eight-run envelope, or convergence of the adaptive
capacity `K_N/N`.  It supplies no operator, trace, zero model,
Hilbert--Pólya construction, or proof of RH.  Route A is `GO`; Route B is
`STOP_SCOPED`; Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The checks cover every pointwise pair and cumulative prefix through
`N=2^20`, alignment with the exact RH-371 endpoints through `N=1024`, every
even start, and three frozen rows.  All finite rows are exact reproduction
only, never asymptotic evidence.
