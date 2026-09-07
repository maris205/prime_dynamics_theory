# TPC320–324 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`88c46824c79e9c202a698cf4db36fcaf98260537`. The five complete TeX
manuscripts, README files, proof packages, and bibliography sidecars were
read. Original sources, hand-edited summaries, scientific code, and
certificates are unchanged.

## Conversion evidence

The five reading layers preserve abstract/body text and formulas under the
declared Pandoc reader/writer roundtrip checks: 316 math nodes and 52
raw-source display blocks. The retained PDFs have 15 extracted pages;
every source section has a unique heading-text page match. Per-paper
records contain source/PDF hashes, source section lines, page maps,
formula catalogues, conversion limits, and a link to this audit.

TPC320–321 contain in-source bibliography entries, retained in the reading
layers. Their unused bibliography sidecars remain untouched. TPC322–323
have no manuscript bibliography; their sidecars contain comments only.
TPC324 uses external BibTeX, preserved in full and hash-locked, with
unresolved citation keys explicit. Bibliographic claims were not verified
against outside sources.

Neither text extraction nor source roundtrips certify visual PDF quality,
PDF/TeX build synchronization, mathematical correctness, or numerical
reproduction. No scientific producer, certificate checker, eigensolver,
large rational anchor, or production cascade was run. Two TPC321 metric
functions were inspected read-only to resolve the normalization discrepancy
below; they were not executed.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC320 | [readouts](../../papers/tpc-320-trace-normalized-spectral-concentration/paper/main.tex#L72); [finite bounds and invariance](../../papers/tpc-320-trace-normalized-spectral-concentration/paper/main.tex#L97); [quotient enclosure](../../papers/tpc-320-trace-normalized-spectral-concentration/paper/main.tex#L135) | For a finite PSD matrix, positive trace gives positive largest eigenvalue and positive squared spectral mass, so the displayed concentration/rank quotients are defined. Use `1<=k<=N`. Normalized entropy additionally requires `N>1`, not merely positive trace; all declared counts satisfy it. Positive-scalar invariance is at fixed dimension and does not equate different scale matrices. The outward quotient formula requires a nonnegative numerator interval and a strictly positive lower trace bound. Strict decrease from intervals requires upper-next below lower-current, not just a point-estimate ratio below one. Gap ratios also require a nonzero denominator eigenvalue. |
| TPC321 | [metrics](../../papers/tpc-321-cross-shell-profile-stability/paper/main.tex#L100); [metric proof](../../papers/tpc-321-cross-shell-profile-stability/paper/main.tex#L124) | Both profiles must have the same dimension, nonnegative coordinates, and unit total mass. `N>1` is needed for the interior maximum and the `1/(N-1)` average. Total variation is one half of the rank-coordinate `l1` distance, not a distance between eigenvalue locations. Ordered equal-mass profiles support the stated non-strict majorization definition; tolerance-based numerical labels do not prove exact signs at all prefixes. Changing a prime shell changes the matrix and is not positive scalar rescaling. The README's integrated-distance normalization differs from TeX and both inspected implementations. |
| TPC322 | [embedding and projector](../../papers/tpc-322-signed-projector-reassembly/paper/main.tex#L89); [ratios and block Gram](../../papers/tpc-322-signed-projector-reassembly/paper/main.tex#L119) | A nonempty finite shell (`m>0`), signs with `e_p^2=1`, and common block domains/codomains give the isometric embedding and projector. The identities before division also hold for zero blocks, but `rho` and `phi` require `D>0`. PSD alone does not prove this positivity. Projection contraction gives `0<=phi=rho/m<=1`, not `rho<=1`; equivalently `rho<=m`. Global sign reversal preserves the ratio and permits `2^(m-1)` gauge-reduced enumeration, but does not supply an arithmetic sign law. A Frobenius-energy ratio is not a contraction estimate for each source vector. |
| TPC323 | [trace/profile coordinates](../../papers/tpc-323-signed-profile-majorization/paper/main.tex#L79); [factorization](../../papers/tpc-323-signed-profile-majorization/paper/main.tex#L103) | The direct trace and coherent trace identities follow from finite Gram algebra; each profile requires its own strictly positive trace. Coherent cancellation can destroy the latter even when the direct trace is positive. Shape and total amplitude retain different information, not probabilistic independence or arbitrary free variation within one frozen sign family. Recovering the signed matrix from its ratio, profile, and eigenbasis also needs the reference direct trace. Majorization compares same-dimensional unit-mass ordered profiles; the four-law finite selection is not uniqueness over all signs or arithmetic weights. |
| TPC324 | [covariance proposition](../../papers/tpc-324-source-profile-holdout/paper/main.tex#L97); [holdout intervals](../../papers/tpc-324-source-profile-holdout/paper/main.tex#L123) | Translation is a bijective coordinate relabeling. Differences and congruence differences are shift-invariant; divisibility masks are invariant under the additional hypothesis that every active prime divides the shift. Keep the same prime-indexed signs, shell, height, and exponent. The conditional conjugation identity holds before normalization; ratio/profile conclusions need the appropriate positive traces. Failure of this sufficient divisibility condition does not alone prove changed spectra or exclude other coincidences. The declared interval separation and shell witnesses were checked directly; numerical profile replication and historical preregistration were not independently reconstructed. |

## Source discrepancies and qualifications preserved

TPC321's [README formula list](../../papers/tpc-321-cross-shell-profile-stability/README.md#L37)
uses `N^-1` for the integrated interior-prefix discrepancy, while
[TeX equation](../../papers/tpc-321-cross-shell-profile-stability/paper/main.tex#L110)
uses `1/(N-1)`. The inspected
[producer metric](../../papers/tpc-321-cross-shell-profile-stability/code/tpc321_cross_shell_profile.py#L204)
and [independent metric](../../papers/tpc-321-cross-shell-profile-stability/experiments/tpc321_independent_checker.py#L119)
both take the mean over the `N-1` interior prefixes, agreeing with TeX.
For the exact ordered profiles `(3/4,1/4)` and `(1/2,1/2)`, the TeX value
is `1/4`, while the README's formula gives `1/8`. Several original Markdown
formula fragments in this batch also have missing escapes or control-character
damage. These summaries remain preserved as originals; the new complete
reading layers are generated from TeX, not reconstructed from those fragments.

TPC323's [proof-package reconstruction sentence](../../papers/tpc-323-signed-profile-majorization/PROOF_PACKAGE.md#L26)
omits the absolute reference scale if read as a standalone sufficiency claim.
The reconstruction is
`G_e = rho_e * tr(G_direct) * V diag(pi_e) V^T`.
For the scalar block family `B_1=B_2=[1]` with all-plus signs, the direct
and coherent energies are 2 and 4; after scaling both blocks by 2 they
are 8 and 16. The ratio 2, profile `(1)`, and eigenbasis are unchanged,
but the signed Gram differs. The sentence is therefore valid only when
the direct trace is already known from the fixed reference family. No
original formula or proof package was edited.

TPC324's [positive-trace proof](../../papers/tpc-324-source-profile-holdout/PROOF_PACKAGE.md#L33)
mentions nonzero literal blocks. That implies a positive direct trace, but
does not alone imply a positive coherent trace: the nonzero scalar blocks
`B_1=B_2=[1]` cancel under signs `(+,-)`. Positive coherent traces on the
declared rows must come from the stated row checks or a separate noncancellation
argument, not solely from PSD/nonzero blocks. TPC322's
[block-Gram proposition](../../papers/tpc-322-signed-projector-reassembly/PROOF_PACKAGE.md#L32)
likewise needs a nonzero block family for its strict `D>0` claim.
These are prerequisite qualifications, not claims that an actual panel row
has zero trace.

TPC320's entropy formula has denominator `log N`; its general invariance
statement must retain `N>1`. The panel has `N=320,640,1280`, so this
qualification does not invalidate its declared rows. The TPC321 and TPC323
definitions allow equality in majorization, whereas TPC324's printed
convention adds at least one strict interior prefix. Each local definition
is retained without silently imposing one convention on all three papers.

The observed path extrema expanded by `10^-12` in
[TPC321](../../papers/tpc-321-cross-shell-profile-stability/paper/main.tex#L152),
[TPC322](../../papers/tpc-322-signed-projector-reassembly/paper/main.tex#L160),
[TPC323](../../papers/tpc-323-signed-profile-majorization/paper/main.tex#L142),
and [TPC324](../../papers/tpc-324-source-profile-holdout/paper/main.tex#L145)
are source-declared numerical guards. Agreement of multiple floating paths,
by itself, is not an independently proved enclosure of the exact finite
matrix quantity: all paths can share error. This archive preserves the
source's certification labels, but does not endorse a rigorous error bound
or reclassify them as mathematical proof. TPC320 states a different
entrywise/Weyl guard protocol; its implementation and error budget were not
audited or rerun here either.

Bounded integer checks confirm that all nine printed parent/holdout intervals
are pairwise disjoint and have the stated cardinalities. The shifts relative
to matching parent sizes are `2240,2240,2240` and `4680,5360,6720`.
For the shells at `Q=24,36,54,80`, respectively, the active primes
`29,37,59,83` each fail to divide every one of these six shifts, so no shift
satisfies the common-divisibility hypothesis for any of the four shells.
This verifies failure of that sufficient hypothesis, not spectral inequality.
Direct trial-division counts give shell sizes `6,9,12,15`, consistent with
the largest gauge-reduced search count `2^14=16384`.

The scalar block example above also checks `rho_plus=2`, `phi_plus=1`,
and zero coherent minus energy. Independently, `diag(3,1)` and `diag(2,2)`
have the same trace 4 but different profiles, while `diag(3,1)` and
`diag(6,2)` have the same profile and different traces. These elementary
examples justify the direction of the amplitude/shape distinction without
replaying the 16-coordinate rational anchors. Panel counts are 24 base rows,
80 TPC320 scale/cluster comparisons, 18 TPC321 adjacent-shell comparisons,
96 TPC323 row/law comparisons, and 48 TPC324 holdout rows.

## Coverage and handoff

```bash
python -B research/tpc-big-road/check_source_markdown_batch.py --first 320 --last 324
```

The new total is 99 `full-source-md`, 0 `reliable-full-md`, 723
`partial-or-notes`, and 1 `source-inaccessible`, across 823 entries.
TPC320–418 now have mechanical full-source reading layers with 4,467 math
nodes in total. Earlier scope notes remain historical batch snapshots.

Next existing-source batch: TPC315–319. TPC418's scientific stop remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with arithmetic advance
`NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new number,
theorem, source correction, or route reopening is authorized by conversion.
