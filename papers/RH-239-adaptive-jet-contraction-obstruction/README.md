# RH-239: Finite-jet contraction and the all-order obstruction

If two adaptive residual jets satisfy `J(tau)<=epsilon` and
`J(eta)<=delta`, then

    J(tau-eta) <= epsilon + delta.

Thus a family with `epsilon_sigma -> 0` is Cauchy in every fixed finite jet.
All 30 adjacent-scale and 16 dual-channel archived comparisons satisfy this
bound with positive slack; the minimum slacks are `0.00246` and `0.00220`.

The actual adjacent distances are not monotonically contracting, and the
theorem says nothing about orders above twelve.  Finite-jet contraction
therefore does not imply locally uniform `det_2` convergence.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_adaptive_jet_contraction.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf adaptive-jet-contraction-obstruction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
