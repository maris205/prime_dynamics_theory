# TPC-256 paper plan

## Research question

Can the exact TPC-255 diagonal/boundary decomposition be evaluated on its
literal coefficient, rather than remaining a structural normal form?

The smallest source-faithful target is the ordered-rank midpoint projection

```text
<z_mid,A_x beta>,
```

on the same real V59 clock, with both unit masks, the deleted diagonal, the
hard endpoints, and the child jump retained.

## Claim ladder

1. `PROVED`: ordered-rank endpoints and Haar normalization are uniform for
   every sufficiently large real `x`.
2. `PROVED`: each truncated divisor layer has identical `1/d` density in the
   two child means; its residual Haar contribution is `O(U/rho)`.
3. `PROVED_SOURCE_BACKED`: de la Vallée Poussin PNT plus second-order `Li`
   expansion gives the explicit positive beta-Haar asymptotic.
4. `PROVED_SOURCE_BACKED`: weighted PNT gives the exact `9/2` constant in
   `B_Q` after `Q=x^(1/3)`.
5. `PROVED`: the full combined output-unit row satisfies
   `|v(t+h)| <= 1_(q|h)+2/q`; Schwartz decay gives first moment `H^2/q`.
6. `PROVED`: hard-window and child-jump crossing counts are each at most
   `|h|`, yielding exponent `55/48`.
7. `PROVED_SOURCE_BACKED`: the diagonal exponent `56/48` dominates by
   `1/48`, forcing the normalized complex phase to `-1`.

## Manuscript architecture

1. Freeze the literal V59 clock, coefficient, operator, and ordered-rank Haar
   direction.
2. Prove real-clock endpoint control and exact layerwise divisor-density
   cancellation.
3. Derive the prime-power summatory formula from strong PNT and compute the
   second-order `Li` curvature constant `2 log(32/27)`.
4. Insert the beta-Haar asymptotic into TPC-255's exact adjoint decomposition.
5. Estimate `B_Q`, input-unit, hard-window, and child-jump lanes without
   separating the jointly centered output mask.
6. State the complex asymptotic and phase-safe corollaries.
7. Record finite validation and the full Gate-B firewall.

## Adversarial controls

- Real clocks with odd and even `N`; no substitution of an integer-only
  threshold for ordered rank.
- Exact divisor counts on consecutive intervals; no Möbius randomness.
- First-slot conjugate-linearity; no hidden self-adjointness or kernel
  evenness.
- Combined output-unit mask; separate zero modes explicitly rejected.
- Hard-window and child-jump counts tested independently.
- A fixed `epsilon<1/48` selected before comparing powers.
- Complex normalized phase used instead of a branch-dependent principal
  argument claim.
- Finite beta samples labelled `NUMERICAL_OBSERVATION`, never `PROVED`.

## Stop boundary

The paper stops at one ordered-rank Haar projection.  It does not promote the
result to a full-output norm, a physical `w` coupling, fixed-atom credit,
`L2`, full Gate B, the strict global `1/400` payment, or a twin-prime theorem.
