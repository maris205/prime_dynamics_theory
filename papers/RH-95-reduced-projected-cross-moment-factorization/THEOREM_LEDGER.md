# RH-95 theorem ledger

## Proved

1. **Projected-cross Gram identity:**
   `K* K = V* G^2 V - (V* G V)^2`.
2. **Cross-cubic identity:**
   `K* G K = V* G^3 V - M_2 A - A M_2 + A^3`.
3. **Reduced factorization theorem:** positive eigenpairs of the `r x r` cross
   Gram reconstruct the selected left directions and determine the full small
   Ritz matrix.
4. **Threshold reconstruction bound:** cross-column perturbations are amplified
   by at most the reciprocal cutoff singular value for a fixed selected right
   frame.
5. **Separated-cutoff projector bound:** a Davis--Kahan estimate controls the
   selected right spectral projector when the squared-singular-value cutoff
   has a gap.

## Validated

- 120 QR-stabilized reduced updates, all direct Ritz monotone.
- Ten of ten endpoint/reference ratios below 1.01.
- Maximum reduced/ambient-SVD tail ratio: 1.0000005281.
- Minimum fourth/first cross singular ratio: 2.7686e-11.
- Five weak-mode updates below 1e-8.
- Eight raw reconstruction orthogonality failures above 1e-6.
- Fifty binary64 moment-compression failures above 1e-3.

## Rejected or left open

- Stable binary64 moment-only closure: rejected on the archived chain.
- Uniform fourth-mode lower bound or cutoff gap: not proved.
- Removal of the ambient action `G V`: not achieved.
- Stage-A closure, Hilbert--Polya, zero identification, and RH: not claimed.
