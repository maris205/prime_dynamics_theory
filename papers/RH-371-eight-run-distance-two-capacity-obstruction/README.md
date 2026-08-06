# RH-371: Eight-run reduction and the cyclic pair-ledger obstruction

RH-371 continues the open distance-two capacity from RH-366.  The frozen
capacity is

```text
K_N = max |sum_{n<=N} mu(n) eps_n|,
eps_n eps_{n+2} != (+1,+1).
```

The paper proves an exact identity for every prefix, not a fitted law.  For
`sigma` in `{+1,-1}`, let `C_sigma,k(N)` count odd step-two intervals of `k`
consecutive Mobius values equal to `sigma`, and let `E_sigma(N)` count
`n=2 mod 4` with `mu(n)=sigma`.  The modulo-9 zero forces every odd run to
have length at most eight, and the path MWIS value is exactly

```text
W_sigma(N) = E_sigma(N)
  + C_sigma,1(N) - C_sigma,2(N) + ... - C_sigma,8(N).
```

Consequently the apparently unbounded run hierarchy is reduced to eight
finite-shift frequencies.  Standard squarefree density and `M_N=o(N)` give
the exact convergence criterion, but no theorem in the repository proves the
required Mobius run-combination limit.

The second result is a strict data-type negative.  The period-18 words

```text
u = +++++-++0--+-----0
v = +++++---0--+---++0
```

have the same zero support, composition, and complete ordered three-symbol
pair ledger at every *cyclic* lag, yet their repeated distance-two capacities
are `K_(18q)(u^q)=10q` and `K_(18q)(v^q)=12q`.  The open-prefix ledgers differ,
and the words are not Mobius.  Thus pair data alone is not a sufficient
statistic for this nonlinear capacity in the general periodic ternary class.

Route A is `GO` for these two theorem edges.  Route B is `STOP_SCOPED`: the
optimizer remains an adaptive arithmetic functional, not a canonical trace,
determinant, prime-power ledger, or spectral model.  Gates A--E remain
false/open, and no Hilbert--Polya construction, Riemann-zero identification,
or proof of RH is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The executable checks use an exact linear Mobius sieve, integer path dynamic
programming, cyclic pair counts, and a group-ring polynomial certificate.
They are finite verification only.
