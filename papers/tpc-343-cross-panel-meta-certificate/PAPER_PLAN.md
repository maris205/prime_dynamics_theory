# TPC-343 paper plan

## Question

Does the nuisance projection observed in the TPC-341 panel define one shared
finite coefficient law when the independently reproduced TPC-342 panel is
stacked with it?

## Frozen comparison

The all-plus `Q=54`, exponent-one, `H=66` operator, nine controls, four source
masks, rank rule, and the two parent panels are locked.  The inherited finite
decision threshold is residual retention `<0.30` for an in-sample nuisance fit
and `>0.40` for the hostile holdout readout.

Two models are audited:

1. `row-block`: each of the six rows has its own nuisance coefficient vector;
2. `shared`: the three nuisance columns are concatenated across all six rows,
   forcing one coefficient vector for the whole panel.

The shared model is evaluated both with raw energy weighting and after dividing
each row's target and nuisance columns by its target norm (equal-row weighting).

## Deliverables

- exact stacked Pythagorean proposition and a finite rational anchor;
- 216 raw records and 54 leave-one-control-out records;
- row-block and shared-coefficient meta readouts;
- reverse-shell independent checker and seven mutation stress cases;
- PDF and local fail-closed Bridge-B audit;
- explicit firewall against arithmetic or twin-prime claims.

## Decision rule

If row-block passes but both shared variants fail, record a scoped
cross-panel coefficient-stability obstruction and move to an alternative basis
or principal-angle audit.  If the shared guard passes, test it on a fresh panel
before assigning any stronger interpretation.  Either outcome remains finite
and earns zero arithmetic credit.
