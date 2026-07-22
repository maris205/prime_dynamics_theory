# RH-67: physical-covariance block envelopes

This directory contains the sixty-seventh RH-layer paper:

> *Physical-Covariance Block Residual Envelopes: Directional Sharpness
> versus Global Positive Size*

## Main result

RH-66 gives residual PSD pieces `P_i >= 0` and envelopes

```text
C(theta) = sum_i P_i / theta_i,
sum_i theta_i = 1.
```

For any positive coefficient covariance `W`, the exact optimizer is

```text
theta_i = sqrt(trace(W P_i)) / sum_j sqrt(trace(W P_j)),
min trace(W C(theta)) = (sum_i sqrt(trace(W P_i)))^2.
```

The second Young parameter has the analogous covariance-optimal formula.
For a rank-one physical covariance this limit recovers the directional
center-radius certificate. A strictly positive regularization

```text
W_epsilon = u u* + epsilon (I-u u*)
```

keeps a globally valid PSD envelope.

## Sharpness/global-size duality

If the physical ray annihilates every residual piece, then

```text
physical excess = O(sqrt(epsilon)),
global envelope size = Omega(epsilon^(-1/2)).
```

This is a genuine tradeoff, not a failure of the block projection.

For the exact diagonal cancellation model:

- isotropic covariance: physical gain `2.92454`, global gain `1.16077`;
- `epsilon=1e-24`: physical gain `1.001027`, global gain `489.96`;
- `epsilon=1e-28`: physical gain `1.0000103`, global gain `4.893e4`.

A 256-bit Arb audit certifies the first two rows.

For generic models, focusing is benign: the nonnormal-chain physical gain
converges from `3.95005` to `3.89914`, and the complex-phase gain from
`1.29505` to `1.28847`, with global spectral gains remaining near `3.93`
and `1.155`.

## Numerical correction to RH-66

The archived RH-66 gain `410.16` for the cancellation ray was produced by
forming large nearly cancelling Gram entries in the original coefficient
coordinates. Factoring vectors in the physical coefficient frame before
forming Grams, followed by the exact scalar reduction, gives the mathematical
isotropic gain `2.92454`. The RH-66 theorem remains valid; RH-67 removes that
binary64 coordinate loss and then identifies the genuine covariance tradeoff.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_covariance_envelope_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_covariance_tradeoff.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf physical-covariance-block-envelopes.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
