# TPC-257 paper plan

## One-sentence contribution

The literal V59 adjoint does not merely have one nonzero midpoint Haar
coefficient: a source-frozen four-block Haar frame proves an explicit,
same-order lower floor in the transverse output subspace.

## Research question

Does the TPC-256 midpoint asymptotic leave open the possibility that the
orthogonal output component of `A_x beta` is lower order?  We answer this for
the smallest nontrivial source-only frame: two quarter-pair contrasts together
with the global midpoint.

## Frozen objects

- `I_x=(x/2,x] intersect Z`, `H=x^(21/32)`, `Q=x^(1/3)`,
  `U=x^(133/400)`.
- The literal coefficient `beta` and operator `A_x` from TPC-256.
- Four consecutive rank blocks, split inside each global child before any
  coefficient, sign, or margin is inspected.
- The three normalized contrasts `z_0,z_1,z_2` defined in the derivation and
  proof packages.

## Claims and evidence

| ID | Claim | Evidence | Label |
|---|---|---|---|
| C1 | The three contrasts are source-only, unit, and pairwise orthogonal. | Exact finite rational identities and stress replay. | PROVED_EXACT |
| C2 | Each beta contrast has an explicit positive `sqrt(x)/log^2(x)` main term. | Strong PNT plus second-order `Li` curvature. | PROVED_SOURCE_BACKED |
| C3 | Each adjoint coefficient has the TPC-255 diagonal normal form with boundary error `O(x^(55/48+epsilon))`. | General bounded-variation extension of the exact compiler. | PROVED_SOURCE_BACKED |
| C4 | The three-mode projection and the transverse projection have explicit norm floors of order `x^(7/6)/log^3(x)`. | C1--C3 and finite-dimensional Parseval. | PROVED_SOURCE_BACKED |
| C5 | One midpoint coefficient can be promoted to a full-output upper bound. | Not asserted; the new theorem is a lower floor. | REFUTED_SCOPED |

## Experiments

1. Exact block lengths, normalization, orthogonality, total variation, and
   dyadic limiting endpoint table.
2. Independent implementation with no producer import and semantic mutation
   rejection.
3. Integer/noninteger clock stress, including arbitrary balanced block lengths,
   variation identities, and positivity of all three curvature constants.

Finite computations are validation of identities and schemas only.  They do
not prove the asymptotic PNT input.

## Planned paper structure

1. Motivation and claim boundary.
2. Four-block rank-Haar geometry.
3. Curvature constants for the three literal beta contrasts.
4. General bounded-variation adjoint compiler and norm floors.
5. Exact certificate, obstruction, and next route.

## Non-claims

This paper proves no arithmetic `L2` upper estimate, no full Gate B, no strict
global `1/400` payment, and no twin-prime theorem.  A lower norm floor is not
used as an upper-bound substitute.
