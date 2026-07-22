# Updated roadmap after RH-94

## What RH-94 removes

RH-93 started one four-step window from an ambient leading packet. RH-94 moves
the only seed to time zero. The seed is intrinsic to the source because the
initial memory Gramian is `S* S / ||S||_F^2`, and its leading packet is the
source's leading right singular subspace.

Four projected-cross directions then carry the packet through the entire
prefix to every RH-93 endpoint. No later ambient eigenspace is inserted.

## Two distinct widths

- `D2` remains the economical late-block contraction gate from RH-93.
- `H4` denotes robust source-to-endpoint tracking by a width-four recursive
  horizon chain.

The finite data support both statements, but they answer different questions.
Two directions suffice for the selected four-step contraction budget; four
directions are the first tested width that stays near the ambient endpoint
reference after the complete prefix.

## Preferred next gate: reduced projected-cross Gram

For `P=VV*` and `K=(I-P)GV`,

    K* K = V* G^2 V - (V* G V)^2.

Thus the singular values and right singular vectors selecting the complement
directions are determined by an `r x r` positive Gram matrix. RH-95 should
turn this identity into a complete reduced factorization, quantify the effect
of small cross singular values, and identify precisely which ambient actions
remain unavoidable.

## Route after the reduced factorization

1. Control the projected-cross Gram tail analytically.
2. Compose repeated `D2` or `H4` blocks after a uniform burn-in.
3. Replace perpetual repetition, if too strong, by a stopped target-exit clock.
4. Build the finite-prefix normalization and observability bridge `O`.
5. Revisit the moving-cloud determinant route only after those gates are
   explicit.

There is no Hilbert--Polya operator, zeta-zero identification, or proof of the
Riemann Hypothesis in this roadmap.
