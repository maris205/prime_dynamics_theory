# TPC-310 paper plan

## Title

Cross-Holdout Aggregation Order and Profile Robustness in a Prime-Shell
Diagnostic

## Question

TPC-309 showed that a finite holdout discordance can move when a source-backed
profile-prefix window is shifted.  TPC-310 asks the next minimal question:
does aggregating the same frozen holdout records remove that profile sensitivity
without introducing a hidden weighting convention?

## Frozen input

Use the released TPC-309 certificate as the only numerical input: 54 profile
cases, three Hamming radii per case, and 162 positive interval records.  Do not
rerun a physical source or alter labels, shell partitions, or completion balls.

## Finite protocol

Enumerate all seven nonempty subsets of `LOW/BASE/HIGH` and all seven nonempty
subsets of radii `{0,1,2}`.  For each of the 49 crossed selectors compute:

1. pooled MSE: sum right/left completion extrema before division;
2. balanced ratio: arithmetic mean of the row-ratio intervals;
3. geometric ratio: geometric mean of the row-ratio intervals.

The threshold rule is inherited: `RIGHT` when the upper endpoint is below
`0.9`, `LEFT` when the lower endpoint is above `1.1`, and unresolved otherwise.

## Claim target

Prove the finite selector and interval algebra.  Establish an independently
replayed finite atlas showing whether the aggregation maps agree.  If they do
not, record the obstruction rather than selecting a preferred map.

## Deliverables

`README.md`, proof and derivation packages, theorem ledger, claim firewall,
computational protocol, citation note, producer, independent checker, exact
stress suite, canonical JSON certificate, Bridge-B checker, and compiled
`paper/paper.pdf`.
