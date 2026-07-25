# TPC-110: Post-Bin Determinant Energy

This paper analyzes determinant binning on the actual canonical
fixed-shift carrier.

Main result:

- normalized binning is a coisometry;
- its adjoint projection is exact fiber averaging;
- its kernel is the direct sum of zero-sum determinant fibers;
- the literal energy is exactly
  \[
  D_X=E_X\alpha_X\overline m_X.
  \]

The sharp structural dichotomy is:

1. if all fibers are singletons, then `D_X` is only the imported
   diagonal energy, one full power below the desired natural scale;
2. if collisions occur, the carrier has a nontrivial cancellation
   kernel, so support and occupancy do not give a lower angle.

Thus a future bound with `lambda_D < 1` must prove positive
equal-determinant off-diagonal coherence of the actual coefficient.
No such arithmetic theorem is claimed here.

## Reproduction

```powershell
python experiments/tpc110_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-110-post-bin-determinant-energy.pdf`

SHA-256:

`98E7AC3AAC498DB2480F9AE7ADA3561639AE2CA39B65192FA19A84B2F867D61E`

Release QA: 5 A4 pages, all fonts embedded, no Type 3 fonts, and all
pages rendered and visually inspected.
