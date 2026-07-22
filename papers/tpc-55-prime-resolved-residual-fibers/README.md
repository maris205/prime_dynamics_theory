# TPC-55: Prime-resolved residual fibers

This directory contains the source and final PDF for:

> *Prime-Resolved Residual Fibers at a Fixed Shift: Exact Grouping SVD,
> Common Möbius Gauge, and Collision-Free Transversals*

## Core result

For the literal fixed-`h0` terminal map, a pre-terminal input is
`u=(m,r,j,gamma)`, its residual label is `s=d(m)r`, and the unique terminal
candidate is `p=(mj+h0)/r`. The paper keeps the full pre-terminal universe,
the terminal-admissible subset, and the physically nonzero subset separate.
Under the inherited row-uniqueness geometry, `D=o(J)`, and for sufficiently
large `X`, it proves that the refined map

```text
u -> (gamma,s,j,p)
```

is injective on one physical source system.  Thus the residual-grouping map
factors exactly, after terminal restriction, into a collision-free
prime-resolved lift followed by the
operation that forgets `p` and sums all terminal primes in the same complete
output fiber `(gamma,s,j)`.

The paper computes the full weighted fiber SVD: every active output fiber has
one visible direction and all orthogonal collision directions form the
kernel.  It gives the exact pseudoinverse, quotient norm, restricted-subspace
angle criterion, and a distinguished-vector coherence identity.

On a cofactor block `r ~ R`, determinant ladders give

```text
max fiber size <= X^(o(1)) (1 + L/R).
```

Consequently, in the balanced range `R >= cL`, whenever the block has
nonzero terminal diagonal energy, a canonical rank-by-prime partition
produces a collision-free subpacket carrying at least an `X^(-o(1))`
fraction of that block energy. This incurs no fixed positive-power rank
loss, but it is only a post-terminal subpacket result: it neither proves
energy occupancy of a balanced block nor lower-bounds the unreduced
coherent sum.

On the inherited coprime squarefree equality support, the two literal
Möbius factors satisfy `mu(d)mu(r)=mu(s)` and hence their product is one
common phase inside a residual fiber. Remaining cancellation is measured
exactly by an explicit physical coherence statistic and can still arise from
the inherited source, mask, profile, and terminal amplitudes.

## Claim boundary

This is an L0 finite-dimensional operator theorem and an L1 structural
specialization of the literal TPC packet. It does not prove terminal
activation, balanced-block occupancy, a lower bound for the full coherent
terminal-prime sum, fixed-shift localization, identification with the native
affine Gram, a parity-sensitive improvement, or a twin-prime result.

## Build

Run `pdflatex`, `bibtex`, and two further `pdflatex` passes in this directory.
The archived paper is `prime-resolved-residual-fibers-fixed-shift.pdf`.
