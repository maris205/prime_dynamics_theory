# TPC235–239 conversion and bounded prerequisite audit

Updated 2026-09-08. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Five existing manuscripts only;
no new paper, theorem, scientific source repair, or publication release.

## Reading scope and mechanical evidence

Independent read-only task `tpc-maintenance-source-scope-235-239-20260908`
read all 63 manuscript/package text files (3,478 lines), including complete
local TeX inputs, READMEs, proof packages, and bibliographies. It extracted
the five preserved PDFs (31 pages). All 68 original text/PDF hashes matched
both the initial audit and the declared source commit. Its sorted hash-ledger
digest was `a2bd57f25090d4685d45f5e05cd6298cecf3f58ef3c0bde24cb974d60a9caf95`.
The source reviewer read versioned `paper/paper.pdf` files. The parent
resolved the conversion names separately: TPC235–236 also have versioned
`paper/main.pdf` files, which the converter selects and which are byte-identical
to the reviewed PDFs. TPC237–239 use versioned `paper/paper.pdf`; ignored
alternate builds are excluded. The initial blanket description of all
alternate main.pdf files as ignored is superseded by these exact checks.

The verdict is `SCOPED_ARCHIVE_REVIEW_ONLY`, not whole-paper semantic
verification or reproduction of source certificate claims. The conversion
preflight preserves 653 math nodes and 123 raw display blocks over 31 PDF
pages, with all five source locks and full abstract/body formula/text
roundtrips passing. Per-paper conversion records retain original child-file
lines, ordered inputs, exact file hashes, complete invoked bibliography
material, and automatic page candidates. Source correctness is not inferred
from those checks.

## Per-paper premise and formula boundaries

