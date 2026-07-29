# RH-258: Unit-Cap Signed-Integer Selector Obstruction

The first monodromy-legal signed relaxation assigns every complete expanded
shell a weight in `{-1,0,1}`.  Exact-integrality MILP optimization over all 32
endpoints gives zero passes.  Best distances range from
`0.1060737090` to `0.3534900682`, or `7.98--93.48` local tolerances.

The MILPs implicitly cover 39,417,456,084,975,216 signed lattice points in
aggregate and finish with zero reported MIP gap.  This excludes only the
unit-cap lattice.  Larger integer caps and actual invariant operator
realizations remain open.

Gates A--E remain false/open.  No Hilbert--Polya operator, zeta-divisor
equality, Riemann-zero identification, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_unit_cap_integer_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf unit-cap-signed-integer-selector-obstruction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
