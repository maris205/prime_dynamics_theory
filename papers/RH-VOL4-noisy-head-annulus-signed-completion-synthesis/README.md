# Prime Dynamics Program, Volume IV

## Noisy heads, annuli, first alias, and signed completion

Volume IV is the provenance-preserving synthesis of RH-282--RH-361. It keeps
all eighty numbered papers as atomic sources and organizes them into eight
complete ten-paper phases:

```text
RH-282--291  modulus-complete noisy heads and spectral tails
RH-292--301  weighted prefixes, clocks, and analytic criteria
RH-302--311  annular mass and endpoint Hardy barriers
RH-312--321  endpoint expansions and synthetic spectral sharpness
RH-322--331  first-alias local physical and affine interfaces
RH-332--341  actual replacement, observation, and signed underdetermination
RH-342--351  boundary-orbit atoms and lower-even signed completion
RH-352--361  actual selected tails and deterministic upper counterloops
```

The central typed identities on one common Hardy clock are

```text
p = tau-a = q-d,   d = h-s,   q = p+d,   h = s+d.
```

They do not identify the deterministic counterloop `s` with an actual noisy
head. The first unpaid physical leaf remains

```text
D_(4k)(R) = sum_(2<=n<4k) |h_(sigma,n)-s_(k,n)| R^n/n -> 0.
```

The volume proves a provenance theorem and a source-relative nonpromotion
theorem: the current selected/normalized actual results and unconditional
deterministic results do not imply an unnormalized same-clock `q`, `h`, or
complete `E_off` budget without a new theorem for `d=h-s`. This is a logical
and information-type boundary, not a physical counterexample.

All Gates A--E remain false/open. The volume does not construct a
Hilbert--Polya operator, identify Riemann zeros, prove a von Mangoldt trace,
prove completed-zeta divisor equality, or prove RH. It is not RH-362.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_volume_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf noisy-head-annulus-signed-completion-synthesis.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
