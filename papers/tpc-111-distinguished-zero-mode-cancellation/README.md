# TPC-111: Distinguished Zero-Mode Cancellation

This paper treats the distinguished determinant zero mode independently
of determinant energy.

Main exact results:

- `Z_X` is invariant under every exact provenance-preserving
  aggregation or coarsening;
- for an ordered sign sequence with prefix sums `S_k`,
  \[
  \sup_{\|W\|_{\mathrm{BV}_*}\le1}
  \left|\sum_i \sigma_iW_i\right|
  =\max_k|S_k|;
  \]
- the literal outer zero mode is bounded by the sum of the actual
  signed-prefix discrepancies times the actual weight variations,
  plus the audited content remainder.

This identifies the fiberwise sharp energy-free input required by the
route.  The outer summed certificate is sufficient and may lose
cancellation between different outer keys.
It does not prove a power saving for the growing fixed-shift
Liouville/Moebius signs, so `eta_Z > 0` remains unproved.

## Reproduction

```powershell
python experiments/tpc111_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-111-distinguished-zero-mode-cancellation.pdf`

SHA-256:

`2B8FCF15B693E679CC7597362E22639F181F2786B56D837808676C2559FC9D4C`

Release QA: 5 A4 pages, all fonts embedded, no Type 3 fonts, and all
pages rendered and visually inspected.
