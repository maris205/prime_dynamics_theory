# RH-140: Normalized Snapshot Enclosure

This paper proves sharp perturbation bounds for the normalized Gram snapshot

`N(S) = S* S / ||S||_F^2`.

For nonzero states `S,H`, with `delta = ||S-H||_F / max(||S||_F,||H||_F)`, the
operator, Frobenius and trace radii are `delta`, `sqrt(2) delta`, and `2 delta`.
All constants are sharp.  Exact orthogonal singular-value truncation improves
the dependence from `delta` to `delta^2`.

The audit transports the 160-bit Arb residuals of RH-77 through this theorem.
All ten rank-four postblock snapshots have certified operator radius below
`2.83e-4`; eight are below `1e-5`.  This closes normalization as a finite
validated interface, but does not yet validate the spectral packet/frame map
or prove an all-level source enclosure.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_snapshot_audit.py --smoke
/root/math/.venv/bin/python experiments/build_snapshot_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf normalized-snapshot-enclosure.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```

