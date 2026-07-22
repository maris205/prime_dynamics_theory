# RH-88: Predictor-corrector energy contraction

This directory contains the eighty-eighth RH-layer paper:

> *Predictor-Corrector Energy Contraction and the Global-Norm Barrier*

## Main theorem

For a current normalized snapshot residual `epsilon_j`, the next Rayleigh
injection factors exactly as

    iota_(j+1) = chi_j epsilon_j,

where `chi_j` is the residual Rayleigh growth divided by the full-state
Rayleigh growth. For the RH-87 memory tail `E_j`, define

    theta_j = iota_(j+1) / E_j,
    gamma_(j+1) = E_(j+1) / (iota_(j+1) + eta E_j).

Then

    E_(j+1) / E_j = gamma_(j+1) (theta_j + eta),

with `0 <= gamma <= 1`. This separates old-packet prediction from the
variational dividend obtained by reoptimizing the packet.

## Audit verdict

- a rigorously tested global operator-norm coefficient exceeds one in all ten
  channels; the global-norm sufficient condition is closed false here;
- the directional point-packet coefficient contracts in only 6 of 10
  channels;
- the memory predictor contracts in 9 of 10 channels;
- after packet reoptimization, all 10 memory tails contract;
- the largest actual contraction factor is below `0.235`;
- the finest right channel has predictor coefficient about `1.0193`, but a
  reoptimization factor near `0.1502` reduces the actual factor below `0.153`.

The next theorem must quantify the reoptimization dividend, likely through a
small residual cross-Gramian or swap certificate.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_predictor_corrector_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_predictor_corrector_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf predictor-corrector-energy-contraction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
