# RH-102: stopped hybrid quotient clock

This directory contains the one-hundred-and-second RH-layer paper:

> *Stopped Hybrid Quotient Clocks: Exact Endpoint-Slack Control Without a
> Ritz Lipschitz Law*

## Main theorem

Let `H_0` be the full-width endpoint and `H_k` the endpoint after `k`
accepted quotient insertions followed by a full suffix.  If each propagated
debit satisfies

```text
d_k >= |H_k - H_(k-1)|
```

and the clock accepts only while `sum d_k <= A`, then every stopped endpoint
satisfies

```text
|H_k - H_0| <= A.
```

For a reference lower bound `R_-`, baseline upper bound `H_0^+`, gate
`Gamma`, and safety fraction `rho < 1`, choosing

```text
A = rho * (Gamma R_- - H_0^+)_+
```

rigorously preserves the endpoint gate.  No Ritz-map Lipschitz law is used.

## Frozen result

The clock composes RH-96 local gap certificates with RH-97 exact propagated
hybrid debits on 30 channel-threshold chains:

- `1e-8`: all five quotients accepted, no stops, all ten endpoints green;
- `1e-6`: 10 accepted and one rejected; unrestricted worst ratio `1.024921`,
  stopped worst ratio `1.001172`;
- `1e-4`: 20 accepted and two rejected; unrestricted worst ratio `1.014092`,
  stopped worst ratio `1.006033`;
- every accepted contribution telescopes exactly and every accepted local gap
  certificate is green.

One `1e-4` stop is deliberately conservative: its unrestricted signed chain
would remain barely green, but its next absolute debit exceeds the remaining
rigorous allowance.

Hybrid replay, a uniform supply of gap-certified quotients, Stage A,
Hilbert--Polya, zero identification, and RH remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_stopped_hybrid_clock_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_stopped_hybrid_clock_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf stopped-hybrid-quotient-clock.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
