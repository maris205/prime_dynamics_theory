# TPC245–249 conversion and bounded prerequisite audit

Updated 2026-09-08. Original source lock:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. This covers five existing papers
only. Original scientific sources, saved artifacts, PDFs, and hand edits
remain unchanged.

## Reading and conversion scope

The independent read-only audit read all 42 manuscript/package text files,
including local macro/section inputs of TPC245–246, every README, proof
package, and bibliography. It extracted five existing PDFs (21 pages) and
reported `SCOPED_ARCHIVE_REVIEW_ONLY`. Its two inventories of the 47 source/
PDF files agreed. This is bounded premise/formula review, not reliable full
semantic verification, physical reproduction, or a new release certificate.

TPC245–246 use the [restricted static-input helper](source_markdown_includes.py);
TPC247–249 retain the existing single-file conversion path. Every included
source is hash-locked to the same commit, with original file/line locations.
The glyph-map allowance remains exact-hash-only and executes no TeX.
TPC245–246 have comment-only, uninvoked bibliography files; no references
are invented. Invoked bibliography material in TPC247–249 is retained.
Per-paper conversion records contain actual counts, formula/text comparisons,
source/PDF hashes, equation catalogues, and automated page candidates.

All five source locks and full abstract/body formula/text roundtrips pass:
386 math nodes and 71 raw display blocks over 21 existing PDF pages.
TPC245 has two unresolved automatic heading locations and TPC246 has one;
TPC247–249 have none. Manual supplements below retain the automated status.
The input-boundary defect/repair history, independent re-audit, and old-169
byte-preservation check are recorded in the
[companion batch audit](TPC_CONVERSION_SCOPE_TPC240_244.md#static-input-repair-and-regression-record).

## Per-paper premises and formula boundaries

All inner products use the source convention: conjugate-linear first slot.

| Paper | Original source anchor | Bounded finding |
|---|---|---|
| TPC245 | [classification](../../papers/tpc-245-sharp-longitudinal-transverse-covariance-disks/paper/sections/3_classification.tex#L3); [split and inverse](../../papers/tpc-245-sharp-longitudinal-transverse-covariance-disks/paper/sections/4_proof.tex#L12); [phase](../../papers/tpc-245-sharp-longitudinal-transverse-covariance-disks/paper/sections/5_sharp_corollaries.tex#L3) | Unit longitudinal direction, prescribed complex moments, nonnegative transverse energies. Center is conjugate(w)b. Transverse dimension ≥2 gives a disk; dimension 1 with positive radius gives a circle. Dimension 0 with either positive energy is unrealizable even if their product is zero. Zero radius is treated before division. The phase formula requires radius strictly below center modulus. |
| TPC246 | [joint domain](../../papers/tpc-246-weighted-covariance-disk-reassembly/paper/sections/2_joint_geometry.tex#L3); [reassembly/inverse](../../papers/tpc-246-weighted-covariance-disk-reassembly/paper/sections/3_exact_reassembly.tex#L3); [transfer](../../papers/tpc-246-weighted-covariance-disk-reassembly/paper/sections/5_source_transfer.tex#L19) | A finite nonempty joint domain and marginal disks give containment; the full Cartesian product gives equality. The aggregate radius uses absolute weights, and the inverse uses their conjugated phases. The same multiplier in both lanes contributes modulus squared. The inherited common-window transfer gives an inflated containing radius, not an exact physical image. |
| TPC247 | [source scalar](../../papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex#L42); [matrix](../../papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex#L70); [blocks](../../papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex#L102); [tagged norms](../../papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex#L138) | Taking the displayed finite scalar as input, prime moduli and unit masks justify diagonal deletion. Outer q and the oriented kernel are retained. Real w gives inner(w,A beta); an unconjugated complex coefficient requires conjugate(w) in the first slot. Exactly-once coverage requires disjoint exhaustive hard blocks. Tagging does not generally preserve the contracted output norm, nor imply Hermiticity, positivity, or synthesis identification. |
| TPC248 | [minimum preimage](../../papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/paper/main.tex#L90); [sphere branches](../../papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/paper/main.tex#L144); [orientation](../../papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/paper/main.tex#L164); [groups](../../papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/paper/main.tex#L186) | Finite-dimensional complex space, fixed probes, and nonnegative radii. Range membership is indispensable in addition to a pseudoinverse inequality. Kernel slack fills missing sphere energy; the injective case gives an equality shell. Physical covariance orientation uses conjugate(G). Independent group balls and a global energy budget give different images. |
| TPC249 | [weighted probe](../../papers/tpc-249-sharp-weighted-shared-lane-contraction/paper/main.tex#L65); [inverse](../../papers/tpc-249-sharp-weighted-shared-lane-contraction/paper/main.tex#L83); [affine model](../../papers/tpc-249-sharp-weighted-shared-lane-contraction/paper/main.tex#L110); [global budget](../../papers/tpc-249-sharp-weighted-shared-lane-contraction/paper/main.tex#L130) | Fixed finite probes/weights and independent complex lane balls. The contracted probe has unconjugated weights; its squared norm is the Hermitian Gram quadratic. The inverse conjugates the target, after excluding zero probe. Independent radii sum support norms; a global radius uses the direct-sum norm. Marginal equality needs positive-ray alignment in positive-budget groups. No asymptotic Gram estimate is proved. |

## Preserved source qualifications

1. The [TPC248 README](../../papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/README.md#L27)
   says the sphere has the solid ball image iff the adjoint kernel is nonzero.
   This misses radius zero: sphere and ball are then both {0}, even in the
   injective case. The manuscript theorem and
   [proof package](../../papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/PROOF_PACKAGE.md#L24)
   correctly retain both formulas at zero radius. This is a wording disagreement,
   not a failure of those displayed formulas.
2. The [TPC246 route paragraph](../../papers/tpc-246-weighted-covariance-disk-reassembly/paper/sections/7_route_boundary.tex#L3)
   displays three arrows but calls the first three exact and the final one
   conditional. Its window theorem and
   [package](../../papers/tpc-246-weighted-covariance-disk-reassembly/PROOF_PACKAGE.md#L149)
   support conditional containment at the final step. The original conflicting
   sentence is preserved and explicitly flagged.
3. TPC248's [abstract](../../papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/paper/main.tex#L47)
   needs its declared complex-ball domain. A fixed real physical family does
   not automatically fill that ball. In the one-dimensional complex space,
   a real unit interval gives an interval image, not the whole complex disk.
4. TPC247's [three-coordinate obstruction](../../papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex#L163)
   is general finite matrix geometry, not a demonstrated counterexample from
   the literal arithmetic kernel. Its test kernel is not independently
   identified with the physical source here.
5. TPC249's arbitrary weights define a weighted functional, not automatically
   TPC247's original scalar with weights one. At literal weights one the
   partition identities give g_c = P_c A beta; this is algebra, not an estimate.
6. TPC246's window corollary inherits the actual separation domain, positive
   interval length, harmonic convention, coefficient identification, and common
   transfer hypothesis. Failure of the sufficient strict margin does not
   prove physical cancellation. TPC249's global radius requires rho≥0;
   its displayed squared budget alone does not state that sign restriction.
   Vanishing on a zero-budget domain does not imply a zero probe vector.

The parent spot-checked the TPC246 sentence, TPC248 README/theorem distinction,
and TPC249 radius domain in the originals. No source was silently repaired.

## Manual existing-PDF locators

One-based physical PDF pages from text extraction, not visual certification:

| Paper | Section coverage | Extra locator |
|---|---|---|
| TPC245 | Abstract/1: 1; 2: 1–2; 3: 2; 4: 2–3; 5: 3; 6: 3–4; 7/8: 4 | Appendix 4; 4 pages total. Section 4 appears as “Proof of Theorem 3.1” on page 2 after reference expansion. |
| TPC246 | Abstract/1: 1; 2: 1–2; 3: 2; 4: 3; 5: 3–4; 6/7: 4; 8: 5 | Appendix 5; 5 pages total. |
| TPC247 | Abstract/1: 1; 2/3: 2; 4/5: 3 | References 4; 4 pages total; title metadata blank but textual title present. |
| TPC248 | Abstract/1: 1; 2: 1–2; 3: 2; 4/5: 3; 6: 3–4; 7: 4 | References 4; 4 pages total. |
| TPC249 | Abstract/1: 1; 2/3: 2; 4/5/6: 3 | References 4; 4 pages total. |

Unexpanded reference headings can evade automatic matching. Extraction may
drop overbars or nested absolute-value symbols, especially the distinction
between G and conjugate(G) in TPC248. These are extraction limits, not
established visual printing errors. Original formula TeX is retained.

## Independent audit evidence and exclusions

Task `tpc-maintenance-source-scope-245-249-20260908` reported unchanged
HEAD/handoff, empty write set, matching 47-file hashes, and exit 0 for all
reads, PDF metadata/extractions, and a stdout-only rational/Gaussian arithmetic
check. The latter checked disk-center conjugation, a weighted inverse,
generic tagged versus contracted norms, Gram orientation/minimum preimage,
and independent versus global support radii. It imported no repository
producer and was not a replay of scientific certificates.

Not independently verified: upstream V59 and TPC219/242/243/244 inputs,
literal +2/fixed-h0 identification, historical producer/checker behavior,
certificate PASS claims, visual rendering, full PDF/TeX synchronization, or
complete semantic correctness. Mechanical conversion tests are reported
separately in the [maintenance handoff](../../TPC_HANDOFF.md).

TPC418 remains `NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, arithmetic
advance `NO`, fixed-power credit `0`, full Gate B `OPEN`. These audits
provide no growing-family theorem, physical identification, or new paper number.
