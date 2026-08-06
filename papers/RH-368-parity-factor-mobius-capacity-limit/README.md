# RH-368: Parity-factor Möbius capacity limit

RH-368 extracts a new, strictly scoped theorem from the postcritically finite
quadratic realization in `dyna_zeta_map`.  The three-cell Markov partition has
matrix

```text
A = [[0,0,1], [0,0,1], [1,1,0]],
```

and its binary factor `A_{\{2\}}` consists of sign words whose `+1` positions
all lie in one parity class.  This is a reduced parity factor; it is not the
four-state distance-two constraint used for the RH-366 adaptive capacity.

For a finite Möbius prefix `mu(1),...,mu(N)`, let `K_N^(2)` be the maximum of
the absolute signed sum over this factor.  If `M_N=sum mu(n)`, `P_r` counts
`mu(n)=+1` in residue class `r mod 2`, and `N_r` counts `mu(n)=-1`, then the
finite identity is

```text
K_N^(2) = max_{r in {0,1}} max(|-M_N+2P_r|, |-M_N-2N_r|).
```

Using the prime number theorem in the two parity progressions and the exact
odd/even squarefree densities

```text
S_odd/N -> 4/pi^2,       S_even/N -> 2/pi^2,
```

gives the all-order limit

```text
K_N^(2)/N -> 4/pi^2.
```

The finite `N=2^20` row (`K=425095`, ratio `0.4054021835...`) is a
reproduction diagnostic only; it is not used as asymptotic evidence.

## Route boundary

Route A is `GO`: the PCF parity-factor realization, the exact finite capacity
formula, and the asymptotic limit are independently proved and executable.
Route B is `STOP_SCOPED`: the maximizing sign word reads the complete Möbius
prefix, so this is an adaptive encoding/capacity theorem, not a canonical
arithmetic coupling or operator trace.

This paper does not solve the RH-366 four-state distance-two capacity problem;
that problem remains bracketed but open.  It also does not identify the PCF
zeta factor with a Hasse--Weil factor, a completed-zeta divisor, or a
von-Mangoldt trace.  Gates A--E remain false/open, and no Hilbert--Polya
operator, Riemann-zero model, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

All finite checks are integer/provenance checks.  The asymptotic statement is
the displayed theorem, not a fit to the endpoint row.
