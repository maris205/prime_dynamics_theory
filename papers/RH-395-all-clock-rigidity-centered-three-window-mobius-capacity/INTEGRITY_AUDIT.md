# RH-395 research-integrity audit

## Source integrity

- RH-394 commit `6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7` is the
  sole direct terminal-log analytic source.  Its complete three-shift table
  law supplies the fixed-table limit and exact-support densities.
- RH-375 commit `071fed1b2a5d8488b9d2e35a99a753953b233584` supplies
  only squarefree phase densities, one-site MWIS values, square-clock
  endpoints, divisibility lift, and same-prime-support finite combinatorics.
  Its ordinary-Cesàro formula is not used as a terminal-clock theorem.
- Tao 2016 and Tao--Teräväinen 2019 are inherited analytic provenance through
  RH-394.  Johnston--Yang and Maynard remain closure-only.
- All four source identities and all cited locator roles are explicit.  No
  remote PDF or source archive is vendored, and six external payload hashes
  are excluded from the whole RH-395 tree.

## Mathematical integrity

- `q`, phase tables, and the terminal clock are fixed before the limit.  The
  limit precedes the finite maximum, and the scalar supremum over finite
  clocks comes last.
- The model explicitly reads `mu(n+1)` and is labeled centered and noncausal;
  no causal or online interpretation is implied.
- Positive projection is pointwise score-monotone and safety-preserving.
  Relation saturation uses nonnegative exact-support weights.
- The optimizer remains eight-state for the all-clock statement.  Four-state
  compression is invoked only for `q>=3`; the `q=1,2` self-loops are solved
  separately.
- Reflection pays the passage from a nonnegative optimizer to absolute
  capacity.
- Exact small-clock expressions and the strict clock-6 gain use rigorous
  rational Euler-product enclosures rather than numerical guesses.
- Square-support saturation uses a coordinatewise shared-letter marginal
  identity, not merely equality of total mass.  Forced zero phases split the
  phase cycles before the run bound is applied.
- The cofinal lcm bridge proves a strict upper bound for every fixed finite
  clock; embedded one-site square-clock relations provide the lower endpoint
  witnesses.

## Artifact integrity

- The 72-row certificate explicitly declares finite reproduction, not
  analytic proof.
- The relation audit scans all 262,144 ordered relation pairs and finds 3,375
  safe pairs.
- Builder-independent false verification rejects all 57 core mutations; the
  result verifier rejects all 45 named result mutations.
- Rigorous comparisons use exact rational intervals and fail on unresolved or
  overlapping bounds.
- Strict JSON rejects duplicate keys and nonfinite constants and preserves
  exact nested types.
- The Draft 2020-12 schema is recursively closed; the official validator
  accepts the stored result with zero errors.
- Result, schema, manifest, and verification report rebuild exactly under
  ordinary and optimized Python.

## Closure and release integrity

The closure has exactly 148 Git objects in groups `128+8+4+8`, plus four
ordered remote locks, for 152 logical inputs.  The release manifest encodes the
group sizes and digests, all-Git digest, logical digest, both source commits,
rights vector, four zero-request replays, semantic-PDF identity, frozen
Stage-1/manuscript hashes, payload exclusion, and whole-tree hygiene.

The publication set has 41 members and the release-stage set has 43 files.
Path traversal, nonregular members, symlinks, caches, bytecode, path/content
sentinels, editor temporaries, carriage returns, EOF defects, unlisted files,
type substitutions, and external payload insertions are tested fail-closed.
No release test contains a bare `assert` statement.

## Declarations and verdict

The manuscript includes data availability, ethics, CRediT author
contributions, conflict of interest, funding, AI-use, and limitations/scope
statements.  Independent final theorem and source audits each returned zero
blockers and zero minors.  Verdict: accept within the fixed-clock centered
noncausal scope.
