# RH-133: Dyadic Packet-Transport Gauges

This paper derives a natural cross-scale gauge from the model's dyadic
coarse embedding and recursively generated four-direction packet frames.
The polar alignment is lifted to an exact-Gram gauge and compared with the
post-hoc minimax gauge.

Finite result: the natural gauge gives 65 positive transfers versus 67 for
the optimum.  On 42 nonzero-tail pairs its median factor loss is about 73.7
and the worst is nearly `1e10`.  A sharp theorem shows that principal angles
alone cannot control this loss, even when all angles vanish.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_dyadic_gauge_audit.py --smoke
/root/math/.venv/bin/python experiments/build_dyadic_gauge_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf dyadic-packet-transport-gauge.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
