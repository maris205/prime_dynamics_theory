# RH-134: Moving-Frame Memory-Tail Recurrences

This paper proves the exact finite-memory birth identity and a sharp affine
Loewner recurrence in moving packet frames.  The old tail contracts, frame
motion contributes explicit forcing, and the boundary-crossing snapshot is
the only rank-birth source.

For `eta=1/512`, depth five, and `tau=1`, the weighted old-tail coefficient
is at most `0.00391387939453125`.  All 330 temporal updates pass the exact
identity and raw/weighted Loewner audits; 24 are first births.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_memory_tail_audit.py --smoke
/root/math/.venv/bin/python experiments/build_memory_tail_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf moving-frame-memory-tail-recurrence.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
