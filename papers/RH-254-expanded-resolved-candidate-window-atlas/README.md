# RH-254: Expanded Resolved Candidate-Window Atlas

This paper implements the first spectral reopening input after RH-251.  The
RH-222 candidate margin is doubled from 16 to 32 at all 32 archived endpoints.
Each endpoint resolves 16 additional bulk roots; the old candidate roots match
the expanded computation with maximum discrepancy `7.41e-9`.

The fixed-count expansion is not automatically shell-complete: 21/32 expanded
windows are complete, while 11/32 terminate in one split conjugate pair.  The
shell-complete expanded ranks range from 33 to 64.  This boundary effect is
recorded explicitly and is handled by the next anchored reachability audit.

Gates A--E remain false/open.  No Hilbert--Polya operator, zeta-divisor
equality, Riemann-zero identification, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_expanded_window_atlas.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf expanded-resolved-candidate-window-atlas.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
