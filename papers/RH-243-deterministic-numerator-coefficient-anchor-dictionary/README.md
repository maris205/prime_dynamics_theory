# RH-243: Deterministic Numerator Coefficient Anchor Dictionary

This paper converts the previously identified deterministic numerator into
the trace-style coefficients used by the current cloud-extracted `det_2`.
If

```text
D_0,bulk,2(z) = G(z)/(1-z^2/lambda)
```

and `P_n` is the deterministic flat periodic trace, then after the current
Hardy scaling `r_H=0.85` the one-step numerator target is

```text
a_n = r_H^(-n) [P_n - 1 - (-1)^n + 2 1_(2|n) lambda^(-n/2)].
```

For the symmetric two-step numerator `H(w)=G(sqrt(w))G(-sqrt(w))`, the
trace-style coefficient is exactly `b_k=a_(2k)`.  Thus `H` anchors only the
even one-step subsequence; it cannot recover odd coefficients.

The order-2 through order-12 target unit-disk logarithmic norm is about
`0.494505`.  This defines the independent target required by RH-238, but it
does not prove that the current selected cloud converges to it.  The actual
cloud coefficient bridge and the all-order envelope remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_coefficient_anchor_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf deterministic-numerator-coefficient-anchor-dictionary.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
