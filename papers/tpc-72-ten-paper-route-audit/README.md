# TPC-72: A Ten-Paper Fixed-Shift Route Audit

This directory contains:

> *A Ten-Paper Fixed-Shift Route Audit: Dependency Closure, Endpoint
> Losses, and the Primitive-Plane Frontier*.

The paper audits TPC-63 through TPC-71 and makes TPC-72 the tenth paper in
the block.

## Main conclusions

- TPC-63--TPC-71 contain no completed L2 arithmetic cancellation theorem.
  They do close necessary L0/L1 interfaces and permanently rule out several
  false routes.
- The represented branch is
  `TPC-63 -> TPC-64 -> TPC-65 -> TPC-66 -> TPC-67`.
- TPC-68 gives abstract certificates for the complete signed missing-native
  operator; `TPC-69 -> TPC-70 -> TPC-71` follows one mixed scalar sector.
- TPC-70 reduces the first cross-key signed coefficient to a primitive
  cofactor-plane sum whose Möbius sign is constant along each prime ray.
- TPC-71 proves an exact divisor lift and two-dimensional Abel certificate.
  The prime number theorem gives cancellation for regular kernels, but the
  actual physical kernel's mass-normalized variation, diagonal tail, and
  complete anchor summation remain open.
- The primitive-plane target is a four-corner scalar contributing to
  `tr(ER)`, not a two-corner entry of the erasure operator. Its bound cannot
  be promoted directly to a pair/star/Perron operator certificate, and the
  normalization must not be applied twice.
- The next operator bridge has three honest options: a direct two-corner
  representation, row-local anchored bounds dominating the relevant stars,
  or complete decorated moments.
- The two branches merge only through physical reassembly. Terminal
  activation, a represented lower frame, missing-mass control, the
  missing-native operator bound, and the nuisance shorting penalty must all
  be proved in one carrier and quantifier scope.
- The complete literal loss must remain strictly below `1/400`; equality is
  not accepted.

## Claim boundary

This is an audit and dependency theorem, not a parity theorem. It proves no
new fixed-shift Möbius saving, no fixed-2 estimate, no prime-pair lower bound,
and no twin-prime conclusion.

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archival PDF is `ten-paper-route-audit.pdf`.
