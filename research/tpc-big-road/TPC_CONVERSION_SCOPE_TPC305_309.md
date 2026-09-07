# TPC305–309 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`ed725e6537012bd17a32d061d9d8e6dd3b253613`. All five complete TeX
manuscripts, README files, proof packages, and external bibliographies were
read. Original manuscripts, hand-edited materials, code, certificates, and
build products are unchanged.

## Conversion evidence and original PDF selection

The five reading layers pass abstract/body formula-sequence and normalized-
text roundtrip checks: 386 math nodes and 31 raw-source display blocks.
The preserved PDFs contain 19 extracted pages; every source section has
a unique heading-text page match. Each record contains source/PDF/BibTeX
hashes, section lines, page maps, formula catalogues, and explicit limits.
External BibTeX is retained in full; citation keys and bibliographic claims
are not independently resolved or verified.

TPC305–307 version `paper/paper.pdf`, while their local `paper/main.pdf`
files are ignored build products. The converter now chooses the known PDF
name present in the locked source commit, preferring `main.pdf` when that
name is versioned and otherwise using `paper.pdf`. It checks the selected
file against that commit, does not use a merely present ignored build,
fails if the versioned original is missing locally, and creates no alias.
TPC308–309 retain their versioned `main.pdf` choice; both original names
remain untouched. All 109 earlier Markdown/record pairs were regenerated
read-only and compared byte-for-byte after the change: unchanged, with
5,105 math nodes and unchanged inventory outputs. The 16 read-only
maintenance regression tests passed, including PDF priority and fallback.

