# TPC-334 paper plan

## Claim

The source cross term has an exact finite support partition, and on the
TPC-333 six-window panel its mass is dominated by non-twin prime shifts.

## Work package

1. Rebuild `Lambda(t+2)` and `b(t)` on the six parent-locked windows.
2. Partition every coordinate by primality of `t`, prime-power status of
   `t+2`, and zero support.
3. Sum category counts and cross masses, checking exact additivity.
4. Replay with an independent primality/factorization implementation and
   stress all support fields and claim labels.

## Decision rule

If the twin share is below ten percent in every row and the non-twin share is
above ninety percent, record a scoped background obstruction and move to an
explicit twin-isolated source.  Otherwise retain support variation as the
next obstruction.  Neither outcome earns arithmetic power credit.
