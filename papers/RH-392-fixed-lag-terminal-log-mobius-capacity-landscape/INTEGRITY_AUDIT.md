# RH-392 research-integrity audit

## Source integrity

- Tao Theorem 2, equation (3), printed/PDF page 3, is the sole remote
  analytic theorem used. Its scope is fixed nonparallel affine forms; no
  uniform period, lag, or rate is imported.
- Johnston--Yang and Maynard are inherited closure-only locks and are not
  used in the proof.
- RH-389 and TPC-137 supply frozen local reduction provenance. The
  arbitrary-nonzero-determinant completion and all-lag phasewise CRT formula
  are proved locally rather than cited as precursor corollaries.
- Tao's version of record is CC BY 4.0, but project policy does not vendor
  its PDF. No article-specific redistribution grant is established for the
  Johnston--Yang or Maynard payloads; their PDFs and the Johnston--Yang
  source archive remain unvendored.
- All five external payload hashes are absent from publication members and
  from a recursive scan of the entire tree.

## Mathematical integrity

- The terminal clock and all period/lag/shift/table data are fixed before
  `X->infinity`.
- The full-Möbius lemma permits every fixed nonzero determinant. Its cutoff
  proof does not assume coprime square-divisor variables; each compatible
  congruence system is split into a finite disjoint union of lcm classes.
- Content extraction records the exact reduced determinant
  `L*Delta/(c_D*c_V)`. The square-divisor tail is determinant-free: fix `P`,
  take `X->infinity`, then let `P->infinity`.
- The local factor uses the distinct set `{0,h mod p^2}` while retaining
  multiplicity after reduction modulo `p`. The four small collision fixtures
  cover both failure modes.
- The finite-shift theorem stops at total degree two. The one-lag
  coordinatewise-biquadratic theorem is stated separately.
- Projection, compatibility, predecessor orientation `r-h`, gcd cycles,
  self-loops, signed charge, reflection, and absolute maximum are all explicit.
- The capacity maximum occurs after fixed-table limits, never before them.

## Artifact integrity

- The certificate has 640 exact rows and an explicit epistemic role of
  finite algebra, not analytic proof.
- False-mode verification is builder-independent. All 24 semantic mutations
  change theorem-critical leaves and are rejected.
- Strict JSON rejects duplicate keys and nonfinite values, distinguishes
  Boolean from integer, and freezes every object, array, and leaf.
- The Draft 2020-12 schema is recursively closed and independently evaluated;
  the official validator accepts the stored result with zero errors.
- Result, schema, manifest, and report rebuild exactly in normal and optimized
  modes.

## Closure and archive integrity

The source closure is exactly 106 release-bound Git objects in groups
`95+8+3`, plus three ordered remote locks, for 109 logical inputs. The fixed
publication has 38 members and the release-stage set has 40 files. Frozen
Stage-1/manuscript hashes, Git identity, remote rights, three zero-request
replays, semantic-PDF identity, five-hash exclusion, no symlinks/caches/
sentinels, and text EOF hygiene are executable gates.

## Declarations and verdict

The manuscript includes data availability, ethics, author contributions,
conflict, funding, and AI-use declarations. There are no human or animal
subjects, personal data, clinical intervention, external funding, or declared
conflict. Independent theorem and source/citation/PDF reviews each returned
zero blockers and zero minors. Verdict: accept.