No scientific producer, full checker, frontier optimizer, physical matrix
replay, or production cascade was run. Limited implementation inspection
and standalone exact arithmetic below do not reproduce the source's
numerical bounds or class labels. No visual PDF certification, PDF/TeX
build synchronization, or full mathematical verification is claimed.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC305 | [transport definition](../../papers/tpc-305-counterfactual-transported-label-budget/paper/main.tex#L65); [budget and prefix](../../papers/tpc-305-counterfactual-transported-label-budget/paper/main.tex#L84); [alignment proposition](../../papers/tpc-305-counterfactual-transported-label-budget/paper/main.tex#L122) | Binary overlap alignment maximizes the inner product over the two signs, including a nonunique optimum at zero. Native off-overlap extension is part of the target and cannot be dropped. Nested columns and existence of each first feasible prefix justify their maximum. Budget quotients need a positive native budget, not just a positive external normalizer; a common positive normalizer cancels exactly. The strict orientation table follows from the opposite right-row target convention. The printed all-parent-flip gauge claim needs a zero-tie qualification, detailed below. |
| TPC306 | [effects](../../papers/tpc-306-two-way-operator-target-interaction/paper/main.tex#L62); [contrast identity](../../papers/tpc-306-two-way-operator-target-interaction/paper/main.tex#L78); [scaling](../../papers/tpc-306-two-way-operator-target-interaction/paper/main.tex#L97) | All four cells must be positive for their logarithms. Expanding the squares gives `m^2-i^2=d_L*d_R`; strict dominance follows from nonzero row effects. The diagnostic `q=|i|/|m|` additionally requires `m!=0`. Positive row rescaling leaves the effects and, when defined, q unchanged; it does not make row-specific completions into the same target vector. The three normalizers are algebraically redundant for exact within-row ratios, not three independent physical replications. |
| TPC307 | [fit and holdout](../../papers/tpc-307-common-ambient-union-shell-holdout/paper/main.tex#L89); [sign and prefix claims](../../papers/tpc-307-common-ambient-union-shell-holdout/paper/main.tex#L121); [package assumptions](../../papers/tpc-307-common-ambient-union-shell-holdout/PROOF_PACKAGE.md#L19) | The union/overlap/exclusive sets partition the finite union. Nonempty overlap and exclusive sets make the binary fit norm and mean holdout loss meaningful; ratio denominators must be positive. The feasible-cost sets are paired by `c -> -c`, giving exact budget invariance. A selected holdout loss is invariant for that paired coefficient or a sign-equivariant selection rule; PSD alone does not ensure uniqueness. Overlap-only fitting is not statistical independence or removal of the expressly inherited Gram-dependent label leakage. |
| TPC308 | [completion definitions](../../papers/tpc-308-adversarial-exclusive-completion-envelope/paper/main.tex#L82); [finite algebra](../../papers/tpc-308-adversarial-exclusive-completion-envelope/paper/main.tex#L103); [ratio conditions](../../papers/tpc-308-adversarial-exclusive-completion-envelope/paper/main.tex#L130) | Require positive holdout length, binary labels, integer radius `r>=0`, and fixed predictions. Flip-subset enumeration is a bijection, counts truncate at `min(r,m)`, and extrema are attained on the finite nonempty set. Enlarging a ball lowers its minimum and raises its maximum without refitting. Positive lower denominator bounds give the displayed conservative quotient enclosure; independently allowed left/right completions also make the exact endpoints attainable, while coupled completions generally give only outer bounds. Simultaneously negate predictions and labels for sign invariance. |
| TPC309 | [profile windows](../../papers/tpc-309-profile-prefix-shift-sensitivity/paper/main.tex#L69); [prefix and frontier](../../papers/tpc-309-profile-prefix-shift-sensitivity/paper/main.tex#L86); [completion facts](../../papers/tpc-309-profile-prefix-shift-sensitivity/paper/main.tex#L131) | The 19-prime pool has three ordered 17-element windows, adjacent intersections of size 16, and LOW/HIGH intersection of size 15. Nesting applies within each ladder, not between the three shifted windows. The fixed physical kernel/shell rows induce different profile-response matrices `V_{U,a}` as a changes; literal matrix equality is not implied. First-feasible indices must exist under a specified squared-residual/RMS convention. Binary completion, positive-length/loss, and common-normalizer requirements remain. No monotonic preference or limiting claim follows from a same-dimensional shift. |

## Source qualifications and counterexamples

TPC305's [alignment proof](../../papers/tpc-305-counterfactual-transported-label-budget/paper/main.tex#L129)
says that flipping a parent flips u and the aligned neighboring label,
leaving aligned products invariant. For `u!=0` the alignment sign flips,
and the claimed full-vector gauge relation follows. At `u=0`, the prescribed
tie sign stays +1 after the flip. Consider an overlap of two coordinates,
one exclusive coordinate on each side, and native labels
`a_L=(1,1;1)`, `a_R=(1,-1;1)`, where the semicolon separates each
exclusive part. Initially the transported vectors are
`t_L=(1,-1;1)`, `t_R=(1,1;1)`. After negating a_L alone, they are
`t_L=(1,-1;-1)`, `t_R=(-1,-1;1)`. Neither new transported vector is a
global sign multiple of its old version. The overlap mismatch count remains
one and the maximum overlap inner product remains zero; those weaker
statements survive. This is a missing tie qualification in the general
proposition, not a claim to have found a failing published physical cell.
The original proposition and deterministic protocol remain preserved.

TPC306's [definition of q](../../papers/tpc-306-two-way-operator-target-interaction/paper/main.tex#L70)
and its scaling proposition need the extra condition `m!=0`. Positive cells
do not supply it: `(B_LL,B_LR,B_RL,B_RR)=(1,2,2,1)` gives
`d_L=log 2`, `d_R=-log 2`, `m=0`, and `i=log 2`. The exact contrast
identity and strict interaction dominance hold, but q is undefined as a
real quotient. This example does not invalidate the separately reported
finite q values; their denominators were not replayed here.

TPC307's [proof-package sign argument](../../papers/tpc-307-common-ambient-union-shell-holdout/PROOF_PACKAGE.md#L62)
correctly pairs optimal coefficients under negation but does not justify
an arbitrary minimizer selection having the same holdout loss. For the
general PSD assumptions written there, take `M=diag(1,0)`, overlap row
`V_O=(1,0)`, holdout row `V_E=(0,1)`, target `b=1`, and tolerance zero.
Every `(1,t)` minimizes the cost. Selecting `(1,1)` with holdout target
`h=1` gives loss zero. For `b=-1,h=-1`, selecting `(-1,1)` is also
optimal but has holdout loss four; selecting the paired `(-1,-1)` instead
gives zero. Thus the general holdout assertion needs paired selection,
unique predictions, or additional source/response compatibility. A
positive-definite metric and a nonempty feasible convex set are one
sufficient uniqueness route. This toy example addresses the abstract PSD
statement, not the rank of the published profile systems or their solver.

TPC309's [prefix prose](../../papers/tpc-309-profile-prefix-shift-sensitivity/paper/main.tex#L90)
compares a “least-squares residual” to `tau^2*||t||^2`; this must mean
the squared residual. The inspected [call site](../../papers/tpc-309-profile-prefix-shift-sensitivity/code/tpc309_profile_prefix_shift_sensitivity.py#L268)
uses the parent [prefix routine](../../papers/tpc-307-common-ambient-union-shell-holdout/code/tpc307_common_ambient_union_shell_holdout.py#L312),
which computes `sqrt(residual_squared/target_norm_squared)` and compares
it to tau plus a declared numerical threshold tolerance. Its
[least-squares routine](../../papers/tpc-307-common-ambient-union-shell-holdout/code/tpc307_common_ambient_union_shell_holdout.py#L296)
returns the squared residual. These are consistent after that interpretation;
the finite tolerance is not exact boundary certification.

The [proof-package phrase](../../papers/tpc-309-profile-prefix-shift-sensitivity/PROOF_PACKAGE.md#L34)
“up to the row rank” must not be treated as an identity between prefix
length and rank. Mathematical feasibility persists to every longer available
prefix even after rank saturation. For example, `V=(0,1)` has rank one
but first exactly feasible prefix two for target 1. The inspected routine
caps k at `min(V.rows,V.cols)` and calls a QR solver; its success on the
locked panel is not a generic rank-deficient-prefix guarantee. No such
physical system was solved again here.

TPC307–309 explicitly describe float64 physical assembly, decimalized
high-precision solves, and padded numerical replay, not directed-rounding
certification. TPC305–306 use stronger certificate language in their
originals, but this maintenance does not independently establish their
enclosure validity. All reproduction blocks mix project-relative code paths
with repository-root Bridge-B paths, and include source-writing commands;
they are retained literally and were not executed.

## Bounded checks and coverage

Standalone exact calculations checked the tied-label counterexample and
the nonunique PSD holdout example. For the completion anchor
`y=(2,0), h=(1,-1)`, radii 0, 1, 2 give loss extrema `(1,1)`, `(1,5)`,
`(1,5)`. Binomial counts for the stated exclusive cardinalities
`(2,5),(2,4),(5,7)`, each repeated in six cells, give `36,186,480`
candidates, total 702. Three profile ladders give `108,558,1440`, total
2106. These are combinatorial checks, not reconstruction of physical losses
or any concordance/discordance census. Window lengths and intersections
were checked directly from the displayed prime tuple.

```bash
python -B -m unittest discover -s research/tpc-big-road -p test_source_markdown_maintenance.py -v
python -B research/tpc-big-road/check_source_markdown_batch.py --first 305 --last 309
```

The new total is 114 `full-source-md`, 0 `reliable-full-md`, 708
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC305–418 now have mechanical reading layers with 5,491 math nodes.
Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC300–304. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new paper number,
source correction, theorem, or route reopening is created by conversion.
