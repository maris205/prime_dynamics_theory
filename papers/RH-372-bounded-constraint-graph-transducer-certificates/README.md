# RH-372: Bounded constraint-graph transducer certificates

RH-372 generalizes the finite-capacity part of RH-366 without claiming a
limit for its distance-two optimizer.  Let `G=(V,E)` be a finite directed
constraint graph and let `ell:V->Z` be a bounded vertex observable.  For a
Mobius prefix `mu(1),...,mu(N)`, the open capacity is

```text
K_N(G,ell) = max_path |sum_(n<=N) mu(n) ell(v_n)|.
```

The first theorem is an exact max-plus recurrence in `O(N |E|)`.  The second
theorem considers a finite-memory transducer with a clock `r=n mod q`.  It is
universally safe when every possible input pair in `{-1,0,1}^2` produces an
edge of `G`.  If the observed label is the one-site factor `g_r(mu(n))`,
then squarefree densities in arithmetic progressions and Davenport's fixed
frequency Mobius estimate give

```text
lim (1/N) sum_(n<=N) mu(n) ell(v_n)
  = 1/2 sum_(r mod q) delta_(q,r) [g_r(1)-g_r(-1)],

delta_(q,r) = sum_{d: (q,d^2)|r} mu(d)/lcm(q,d^2).
```

The certificate is therefore a rigorous lower bound on `liminf K_N/N`.
For fixed clock and memory budgets, all finite transducer tables can be
exhausted exactly.  The artifact checks the RH-366 four-state graph, the
RH-368 three-cell parity-factor graph, and a distinct q=3 safe-switch on the
RH-366 graph.  The latter has a two-state universal-safety completion, limit
constant `9/(4 pi^2)`, and uses the two equal-length loops `0000` and `0210`.

This is a bounded classification theorem, not a classification of all mixing
subshifts.  If the observable depends on transducer memory, the displayed
formula is intentionally inactive: higher-order Mobius correlations would be
needed.  The transducers read the arithmetic prefix offline and do not define
a canonical operator, determinant, prime-power trace, or Riemann-zero model.
Route A is `GO` narrowly; Route B is `STOP_SCOPED`; Gates A--E remain
false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

All generated rows are finite verification or source-lock records.  The only
asymptotic inputs are the explicitly cited squarefree progression density and
Davenport cancellation theorem.
