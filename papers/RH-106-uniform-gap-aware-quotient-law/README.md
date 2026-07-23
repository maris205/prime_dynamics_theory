# RH-106: uniform gap-aware quotient law

This directory contains the one-hundred-and-sixth RH-layer paper:

> *Uniform Gap-Aware Quotient Laws: Price Envelopes, Stopped Safety, and a
> Ratio-Collapse Boundary*

## Main theorem

For a locally retained/omitted compression, define

```text
g_i   = retained-to-omitted gap,
c_i   = omitted cross Frobenius norm,
ell_i = c_i^2 / g_i.
```

If each propagated endpoint debit is at most `K ell_i`, there are `N`
candidates, and the stopped allowance is `A`, then

```text
N K sup_i ell_i <= A
```

guarantees that every candidate is accepted and the endpoint gate is
preserved. If the inequality is unavailable or fails, stopping at the first
unaffordable debit still preserves the endpoint gate.

The all-level power criterion is

```text
2*chi - gamma - kappa >= s,
```

where `chi` is coupling decay, `gamma` is gap decay, `kappa` is propagation
growth, and `s` is endpoint-slack decay. A fixed positive gap is not required;
the invariant is `c^2/g`.

## Frozen audit

- 38 candidates over thresholds `1e-8`, `1e-6`, `1e-4`;
- 35 accepted and 3 rejected;
- all 38 local gap certificates green;
- primary five candidates all accepted;
- maximum replay-debit/local-price ratio: `0.974091`;
- worst unrestricted endpoint ratio: `1.024921`;
- worst stopped endpoint ratio: `1.006033`.

The abstract uniform law and stopped fallback are proved. The physical
all-level gap/cross-energy/propagation/slack exponents remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_quotient_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_quotient_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf uniform-gap-aware-quotient-law.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
