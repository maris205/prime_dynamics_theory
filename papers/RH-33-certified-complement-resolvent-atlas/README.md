# RH-33: certified complement-resolvent atlas

This paper closes the full-boundary complement-resolvent gate left open by
RH-32 at the stored scale sigma = 1e-2.

For the exact finite model defined by the archived binary64 factors:

- 109 sparse-Grushin center certificates are independently rechecked against
  the exact stored target;
- every Frobenius residual is below 5.747e-9;
- center inverse bounds range from 50.486 to 553.228;
- 88 RH-28 parent midpoints and 21 adaptive rational gap midpoints cover the
  contour;
- the final exact rational partition has 949 leaves and no unresolved leaf;
- the largest 256-bit Arb Neumann product is
  0.9998708523281207 < 1;
- the largest transported-bound / RH-28-budget ratio is
  2.1063796128019612e-11.

Therefore the RH-28 matrix Rouché inequality holds on the entire stored
circle. Combined with the RH-32 projected winding certificate, this proves

\[
\operatorname{wind}_\Gamma \det F = 1.
\]

For the exact stored augmented block

\[
\mathcal M_{\rm st}=\begin{pmatrix}D&E\\ C&B\end{pmatrix},
\]

the exact Schur identity gives the relative count

\[
N_\Gamma(\mathcal M_{\rm st})-N_\Gamma(B)=1.
\]

The interior complement count remains open. Thus this is not yet an ordinary
one-zero theorem, a one-eigenvalue theorem for the original physical
discretization, a continuum result, a Hilbert–Pólya construction, or a
statement about zeta zeros or the Riemann hypothesis.

## Fast verification

~~~bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
MPLBACKEND=Agg python experiments/make_figures.py
python experiments/verify_archive.py
~~~

## Rebuild the final cover

The expensive center JSON files are resumable. With the committed centers,
refresh the exact 256-bit transport and final leaf ledger by

~~~bash
PYTHONDONTWRITEBYTECODE=1 python experiments/audit_refined_atlas.py \
  --sigma 0.01 --max-extra-refinement 8
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
~~~

To certify new adaptive gap centers:

~~~bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 python experiments/run_atlas_batch.py \
  --sigma 0.01 --workers 8 --chunk-size 256 \
  --target-file results/refined_atlas_sigma_1e-02.json
~~~

The formal manuscript is certified-complement-resolvent-atlas.pdf.
