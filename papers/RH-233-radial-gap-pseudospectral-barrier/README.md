# RH-233: Radial-gap pseudospectral barrier

RH-222 supplies positive radial gaps, but RH-232 shows that the associated
left/right spectral angles can be tiny.  This paper gives the exact model
obstruction

    A = [[lambda, M], [0, mu]],
    P_lambda = [[1, M/(lambda-mu)], [0, 0]].

The eigenvalue gap stays fixed while the projector norm grows linearly in
`|M|`.  In the archived dynamics the smallest shell gap is positive, about
`7.40e-5`, while the largest projector norm is about `2.26e12`; the fitted
small-noise growth exponents are approximately `7.41` and `6.55` in the two
channels.

This is a pseudospectral warning, not a disproof of the eigenvalue atlas.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_pseudospectral_gap_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf radial-gap-pseudospectral-barrier.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
