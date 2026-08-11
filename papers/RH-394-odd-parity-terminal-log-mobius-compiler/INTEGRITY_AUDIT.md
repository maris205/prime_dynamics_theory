# RH-394 research-integrity audit

## Source integrity

- Tao--Teräväinen Corollary 1.8 is the sole new direct analytic source. It is
  used only with positive exponents in `{1,2}` whose total exponent is odd.
- Remark 1.5 and Appendix A, Theorem A.1, pay the fixed affine phase bridge.
- RH-393 is the direct frozen predecessor for the all-even and two-odd
  channels. RH-392 and Tao 2016 are inherited two-point provenance.
- Johnston--Yang and Maynard are closure-only and are not promoted to proof
  inputs. No RH-390 or RH-391 dependency is introduced.
- No remote PDF or source archive is vendored. Six external payload hashes are
  excluded from publication members and the complete RH-394 tree.

## Mathematical integrity

- `m,q`, pairwise-distinct shifts, phase coefficients, and every admissible
  terminal clock are fixed before `X->infinity`.
- The local density deduplicates residues modulo `p^2` before counting
  modulo-`p` collisions and records all three `p` versus `q` branches.
- The all-even proof uses finite CRT and a union tail; the two-odd proof keeps
  the order fixed `P`, terminal limit, then `P->infinity`.
- For every positive odd support, `n=qt+r` produces fixed positive-slope
  affine forms with nonzero pairwise determinants. The proof pays transformed
  endpoints, the `O(t^-2)` weight error, harmonic normalization, clocks as
  large as `X`, and the sequential all-clock criterion.
- Exact-support inclusion--exclusion gives nonnegative `Pi` and phase mass
  `1/q`. Subset Möbius inversion proves the intrinsic Fourier criterion.
- The complete `m=3` law, sole `m=4` `c1111` boundary,
  `binom(16,8)*2^65` count, linear-form classification, `M_k`, and `B_d`
  product are proved in the manuscript rather than inferred from a program.
- Tables failing the four-cube test are classified only as outside the theorem.

## Artifact integrity

- The 658-row certificate explicitly declares finite reproduction, not
  analytic proof.
- False verification is builder-independent; 32 core and 32 result mutations
  are rejected.
- Strict JSON rejects duplicates and nonfinite values and preserves exact
  nested types.
- The Draft 2020-12 schema is recursively closed; the official validator
  accepts the stored result with zero errors.
- Result, schema, manifest, and report rebuild exactly under normal and
  optimized Python.

## Closure and archive integrity

The closure has exactly 128 Git objects in groups `117+8+3`, plus four
ordered remote locks, for 132 logical inputs. The fixed publication has 39
members and the release-stage set has 41 files. Frozen hashes, source identity,
rights, four zero-request replays, semantic-PDF identity, payload exclusion,
regular safe paths, exact membership, and whole-tree hygiene are executable
gates.

## Declarations and verdict

The manuscript supplies data availability, ethics, CRediT, conflict, funding,
AI-use, and limitations statements. Independent final theorem and source
audits each returned zero blockers and zero minors. Verdict: accept within the
stated fixed-data scope.
