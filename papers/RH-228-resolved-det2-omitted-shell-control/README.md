# RH-228: Resolved det2 Omitted-Shell Control

For `|z lambda|<1`,

```text
|log(1-z lambda)+z lambda|
  <= |z lambda|^2 / (2(1-|z lambda|)).
```

Summing gives a uniform logarithmic `det_2` tail bound on a disk. Applying it
to the 12--14 complete shells resolved beyond each RH-222 selected cloud gives
`q<=0.29818` on `|z|<=1`. The largest bound is `0.16804`, while the
largest observed grid tail is `0.07532`; every bound has positive slack.

This controls only the resolved omitted shells. It says nothing yet about the
unresolved operator complement.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_resolved_tail_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf resolved-det2-omitted-shell-control.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
