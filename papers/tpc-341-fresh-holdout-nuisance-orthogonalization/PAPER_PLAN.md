# TPC-341 paper plan

## Research question

Does the apparent removal of the twin-prime response by the non-twin,
prime-power, and zero-support nuisance span survive a control that was not
used to form that span?

## Frozen design

- Parent: TPC-340 producer and certificate, both hash-locked.
- Use three non-overlapping windows with origin/scale pairs
  `(48097,1024)`, `(48609,1024)`, and `(49217,1024)`.  Their source values
  and the shifted prime-power arguments remain below the parent cutoff
  `50,000`.
- Keep the all-plus `Q=54`, exponent-1, `H=66` operator and the nine-control
  orbit unchanged.
- Form the nine-control mean for each class.  Project the twin mean onto the
  span of the three nuisance means (non-twin, prime-power, zero-support).
- For each omitted control, form nuisance means from the other eight controls
  and test the omitted twin output.  This is a leave-one-control-out holdout,
  not a claim of probabilistic independence.

## Decision rule

Record the exact finite orthogonal decomposition and require all rank and
Pythagorean checks to pass.  The predeclared diagnostic guards are in-sample
retention `< 0.30` and held-out retention `> 0.40`.  If both hold, classify
the mean-only removal as a control-stability obstruction: the projection can
fit the aggregate mean while failing on held-out controls.  Do not convert
either finite statistic into arithmetic cancellation credit.

## Batch endpoint

TPC-341 is the fifth paper in the current batch (TPC-337 through TPC-341).
After its certificate and hostile validation, stop before creating TPC-342 and
perform a batch review.
