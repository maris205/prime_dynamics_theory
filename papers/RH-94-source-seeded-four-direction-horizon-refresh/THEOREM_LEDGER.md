# RH-94 theorem ledger

## Proved in this paper

1. **Source-seed equivalence.** The leading eigenspace of
   `S* S / ||S||_F^2` is the leading right singular subspace of `S`, with the
   usual spectral-gap interpretation when the cutoff eigenvalue is repeated.
2. **Source-seeded recursive horizon theorem.** A packet initialized at time
   zero can be propagated through any finite Gram sequence by projected-cross
   Ritz refresh. Each update is a rank-preserving variational correction in a
   space of dimension at most `r+k`; no later ambient leading eigenspace enters
   the recursion.
3. **Per-step Ritz monotonicity.** The corrected packet tail for the new Gramian
   is no larger than the predictor tail of the incoming packet.
4. **Reduced frame certificate.** A full-rank bottom trial frame certifies the
   complement gain using only the `(r+k)`-dimensional compression.

## Validated at 384 bits

- Ten source-seeded channels and 120 primary width-four updates.
- Ten of ten width-four endpoint/reference ratios below 1.01.
- Worst width-four endpoint/reference ratio: 1.0011724273.
- Minimum width-four projected-cross capture: 0.9753653055.
- All 120 direct Ritz steps monotone and all generalized frame gains positive.
- Source-SVD/initial-Gram projector discrepancy at most 7.96e-14.
- Width-two and width-three worst endpoint ratios: 11.39799356 and
  1.44893935.

## Not proved

- A source-free or source-linear-time seed construction.
- An ambient-free realization of the action `G_t V_{t-1}`.
- A uniform all-level width-four theorem or repeated-block contraction law.
- Stage-A closure, a Hilbert--Polya operator, zero identification, or RH.
