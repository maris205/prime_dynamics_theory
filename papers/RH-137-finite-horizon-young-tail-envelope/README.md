# RH-137: Finite-Horizon Young Tail Envelopes

This paper exactly eliminates the Young parameter from a one-step relative
tail recurrence:

`inf_tau [A(1+tau)x + q + B(1+1/tau)] = q + (sqrt(Ax)+sqrt(B))^2`.

The resulting monotone nonlinear map has a sharp safety radius.  Greedy
pointwise gauge selection is horizon-optimal within the fixed 33-candidate
RH-136 family.

Full audit: the propagated envelope safely certifies 328/330 transitions and
28/30 complete chains, exactly matching the actual safe/unsafe split.  It
crosses 31 of 33 transitions that cannot have a contractive long-run affine
floor.  The two failures have gauge-independent birth forcing `9.40589 > 1`
and actual target tail `9.43632 > 1`.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_finite_horizon_audit.py --smoke
/root/math/.venv/bin/python experiments/build_finite_horizon_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf finite-horizon-young-tail-envelope.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
