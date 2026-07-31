# RH-329: Validated isolated exchange-model audit

RH-328 reduced the joint first-alias question to a fixed-reference matching
equation but did not supply physical shell data.  This paper freezes a fully
specified graded finite-dimensional model defined from exact rational data
before evaluating that equation.
It is an isolated audit, not an identification of the noisy transfer
operator.

For each integer `k >= 2`, the model contains exact alias, scalar parity, identical
boundary, and two-state exchange blocks.  Its frozen shell data are

```text
L_k       = A_k,
c_iso     = 4/5,
c0        = 3/5,
B_k       = 0,
E_obs,k   = 0,
R_k       = 0.
```

The exchange block

```text
K_c = 1/2 [[1+c,1-c],[1-c,1+c]]
```

has `Tr(K_c^m)=1+c^m`.  Thus the shell packet is derived from matrices,

```text
S_k = A_k ((4/5)^(2k) - (3/5)^(2k)),
```

and is not fitted after observing the demand.  Both shell-channel Duhamel
comparisons retain all `4k` prefix/suffix weights.  Every leg defect is
exactly zero, so the model majorant is exactly zero.

The implementation deliberately uses the positive contrast class
`0 <= c <= 1`; it makes no sign-identification claim for the larger
even-power class `|c| <= 1`.

The exact residual is

```text
e_k = S_k + P_k - A_k.
```

With the model-defining exact rationals in `src/isolated_audit/core.py`,

```text
P_k/A_k -> C_* C_M,
0 < C_* C_M < 1,
e_k/A_k -> -(1-C_* C_M) < 0,
A_k/H_k -> infinity,
H_k = k R^(-2k).
```

Consequently `e_k/H_k -> -infinity`.  Meanwhile the RH-328 required power

```text
y_k = (3/5)^(2k) + 1 - P_k/A_k
```

converges to `1-C_* C_M` in `(0,1)`.  The best-case reachability screen is
therefore eventually zero, but its required contrast radius tends to one,
whereas the frozen model contrast remains `4/5`.  This is a strict scoped
negative result: reachability does not rescue this isolated fixed-contrast
model.

More explicitly,

```text
H_k/A_k     = (k/a_k) (beta R)^(-2k),
H_k/(k A_k) = a_k^(-1) (beta R)^(-2k).
```

The power mismatch has a nonzero limit and the contrast-radius gap tends to
`1/5`, so this model violates both exponential precision demands from
RH-328.

The decimal strings used for `Lambda`, `C_M`, `C_*`, and `C_b` are exact
rational definitions of this model.  They are not interval certifications
of physical constants.  The finite table is a reproduction check only; the
asymptotic theorem is proved symbolically.

Nothing here identifies the actual noisy operator, proves its shell law,
controls its Duhamel defects or far remainder, transfers the isolated result
to the full trace, or proves full-trace divergence.  No Gate A--E closure,
Hilbert--Polya operator, Riemann-zero identification, von Mangoldt trace,
completed-zeta divisor equality, or RH conclusion is obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf validated-isolated-exchange-model-audit.pdf
```
