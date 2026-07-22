# RH-97: nonlinear hybrid horizon budget

This directory contains the ninety-seventh RH-layer paper:

> *Nonlinear Hybrid Horizon Budgets for Recursive Weak-Mode Quotients*

## Main theorem

For arbitrary nonlinear full maps `F_t`, adaptive maps `A_t`, initial state
`x`, and endpoint functional `J`, define the hybrid chain `H_j` to use
`A_1,...,A_j` followed by `F_{j+1},...,F_N`. Then

    J(H_N x) - J(H_0 x)
      = sum_j [J(H_j x) - J(H_{j-1} x)].

This is an exact nonlinear Duhamel/telescoping identity. Taking absolute
values yields a rigorous a posteriori horizon budget without linearizing the
Ritz refresh map.

## 384-bit result

- All ten channel decompositions telescope and match the adaptive endpoint.
- The five primary `1e-8` omissions have worst absolute propagated budget
  `1.00343e-5` of the reference tail.
- The signed endpoint shift is at most `7.06e-7` of the reference tail.
- At `1e-6`, the worst absolute budget is `0.0249207`; at `1e-4`, it is
  `0.0140915`. Each fails in exactly one channel, matching the endpoint gate.
- Some propagated contributions are negative: future full refresh can reverse
  a local quotient loss.

The next layer should replace exact hybrid replay by a finite block
propagation envelope that can be checked before running every hybrid chain.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_hybrid_horizon_budget_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_hybrid_horizon_budget_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf nonlinear-hybrid-horizon-budget.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
