# TPC-149: Small-polylog determinant-two Mobius corridor

Paper title:

> *A Small-Polylogarithmic Determinant-Two Mobius Corridor:
> Uniform Actual-Core Cancellation with Bounded Periodic Data*

## Main theorem

There are absolute constants `eta_0,kappa_0>0` such that, for every
sufficiently large ambient scale `X`, outside one local exceptional
set of normalized
logarithmic measure `O((log X)^(-kappa_0))`, one has uniformly

```text
(a*s/N) *
|sum_{N < a*d+a*s*z <= 2N}
   mu(d+s*z) mu(u+a*z) rho(z)|
  << ||rho||_infinity * (log X)^(-kappa_0)
```

for all determinant-two data

```text
a,s,R positive integers, d,u integers,
gcd(a,s)=1, a*s odd, s*u-a*d=2,
```

and all bounded periodic `rho` of period `R` satisfying

```text
a*s*R <= (log X)^(eta_0).
```

The theorem follows by combining:

- the exact quotient-Mobius functions from TPC-148;
- Tao--Teravainen Theorem 3.1 in its general nonpretentious branch;
- the density-normalized periodic reassembly theorem of TPC-147; and
- a union bound over unique ordered pairs `(a,s)` only.

The exceptional set does not need to be unioned over intercepts,
residues, periods, or values of `rho`, because the source exceptional
set for a fixed multiplicative-function pair is uniform in the
allowed modulus, residue and shifts.

## Exact boundary

This is a proved L1 theorem on the literal determinant-two Mobius
periodic core.  It does not assert that the current frontier archive
has supplied its missing occurrence lift.  It also does not cover a
nonperiodic physical multiplier, a generic additive phase, an
arbitrary interval or all prefixes, or the four-point Fejer kernel.
It has zero fixed-X-power exponent and is not positive L2, `1/400`,
a prime-pair theorem, or a twin-prime theorem.

## Reproduce

Run TPC-147 and TPC-148 first, then:

```powershell
python experiments/tpc149_actual_core_corridor_audit.py
python experiments/tpc149_actual_core_corridor_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-149-small-polylog-determinant-two-mobius-corridor.pdf`
