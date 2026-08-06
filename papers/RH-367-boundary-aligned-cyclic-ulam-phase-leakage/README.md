# RH-367: Boundary-aligned cyclic-Ulam structure and phase-local leakage

RH-367 records a narrow, source-locked theorem edge from the postcritically
finite quadratic map

```text
f_u(x) = 1-u x^2,
u^3-2u^2+2u-2=0,
J=[-(u-1),1].
```

Write `r=u-1`, `B_0=[-r,r]`, and `B_1=[r,1]`.  The exact endpoint
identities exchange the two bands.  For every finite cell partition whose
boundary contains `r`, the exact cell-overlap Ulam matrix has the block form

```text
P_h = [[0,A],[B,0]],       P_h s = -s,
```

where `s` is `+1` on `B_0` cells and `-1` on `B_1` cells.  This is a finite
row-stochastic theorem and does not assert an isolated continuum resonance.

If one cell crosses `r`, let `theta` be its fraction in `B_0`.  The projected
sign defect is exactly

```text
1-(2 theta-1)^2 = 4 theta(1-theta),
```

and a cell of width `h` contributes `4 h theta(1-theta)`.  The global
stationary same-band mass and the displacement of a numerically tracked
near-`-1` eigenvalue are phase-dependent finite diagnostics.  The locked scan
has 33 phases at each of `N=256,512,1024,2048`, plus one exact aligned row:
136 rows in total, four aligned and 132 crossing.

## Route boundary

Route A is `GO`: the aligned block/sign theorem, the exact crossing-cell
identity, and the reproducible phase protocol are independently useful and
fully testable.  Route B is `STOP_SCOPED`: the source supplies no common
strong-space projector/resolvent theorem, no continuum perturbation result,
and no canonical arithmetic operator.

The source's fitted square-root-like noise slopes remain finite-range
diagnostics only.  RH-367 does not claim a universal `sqrt(sigma)` law, an
isolated continuum `-1` resonance, a zeta factor, a von-Mangoldt trace, a
Hilbert--Polya operator, a Riemann-zero model, or RH.

## Overlap boundary

RH-3 proves the continuum parity eigenmode and periodogram consequences;
RH-10 studies long-cycle/noise traces and parity-renormalized determinants;
RH-55 proves a folded-Gaussian midpoint--Ulam strong--weak transfer.  None
proves the arbitrary aligned finite-Ulam block theorem together with the
crossing-cell phase defect recorded here.  The overlap ledger is frozen in
`RH_HANDOFF.md`.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The executable artifact checks exact finite identities, all source hashes,
the four-volume foundation hash, phase-scan counts, and the claim firewall.
The imported phase scan is a reproducibility diagnostic, not an asymptotic
or continuum theorem.
