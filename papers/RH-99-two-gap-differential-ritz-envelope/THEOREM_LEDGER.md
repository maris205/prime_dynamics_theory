# RH-99 theorem ledger

## Proved

1. **Cross covariance derivative formula** for
   `C(P)=(I-P)GPG(I-P)`.
2. **Spectral projector Sylvester bound:** a separated Hermitian spectral
   projector derivative is bounded by twice the operator derivative divided
   by the cluster gap.
3. **Two-gap refresh derivative theorem:** the projected-cross Ritz refresh
   derivative is controlled by the cross squared-singular gap and output Ritz
   gap.

## Validated where the hypotheses are available

- 115/120 updates have both guarded gaps positive.
- 690/690 probes at those updates lie below the two-gap bound.
- Five weak-mode quotient updates improve the full-width formal bound.

## Negative branch

- Five fine-scale Ritz gaps are not certifiably positive.
- Maximum formal bound exceeds 1e40 and can be 1e36 times a probe derivative.
- Zero of five actual quotient displacements lie inside the first-order
  separation radius.

## Not proved

- A finite neighborhood or invariant Lipschitz tube.
- A replay-free block envelope, repeated-block theorem, Hilbert--Polya, or RH.
