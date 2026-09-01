# TPC-322 paper plan

## Research question

Can the PSD direct-sum operator from TPC-321 be given a precise finite signed
projector/reassembly interface, and do natural prime-order sign laws produce a
stable operator-level energy ratio?

## Contribution

1. Define the sign-labelled diagonal isometry and its orthogonal projector.
2. Prove the exact projector, cross-block Gram, and global-sign identities.
3. Audit all 24 rows of the TPC-321 panel, four canonical sign laws, and all
   sign vectors modulo global sign.
4. Record the obstruction separately from any arithmetic (L^2) claim.

## Planned claim levels

- `PROVED_EXACT_FINITE`: projector and reassembly algebra, contraction bound,
  and the exact small rational anchor.
- `NUMERICALLY_CERTIFIED_FINITE`: dual accumulation paths and exhaustive sign
  extrema on 24 literal matrices.
- `NUMERICAL_OBSERVATION`: counts for the four named sign laws.
- `REFUTED_FINITE_PANEL`: the declared all-plus and alternating universal
  laws on this panel.
- `OPEN`: canonical arithmetic signs, growing source image, signed (L^2),
  fixed-power credit, and Gate B.

## Follow-up rule

If the finite sign atlas is flexible, the next paper must test whether a
canonical sign law survives at the spectral-profile level.  If it is rigid,
the next paper should attempt the corresponding growing estimate.  No next
paper may infer a prime-sum theorem from the ratios alone.
