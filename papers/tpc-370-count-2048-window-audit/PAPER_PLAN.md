# TPC-370 paper plan (pre-response declaration)

## Question

Does the beta=2 high-`Q`, all-plus spectral-cap failure observed at
`count=1024` in TPC-367--369 persist, change phase, or disappear when the
same finite prime-shell operator is evaluated on a `count=2048` window?

## Frozen protocol

- inherited origins: `(1010001,1018021,1026041)`, the fixed indices
  `(0,20,40)` of the already declared grid `1010001+401j`;
- no new response, source, law score, or geometry ranking is consulted;
- count: `2048` only;
- shell anchors: `Q={512,2048,8192}`;
- kernel exponent: `1`;
- height: `66`;
- laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`;
- beta values: `0,2`;
- weight: `w_(p,beta)=(p/Q)^beta`;
- working caps: spectral `0.64`, Schur `0.83`;
- inherited exact anchor: `[1010346,1010359)` at `Q=4`, shell `{5,7}`.

The Cartesian product has 3 origins times 3 shell anchors times 1 exponent
times 2 betas times 4 laws, hence 72 rows.  The exact anchor is inherited as
a fixed unsigned finite witness; it is not selected from the count-2048
response.

## Outcome-neutral decision rule

The protocol and all parameters above are fixed before the first count-2048
response is evaluated.  The producer must record the complete observed
failure-key set and phase counts without rejecting a non-replication.  If the
TPC-369 six-key pattern persists at count 2048, the next minimal question is
residue/origin phase localization at the same count.  If the pattern changes,
the next question is a predeclared localization of the changed phase.  Either
outcome remains a finite audit and carries no arithmetic or fixed-power
credit.
