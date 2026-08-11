# RH-396 research-integrity audit

## Source integrity

- RH-394 commit `6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7` is the sole
  analytic input.  Its complete fixed three-shift table law supplies the
  terminal limit, phase density, phase sum, mass, and all-clock conclusion at
  the fixed shifts `(+h,0,-h)`.
- RH-395 commit `20de7202518f4488cbd9c7d63bf94aaa3dc94476` supplies only
  finite `h=1` relation-saturation and tropical-optimizer precedent.
- RH-375 commit `071fed1b2a5d8488b9d2e35a99a753953b233584` supplies only
  finite one-site MWIS and square-clock precedent.  Neither RH-375 nor RH-395
  is promoted to an analytic terminal-clock source.
- Tao 2016 and Tao--Teräväinen 2019 are inherited provenance through RH-394.
  Johnston--Yang and Maynard remain inherited closure-only objects.
- All source identities and cited roles are explicit.  No external PDF or
  source archive is vendored; six payload hashes are excluded from the whole
  RH-396 tree.

## Mathematical integrity

- `h`, `q`, the table family, and the terminal clock class are fixed before
  the limit.  Each fixed-table limit precedes the finite maximum, and the
  scalar supremum over finite clocks comes last.
- The rule reads `mu(n+h)` and is explicitly centered and noncausal.
- The phase sum uses collision-aware `kappa_h(S)`, not a collision-free
  constant indexed only by `|S|`.
- Positive projection is score-monotone and safety-preserving; saturation
  uses nonnegative exact-support weights; reflection pays the absolute value.
- The all-clock formula remains eight-state.  Four-state compression is used
  only when `q` does not divide `2h`; the self-loop obstruction is explicit.
- On square support, `alpha` is raw and `M` weighted.  The equality `C=M`
  requires the support to contain `p0(h)`.  The shared marginal includes the
  nontrivial `t=0` difference as well as the two sign states.
- Same-support scaling has no extra gcd hypothesis.  The exact `h=6`
  counterexample prevents removing the base-support condition.
- Euler-run densities are exact nonnegative finite/infinite densities, not
  empirical frequencies.  The cutoff makes the endpoint sum finite.
- Fresh-prime recurrence distinguishes plateau from strict steps.  Strict
  finite nonattainment uses CRT eventual strictness, not a false every-step
  claim.
- The lag argument proves a strict fixed-lag baseline and an unattained
  infimum only; it does not assert a lag ordering.

## Artifact integrity

- The 96-row certificate explicitly declares finite reproduction rather than
  analytic proof.
- The relation oracle scans 262,144 ordered relation pairs and finds 3,375
  safe pairs.
- Builder-independent verification rejects 32/32 core mutations; the result
  and schema layers reject 65/65 and 28/28 named mutations.
- All rigorous numerical comparisons use integers, fractions, and outward
  rational intervals.  The three displayed endpoint intervals are
  orientation-only and are never promoted to nine-digit certificates.
- Strict JSON rejects duplicate keys and nonfinite constants and preserves
  exact nested types.
- The Draft 2020-12 schema is recursively closed; the official validator
  accepts the stored result with zero errors.
- Result, schema, manifest, and verification report rebuild exactly under
  normal and optimized Python.

## Closure and release integrity

The closure has exactly 160 Git objects in groups `148+8+4`, plus four
ordered remote locks, for 164 logical inputs.  The release manifest binds the
group sizes and digests, all-Git digest, logical digest, source commits,
rights vector, four zero-request replays, semantic-PDF identity, frozen
Stage-1/manuscript hashes, payload exclusion, and whole-tree hygiene.

The publication set has 41 members and the release-stage set has 43 files.
Path traversal, type substitutions, nonregular members, symlinks, caches,
bytecode, path/content sentinels, editor temporaries, carriage returns, EOF
defects, unlisted files, special files, and payload insertion are tested
fail-closed.  Release tests contain no bare `assert` statement.

## Declarations and verdict

The manuscript includes data availability, ethics, CRediT author
contributions, conflict of interest, funding, AI-use, and limitations/scope
statements.  Independent final theorem and source/PDF audits each returned
zero blockers and zero minors.  Verdict: accept within the fixed-lag,
fixed-clock, centered, noncausal scope.
