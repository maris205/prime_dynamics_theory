# RH-322: Certified critical folded-row half-line profile

For a physical folded Gaussian row centered at `1 - sigma*a`, push forward by
the boundary coordinate `v = (1-y)/sigma`.  The paper proves the exact identity

```text
||h_folded_(sigma,a) - g_a||_1
  = 2 * normal_survival(1/sigma-a) / Phi(a),

g_a(v) = phi(v-a) / Phi(a),  v >= 0.
```

The same identity holds for the direct positive lobe.  The profile family is
globally stable in the clearance parameter,

```text
||g_a - g_d||_1 <= |a-d|,
```

so `a_sigma -> d` gives total-variation convergence with an explicit error.
All polynomial moments converge, with

```text
E_d[V]   = d + phi(d)/Phi(d),
Var_d(V) = 1 - d*r(d) - r(d)^2.
```

Distinct limiting clearance ratios give distinct profiles.  Thus the
first-alias integer phase cannot be discarded unless `delta_k/sigma` is
controlled.

This is a local one-row theorem.  It does not combine the paired parity layer,
neighboring shell, or moving-order remainder, and it is not a joint
first-alias trace law.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf certified-critical-folded-row-half-line-profile.pdf
```
