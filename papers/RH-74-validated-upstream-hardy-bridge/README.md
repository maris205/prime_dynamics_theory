# RH-74: validated upstream Hardy bridge

This directory contains the seventy-fourth RH-layer paper:

> *Validated Upstream-to-Frozen Hardy Bridges for the Folded-Gaussian Production Chain*

## Main theorems

The RH-72 matrix ball is propagated through the RH-73 stationary and parity
systems.  A norm-bounded matrix perturbation augments the stationary Neumann
denominator, the bordered right-eigenpair Newton map, and the bordered left
solve.  This produces rigorous Perron/parity projector and bulk balls for the
analytic midpoint matrix, not merely the repaired dyadic center.

For nonzero matrices `B` and `B0`,

    ||B/||B||_F - B0/||B0||_F||_F
      <= 2 eps/(||B0||_F-eps),

whenever `||B-B0||_F <= eps < ||B0||_F`.  This controls both normalized
coarse/detail couplings and yields complete operator/source/observation error
balls against the frozen RH-70 systems.

For `A=A0+E`, the discrete Volterra identity gives

    D_k <= eps sum_{j<k} C_{k-1-j}(C_j+D_j),

where `C_k >= ||A0^k||` and `D_k >= ||A^k-A0^k||`.  Combining this finite
prefix with a four-block true/reference tail gives a rigorous Hardy norm of
the full transfer-sequence difference.

## Five-scale certificate

At `sigma = 0.16, 0.08, 0.04, 0.02, 0.01`, in both left and right channels:

- analytic stationary/parity factor transfer is green;
- normalized source/observation transfer is green;
- true and frozen block powers are contractive;
- the full upstream-to-frozen Hardy difference is below the inherited 1%
  headroom.

The largest operator, source, and observation errors are respectively
`2.64e-11`, `2.63e-11`, and `1.74e-11`.  The largest bridge is `2.03e-6`.
The worst bridge uses only `0.217%` of its available RH-71 slack.

## Route consequence

The five archived scales now have an end-to-end certificate from analytic
folded-Gaussian assembly through spectral deflation, normalized transfer
blocks, and terminal Hardy completion.  The finite-scale upstream gate is
closed.  Full Stage A1 remains open because no theorem yet controls the whole
small-noise/dyadic family uniformly.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_validated_upstream_bridge.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf validated-upstream-hardy-bridge.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~
