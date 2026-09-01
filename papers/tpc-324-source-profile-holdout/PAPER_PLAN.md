# TPC-324 paper plan

## Question

Does the all-plus trace-normalized profile-majorization pattern from TPC-323
survive source-location changes that preserve every other modeling choice?

## Frozen intervention

Use two disjoint panels, one natural continuation and one gap-separated
offset, with source counts `320,640,1280`.  Keep `H=66`,
`Q={24,36,54,80}`, `s={1,2}`, the deleted diagonal, centered residue term,
four sign laws, and all profile tolerances unchanged.

## Claim-bearing outputs

1. Prove the conditional translation-covariance identity for shifts divisible
   by the active shell primes.
2. Certify the two-panel finite profile census with three accumulation/spectral
   paths and an independent reverse/einsum reconstruction.
3. Report whether the all-plus law and the three alternative-law counts match
   TPC-323 panel-by-panel.
4. State explicitly that no arithmetic or asymptotic credit is earned.

## Falsification rule

If any holdout row is reverse, mixed, or unresolved for all-plus, or if either
panel fails the parent-law census, the result is reported as a failed
replication/obstruction.  No panel is removed after computation.

## Paper structure

1. Motivation and relation to TPC-323.
2. Literal block family and normalized profile definitions.
3. Conditional covariance lemma.
4. Frozen holdout protocol and independent checks.
5. Finite results and amplitude/shape interpretation.
6. Claim firewall, limitations, and next route.
