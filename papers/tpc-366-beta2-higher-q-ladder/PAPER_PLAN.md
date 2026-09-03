# TPC-366 paper plan

## Question

After beta=2 survives the TPC-365 fresh panel, does the fixed rule remain
below the inherited finite spectral and Schur working caps when the shell
anchor is extended from `Q=512` to `Q=8192` on a new scale panel?

## Frozen finite protocol

- candidate origins: `620001+307j`, `0<=j<41`;
- pilot count: `256`;
- selection beta: `2`;
- selection score: the largest `max(G)/min(G)` over
  `Q={512,1024,2048,4096,8192}` and exponents `{1,2}`;
- selection tie-break: descending score, then ascending origin;
- greedy minimum separation: `2048`;
- selected origins: `(623071,631360,629211)`;
- audited counts: `256,512`;
- audited shell anchors: `512,1024,2048,4096,8192`;
- audited exponents: `1,2`;
- laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`;
- compared betas: `0,2`, with beta=2 frozen from TPC-365.

The full Cartesian product has `2*3*2*5*2*4=480` rows.  Both spectral and
Schur caps are recorded.  The values `0.64` and `0.83` are finite working
thresholds only.

## Claim discipline

The exact contribution is the deterministic response-blind selection rule,
the finite weighted-block/geometry construction, positivity, and the
Schur/Frobenius inequalities.  The numerical contribution is a complete
higher-Q all-law ladder with a beta=0 control.  A zero-failure beta=2 ladder
is a finite scoped observation; it is not shell-uniform, source-valid,
asymptotic, arithmetic, or a Route-A/Route-B pass.

## Decision rule for the next paper

If the fixed beta=2 ladder fails, the next paper should localize the first
failure by Q, law, and window length.  If it passes, the next minimal attack
should remove geometry-based origin selection by using longer windows and
unselected or predeclared origins, while keeping beta=2 unchanged.
