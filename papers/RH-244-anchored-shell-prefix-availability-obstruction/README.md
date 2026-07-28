# RH-244: Anchored Shell-Prefix Availability Obstruction

RH-238 selected the first shell-complete prefix whose order-12 logarithmic
trace jet was close to zero.  RH-243 supplies a nonzero deterministic
numerator anchor.  These are different selection problems.

For the weighted jet metric

```text
d(x,y) = sum_(n=2)^12 |x_n-y_n|/n,
```

the equal-radius balls about zero and the RH-243 anchor are disjoint whenever
`2 epsilon < 0.49450543569144195`.  This holds for every archived rule
`epsilon_sigma=sigma`, since `sigma<=0.04`.

An exhaustive scan of all 543 shell-complete prefixes in the frozen RH-222
candidate windows gives zero anchored passes at 32 endpoints.  The best
endpointwise mismatches range from `0.39723767197524446` to
`0.48457639371229216`, at ranks 4 through 18; even the best mismatch is more
than 10.47 times its tolerance.

This is a scoped obstruction for the frozen prefix class, orders 2--12, and
the tolerance rule `epsilon_sigma=sigma`.  It does not exclude non-prefix
clouds, larger candidate windows, a different selector, or an asymptotic
construction.  The all-order envelope and the coefficient bridge remain
open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_anchored_prefix_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf anchored-shell-prefix-availability-obstruction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
