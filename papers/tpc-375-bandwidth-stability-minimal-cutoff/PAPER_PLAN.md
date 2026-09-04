# TPC-375 paper plan

## Question

TPC-374 showed that the predeclared band of block distances at most three
reproduces the six beta=2 parent failures.  The next minimal question is
whether the same failure support already appears at a smaller cutoff.

## Frozen protocol

Freeze beta `2`, the all-plus law, exponent one, the three inherited origins,
count `2048`, and all three shell anchors `Q=(512,2048,8192)`.  This is the
complete 9-row beta=2 panel, not a selection of the observed failures.  With
the same full-window geometry as the parent, form nested bands

```text
B_c(i,j) = T(i,j) if |block(i)-block(j)| <= c, and 0 otherwise,
c in {0,1,2,3}.
```

The full eigensystem is computed once per row.  The selected mode is the
largest-absolute-eigenvalue mode, with the minimum mode winning ties.  No
cutoff or row is selected after a metric is read.

## Decision rule

Record the first cutoff whose spectral-cap failure keys equal the inherited
parent keys.  A cutoff with no match is an obstruction to that bandwidth;
neither outcome is promoted to a growing-window or uniform theorem.

## Claim boundary

This project is a finite bandwidth census and selected-full-mode Rayleigh
audit.  It does not establish bandwidth uniformity, cross-block causality,
origin/window transfer, source-valid normalization, arithmetic `L2`, fixed
power credit, Route-A/Route-B closure, or a twin-prime theorem.  Official
evaluator files are absent; local Bridge-B remains fail-closed repository
evidence only.

## Next decision

The observed minimal cutoff is used only as the next frozen candidate for an
independently declared origin/window holdout.  The clue is
`TEST_BANDWIDTH_HOLDOUT`.
