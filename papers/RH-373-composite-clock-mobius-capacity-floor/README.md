# RH-373: Composite-clock Möbius capacity floor

RH-373 continues the RH-366 distance-two capacity problem.  It gives an
explicit phase selector with clock `q=180` and a finite two-state completion
on the frozen RH-366 graph.  The selected phase set has no pair differing by
two modulo 180, so the selector is admissible for every possible input
sequence.  Squarefree densities in the 180 arithmetic progressions and
Davenport cancellation give the exact unconditional correlation

```text
97/(24*pi^2) = 4/pi^2 + 1/(24*pi^2).
```

Therefore

```text
liminf K_N/N >= 97/(24*pi^2),
```

improving the RH-366 lower floor `4/pi^2`.  The result is a single explicit
certificate; it is not an optimization over all clocks or all transducers.

The paper also records a literal universal-safety completion of the selector
on the four-state RH-366 graph.  The artifact checks all `3240` universal
state/phase/input-pair rows, the one-site condition, exact prefix witnesses
through `N=2048`, and the endpoint `N=2^16`.

Route A is `GO` narrowly.  Route B remains `STOP_SCOPED`: the ordinary limit
of the adaptive distance-two capacity, the supremum over clock families, and
memory-dependent Möbius correlations remain open.  The selector is a
prescribed arithmetic observable depending only on phase and the current
Möbius value, not an intrinsic operator, determinant, prime-power trace,
Riemann-zero model, or proof of RH.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```
