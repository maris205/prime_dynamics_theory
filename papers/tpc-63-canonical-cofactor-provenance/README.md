# TPC-63: Canonical Cofactor Provenance at a Fixed Shift

This directory contains the source and final PDF for:

> *Canonical Cofactor Provenance at a Fixed Shift: Minimal Faithful
> Relations, Exact Exposure Factorization, and the Single-Band Completion
> Barrier*.

## Main results

- A literal full incidence and its `(m,r)` pair projection are separated.
  Exact finite-scale criteria determine when rectangular completion preserves
  the pre-terminal raw form, the terminal atomic map, or the grouped physical
  operator. These are three different tests.
- The paper constructs the unique least terminal-faithful pair relation when
  such a relation exists. Active spurious crosses are the sharp obstruction;
  if they occur, the full incidence hypergraph is the canonical interface.
- Removing the retained-pair test from the literal terminal predicate gives a
  coefficient-independent maximal eligible relation. Every declared relation
  selects the same native-high carrier as its effective core inside that
  maximal relation; a rectangular terminal operator still needs the separate
  faithfulness test.
- Native-high exposure factors exactly into terminal-support alignment and
  retained-relation completion. The coefficient-uniform constant is a rowwise
  minimum, while the distinguished constant is the corresponding physical
  weighted average.
- The balanced inherited prime band, and every band certified by the old
  freezing inequality, is eventually disjoint from the critical very-high
  face. Retuning to the top critical cofactor scale makes the inherited
  coefficient-blind freezing loss exceed the full `1/400` budget. Even after
  an independently justified retuning, a complete omitted dyadic block makes
  the inherited Brun--Titchmarsh harmonic certificate yield zero fixed-power
  saving.
- Retaining all dyadic labels by orthogonal direct sum gives exact multiscale
  raw-energy coverage at only `O(log X)` label complexity. Erasing those labels
  is a separate reassembly map and is not norm-monotone from below.

## Claim boundary

The incidence identities, relation lattice, minimax laws, and countermodels
are L0. Their specialization to one literal nonzero shift, coefficient field,
and raw atomic norm is L1. The paper does not prove that the inherited opaque
relation already equals the canonical maximal relation, a positive uniform
exposure constant, a fixed-power missing-mass saving, a new Moebius
cancellation estimate, a fixed-shift parity improvement, a prime-pair lower
bound, or a twin-prime result.

## Build

From this directory, run:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archived paper is `canonical-cofactor-provenance-fixed-shift.pdf`.
