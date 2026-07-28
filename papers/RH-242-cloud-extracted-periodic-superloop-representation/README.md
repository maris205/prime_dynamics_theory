# RH-242: Cloud-Extracted Periodic Superloop Representation

At fixed positive noise, the folded Gaussian operator has an exact closed-loop
trace formula.  After Hardy scaling, put the Perron value, parity value, and
selected cloud in a finite diagonal atomic sector.  The cloud-extracted trace
is exactly the graded trace of the physical and atomic sectors:

```text
tau_n = physical closed-loop sum - selected atomic counterloop sum
      = Str((A direct-sum S)^n),  n >= 2.
```

This is projection free.  It exposes cloud removal without using the
ill-conditioned Euclidean Riesz projector.  It is not yet a cancellation
majorant: the counterloops are spectral and signed/complex, rather than a
positive subset of the original Markov loops.

Among the 352 archived order-2 through order-12 residuals, 179 are negative
and 173 positive; every order has both signs.  Therefore ordinary deletion of
nonnegative physical loops cannot represent all archived residuals.  A future
bound must retain signed grouping.

The paper proves separately that an all-order envelope and a deterministic
numerator coefficient anchor are logically independent.  Neither is supplied
by the loop identity, and Gates A--E remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_periodic_superloop_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf cloud-extracted-periodic-superloop-representation.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
