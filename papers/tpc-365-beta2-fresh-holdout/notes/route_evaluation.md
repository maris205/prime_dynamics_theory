# TPC-365 route evaluation and proof boundary

## Strongest positive result

The beta=2 rule, fixed before signed holdout evaluation, has zero spectral-cap
violations on 192 rows from three new separated high-origin windows.  The
maximum normalized spectrum is `0.61633188509480319`, and the result is
reproduced in reverse prime order.  The beta=0 control has 30 failures on the
same finite protocol.

## Strongest obstruction

The origins were selected by a declared geometry score, so the panel is
response-blind but not statistically independent of the geometry observable.
More importantly, the finite transfer does not show that beta=2 is the
source-valid normalization, nor that the cap persists for growing `Q` or
arbitrary origins.  The arithmetic source norm and packet reassembly remain
untested.

## Route decision

`TPC365_STATUS = NUMERICALLY_CERTIFIED_FINITE_BETA2_FRESH_HOLDOUT`.

`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and
`FULL_GATE_B=OPEN`.  The official evaluator files named by the Session are
absent, so no official Route-A or Route-B pass is asserted.  The next
minimal experiment is a fixed-beta=2 higher-`Q` and new-scale ladder.  A
failure should be retained as a scale obstruction; a pass remains finite
evidence only.
