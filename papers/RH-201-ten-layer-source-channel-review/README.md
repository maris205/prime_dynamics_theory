# RH-201: Ten-Layer Source-Channel Review

RH-192--RH-200 correct the physical state type and recover a stronger local
result:

- a rank-four packet is not a full Frobenius Riesz shell because
  `X -> AX` repeats every base mode `m` times;
- the source-cyclic and source-observation quotients remove that false
  multiplicity without discarding the physical moment sequence;
- all 48 accepted temporal roots match one genuine four-mode physical edge
  packet per side;
- exact Riesz channels yield an optimally balanced invariant packet with
  finite determinant, Newton traces, and residue-weighted moments;
- the temporal packet aligns with this endpoint, while the exact physical
  condition remains large (`192` left, `950` right);
- a conjugate-pair outer-edge rule selects a quartet on all six audited
  scale/channel cases.

The aggregate ledger contains 1,352 finite items and zero identity-audit
failures.  The next wall is validated and transported Riesz projectors across
refinement levels.  Gate A is not closed; Gates B--E, Hilbert--Pólya, zeta
zeros, and RH remain untouched.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_source_channel_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ten-layer-source-channel-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
```