| Paper | Original source anchors | Bounded qualification |
|---|---|---|
| TPC235 | [physical crosswalk](../../papers/tpc-235-v59-physical-depth-crosswalk/paper/sections/2_physical_crosswalk.tex#L7); [single-clock comparison](../../papers/tpc-235-v59-physical-depth-crosswalk/paper/sections/3_single_clock.tex#L7); [polarization](../../papers/tpc-235-v59-physical-depth-crosswalk/paper/sections/4_polarization.tex#L3) | Positive scales, integral moduli, and an existing modular inverse are needed. The depth substitution preserves scale arguments and modulus; its compatibility iff is not an iff for accidental equality of sampled values or empty rows. Polarization requires the same linear transform for all four labels and an explicit inner-product convention. Independent unit normalization requires four nonzero outputs. The denominator-grid census does not count nonzero source weights. |
| TPC236 | [gcd-fiber bound](../../papers/tpc-236-physical-multiwrap-collision-envelope/paper/sections/2_gcd_fiber.tex#L7); [weighted Bessel/direct sum](../../papers/tpc-236-physical-multiwrap-collision-envelope/paper/sections/3_bessel.tex#L3); [exponent ledger](../../papers/tpc-236-physical-multiwrap-collision-envelope/paper/sections/5_v59_ledger.tex#L18) | The envelope inherits 4Q<H, positive integer h≤Q, and shell primes Q<q≤2Q. The zero residue is empty. The Bessel bound is in residue coordinates and the pre-reassembly direct sum is orthogonal; common bounded maps pay their squared norms. An upper collision toll is not a proved asymptotic lower bound or sharpness result. |
| TPC237 | [frozen source](../../papers/tpc-237-collision-compressed-finite-window-reassembly/paper/sections/2_source.tex#L3); [compressed energy](../../papers/tpc-237-collision-compressed-finite-window-reassembly/paper/sections/3_collision_compression.tex#L34); [window](../../papers/tpc-237-collision-compressed-finite-window-reassembly/paper/sections/4_finite_window.tex#L3) | The source explicitly fixes squarefree D_x, signed C_h, outer q weight one, primitive coordinates, fixed J, and profile norm bound M. Large x provides U<Q, 4Q<H, and an empty h=1 row. The absolute harmonic majorant gives an unsigned upper bound. The exponent statement must retain JM² or assume it contributes no extra power. Upstream physical attachment is inherited, not established by notation. |
| TPC238 | [domain/lower frame](../../papers/tpc-238-finite-window-lower-frame-obstruction/paper/sections/2_setup.tex#L28); [Gram proof](../../papers/tpc-238-finite-window-lower-frame-obstruction/paper/sections/3_lower_frame.tex#L80); [obstruction scope](../../papers/tpc-238-finite-window-lower-frame-obstruction/paper/sections/4_route_consequence.tex#L4) | N≥1, U≥1, distinct finite primitive frequencies, and positive separation are required. Empty/singleton cases are treated in the package. Gram direction is beta−alpha. The supplied normalized lower constant is not an optimal-frame asymptotic. The obstruction is relative to already-collapsed coefficient energy; a ratio formulation needs a nonzero coefficient vector. |
| TPC239 | [analytic inputs](../../papers/tpc-239-brun-titchmarsh-primitive-bucket-envelope/paper/sections/2_source_setup.tex#L77); [AP compiler](../../papers/tpc-239-brun-titchmarsh-primitive-bucket-envelope/paper/sections/3_primitive_ap_compiler.tex#L26); [composition](../../papers/tpc-239-brun-titchmarsh-primitive-bucket-envelope/paper/sections/4_v59_composition.tex#L20) | The factor 16 is the multiplier upper count times the inherited Brun–Titchmarsh bound, under 4Q<H and 2≤h≤U<Q with unit residues; h=1 is separate. Uniform logarithmic improvement also needs the inherited maximal-order totient bound and fixed power gap Q/U. The trace estimate remains unsigned with the same fixed-power exponent; comparison of upper envelopes is not a ratio of actual energies. |

## Preserved discrepancies and source qualifications

### TPC235: the printed finite fixture is not admissible as stated

The [certificate section](../../papers/tpc-235-v59-physical-depth-crosswalk/paper/sections/5_certificate.tex#L3),
also printed across actual PDF pages 3–4, sets (H,Q,h,q)=(21,5,14,10)
and reports physical/model cutoffs five/zero. The bounded exact check gives:

- gcd(10,14)=2, so the modular inverse used by the row does not exist.
- q=10 is not prime.
- The physical cutoff floor(hq/H) is 6.
- Matching the modeled modulus gives L=7/10 and modeled cutoff 1.

The manuscript's displayed depth value 10/3 is a valid scale identity but
does not fix these domain/cutoff discrepancies. Original text, PDF and
historical certificate digest remain untouched. No scientific certificate
was inspected or rerun; the arithmetic above is only a direct check of the
printed tuple. The parent spot-checked the tuple and claimed cutoffs.

TPC235 calls its inner product “the project's convention” without defining
the slot convention locally. Its displayed positive-i^j polarization, with
the slots as printed, requires linearity in the first slot. It must not be
combined silently with a conjugate-linear-first convention. The common-map
and nonzero-output requirements remain regardless of that notation choice.

### Remaining source boundaries

- TPC235's [coefficient definition](../../papers/tpc-235-v59-physical-depth-crosswalk/paper/sections/2_physical_crosswalk.tex#L14)
  and TPC236's [introduction](../../papers/tpc-236-physical-multiwrap-collision-envelope/paper/sections/1_introduction.tex#L10)
  leave D_x locally undefined. TPC237 defines its own squarefree source set;
  that does not retroactively establish the earlier physical attachment.
- TPC235's all-residue sum and TPC237's primitive kernel cannot be identified
  merely because their symbols agree. The TPC218 identification is an
  unverified upstream source assertion in this bounded review.
- TPC236's [h=80 triple-collision fixture](../../papers/tpc-236-physical-multiwrap-collision-envelope/paper/sections/4_triple_collision.tex#L12)
  uses floor-model uniform amplitudes. TPC237's
  [h=82 fixture](../../papers/tpc-237-collision-compressed-finite-window-reassembly/paper/sections/6_certificate.tex#L12)
  is squarefree/source-active but replaces log d by one. Neither establishes
  growing sharpness of literal divisor-weighted mass.
- TPC239 [allows cross-multiplier overcount](../../papers/tpc-239-brun-titchmarsh-primitive-bucket-envelope/paper/sections/3_primitive_ap_compiler.tex#L66).
  In its stated domain, 2M_h≤4hQ/H<h makes distinct allowed multipliers
  distinct modulo h; multiplication by unit a inverse preserves this.
  Thus one bucket's multiplier classes do not duplicate a prime. Deleting
  the q-dependent cutoff can still enlarge the census. This qualification
  does not invalidate the upper bound and is not an instruction to edit it.
- TPC239's [source note](../../papers/tpc-239-brun-titchmarsh-primitive-bucket-envelope/paper/sections/2_source_setup.tex#L89)
  acknowledges the missing book-page scan for its analytic citation. That
  limitation and all historical certificate/font/visual-QA claims remain
  source-reported, not newly verified here.

## Existing-PDF manual locators

One-based actual PDF pages from full text extraction; numbered headings,
not prose mentions, determine the locations. Abstracts are on page 1.

| Paper | Numbered section starts in order | Supplements |
|---|---|---|
| TPC235, 4 pages | 1, 2, 2, 3, 3, 4 | Compatibility theorem 3; fixture 3–4; References 4. |
| TPC236, 5 pages | 1, 2, 2, 3, 4, 4, 4 | Bessel corollary 3; final section continues 5; References 5. |
| TPC237, 6 pages | 1, 2, 3, 3, 4, 5, 5 | Theorem 4.2 on 4; declarations/References 6. |
| TPC238, 7 pages | 1, 2, 3, 5, 5, 6 | Subsections 3.1/3.2 on 3; Lemma 3.4 and 3.3 on 4; 5.1/5.2 and Table 1 on 6; appendix/References 7. |
| TPC239, 9 pages | 1, 2, 4, 5, 6, 7, 8 | Subsections 2.1/2.2 on 2/3; 4.1/4.2/4.3 on 5/5/6; Theorem 4.2 starts 5, proof 6; appendix A/A.1 on 8, A.2/A.3 on 9; References 9. |

The automatic TPC238 map has one unresolved heading; TPC239 has four.
These manual supplements do not turn them into unique automatic matches.
Overbars/nested norm delimiters can be lost in extraction, especially
TPC238 page 4. TeX controls formula transcription; no visual rendering
certification or printing-defect finding follows from extraction alone.

## Audit evidence, exclusions, and stop

The read-only reviewer reported unchanged HEAD/handoff, no file changes,
and exit 0 for its complete reads, source/commit hashes, PDF metadata/text
extraction, and one standard-library exact fixture calculation. It did not
read numerical artifacts, run scientific modules, compile, render, access
the network, or delegate further work. The parent did not repeat completed
policy or PrimeGaps186 reviews.

Unverified: V59/TPC218 attachment, TPC217/large-sieve provenance, upstream
TPC226–234 claims, analytic references, all historical computational/release
claims, full source/PDF synchronization, and reliable full semantic review.
The denominator h does not supply physical fixed-h0 identification.

TPC418 retains arithmetic advance `NO`, fixed-power credit `0`, full Gate B
`OPEN`, and `NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`. No source-location
or mechanical-conversion check reopens that route or creates a new number.
