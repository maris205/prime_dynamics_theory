# RH-328: Joint alias/parity/shell matching equation

This paper places the RH-326 parity and counterloop packets and the RH-327
localized boundary, shell, and remainder slots in one fixed-reference
equation.  With

```text
e = B + S + R + P - A,
D = A - P - B,
X = L * (c_phys^(2k) - c0^(2k)),
S = X + E_obs,
y = c0^(2k) + D/L,
```

the exact conditional ledger is

```text
e = L * (c_phys^(2k) - y) + E_obs + R.
```

The word *conditional* is essential: the repository has not identified the
actual shell with the exchange model, proved a physical scale `L`, or
identified either physical contrast.  The equation is an exact certificate
once those typed fields are supplied; it is not a theorem that they exist.

In alias-normalized variables

```text
q   = P/A,
b   = B/A,
ell = L/A,
z0  = c0^(2k),
```

the required even power is exactly

```text
y = z0 + (1-q-b)/ell.
```

On a fixed phase, RH-326 gives `q -> C_* C_M lambda^eta`, while the retained
clearance is `d -> C_b lambda^(-2 eta)`.  If `y` stays in a compact subset of
`(0,1]`, the required contrast radius is

```text
r_k = y^(1/(2k)) = 1 + log(y)/(2k) + o(1/k).
```

When `L/A -> ell` with `0 < ell < infinity` and
`E_obs + R = o(H_k)`, matching at the target `H_k = k R^(-2k)` requires
even-power precision

```text
o(H_k/L) = o((beta R)^(-2k))
```

and hence contrast-radius precision

```text
o(H_k/(kL)) = o((beta R)^(-2k)/k).
```

This is a sharp conditioning law for the conditional exchange coordinate,
not a physical precision theorem.

The paper also proves a scoped negative result.  A fixed-reference
reachability screen can pass exactly while the physical contrast misses by
order `L`: take `c0=0`, `D=theta*L`, and `c_phys=0`.  Then `dist(D,I)=0`, but
the mismatch is `-theta*L`; if `L/H_k -> infinity`, the normalized residual
diverges.  Thus best-case reachability is not physical matching.

RH-325's Duhamel majorant enters as `U=sum_j W_j delta_j`.  With
`|E_obs| <= U` and `|R| <= V`, the exact uncertainty interval is

```text
[m-U-V, m+U+V],  m = L*(c_phys^(2k)-y).
```

This yields sharp best- and worst-case residuals, but it does not control the
actual observation norm, prefix/suffix weights, second critical leg, or far
remainder.  No full-trace replacement, Gate A--E closure, Hilbert--Polya
operator, Riemann-zero identification, or RH conclusion is obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf joint-alias-parity-shell-matching-equation.pdf
```
