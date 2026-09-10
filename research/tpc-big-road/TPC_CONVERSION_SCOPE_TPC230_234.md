# TPC230–234 conversion and bounded prerequisite audit

Updated 2026-09-08. Original source lock:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. This is maintenance of five
existing papers, without altering their scientific sources or creating a
paper number.

## Reading scope and conversion preflight

Independent read-only task `tpc-maintenance-source-scope-230-234-20260908`
read all 53 source/package text files, including 33 local section inputs,
READMEs, proof packages and bibliographies: 2,214 LF-delimited lines. It
extracted all five preserved PDFs, totaling 18 actual pages. All 58 source/
PDF hashes matched the initial audit and baseline Git blobs; the ordered
raw hash-ledger digest was
`26ac0b49424bb948eac01cdefb54a85cc1e1bdbdc379b12464bdf081d0755ad9`.
Its verdict is `SCOPED_ARCHIVE_REVIEW_ONLY`, not reliable full semantic
verification, historical numerical reproduction, or conversion certification.

The reviewer read `paper/paper.pdf`. The parent confirmed that all five
also have versioned `paper/main.pdf`, selected by the converter, with exactly
the same bytes as the reviewed PDFs. These main.pdf files are not merely
ignored local builds. Both original names/files are preserved.

The five conversion preflights preserve 398 math nodes and 59 display blocks
over 18 pages, with full abstract/body formula/text roundtrips and source
locks passing. All automatic source-heading maps are unique in this batch.
Each conversion record retains source bytes/hashes, ordered child inputs,
original file/line locations, full invoked bibliography material, raw-display
catalogues, and scope limits. TPC230's source-format exception is explicit below.

## TPC230: compact source and confirmed bare-CR anomaly

