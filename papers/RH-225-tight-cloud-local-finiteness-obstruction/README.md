# RH-225: Tight Clouds versus Locally Finite Divisors

Uniform tightness is useful for empirical probability measures but fatal for a
direct unweighted rank-growing zero divisor. If cloud ranks tend to infinity
and their empirical measures are tight, one fixed compact set contains a
positive fraction of every cloud. Its divisor mass therefore diverges.

In the finite RH-222 atlas, all normalized roots lie in `|z|<=2` and all raw
Hardy-scaled resonances lie in `|z|<1`. Compact counts grow by 31 roots on the
left and 30 on the right.

This exact obstruction rejects using normalized or raw resonances themselves
as determinant zeros. It does not reject reciprocal Fredholm zeros
`z=1/lambda`, which can escape to infinity as resonances approach zero.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_divisor_obstruction_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf tight-cloud-local-finiteness-obstruction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
