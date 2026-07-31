# RH-331: Ten-layer first-alias frontier review

RH-331 audits RH-322--RH-330 as one typed chain.  The chain has reached an
exact transfer architecture, but it has not identified that architecture
with the actual noisy full trace.

On the moving first-alias clock `H_k = k R^(-2k)`, and only after identifying
the actual critical coefficient with the five-slot packet, the exact
relations are

```text
E_prefix = E_off + |e_actual,k|/(2 H_k),
e_actual,k = e_model,k + Theta_k,
Theta_k = Delta_B + Delta_S + Delta_R + Delta_P - Delta_A.
```

Consequently, a closing model transfers exactly when
`Theta_k = o(H_k)`, while an arbitrary model requires
`Theta_k = -e_model,k + o(H_k)`.  Weighted-prefix closure also independently
requires `E_off -> 0`.

The observable shell has the gauge freedom

```text
X -> X+t,       E_obs -> E_obs-t,       S=X+E_obs unchanged.
```

Therefore only `Delta_S` is intrinsic unless a physical identification map
has frozen the split in advance.

The strict layer classification is:

- RH-322: exact local folded-row profile;
- RH-323: exact local affine probability chain;
- RH-324: sharp one-physical-leg remainder;
- RH-325: conditional moving-order composition criteria and counterexamples;
- RH-326: exact parity/alias algebraic packet identity;
- RH-327: actual typed trace partition plus synthetic shell
  nonidentifiability;
- RH-328: conditional matching equation and scoped reachability negative;
- RH-329: validated negative result for one frozen graded model;
- RH-330: exact but inactive actual/model transfer criterion;
- RH-331: typed-chain audit and a scoped underdetermination proposition.

The current route coordinate is

```text
first_alias_transfer_criterion_exact_actual_replacement_open
```

The independent review conclusion is a strict negative statement about the
available abstract typed-ledger information class: the RH-322--RH-330
conclusions admit signed ledger completions with identical unsigned data but
opposite critical verdicts.  This does not construct two physical noisy
operators or assert that both completions are physically realizable.  It
shows only that neither actual critical closure nor actual divergence follows
until a physical signed replacement theorem is added.

Actual critical-coefficient and model identification, the second physical
leg, all-leg phase transport, physical signed two-channel Duhamel
enclosures, parity/alias replacement, a signed far remainder, the off-alias
weighted background, and determinant gluing remain open.  RH-329's isolated
negative and RH-330's scalar repair do not decide the actual operator.

Finite rows are reproduction checks only.  No full-trace replacement or
divergence, Gate A--E closure, Hilbert--Polya operator, Riemann-zero
identification, von Mangoldt trace, completed-zeta divisor equality, or RH
conclusion is obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ten-layer-first-alias-frontier-review.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
/root/math/.venv/bin/python experiments/build_batch_archive.py
/root/math/.venv/bin/python experiments/verify_batch_archive.py
```
