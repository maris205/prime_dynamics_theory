# RH-281: Ten-layer counterloop/quotient frontier review

RH-272--RH-281 split the next frontier into two honest branches.  The
resolution-clocked monodromy counterloop gives an exact all-order
coefficientwise deterministic bridge and a sharp minimal-rank theorem.
Aggregate Fourier control is the correct noisy-cloud requirement, and the
archived seven-row audit does not certify it.  Independently, raw
Hilbert--Schmidt mass diverges like `sigma^(-1/2)`, fixed-rank Calkin quotients
cannot contract at zero noise in the natural stationary `L2` geometry, while
positive-noise shell charts do activate RH-269 locally.  A variable-rank
block-power criterion is available but
uninstantiated.

The spectral ledger remains `(false,false,false,true,true)`; the separate
graded-counterloop ledger is `(true,true,false,true,true)`.  Both complete
counts are zero.  Gates A--E remain false/open.

## Reproduction and archive audit

From each paper directory, rebuild `results/result.json`, run its tests, and
compile `main.tex`.  From this review directory, generate and verify all ten
individual publication manifests and the batch manifest with:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
```
