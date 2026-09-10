# TPC250–254 conversion and bounded prerequisite audit

Updated 2026-09-08. Source lock:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. All five complete TeX
manuscripts, README files, proof packages, and bibliography files were read.
Original scientific sources, certificates, code, hand-edited materials, and
pre-existing build products remain unchanged.

## Conversion evidence and non-content dependency

All five abstract/body formula-sequence and normalized-text roundtrips pass:
545 math nodes and 95 raw-source display blocks over 21 extracted PDF pages.
All five external bibliographies are retained as full, hash-locked BibTeX;
unresolved citations remain explicit code. This is mechanical preservation,
not independent bibliography verification, a full semantic review, or a
certificate that the preserved PDF and TeX are synchronized.

TPC250's preamble contains
[`input{glyphtounicode}` with its original backslash](../../papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/paper/main.tex#L7).
The converter previously rejected every external TeX input. It now permits
only one exact, standalone preamble `\input{glyphtounicode}` after resolving
the dependency with `kpsewhich` and checking the audited SHA-256
`395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851`.
The resolved system file is TeX Live's `glyphtounicode.tex` (version comment
2.95): a whole-file syntax census found six comments and 5,505 literal
`pdfglyphtounicode` assignments, with no unexpected lines among 5,511 lines.
It is PDF glyph-to-Unicode mapping data, not manuscript prose or equations.

The original command, TeX line, filename, and dependency hash are retained
in a separately labeled code appendix to the reading layer. The table is
not expanded and no TeX is executed. Unknown inputs, body inputs, duplicate
inputs, other external dependencies, unresolved paths, changed/shadowed file
contents, and explicit glyph-primitive redefinitions remain fail-closed.
The same strict dependency hash is checked again during conversion replay.
This deliberately narrow allowance is not general support for TeX includes.

The maintenance regression suite passes 31 tests, including dependency
hash/line retention, unknown/body/duplicate input rejection, shadowed-file
rejection, missing resolution, primitive redefinition, and TPC250 conversion.
All 164 previously converted papers were independently regenerated in memory:
their Markdown and provenance records remain byte-for-byte unchanged, with
9,305 math nodes preserved. No previous source or conversion needed rewriting.

