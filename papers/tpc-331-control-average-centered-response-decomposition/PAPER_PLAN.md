# TPC-331 paper plan

## Parent question

TPC-330 showed that three nontrivial affine placements agree on a positive
all-plus response while identity and reversal remain mostly negative.  The
next smallest structural question is not another placement census:

> Can the five-control response be split exactly into a coherent mean source
> component and a centered position component, and which component carries
> the finite positive sign?

## Frozen protocol

- Parent: TPC-330 producer/certificate, locked by normalized SHA-256.
- Origins: `28001, 36001`; scales: `4096, 8192`.
- Shell anchors: `Q={24,36,54,80}`; kernel exponents: `s={1,2}`.
- Height: `H=66`; comparison cutoff: `2`; Euler product cutoff: `50000`.
- Sign laws: all-plus, alternating-index, mod-4 character, half split.
- Controls: identity, affine `(3,11)`, `(5,17)`, `(7,29)`, and reversal.
- Ratio guard: `5e-8`; logarithmic source enclosure inherited from V59.

## Claim-driven work packages

1. Define `w_j=P_jv`, `v_bar=mean_j w_j`, and `z_j=w_j-v_bar`.
2. Prove the mean/centered Pythagorean identity for any finite quadratic form.
3. Apply it to `E`, the coordinate diagonal `D`, and `O=E-D`.
4. Recompute all 32 rows and 128 law-level decompositions independently.
5. Add an exact rational 16-point anchor for all three components.
6. Attack the result with missing-field, claim-firewall, and exact-algebra
   mutation tests; compare normal and optimized executions.

## Predeclared success and failure criteria

Success is a reproducible finite decomposition with all three identities,
resolved component classifications, and an independent exact anchor.  A
positive average or centered census is a finite structural observation only.
Failure would be an unresolved ratio, an identity residual beyond the declared
replay tolerance, a disagreement between accumulation orders, or a mutation
accepted by the stress checker.

## Expected interpretation

The useful outcome is a localization statement: whether the positive affine
response is carried by the coherent mean, the centered position residual, or
both.  Even a clean localization does not imply a source-uniform estimate;
the growing arithmetic `L2` gate remains separate.

## Next decision rule

- If the centered component has a stable finite sign and nontrivial energy
  fraction, test it on a growing source ensemble within this same family.
- If the coherent component alone controls the sign, formulate a source-aligned
  operator bound before adding more controls.
- If the decomposition is inconclusive, record the obstruction and stop
  expanding finite permutations; do not manufacture a sixth component.
