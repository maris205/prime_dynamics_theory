# RH-60: finite-horizon phase-aware Stein tails

This directory contains the sixtieth RH-layer paper:

> *Finite-Horizon Phase-Aware Stein Tails for Directional Hardy Fusion:
> Completing the Schur Packet Route*

## Main result

Suppose a stable Schur-prefix system has an observability Stein
supersolution `O_tilde`:

```text
O_tilde - T^* O_tilde T >= Y^* Y.
```

For every finite horizon `L`, the exact observability Gramian satisfies

```text
O <= O_L + (T^*)^L O_tilde T^L,
O_L = sum_(m=0)^(L-1) (T^*)^m Y^* Y T^m.
```

The finite term keeps all packet cross-phases. For packet tails with norms
`t_j(L)`, the fused Hardy energy obeys

```text
E <= E_L + sum_j t_j(L),
E_L^2 = 1^* K_L 1.
```

This is exact phase-aware finite-time fusion followed by a positive tail
completion. At `L=0` it reduces to the RH-59 packetwise metric upper.

## Five-scale result

The audit inherits RH-59's binary64 flag metrics and uses a fixed `L=32`.
At `sigma=0.01`:

- exact left/right Hardy energies: `1.46807`, `1.76031`;
- RH-59 full-time metric uppers: `19.21957`, `12.13822`;
- RH-60 phase-aware completions: `1.47497`, `1.76413`;
- finite phase terms: `1.468073`, `1.760309`;
- tail sums: `0.006892`, `0.003819`.

The five-scale fitted growth exponents of the selected completion are `0.169`
and `0.200`, close to the exact-energy fits `0.168` and `0.199`. A horizon
sweep reaches the same values by `L=64`.

## Theoretical boundary

Analytic finite-dimensional results:

- finite-horizon packet Gram positivity and exact phase fusion;
- Loewner finite-horizon plus Stein-tail completion;
- packetwise hybrid bounds and the global phase-aware Minkowski bound;
- geometric tail decay when a normalized contraction estimate is available.

Computer evidence:

- production Schur forms, finite Grams, and inherited RH-59 metrics are
  binary64 diagnostics;
- the 256-bit Arb certificate covers one two-scalar-block model only;
- `L=32` is a fixed five-scale observation, not a proved physical-family
  horizon or continuum tail theorem.

Stage A1, unconditional Stage A4, a self-adjoint Hilbert--Polya operator,
`T log T` counting law, arithmetic prime-power trace formula, zeta-zero
identity, and Riemann-hypothesis conclusion remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_phase_tail_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_phase_tail_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-horizon-phase-aware-tails.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
