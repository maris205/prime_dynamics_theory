# RH-142: Factorized Arb Snapshot-Packet Closure

This paper preserves the quadratic low-rank cancellation directly in Arb.
The rank-four approximation is stored as an exact product `H = L R`, its
normalized fourth-mode gap is lower-bounded from the two 4-by-4 factor Grams,
and `N(S)-N(H)` is evaluated at 512-bit precision.

Eight of ten frozen binary source channels pass using the Frobenius norm as
an operator upper.  The two coarse channels need validated interval
eigenvalue radii; both then pass.  The minimum gap ratio is above `1.022`, so
all ten rank-four source packets are now rigorously identified for the frozen
binary model.  The coarse right projector radius is still about `0.957`, so
this does not yet enclose the recursive threshold update or give an all-level
packet theorem.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_factorized_arb_audit.py --smoke
/root/math/.venv/bin/python experiments/build_factorized_arb_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf factorized-arb-snapshot-packet-closure.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```