TPC250's section “The coherence envelope” has automated PDF hits on pages
2 and 5. Direct `pdftotext -layout` inspection identifies the actual heading
`3 The coherence envelope` on page 2; page 5 contains a prose sentence
starting with the same words. The automated record remains
`UNMAPPED_OR_AMBIGUOUS`, with both candidates retained. Every other new
source-section/page map is unique. No visual PDF certification is claimed.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC250 | [active set and zero cases](../../papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/paper/main.tex#L92); [coherence theorem](../../papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/paper/main.tex#L128); [support budgets](../../papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/paper/main.tex#L195); [sharpness](../../papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/paper/main.tex#L233) | Finite complex Hilbert family; active entries have positive weighted norm, so pair denominators are nonzero. The source correctly defines coherence as zero for zero/singleton active sets and leaves kappa undefined at D=0. The strict noncancellation criterion is sufficient, not necessary. PSD sharpness families establish universal coefficients, not attainability at every prescribed parameter tuple. Independent lane budgets and a global direct-sum budget have different radii. |
| TPC251 | [declared partition](../../papers/tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler/paper/main.tex#L46); [margin compiler](../../papers/tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler/paper/main.tex#L106); [external scalar](../../papers/tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler/paper/main.tex#L148) | Nonempty disjoint exhaustive blocks and literal weights one give the contracted physical output before projection. Complex Gram subtraction uses conjugate(m_b)m_b'; it represents an actual orthogonal projection, not an arbitrary rank-one subtraction assumed PSD. The bound is a pointwise enclosure, not an exact disk image. E≥0 and the independent error bound for F are additional inputs. Strict dominance yields nonzero F; equality need not. |
| TPC252 | [binary update](../../papers/tpc-252-declared-partition-refinement-degeneracy/paper/main.tex#L98); [fixed-family subtraction](../../papers/tpc-252-declared-partition-refinement-degeneracy/paper/main.tex#L170); [singleton optimum](../../papers/tpc-252-declared-partition-refinement-degeneracy/paper/main.tex#L197) | Hold w,g fixed and split one parent into two nonempty children. The exact transverse radius is nonincreasing, but neither covariance magnitude nor the recomputed coherence radius is asserted monotone. Fixed-probe Gram subtraction does not identify native arrays whose input/output indices change. The margin maximum is over all legal partitions including singletons, with the same fixed E; restricting partitions or changing the source/error contract is a different optimization. |
| TPC253 | [rank geometry](../../papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/paper/main.tex#L68); [integer crosswalk](../../papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/paper/main.tex#L123); [partial sums](../../papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/paper/main.tex#L154); [literal adjoint](../../papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/paper/main.tex#L208) | N≥2 makes both children nonempty; positive-on-L means positive real values and fixes the phase of the real Haar contrast. Its projector is rational even when rho is irrational. The threshold floor(3k/4) is proved only for integral k≥3. Means and flat units require nonempty J, although the introductory notation writes merely J subset I. Complex covariance has no automatic sign. The adjoint identity uses no self-adjointness or kernel symmetry. |
| TPC254 | [H2 input](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L77); [m=1 extraction](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L122); [quantifiers](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L155); [norm-only witness](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L214) | Freeze admissible finite K, then gamma=1/4, fixed M and sufficiently strong H2 parameter, then x large. Nonnegative summands and unit m=1 weight bound every active interval before choosing the two children. Their sizes are comparable to x at large x. The inherited H2 comparison theorem is not independently re-proved here. Arbitrary fixed logarithmic strength is not a fixed power, and the adjoint norm remains unpaid in the source's historical interface. |

## Source wording and scope qualifications

### TPC250: marginal obstruction is not every marginal-data question

The [same-marginal proposition](../../papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/paper/main.tex#L297)
uses two unit vectors with weights (1,1). Its aligned and anti-aligned
families have identical marginals and squared sum norm 4 or 0. This proves
that those marginals permit complete cancellation and that no bound strictly
positive on **every** marginal dataset can hold. It does not show that
marginal data can never force positivity in a specified unequal-length case.
For example, weights (2,1) on two unit vectors give
`||2v1+v2|| ≥ 2−1 = 1` by reverse triangle, with equality when v2=−v1.
The general elementary lower bound is
`max(2 max_i a_i − L, 0)` for the norm. Preserve the source proposition while
not promoting its equal-length obstruction into the broader impossibility.

Likewise, `mu(kappa−1)<1` is not necessary for a particular sum to be nonzero:
the aligned equal-weight two-vector example has mu=1, kappa=2, and g≠0,
although the strict criterion fails. The source's theorem only states the
sufficient implication.

### TPC251–253: declared geometry, exact cancellation, and endpoint labels

The [TPC251 eight-coordinate replay](../../papers/tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler/paper/main.tex#L192)
is explicitly synthetic in its detailed caption and scope. Its abstract's
operator-replay values are not evidence of a literal arithmetic instance.
In its second block, the two projected probes cancel and the physical w
residual is zero, even though their coherence upper U is 2. A positive
coherence envelope is not proof of positive contracted residual energy.

TPC252's singleton maximum transfers all source information into C_long=C_x;
it is not a cheaper evaluation theorem for the unknown physical scalar.
Its two-coordinate non-invariance example is existential. The stable
constant-source example in the same manuscript prevents an every-source
instability interpretation. Refinement of the declared decomposition does
not change A, beta, w, or the full scalar.

The [TPC253 crosswalk table](../../papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/paper/main.tex#L138)
labels its last column “left endpoint.” The entries 3m, 3m, 3m+1, 3m+2
are the **last coordinate of the left child**, not its first coordinate.
The proposition and proof-package table correctly identify their role.
The heading is retained literally. For the nonintegral clock x=27/2,
I={7,...,13}, L={7,8,9}, while floor(3x/4)=10; the integer crosswalk
cannot replace the ordered-rank definition there.

The [mean notation](../../papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/paper/main.tex#L156)
should be read on nonempty J: S_f(empty)=0 is valid, but
mu_f(empty)=S_f(empty)/0 is undefined. All children actually used in the
theorem are nonempty, so this is a notation-domain qualification rather
than a failure of its covariance formulas. The inherited superscript in
b_x^(z) is explicitly not the Haar vector z.

### TPC254: sharp Cauchy constant versus every two-dimensional vector

The [norm-only proposition](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L214)
first quantifies over every real unit z and then says that at N=2 equality
holds in Cauchy. Its proof and [proof package](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/PROOF_PACKAGE.md#L78)
establish equality for the particular balanced contrast
z=(1,−1)/sqrt(2), which suffices to show sharpness of the universal constant.
Equality is not valid for every real unit z under the preceding construction.

For z=(z1,z2), beta=(1,1), and
`A=[[0,lambda z1],[lambda z2,0]]`, the displayed row-sum construction gives

```text
<z,A beta> = lambda,
A* z = lambda (z2^2,z1^2),
||A* z||^2 ||beta||^2 = 2 lambda^2 (z1^4+z2^4).
```

For lambda≠0, equality requires z1²=z2²=1/2. In particular,
z=(1,0), lambda=1 gives squared moment 1 but squared Cauchy right side 2.
The original proposition's broad equality wording is preserved and this
quantifier limitation is recorded; its balanced sharpness example remains
valid. These matrices are synthetic and do not refute a literal V59 estimate.

The abstract's “fixed finite cutoff” refers to a fixed finite exponent K;
Z_x=(log x)^K itself varies with x for positive K. Fixed constants and
thresholds in M,K cannot be used at M=M(x) or K=K(x) without a new uniform
input. The source's historical adjoint-lane gap is not rewritten using later
papers during this conversion.

## Independent bounded checks actually executed

- Four exact PSD Gram matrices reproduce upper saturation at m=3, mu=1/3
  (D=3,L=3,quadratic=5), lower saturation at mu=2/5 (quadratic=6/5),
  three-vector simplex cancellation, and the collinear negative raw lower
  endpoint −4 with quadratic zero. Unequal weights (2,1) on opposite unit
  vectors give squared norm 1. No producer was imported.
- An independent reconstruction of TPC251's displayed vectors reproduces
  C_long=11/2, Q_trans=−1, C=9/2, R_trans=R_coh=1 and the external lower
  margin 4 at E=1/2. Direct projected Gram subtraction also agrees.
- A complex four-coordinate refinement reproduces covariance pairs
  (C_long,Q_trans)=(6,6) and (10,2), full scalar 12, and exact radii 6 and 2.
  The increment is conjugate(1+i)(2+2i)=4, not 4i. Fixed-family Gram
  subtraction is checked on two independent nonreal probes. An initial
  scratch comparison used unsimplified symbolic-expression equality; it was
  corrected to compare simplified exact expressions and the checks passed.
- Rational projector identities, zero mean, rank-one trace, idempotence,
  and even/odd rho² formulas pass at N=2,3,5,6,9. Integer crosswalk checks
  pass at k=3,...,27, including all four residue classes. The x=27/2
  nonintegral distinction is checked exactly with fractions.
- The balanced N=2 Cauchy example has squared sides 1 and 1; the unbalanced
  z=(1,0) case has squared sides 1 and 2, confirming the equality-domain
  qualification above.

These bounded checks do not rerun the original 128-, 160-, or 192-family
experiments, the mutation suites, the physical kernel or prime calculations,
or a publication cascade. No original source is repaired to make an audit
pass. The current TPC418 scientific stop, zero fixed-power credit, open full
gate, and prohibition on a new TPC419 remain unchanged.
