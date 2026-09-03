# TPC-368 paper plan

## Question

Does the TPC-367 beta=2 long-window failure persist on a second origin family
whose members are declared before any signed response or geometry score is
computed?

## Frozen protocol

- candidate grid: `a_j=810001+353j`, `0<=j<41`;
- predeclared indices: `0,20,40`, hence origins `(810001,817061,824121)`;
- no response, source, law result, or geometry score is used in selection;
- counts: `512,1024`;
- shell anchors: `Q={512,2048,8192}`;
- kernel exponent: `1`;
- laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`;
- compared betas: `0,2`;
- height: `66`;
- finite working caps: spectral `0.64`, Schur `0.83`;
- weight: `w_(p,beta)=(p/Q)^beta`;
- normalization: weighted square-energy symmetric congruence.

The Cartesian product has
`2*3*1*2*4=48` settings per beta and 144 law rows in total.  The exact
anchor is the half-open interval `[810342,810355)` at `Q=4`, exponent one,
for beta `0` and `2`.

## Claim boundary

The exact claims are the deterministic origin protocol, the weighted block
formula, nonnegative-square geometry, exact-anchor positivity, symmetry, and
the elementary finite Schur/Frobenius envelopes.  The numerical claims are
limited to the canonical 144-row certificate and its independently written
reverse-shell replay.  No source-valid normalization, growing operator
bound, source-uniform arithmetic `L2`, shell reassembly, fixed-power credit,
Route-A/Route-B pass, or twin-prime conclusion is permitted.

## Decision rule

If the six beta=2 failure keys recur, record a second-family replication and
test the natural next stress point: a third predeclared family or count 2048.
If they do not recur, map residue-phase dependence before changing the beta
rule.  The current result is intentionally a finite decision point rather
than a claim of asymptotic stability.
