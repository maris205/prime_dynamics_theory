# RH-103: prefix and observability power ledger

This directory contains the one-hundred-and-third RH-layer paper:

> *An Explicit Sigma-Power Ledger for Prefix and Observability Bridges:
> Max-Plus Composition and Two Independence Barriers*

## Main theorem

For one directional Hardy triple, write the source as `X=N Xbar`, split at a
block horizon, and let:

- `U` be the upstream Hardy bridge;
- `P` be the unit-source finite-prefix norm;
- `Z` be the reduced packet future;
- `Omega` be the future observability factor;
- `R` be the packet residual.

Then

```text
E <= U + N (P + Z + Omega R).
```

If signed powers are defined by `f=O(sigma^-a polylog)`, the side power is

```text
alpha_s = max(0, u_s, n_s+p_s, n_s+z_s, n_s+o_s+r_s).
```

The two side powers add.  Their total must fit the shared RH-49 quarter-power
budget.

## Route result

Normalization, logarithmic rank, depth-five memory, the fixed stopped gate,
and mesh substitution all have zero sigma power.  However two exact stable
families prove that normalized packet success does not control:

- arbitrary finite-prefix transient power;
- arbitrary absolute observation power.

Both examples have normalized Gram equal to one and zero packet relative
tail.  Therefore RH-101 and RH-102 do not reduce the preferred Stage-A route
to `Q` alone.  The old `O` gate must be decomposed into explicit prefix,
reduced-future, observability-residual, and uniform upstream scalar laws.

## Five-anchor audit

- all five finite compositions remain green;
- conditional Hardy upper is at most `1.835971`;
- rank clock is at most seven;
- memory depth is five;
- primary stopped endpoint ratio is at most `1.00117243`;
- stress identification envelope decreases from `0.07354` to `0.002961`.

These are finite facts, not all-level exponent theorems.  Stage A,
Hilbert--Polya, zero identification, and RH remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_power_ledger.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_power_ledger.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf prefix-observability-power-ledger.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
