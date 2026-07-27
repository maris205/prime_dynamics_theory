# TPC-135: The TPC-17/18 block frontier

Paper title:

> *The Uncovered Block Frontier in the TPC-17/18 Route:
> Eligibility Partitions and a Coefficientwise All-Block Obstruction*

## Result

The paper applies one canonical maximal-integer `D0` policy to every
actual TPC-134 block. Eligible blocks satisfy the published Maynard
profile and the strict TPC-18 tail geometry. Every other block is
retained in an explicit frontier with one deterministic reason code.

It proves the exact identity

```text
B = eligible_prefix + eligible_tail + frontier.
```

The already-published TPC-17 input makes the eligible prefix soft in
its valid scope. It does not estimate the frontier.

For every nonzero smooth weight and all sufficiently large scales, a
support-envelope native column exists whose source scale is
`ell ~ U = sqrt(R)`. Every dyadic child of that formal column has
`L <= 2R`, hence lies outside the eligible TPC-17/18 domain. Therefore
an eligible-only compiler cannot be a coefficientwise all-block
archive without a separate frontier route. The argument does not
assert that the column's full arithmetic coefficient is nonzero:
`r_Q(ell*k+h0)` may vanish.

This is a scoped L1 obstruction. It proves neither that the frontier
scalar is large nor that another representation is impossible. There
is no new positive L2 result and no prime-pair or twin-prime theorem.

## Reproduce

Default deterministic write:

```powershell
python experiments/tpc135_domain_cover_audit.py
```

Read-only check:

```powershell
python experiments/tpc135_domain_cover_audit.py --check
```

Compile:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
