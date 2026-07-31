# RH-326: Parity-renormalized first-alias packet identity

This paper restores the Hardy normalization suppressed in RH-310 and keeps
the raw trace, parity, radial counterloop, and roots-of-unity alias packets
separate.  With

```text
lambda_minus = -(1-delta_sigma),
c^H_(sigma,n) = r_H^(-n) [Tr K_sigma^n - 1 - lambda_minus^n],
c^H_n         = r_H^(-n) [P_n - 1 - (-1)^n],
```

the exact parity packet is

```text
P_(sigma,n)
  = r_H^(-n) [(-1)^n - lambda_minus^n]
  = (-1)^n r_H^(-n) [1-(1-delta_sigma)^n].
```

Thus it is positive at the even first alias and negative at odd orders.  The
counterloop defect splits exactly as

```text
s_(k,n)-p_n^pole
  = 2*1_(2|n)*(beta^n-beta_k^n)
    + 2*k*beta_k^n*1_(2k|n).
```

At `n=2k`, if `a_n^num = c^H_n-p_n^pole`, the full algebraic residual is

```text
c^H_(sigma,2k) - s_(k,2k) - a_(2k)^num
  = r_H^(-2k) [Tr K_sigma^(2k)-P_(2k)+1-lambda_minus^(2k)]
    - [(2k-2)*beta_k^(2k)+2*beta^(2k)].
```

The signs are essential: the even parity term enters positively and the
counterloop alias defect is subtracted.

On a phase subsequence

```text
eta_sigma = k - log(1/sigma)/(2 log lambda) -> eta,
```

the scalar parity-to-alias ratio tends to

```text
C_* C_M lambda^eta.
```

There is a unique scalar balance phase
`eta_* = 3.0609149137...`.  For the common floor/ceil/nearest phase window
`|eta| <= 1`, the ratio is at most `0.3438880199...`; scalar parity alone
therefore cannot match the alias packet at the required scale.  This is a
scoped negative result, not a failure of the actual trace route: a physical
boundary packet and the neighboring shell may supply the missing signed
contribution.

The RH-327 interface retains the clearance phase, the `(V,U,W)` coordinate
frame with orientation `(+,-,+)`, the trace normalization, a local boundary
packet slot, a neighboring-shell slot, and a remainder slot.  RH-322--RH-324
provide local forward-probability laws but no trace observation identifying
those laws with the raw trace packet.  The second physical leg, trace
observation bound, neighboring shell, joint matching equation, and full-trace
replacement remain open.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf parity-renormalized-first-alias-packet-identity.pdf
```
