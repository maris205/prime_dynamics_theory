# RH-248: Anchored Shell-Zonotope Reachability Obstruction

RH-244 showed that shell-complete prefixes miss the RH-243 deterministic
anchor.  Here each complete conjugate shell is allowed independently, so the
test no longer depends on radial ordering.

For orders 2--12 let `v_j` be the real power vector of shell `j`, and let `d`
be the unselected trace vector minus the RH-243 anchor.  We solve

```text
delta_box = min_(0 <= w_j <= 1) sum_n |d_n - (V w)_n|/n.
```

The LP has an explicit dual certificate.  Across all 32 frozen endpoints,
the convex box distance is `0.14649763462315904` to
`0.4240179027308174`, while the smallest tolerance is much smaller; hence
there are zero passes even in the whole shell zonotope.  The largest
primal--dual gap is `7.72e-15`.

The audit also records 543 prefixes, 5,012 contiguous shell intervals, and
139,572,890 rank-at-least-four binary shell subsets.  None passes.  Every
best contiguous interval starts at the outer shell, so intervals give no
improvement over prefixes.  A one-coordinate dual certificate already
separates 24 endpoints (18 at order 2 and 6 at order 6); the remaining eight
use the full multi-order dual.

This excludes only the frozen candidate window with each shell used at most
once.  It does not exclude expanded windows, signed/complex grouping,
continuum mechanisms, or repeated roots as algebraic multiplicities.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_zonotope_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf anchored-shell-zonotope-reachability-obstruction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
