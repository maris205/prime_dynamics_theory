# RH-263: Parity-Resolved Deterministic-Numerator Tail

RH-263 makes the deterministic numerator anchor explicit at every order.
From the RH-15 factorization, with `r_H=0.85`, `lambda=1.678573510428322...`,
and `T` the reduced beta=1 operator,

```text
a_1 = 0,
a_n = (r_H lambda)^(-n)/(1+lambda^(-n))                 (odd n >= 3),
a_(2k) = r_H^(-2k) [2 tr(T^k) + 2 lambda^(-2k)/(1+lambda^(-k))
                     - lambda^(-2k)/(1-lambda^(-2k))].
```

The formula is all-order and deterministic.  A cross-check against every
RH-253 row from orders 2--28 has maximum floating residual below
`6.5e-14`; that finite check does not become a cloud coefficient bridge.

Using the same factorization, the odd tail is explicit and the even tail is
controlled by the trace-ideal majorant.  At the first omitted order 29, the
parity-resolved protocol gives the safe log-tail bound
`2.6624745e-5` and relative error below `2.6625100e-5` (details are recorded
in the companion direct tail certificate).  This is a deterministic target
statement only.  Legal anchored heads, a cloud bridge, a uniform quotient
tail, and Gates A--E remain open/false.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_parity_anchor_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf parity-resolved-deterministic-numerator-tail.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
