# RH-378: Safe window memory and online capacity transducers

RH-378 proves four exact finite-memory results for the RH-366 distance-two
capacity problem.

1. A fixed `q`-periodic causal `ell`-window table is universally safe exactly
   when all `q*3^(ell+2)` compatible de Bruijn blocks pass.  Current-zero
   scores have a canonical formal monomial basis with unique coefficients,
   `prod_(j<ell) x_j^alpha_j * x_ell^e`, of dimension
   `2*q*3^(ell-1)`.  This is not an arithmetic minimality theorem.
2. Exactly `13` of the `512` lag-two tables are universally safe.  Their
   six-term Möbius ledger has rank five and relation
   `c22=-c02-c11`.  Seven tables have unconditional limits.  Each of the
   remaining six has a limit iff ordinary shift-two Chowla
   `D2(N)=o(N)` holds.  The two subclass optima are only within these 13
   tables; the larger one is conditional.
3. Two fixed four-state orientation machines output `Smax` and `Smin` for
   every ternary prefix, and `K=max(abs(Smax),abs(Smin))`.  Four states are
   necessary for exact realization of either frozen output stream.  There is
   no single deterministic universally safe causal policy attaining `abs(score)=K` on
   every input branch and every prefix.
4. A stateless contiguous length-15 table is universally safe and reproduces
   either orientation machine on the step-two run-at-most-eight class, which
   contains the Möbius word.  Length 15 is minimal only among `q=1` causal
   contiguous stateless exact-stream realizations on this class.  Nine
   same-parity sigma sites spanning 17 integer positions give the first
   unrestricted counterexample.

The artifact exhausts the 512 lag tables, two 243-row graph lifts, 72 Mealy
safety cases, all 88,572 ternary words of lengths at most 10, four horizons
of deterministic causal policy trees, 512 parity-window assignments, and every Möbius
prefix through `2^20`.  Finite rows reproduce identities; they are not
asymptotic evidence.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

Route A is `GO`; Route B is `STOP_SCOPED`.  RH-378 does not prove
`D2=o(N)` or convergence of the adaptive capacity.  Gates A--E remain
false/open.  There is no intrinsic operator, prime-power trace formula,
zeta-zero identification, Hilbert--Pólya construction, or proof of RH.
