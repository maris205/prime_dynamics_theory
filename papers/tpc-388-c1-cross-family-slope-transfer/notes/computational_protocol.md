# TPC-388 computational protocol

- Python 3 and NumPy; numerical-library threads are fixed to one.
- Sieve primes through 20000 and use `(Q,2Q]` for `Q=2048,8192`.
- Use the new affine origin family at counts 512, 768, and 1024 with the
  three-origin calibration/two-origin holdout split.
- Rebuild the current-family matrices independently in descending shell order.
- Apply the TPC-387 cell slope without refitting; record a local-fit control,
  all raw metrics, ratios, and failure flags in canonical JSON.
- Run ordinary/optimized checks, 25 mutations, Bridge-B, and three-pass
  `pdflatex` PDF QA before release.
