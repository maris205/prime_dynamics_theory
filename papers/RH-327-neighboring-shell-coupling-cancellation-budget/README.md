# RH-327: Neighboring-shell coupling and cancellation budget

This paper first defines the neighboring critical shell in the same cyclic
trace data type as RH-326.  Partition the physical basepoint into the RH-19
boundary window `J_minus`, its critical sibling `J_plus`, and the far
complement `F`.  With

```text
L_(sigma,n)(J) = Tr(M_J K_sigma^n),
P_n(J) = sum over f^n(x)=x with x in J of 1/|1-(f^n)'(x)|,
```

the Hardy-scaled slots satisfy the exact actual identity

```text
T_(sigma,n) = B_(sigma,k,n) + S_(sigma,k,n) + R_(sigma,k,n).
```

Here `S` is the basepoint-localized neighboring-sibling trace defect.  This
constructs an actual signed shell slot, but it does not estimate its sign or
magnitude, identify it with the RH-322--RH-324 forward probability laws, or
show that `R = o(k*R^(-2k))`.

The paper then proves a scoped nonidentifiability theorem.  For

```text
Pi_s = (1/2) [[1,1],[1,1]],
Pi_a = (1/2) [[1,-1],[-1,1]],
K_c  = Pi_s + c*Pi_a,  |c| <= 1,
```

one has exactly

```text
K_c^m = Pi_s + c^m Pi_a,
symmetric compression = 1,
Tr(K_c^m) = 1 + c^m.
```

Tensoring this branch channel with a rank-one reset onto the RH-323 affine
law preserves the clearance `d`, coordinates `(V,U,W)`, orientation
`(+,-,+)`, and output shift `kappa_aff*d`.  Every branch-blind power datum is
independent of `c`, while the trace still sees `c^m`.  Thus equal sibling
mass and local affine probability data do not identify the signed trace
shell.  The reset completion is synthetic and is not the physical kernel.

For fixed deterministic reference contrast `c0`, even order `2k`, and shell
scale `L`, the signed noisy-minus-reference exchange defect

```text
X = L * (c^(2k) - c0^(2k))
```

has the exact image

```text
[-L*|c0|^(2k), L*(1-|c0|^(2k))].
```

The best residual for a demanded shell value `D` is its distance to this
interval.  Only when both contrasts are allowed to vary over the synthetic
information class does the union become `[-L,L]`; the physical reference
must not be optimized during matching.  A fixed nonzero fraction of `L`
forces at least one contrast to approach unit modulus at rate `1-O(1/k)`.

Combined with RH-326, the exact actual ledger is

```text
e = B + S + R + P - A.
```

RH-328 must identify the physical shell scale and observation, and prove
the actual fixed-contrast mismatch and `R` are `o(k*R^(-2k))`.  The distance
to the attainable interval is only a necessary best-case pre-screen; it does
not prove that the physical contrast attains the interval projection.  No
joint matching equation, full-trace replacement, Gate A--E closure,
Hilbert--Polya operator, Riemann-zero identification, or RH conclusion is
obtained here.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf neighboring-shell-coupling-cancellation-budget.pdf
```
