# TPC-125: Prescribed-shift intertwining

Paper title:

> *Prescribed-\(h_0\) Intertwining through the Physical Archive:
> Exact Commutator Defects, Direct Slicing, and Sharp De-Aliasing
> Costs*

## Core result

For each archive stage `T_j`, let `P_j` select the prescribed shift
and let `T_j^0` be the declared fixed-`h0` stage. Define

```text
D_j = P_j T_j - T_j^0 P_(j-1).
```

The complete slicing defect is exactly

```text
P_s T_s ... T_1 - T_s^0 ... T_1^0 P_0
 =
 sum_j T_s^0 ... T_(j+1)^0 D_j T_(j-1) ... T_1.
```

Thus direct fixed-shift slicing is certified coefficientwise when the
composite defect is zero; stagewise `D_j=0` is a strong
proof-carrying sufficient condition.

If only averaged observations are available, the route is different.
For actual observation `A`, weight `Omega`, profile Gram

```text
G_prof = A* Omega A
```

and fixed-shift evaluation vector `b0`, a finite transfer exists iff
`b0` lies in `range(G_prof)`. Its sharp squared cost is

```text
K(h0) = b0* G_prof^dagger b0.
```

When `b0=0`, this sharp cost is `0` and the target functional is
identically zero; no nonzero extremizer is required.

If an averaged amplitude saves `sigma` and
`K(h0) <= X^(2 lambda_loc + o(1))`, the transferred fixed-shift
saving is only `sigma - lambda_loc`.

## Current verdict

The exact algebra and rational regression model pass. The machine
certificate labels this result as a finite regression only; its route
verdict remains separate. The complete shift-tagged growing archive
and its actual profile basis are absent:

```text
FIXED-h0 INTERFACE VERDICT = NOT_TESTABLE_FROM_CURRENT_ARTIFACTS
```

TPC-121 and TPC-122 use literal fixed-`h0` inputs, but do not prove
this archive commutation or localization theorem.

## Claim level

- Intertwining telescope and sharp finite localization: L0.
- Typed attachment to TPC-123/124: conditional L1.
- No averaged arithmetic estimate, growing profile-cost theorem,
  fixed-`h0` L2 saving, parity breakthrough or twin-prime theorem.

## Reproduce

```powershell
python experiments/tpc125_shift_intertwining_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-125-prescribed-shift-intertwining.pdf`

SHA-256:

`615108cfa02037ffae2ce40eeec74d2db477f8bb636e5f7673779ba8abac05c9`
