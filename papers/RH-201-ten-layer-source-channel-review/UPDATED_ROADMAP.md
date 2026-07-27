# Roadmap after RH-201

## Corrected current coordinate

```text
full Frobenius rank-1/rank-4 Riesz shell             [rejected exactly]

single-source cyclic state                           [proved]
source-observation Riesz channels                     [proved]
outer-edge conjugate quartet                         [finite three-scale support]
canonical balanced quartet                           [exact, contour-relative]
temporal alignment + finite determinant/trace ledger [finite positive]

validated Riesz contours and projector enclosures    [open, next]
interlevel projector/source/residue transport         [open, next]
growing cloud ledger Q                                [open]
all-level physical interface R / Gate A               [open]
Gates B--E                                             [untouched]
```

## Recommended RH-202 target

Put the outer-edge quartets at `sigma=0.04,0.02,0.01` into common
coarse/fine coordinates using the existing embeddings.  Compute and, where
feasible, validate:

1. contour enclosures and Riesz projector ranks;
2. interlevel principal angles after embedding;
3. projector intertwining defects;
4. transported source/observation residues and determinant coefficients;
5. whether a single correspondence survives both left and right channels.

A positive result would create the first actual shell-transport map `H` for
the source-channel packet.  A negative result would show that the fixed outer
quartet is only a local edge diagnostic and that a larger cluster/cloud rule
is required.

## Macro gates

- Gate A: canonical dynamical spectral determinant and intrinsic cloud —
  still open; this batch supplies one finite channel building block.
- Gate B: time-oriented unitary/scattering completion — untouched.
- Gate C: self-adjoint generator and internally derived `T log T` count —
  untouched.
- Gate D: prime-power/von Mangoldt trace identity — untouched.
- Gate E: equality with the completed zeta divisor — untouched.

No Hilbert--Pólya operator, zeta-zero identification, or Riemann-hypothesis
conclusion is asserted.
