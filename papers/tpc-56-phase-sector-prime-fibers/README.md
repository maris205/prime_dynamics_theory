# TPC-56: Phase-sector coherent prime fibers

This directory contains the source and final PDF for:

> *A Universal Phase-Sector Selector for Fixed-Shift Coherent Prime
> Fibers: Constant-Energy Extraction, Adaptive Necessity, and the Exact
> Physical Gate*

## Core result

TPC-55 identified the literal fixed-`h0` residual output as a coherent
sum over distinct terminal primes inside each complete output fiber
`y=(gamma,s,j)`.  TPC-56 proves that this coherent square has a universal
constant-energy lower subpacket after one explicit, coefficient-adaptive
phase split.

After removing the exact common output gauge on every active fiber,
partition the gauge-normalized realized terminal amplitudes into `M` equal
phase sectors.
For at least one global sector,

```text
grouped energy of the selected sector
    >= cos(pi/M)^2 / M * full terminal diagonal energy.
```

Among equal finite sectorizations, `M=5` is optimal and gives the exact
constant

```text
(3 + sqrt(5)) / 40 = 0.1309016994...
```

The same sector index is used in the normalized coordinates across all
fibers after their literal common gauges are removed; the corresponding
absolute angular windows are fiber-dependent rotations.  Thus no
maximal-fiber-multiplicity factor appears, and no balanced-cofactor
hypothesis is needed.  A rotating
window gives the slightly larger certified constant
`0.1311275283...`.  A phase-error theorem quantifies stability.

The selector is a genuine coordinate projection after it is chosen, but
its support depends on the realized terminal phases.  On the unrestricted
coordinate space, any coefficient-independent selector retaining two
coordinates in one fiber has a nonzero vector in the collision kernel.
For a literal two-atom carrier with nonzero baseline factors, the free
bounded source phases can realize the same cancellation locally after
scaling.  This is a fiberwise obstruction, not a global no-go for the
coupled literal coefficient class.

## Claim boundary

This is an unconditional finite-dimensional theorem (L0) and an exact
L1 specialization to the already reassembled, fixed-`h0`, literal
terminal-prime fibers.  Relative to a separately proved terminal
activation estimate, the selected packet has zero positive polynomial
coherence loss.

It does **not** prove a lower bound for the undeleted physical output,
terminal activation, balanced-block occupancy, a coefficient-independent
pre-terminal realization of the selector, frozen-to-`h0` localization,
native affine-Gram comparison, a parity improvement, or a twin-prime
result.  Shift averages and favorable signed projective layers are shown
not to provide the missing pointwise lower bound without separate
localization and lower-reassembly theorems.

## Build

Run `pdflatex`, `bibtex`, and two further `pdflatex` passes in this
directory.  The archived PDF is
`phase-sector-selector-fixed-shift-prime-fibers.pdf`.
