# RH-81: Stage-A to A5 route review

This directory contains the tenth layer in the RH-72--RH-81 block:

> *From Validated Assembly to Moving-Cloud Renormalization: A Ten-Layer
> Audit and the Minimal Stage-A/A5 Completion Frontiers*

## Synthesis theorem

For a monotone dependency formula built from closed/open primitive gates with
AND and OR, the inclusion-minimal completion bundles are computed recursively:

- a closed leaf contributes the empty set;
- an open leaf contributes its singleton;
- OR takes the inclusion-minimal union of child families;
- AND takes inclusion-minimal unions across the Cartesian product of child
  families.

Applied to the current route,

    Stage A1 = finite-scale chain AND
               (all-level full-block law OR all-level effective-rank law).

The finite-scale chain is green, so Stage A has exactly two singleton
completion alternatives:

1. prove the RH-75 all-level log-square block law; or
2. prove the RH-77 all-level postblock effective-rank law.

The second is preferred because RH-76 closed the single-arc explanation while
RH-77 found rank two captures at least 99% and rank four at least 99.9999% at
all five anchors.

For a relative fixed-disk A5 limit, each Stage-A alternative must be joined by
three further gates: an actual moving-cloud Riesz projection, its coefficient
bridge, and a uniform trace-class complementary limit.

## Ten-layer verdict

- RH-72--RH-74 close the complete five-scale production chain.
- RH-75 gives one explicit all-level sufficient law.
- RH-76 is a branch-level negative result, not a Stage-A obstruction.
- RH-77 supplies the leading effective-rank fallback.
- RH-78 proves either corridor would close Stage A with zero sigma power.
- RH-79 reaches trace-norm squares and shrinking-disk determinants but exposes
  the generic fixed-disk exponential wall.
- RH-80 proves fixed scalar pole cancellation also fails across the cloud
  circle and isolates the moving-cloud relative determinant route.

The route remains viable. Stage A has one theorem wall with two alternative
forms; A5 has a precise three-gate operator wall after Stage A.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_route_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_route_review.py --smoke
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_frontier_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_frontier_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf stage-A-to-A5-route-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

