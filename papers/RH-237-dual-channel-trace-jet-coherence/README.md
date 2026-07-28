# RH-237: Dual-channel trace-jet coherence

For trace vectors `tau=(tau_1,...,tau_12)`, define the radius-`R` logarithmic
jet distance

    J_R(tau,eta) = sum_{n=2}^{12} |tau_n-eta_n| R^n/n.

The fine and Haar-coarse RH-236 channels were compared at radii `0.5`, `0.75`,
and `1`.  All 16 unit-disk cases pass the `0.02` gate.  The maximum distances
are `0.00347`, `0.00788`, and `0.01415`, respectively.

This strengthens the finite discretization check, but it is not an all-order
determinant comparison and does not establish cross-scale convergence.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_trace_jet_coherence.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf dual-channel-trace-jet-coherence.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
