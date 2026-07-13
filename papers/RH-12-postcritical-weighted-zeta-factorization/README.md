# Postcritical weighted-zeta factorization

This directory contains the twelfth-layer theory paper in the quadratic
prime-dynamics program:

> *Postcritical Factorization of a Weighted Zeta Function at a Quadratic
> Band-Merging Map: An Analytic Circle Lift, Equivariant Fredholm
> Determinants, and a Spectral Noncancellation Criterion*

The paper constructs an analytic expanding circle lift of the central
two-step component and proves the exact identity

```text
q_n = E_{1,n} - O_{2,n} - lambda^(-n) + lambda^(-2n).
```

It follows that the weighted zeta function has the exact meromorphic factor

```text
(1-z/lambda)/(1-z/lambda^2).
```

The manuscript does **not** claim that the numerator is automatically an
uncanceled zero. It proves that a simple zero at `z=lambda` is equivalent to
the absence of the non-Perron eigenvalue `lambda^(-1)` in one specified even
transfer sector. The exhaustive computations provide evidence for that
spectral exclusion but are clearly labeled non-rigorous.

## Reproduction

The ordinary audit and tests complete quickly:

```bash
/root/math/.venv/bin/python -m pytest -q
PYTHONPATH=src /root/math/.venv/bin/python experiments/run_postcritical_factorization.py
```

The independent 50-decimal tail recomputes every one of the `2^n` inverse
words for `14 <= n <= 20` and is CPU intensive:

```bash
PYTHONPATH=src /root/math/.venv/bin/python experiments/run_high_precision_tail.py \
  --minimum-length 14 --maximum-length 20 --decimal-places 50 --workers 64
```

Run the ordinary audit once more after the multiprecision tail if the figures
and summary should incorporate the high-precision values. Build the paper
with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
