# TPC300–304 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`55240d2d7254cbf8bd7fc0b4755fa8f24254e424`. All five complete TeX
manuscripts, README files, proof packages, and external bibliographies were
read. Original scientific sources, hand-edited notes, code, certificates,
and local build products remain unchanged.

## Conversion evidence

The five new reading layers pass the abstract/body formula-sequence and
normalized-text roundtrip checks: 286 math nodes and 34 raw-source display
blocks. Their preserved PDFs contain 15 extracted pages, with a unique
heading-text page match for every source section. The versioned original
PDF is selected from the source commit, not from an ignored local build.
Every record includes source/PDF/BibTeX hashes, section lines, page maps,
display catalogues, known conversion limits, and this supplemental audit.
External BibTeX is retained in full, without resolving citation keys or
independently verifying titles and bibliographic claims.

No producer, full scientific checker, physical Gram construction, numerical
optimizer, certificate regeneration, or production cascade was executed.
The small exact examples below check specific algebraic conditions only.
Read-only inspection of the TPC304 transport implementation does not
reproduce its saved physical labels or budget crosswalk. No visual PDF
certification, PDF/TeX build synchronization, or full proof validation is
claimed by the conversion status.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC300 | [weak dual](../../papers/tpc-300-native-budget-dual-certificate/paper/main.tex#L71); [active frontier](../../papers/tpc-300-native-budget-dual-certificate/paper/main.tex#L112); [rational compiler](../../papers/tpc-300-native-budget-dual-certificate/paper/main.tex#L151) | Real compatible data, `M>0`, `rho>0`, `R>=0`, and primal feasibility make the ridge system invertible and the weak-dual value a lower bound. Positive definiteness also supplies coercivity and attainment. The reciprocal KKT multiplier is for the squared-residual constraint and a positive active multiplier. The strict interval `dist(b,range V)<R<||b||` gives a visible target component, Slater feasibility, and a unique positive residual crossing; the boundary cases are not covered. Rational inputs, including R squared rather than necessarily R, yield rational coefficients and a rational weak-dual value. A rounded rational rho is not the exact active optimizer merely because its dual is close. |
| TPC301 | [budget assumptions](../../papers/tpc-301-budget-gap-robustness-audit/paper/main.tex#L48); [finite identities](../../papers/tpc-301-budget-gap-robustness-audit/paper/main.tex#L78); [common weighted prefix](../../papers/tpc-301-budget-gap-robustness-audit/paper/main.tex#L137) | Nonzero targets, `0<tau<1`, `M_k>0`, and feasibility ensure positive budget quotients. Tolerance nesting fixes k; relative target scaling uses a nonzero scalar and scales the allowable radius too. First-feasible-prefix comparisons require existence, which is not a consequence of nested column spaces alone. The weighted-selected prefix is common only after checking `k_positive<=k_weighted`; this ordering is not universal. All three normalizers must be positive and target-independent at the same prefix. Their ratio cancellation is algebraic, not independent replication. |
| TPC302 | [Gram and targets](../../papers/tpc-302-growing-shell-budget-gap-audit/paper/main.tex#L40); [sign enumeration](../../papers/tpc-302-growing-shell-budget-gap-audit/paper/main.tex#L67); [budget nesting](../../papers/tpc-302-growing-shell-budget-gap-audit/paper/main.tex#L93) | Finite real output Grams are PSD; a positive trace is additionally required for the displayed normalized R. A nonempty binary sign domain has two-element global-sign orbits, so fixing the first sign selects one representative. This is not a normalization for arbitrary real coefficient vectors. Rational exact comparison requires clearing a common positive denominator and checking the actual incremental update, not merely traversing every Gray bit string. Prefix cost nesting uses consistent profile Grams as well as nested response columns. Exact Gram/sign ratios remain distinct from numerically solved budget ratios. |
| TPC303 | [fixed-source scope](../../papers/tpc-303-cardinality-monotonicity-obstruction/paper/main.tex#L38); [interval order](../../papers/tpc-303-cardinality-monotonicity-obstruction/paper/main.tex#L52); [same-prefix interpretation](../../papers/tpc-303-cardinality-monotonicity-obstruction/paper/main.tex#L72) | Valid ordered enclosures and strict endpoint separation imply the stated order. Touching/overlapping intervals alone prove neither order nor equality. One descent refutes a nondecreasing law on the declared finite cardinality spine; proving that every individual series is neither increasing nor decreasing needs an ascent and descent in each, not just aggregate counts. Same prefix index fixes the source profile space here because the source and ordered ladder are locked, but the physical image, shell, and target still change. Moving shells are not an inclusion chain, and finite descents do not refute eventual lower bounds. |
| TPC304 | [transport identity](../../papers/tpc-304-overlapping-shell-label-transport/paper/main.tex#L52); [proof](../../papers/tpc-304-overlapping-shell-label-transport/paper/main.tex#L71); [crosswalk](../../papers/tpc-304-overlapping-shell-label-transport/paper/main.tex#L85) | Nonempty finite overlaps and binary labels give `rho=abs(u)/n`, `d=(1-rho)/2`, `0<=rho<=1`, and `0<=d<=1/2`. These scalar quantities are gauge-invariant even at u zero; uniqueness or equivariance of a selected alignment sign is a different issue. The source proof drops an absolute value in an intermediate identity, while its theorem and inspected implementation retain it. Correlation means and disagreement fractions must not be conflated. The fracture threshold is a declared finite convention, and a shared location of label change and budget descents is association, not causal identification. |

## Source qualifications and preserved discrepancies

TPC300's [singular-coordinate proof](../../papers/tpc-300-native-budget-dual-certificate/paper/main.tex#L124)
displays the squared residual. Its monotonicity is strict when at least one
visible singular component has nonzero target coefficient; the strict
radius interval already excludes an entirely invisible target. At an
inactive radius `R>=||b||`, the zero coefficient has zero primal budget,
and an active positive-rho equality cannot be inferred. At the least-
squares boundary, the active point may occur only as rho tends to zero.
Likewise `mu=1/rho` is not a finite reciprocal rule for a zero KKT
multiplier. The original theorem states the needed strict active range;
its shorter summaries are read under those conditions. Weak duality does
not require the dual to be positive or the ridge vector to be feasible.
Hashes of exact fractions protect representation identity, not truth of
the linear solve or tightness against an unverified parent enclosure.

TPC301's [proof-package prefix argument](../../papers/tpc-301-budget-gap-robustness-audit/PROOF_PACKAGE.md#L31)
says that the set of feasible indices “therefore has a first element.”
Nesting gives a first element only if the finite set is nonempty. For
`V_k=0` at every available prefix, target b=1, and tau=1/2, all normalized
least-squares residuals are 1; even positive-definite profile metrics do
not create a feasible index. The correction is an explicit existence
qualification, not a claim that any published row is infeasible. The
main protocol separately checks the positive-target prefix ordering;
using the weighted prefix without that check is not justified by the
single-target nesting lemma.

TPC302's [prefix proof](../../papers/tpc-302-growing-shell-budget-gap-audit/PROOF_PACKAGE.md#L20)
uses a larger coefficient space. The costs remain comparable because
`U_k` are prefixes of one fixed U, `M_k=U_k^T U_k`, and zero-padding
keeps both the physical image and source norm unchanged. Nested V columns
alone would not suffice with unrelated metrics: at tolerance zero and
target 1, `V_1=(1), M_1=(1)` has budget 1, while
`V_2=(1,0), M_2=diag(100,1)` has budget 100. This does not contradict
the source's consistent-Gram construction. It states the additional
premise used in the shorthand feasible-set argument.

The [TPC302 proof-package wording](../../papers/tpc-302-growing-shell-budget-gap-audit/PROOF_PACKAGE.md#L40)
“all reported ratios are exact rational replays” must be restricted to
the rational Gram/sign observables discussed there. The following sentence
and manuscript separately describe 60-digit numerical frontier solves;
their budget quotients are not established as exact optimized rational
values by this maintenance. Likewise “equal-sign” in the enumeration
paragraph means the declared equal-magnitude binary domain, not only
the two all-equal labels. PSD and sign symmetry by themselves prove
neither a strict minimum below the diagonal normalization nor an
all-positive value above it; those are source-reported finite comparisons.

TPC304's TeX proof at [line 75](../../papers/tpc-304-overlapping-shell-label-transport/paper/main.tex#L75)
and proof package at [line 15](../../papers/tpc-304-overlapping-shell-label-transport/PROOF_PACKAGE.md#L15)
write the raw inner product as `u=n-2*d_min`. The right-hand side is
nonnegative, so the identity needs `abs(u)`, or u must first be explicitly
redefined as the aligned inner product. With one coordinate a=1, b=-1,
raw u is -1 and the optimal mismatch count is zero, so the printed raw-u
identity reads `-1=1`. The displayed theorem correctly uses `abs(u)`.
The inspected [transport implementation](../../papers/tpc-304-overlapping-shell-label-transport/code/tpc304_overlapping_shell_label_transport.py#L169)
also uses `abs(raw_inner_product)`, computes mismatches after alignment,
and records raw and aligned values as distinct fields. This is a proof-
line omission, not evidence that the saved correlation computation uses
the wrong sign. The inspected file matches the source commit and has
SHA-256 `5f1eeab4ad8200fad7d1a06af0b2a25534bd07f2d471250e6e22d22a856b25d9`.

The [paragraph following TPC304's table](../../papers/tpc-304-overlapping-shell-label-transport/paper/main.tex#L108)
places the middle disagreement fraction 5/11 next to outer group means
1/2. The latter are correlation means. In the same metric, the middle
correlation is 1/11 and each outer correlation mean is 1/2; the middle
disagreement is 5/11 and each outer disagreement mean is 1/4. The
minimum-correlation and maximum-disagreement statements agree after
keeping these two scales separate. The original prose is retained.

TPC300–302 retain separate numerical claim levels. Exact rational
coefficients/Gram computations do not by themselves establish all bounds
through a high-precision optimizer. TPC303–304 inherit the parent
numerical enclosures and class labels; this audit does not upgrade them.
The inherited 1,380-edge metadata, 219 explicit targets on 18 rows, and
430 explicit targets on 34 rows are kept as distinct source census
fields, not silently reconciled or recounted as one quantity. Reproduction
commands are retained literally, including `--write` and the mixed
project/repository working-directory assumptions; none were executed.

## Bounded checks and coverage

For the scalar case `V=M=b=1, R=1/2`, exact fractions give at rho=1/2:
`c=2/3`, `D=1/6`, true budget `1/4`, and feasible primal cost `4/9`.
At rho=1 the active point is `c=1/2` and dual, budget, and primal all
equal `1/4`. This checks both weak inequality and an active equality,
without replaying any physical ridge system.

Exhausting every pair of binary labels of lengths 1 through 4 gave 340
standalone transport fixtures. The displayed absolute-value identity and
normalized mismatch formula passed in all 340; the raw-u equality failed
in the 118 negative-inner-product fixtures. This is not the project's
scientific stress suite or its six stored label rows. Small count checks
gave `18*4=72` rational witness slots, `18*3*3*2=324` and
`34*3*3*2=612` frontier slots, and `2*3*3*3=54` adjacent comparisons.
The source's budget values, tightness floors, and per-series classes were
not recomputed.

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 300 --last 304
```

The new total is 119 `full-source-md`, 0 `reliable-full-md`, 703
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC300–418 now have mechanical reading layers with 5,777 math nodes.
Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC295–299. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. Conversion creates
no new paper number, source correction, theorem, or route reopening.
