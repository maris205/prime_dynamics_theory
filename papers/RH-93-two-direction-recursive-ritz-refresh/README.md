# RH-93: two-direction recursive Ritz refresh

This directory contains the ninety-third RH-layer paper:

> *Two-Direction Recursive Ritz Refresh: An At-Most-Nine-Dimensional Closure
> of the Four-Step Schur Packet Chain*

## Main theorems

For an enriched compression with `k` complement directions,

```text
H = [[A,B],[B*,D]],
```

the leading rank-`r` Ritz packet gains

```text
Delta_k = trace(D) - sum(the k smallest eigenvalues of H).
```

The top `k` left singular vectors of the projected cross operator

```text
(I - VV*) G V
```

maximize captured cross Frobenius energy.

For any full-rank trial frame `W`, the generalized frame trace gives the
reference-free certificate

```text
trace((W*W)^(-1) W*H W) + delta <= trace(D)
    => Delta_k >= delta.
```

The corrected Ritz packet is then used recursively as the packet for the next
update, so no ambient leading-packet reset is required inside the block.

## 384-bit result

Across the ten RH-92 windows:

- recursive width one fails the `0.24` four-step target in four fine channels;
- recursive width two passes all ten channels;
- all 40 generalized two-frame forms are strictly negative;
- the largest direct two-direction block mean is `0.22850222`;
- the top two directions capture at least `96.376%` of projected-cross energy;
- the primary compressed dimension is at most 9;
- width three reduces the worst endpoint/reference tail ratio to `1.05595`.

Thus the second direction is genuinely necessary in the frozen recursive
chain. A uniform all-level two-direction law remains open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_two_direction_refresh_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_two_direction_refresh_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf two-direction-recursive-ritz-refresh.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
