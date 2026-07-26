# TPC-118: Strict endpoint optimization

Paper title:

> *Strict Endpoint Optimization for the Physical TPC Route: A
> Nonduplicated Loss Registry, Exact Rational Primal-Dual
> Certificates, and the Equality Stop*

## Core result

Every physical operator event receives one provenance token and one
amplitude exponent. Exact duplicates are merged, distinct maps are
added, and a proved joint bound replaces its dependencies instead of
being charged alongside them. Unknown exponents remain unknown.
Two theorems bounding the same physical event are alternative
evidence, not two additive tokens; one route must select its actual
theorem-backed bound.

On each affine route cell, the endpoint is the rational LP

```text
minimize  c^T x + d
subject to A x >= b, x >= 0.
```

The dual is

```text
maximize  b^T y + d
subject to A^T y <= c, y >= 0.
```

- An exact primal point below `1/400` proves strict compatibility for
  a complete theorem-backed registry.
- An exact dual point at or above `1/400` stops that route only when
  it uses the same complete actual theorem-backed registry.
- Matching primal and dual values exactly `1/400` are an equality
  stop, not a pass.

## Current verdict

The growing costs for the physical frame, grouping, fixed-shift
localization, complete tail and TPC-18 cover/remainder are not all
proved. The actual endpoint state is therefore `INCOMPLETE`; the
missing exponents may not be entered as zero.
Unresolved feasibility/boundedness or a missing upper/lower
certificate is also `INCOMPLETE`, not an implicit route decision.

## Claim level

- Registry and primal-dual logic: L0.
- Mapping TPC-113--117 interfaces into the ledger: L1 audit.
- No strict actual-carrier endpoint certificate, new L2 fixed-shift
  saving, parity breakthrough or twin-prime theorem.

## Reproduce

```powershell
python experiments/tpc118_endpoint_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`strict-endpoint-optimization.pdf`

SHA-256: `c9a421c6d73a56ddd454e7a0365f8480acfdc3a46cb4d07dc6928c6a1450c422`