The preserved [main source](../../papers/tpc-230-matched-resonance-mass-ceiling/paper/main.tex#L8)
puts the document/title/abstract wrapper and abstract input on line 8,
followed by six adjacent body inputs on line 9. The converter supports only
those two narrowly defined root-source command-only forms, besides its
previous standalone inputs. It retains their order and maps each separated
wrapper/input fragment to its original main-file line. Arbitrary adjoining
prose, math, labels, comments, dynamic filenames, conditional wrappers,
compact child-source inputs, and compact glyph-map inputs remain unsupported.

The [mass-ceiling child](../../papers/tpc-230-matched-resonance-mass-ceiling/paper/sections/2_mass_ceiling.tex#L6)
contains 1,119 original bytes, 38 LF bytes, two bare CR bytes and no CRLF
pairs. The CR bytes occur at zero-based offsets 156 and 641, on original
LF-delimited lines 6 and 28. The byte sequence is `{`, CR, `m`, space;
it is not the bytes of the TeX command `\rm`. Existing PDF page 1 extracts
the corresponding subscripts as `q mmatched` and `q munmatched`. This is
a confirmed source-notation anomaly with corresponding extracted text,
not a claim about visually inspected typography.

The matched/unmatched interpretation is supported separately by the
[proof-package decomposition](../../papers/tpc-230-matched-resonance-mass-ceiling/PROOF_PACKAGE.md#L25).
The converter does **not** reconstruct a missing command or silently repair
the stray `m`. It normalizes CR/CRLF only in the in-memory reader input,
with a visible reading-layer notice and a separator-count ledger. All
original file hashes remain hashes of original bytes. Expanded-display
hashes describe normalized reader blocks and are expressly distinguished
from those file-byte hashes.

| Original LF-delimited source location | Universal-newline location | Retained locator policy |
|---|---|---|
| Line 6, matched-mass subscript | Lines 6–7 | Both reader fragments link to original line 6. |
| Line 28, unmatched-row subscript | Lines 29–30 | Both reader fragments link to original line 28. |
| Line 20, normalized implication | Line 21 | Original link remains line 20. |
| Line 32, anti-alignment choice | Line 34 | Original link remains line 32. |

No other reviewed source file in this five-paper batch contains CR. The
helper still rejects CR by default; the converter's explicit normalization
mode must disclose it. Other unsupported splitline separators remain rejected.
Thus the prior wrong-parent-line CR defect is not reintroduced by treating
normalized positions as original ones.

The parent additionally compared Pandoc's direct reading of TPC230's original
input tree with the explicitly expanded reader input: both contained 49
math nodes, identical formula sequences and normalized text, and no reader
warnings. The expansion contained eight source files, seven input edges,
and 148 correctly sized reader-line mappings. This checks reading behavior,
not source correctness or a different TeX engine's rendered semantics.

## Per-paper prerequisite and formula scope

| Paper | Original source anchors | Bounded qualification |
|---|---|---|
| TPC230 | [matching theorem](../../papers/tpc-230-matched-resonance-mass-ceiling/paper/sections/2_mass_ceiling.tex#L1); [density toll](../../papers/tpc-230-matched-resonance-mass-ceiling/paper/sections/3_density_toll.tex#L3); [literal normalization](../../papers/tpc-230-matched-resonance-mass-ceiling/paper/sections/4_literal_rows.tex#L3) | The matching-block decomposition gives E_AP≥D−M. Ratios require D>0; density comparison also requires a nonempty row set and positive lower/upper mass bounds. Sharpness permits selecting opposite paired vectors, not arbitrary prescribed unequal masses. The literal comparability bound inherits the dilation-four support model and common atom normalization. The stated edge-density threshold is necessary, not sufficient or payment of a strict endpoint. |
| TPC231 | [local arithmetic](../../papers/tpc-231-finite-resonance-sieve-obstruction/paper/sections/2_local_arithmetic.tex#L3); [sieve](../../papers/tpc-231-finite-resonance-sieve-obstruction/paper/sections/3_selberg_bound.tex#L13); [fixed family](../../papers/tpc-231-finite-resonance-sieve-obstruction/paper/sections/4_finite_families.tex#L5) | Integral Q, strict prime shell, and primitivity underlie the local-root law; the primitive edge set is empty in the excluded branch. The source uses a classical sieve bound and PNT normalization, not a prime-pair lower bound. The generalized coefficient family is fixed finite. Energy transfer needs the stated collision representation and Q-independent comparison constants. |
| TPC232 | [assumptions/count convention](../../papers/tpc-232-subcritical-growing-resonance-depth/PROOF_PACKAGE.md#L5); [geometry](../../papers/tpc-232-subcritical-growing-resonance-depth/paper/sections/2_collision_geometry.tex#L3); [uniform sieve](../../papers/tpc-232-subcritical-growing-resonance-depth/paper/sections/3_uniform_sieve.tex#L29); [energy](../../papers/tpc-232-subcritical-growing-resonance-depth/paper/sections/4_depth_threshold.tex#L29) | Integral Q,L, fixed positive A, 1≤L≤(log Q)^A, and primitive literal cutoffs are required. L<Q/4 is eventually automatic there. Channel occurrences are counted modulo the two global-sign coordinates, not twice that count or the incident-row count. The subcritical sparsity result still needs fixed positive mass comparability for energy transfer; critical sufficiency and physical-clock attachment remain absent. |
| TPC233 | [raw mass/domain](../../papers/tpc-233-critical-depth-row-mass-obstruction/paper/sections/2_raw_mass.tex#L3); [clock/endpoint input](../../papers/tpc-233-critical-depth-row-mass-obstruction/paper/sections/3_critical_clock.tex#L3); [constructed separation](../../papers/tpc-233-critical-depth-row-mass-obstruction/paper/sections/3_critical_clock.tex#L46) | Integral Q≥8, 3≤L<Q/4 and a nonempty prime shell are needed. Raw mass is common-amplitude support count, not physical divisor weighting. The obstruction is a constructed sequence with a lower mass-ratio bound, using an explicit PNT remainder for shrinking relative windows. It does not establish divergence for every clock or invalidate every source-valid normalization. |
| TPC234 | [normalized-row theorem](../../papers/tpc-234-normalized-collision-bessel-stability/paper/sections/2_bessel_theorem.tex#L3); [literal/abstract witness](../../papers/tpc-234-normalized-collision-bessel-stability/paper/sections/3_literal_block.tex#L17); [source boundary](../../papers/tpc-234-normalized-collision-bessel-stability/paper/sections/4_certificate.tex#L20) | Nonzero unit-normalized rows share one coordinate Hilbert space, with support multiplicity at most two. The conclusion is an upper Bessel bound, not a positive lower frame, invertibility, or bounded condition number. The constant-two sharpness example is abstract; the literal finite block has the stated different ratios. Physical rescaling is not authorized by this geometry. |

## Other preserved source qualifications

- TPC231's singular-series display follows its primitive domain, whereas
  the theorem states uniformity over Q≥8 and separately handles the empty
  nonprimitive branch. Do not extend the local-root derivation into that
  branch. The [manual equation tag](../../papers/tpc-231-finite-resonance-sieve-obstruction/paper/sections/3_selberg_bound.tex#L17)
  prints (7) on PDF page 2 before an automatic (6) on page 3. Numbering is
  preserved, not reconstructed by the reading layer.
- TPC232's [solubility/coprimality wording](../../papers/tpc-232-subcritical-growing-resonance-depth/paper/sections/3_uniform_sieve.tex#L3)
  inherits primitive collision coefficients. An unrestricted soluble integer
  equation does not imply coprimality. Enlarging a later positive weight sum
  does not extend the exceptional-root law to nonprimitive pairs.
- TPC233's [“best structure-only” wording](../../papers/tpc-233-critical-depth-row-mass-obstruction/paper/sections/2_raw_mass.tex#L37)
  does not independently prove optimality. A growing upper envelope alone
  cannot prove growing actual mass ratio; its later constructed lower bound
  is the source of that obstruction.
- TPC234's [conditioning-repair wording](../../papers/tpc-234-normalized-collision-bessel-stability/paper/sections/5_conclusion.tex#L3)
  must retain the upper-bound limitation. The duplicate-row sharpness example
  itself permits a zero mode.

These are bounded deductions from the displayed sources and direct byte/text
observations, not new numerical reproductions. The source reviewer ran no
separate algebra program or scientific checker.

## Existing-PDF locators

One-based physical pages from complete text extraction, cross-checked with
PDF metadata. Numbered introduction contribution lists are not section headings.

| Paper | Numbered section starts in source order | Supplements |
|---|---|---|
| TPC230, 3 pages | 1, 1, 2, 2, 2, 3 | Theorem and malformed subscripts 1; proof continues 2; References 3. |
| TPC231, 4 pages | 1, 2, 2, 3, 4, 4 | Sieve proof continues 3; fixed-family theorem/energy transfer 3; Table 1/References 4. |
| TPC232, 4 pages | 1, 2, 2, 3, 4, 4 | Introduction contributions on 1–2; sieve continues 3; energy corollary proof 4; References 4. |
| TPC233, 4 pages | 1, 2, 2, 3, 4 | Endpoint lemma 2; separation theorem 3; digest/route prose continues 4; References 4. |
| TPC234, 3 pages | 1, 2, 2, 3, 3 | Literal support table 2; displayed ratios 3, not earlier prose mentions; References 3. |

Abstracts are on page 1; no appendices or numbered subsections occur. These
locations do not establish visual PDF QA or full TeX/PDF synchronization.

## Evidence limits and scientific stop

### Converter and source-anchor re-audit

Read-only task `tpc-maintenance-compact-cr-provenance-audit-20260908`
independently checked all 148 TPC230 reader-line mappings, seven ordered
input edges, eight source hashes, and the normalized hashes of both
CR-affected displays. The actual raw-byte converter path passed, but the
first audit returned `REQUEST_CHANGES_SCOPED` for two adjacent boundaries:
the default helper reader performed universal-newline conversion too early,
and link validation counted universal-newline reader lines rather than raw
LF-delimited source lines.

The default reader now decodes original bytes, with an explicit callback
contract; the link bounds now count LF bytes plus an unterminated final line.
Mocked binary/text readers exercise both default and explicit normalization
modes, rejecting a spurious source line 3 while accepting actual line 1 in
the CR fixture. No fixture files were written. The independent follow-up
replayed both defects in normal/optimized modes, passed six bounded replay
tests in each, and returned `ACCEPT_SCOPED` with no remaining reported defect.

The complete named maintenance suites pass 74 tests in normal and `-O`
modes, both for the parent and independent reviewer. The first audit's
negative probes exposed the defects; they were not passing implementation
tests. Its first actual-source probe also had one mistaken audit expectation
(one CR-affected display instead of two), corrected before the six actual-
source checks passed. No product/source file was changed to fix that expectation.

The reviewed final maintenance hashes include:

| File | SHA-256 |
|---|---|
| source_markdown_includes.py | `e8a18189f5b2d54fb074cd47053abf9d049cb631323ef3ecd4f96521a96f5c8e` |
| maintain_source_markdown.py | `a99738ce52a5f5b384c801e09b77730da7cb17de11baad2a09150616dad1259d` |
| check_source_markdown_batch.py | `5a473ff312d5c620c43a05421239e875417cc12d5bc3195c08357c920b3e3e05` |
| test_source_markdown_includes.py | `36dda50cee492801a5edb64f4a1776cd36edc0bbffe34266e7b8c1bb7468ab9e` |
| test_source_markdown_links.py | `84ab87713820934bfa488bd25a14ca3b4b5a2a49caea5fafe46061e062c3c8e9` |

The parent separately replayed all 179 previously completed TPC240–418
Markdown/provenance pairs: every pair remained byte-identical, with 10,869
math nodes and all source locks/text roundtrips retained. The reviewer did
not duplicate that replay, the direct-reader comparison, or the PDF-alias
check. Acceptance is not arbitrary-TeX safety, semantic proof verification,
source/PDF synchronization, or a paper-release gate.

After both new batches were generated and indexed, the integrated TPC230–239
check passed all ten source locks/formula/text roundtrips and 7,145 local-link
checks across 28 documents. No local-path, raw-LF-line-bound, or same-document
anchor issue was reported. Cross-document non-line fragments remain outside
the checker. No scientific or full semantic verdict follows from this receipt.

### Original-source review limits

The reviewer reported no writes, unchanged HEAD/handoff, and all 58 original
hashes matching baseline Git. Its complete source/PDF reads and byte/hash
checks exited 0. No network, scientific code, certificate mutation suite,
compilation, rendering, or further delegation was used.

Unverified upstream inputs include the original TPC226 model, TPC229
matching theorem, sieve formulations/uniformity, PNT/totient estimates,
TPC233's zero-free-region remainder, and all historical certificate/digest/
primality/scan claims. Bibliographic metadata was retained, not externally
authenticated. Reliable full semantic verification remains unearned.

TPC418 arithmetic advance stays `NO`, fixed-power credit `0`, full Gate B
`OPEN`, and round2 `NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`. No physical
h0/source identification, growing theorem, or new paper number is supplied.
