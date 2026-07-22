# TPC-53: Literal factor dictionary

This directory contains the source and final PDF for:

> *A Literal Factor Dictionary for Prime-Squarefree Orbit Packets: Exact Atomic Normalization and Certified Interior Overlap*

## Core result

For one explicitly declared representative four-factor direct left packet,
the paper proves the exact coordinate dictionary left conditional in TPC-52:

- the outer coefficient is the literal source coefficient;
- the opposite-row logarithmic base weight is the coefficient-free `e=0`
  weight, while its fixed unary shape remains in both profiles;
- the static mask remains literal;
- direct residue amplitudes and all Mellin normalizations are tracked exactly;
- the norm is the retained-label pre-terminal atomic norm.

A strict reachable-support point yields an explicit positive overlap on a
fixed compact source-row-orbit subpacket. The subpacket has positive geometric
density and zero positive polynomial endpoint cost, so its canonical Mellin
actual direction has bounded condition number.

The paper also proves that positive geometric density need not imply positive
actual energy coverage: an arbitrary bounded source factor, or unbalanced
cofactor multiplicity, may concentrate all energy outside the compatible cell.

## Claim boundary

This is an L1 physical-interface theorem. It does not prove a coherent prime
square, residual-grouping stability, native-Gram identification, a parity
breakthrough, or a twin-prime result.

## Build

Run `pdflatex`, `bibtex`, and two further `pdflatex` passes in this directory.
