# TPC185–189 conversion and bounded prerequisite audit

Updated 2026-09-08. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Five existing manuscripts only;
no new paper, original-source repair, theorem, or publication release.

## Mechanical evidence and limits

The conversion preflight retains 25 math nodes and zero raw displayed-
equation blocks over 10 preserved PDF pages. All five source locks and full
abstract/body formula and normalized-text roundtrips pass. Original TeX,
invoked bibliography and PDF hashes and original-line/PDF-heading matches
are retained in the per-paper conversion records. All automatic source-
section headings have unique PDF text matches. This is location evidence,
not source/PDF synchronization certification.

All five originals use root main.tex, references.bib and exact directory-
basename PDFs. Reading layers remain at paper/main.md with relative links
back to those originals; nothing is copied, moved or silently corrected.
All five lack a separate PROOF_PACKAGE.md. Bibliographies are retained as
full original BibTeX, not externally verified or reconstructed references.

The source-input helper, batch checker and inventory generator are unchanged.
The converter receives the [narrow TPC181 multi-target-reference repair](TPC_CONVERSION_SCOPE_TPC180_184.md#multi-target-reference-repair-and-regression-scope).
All 126 named maintenance tests pass in normal and optimized modes,
including 15 new reference tests. Full semantic validation and
reliable-full-md status remain unearned.

## Independent source-reading scope

Read-only task `tpc-maintenance-source-scope-185-189-20260908` completed its
bounded source and page-location review, with supported claim level
`SCOPED_ARCHIVE_REVIEW_ONLY`, no archive-level fatal mismatch and no writes.
It fully read 15 original text files: five READMEs, five complete root
main.tex files and five invoked references.bib files, totaling 460 raw LF
characters. Five versioned exact-basename PDFs were fully extracted to
stdout and read across all 10 physical pages. There are no invoked local
TeX children, separate proof/derivation packages or additional relevant
source/theorem/route/claim notes in these five directories.

All 20 text/PDF originals matched baseline Git blobs and their working-file
Git object IDs matched the corresponding tree entries. All 20 SHA-256
values were unchanged at completion. The canonical 20-original ledger
SHA-256 is `304ce807e3ad722d95f6733725e3d8ecedd28e943dbc3e418c775b2c2d9a16ec`.
Serialization is repository-relative path, TAB, lowercase SHA-256 and LF,
sorted with LC_ALL=C, with the final LF included. Source, bibliography and
PDF hashes are also retained in each conversion record.

Initial/closing HEAD and origin/main matched the declared commit. The
initial/closing handoff hash was
`32a1eae462e9914a4b9ad3416390be56dd2019bf7ab83890e1eb21102f5c09a9`.
The same nine dirty tracked paths and empty index were preserved. The
reviewer's closing snapshot saw 523 untracked paths, up from 501; the
22 added reading-layer/provenance/scope files were primary-owned. That
snapshot preceded the primary's additional reference-test file and does
not claim to rehash the entire pre-existing untracked collection.

All 54 reported shell invocations returned zero. The complete command
families were source/policy reads, path inventories, status/index/HEAD
checks, SHA-256 and Git-blob comparisons, pdfinfo and full pdftotext.
The 20 Git-blob pipelines each reported component statuses 0/0; the
canonical ledger pipeline reported 0/0/0/0. No science producer, JSON
artifact, external theorem, upstream paper, TeX build or PDF render was
read as a substitute proof receipt or executed.

## Original text counts and manual PDF locations

| Existing paper and source | README raw LF | main.tex raw LF | BibTeX raw LF | PDF pages |
|---|---:|---:|---:|---:|
| [TPC185](../../papers/tpc-185-prefix-block-equivalence/main.tex) | 32 | 55 | 5 | 2 |
| [TPC186](../../papers/tpc-186-dyadic-shadow-local-oscillation/main.tex) | 32 | 55 | 5 | 2 |
| [TPC187](../../papers/tpc-187-size-only-local-oscillation-barrier/main.tex) | 32 | 55 | 5 | 2 |
| [TPC188](../../papers/tpc-188-bad-endpoint-route-decision/main.tex) | 32 | 55 | 5 | 2 |
| [TPC189](../../papers/tpc-189-direct-twist-literal-target-contract/main.tex) | 32 | 55 | 5 | 2 |

All five sources share these original line positions. The reviewer checked
each separately using complete extraction and physical page boundaries:

| Source location, in each linked main.tex | PDF location, in each preserved manuscript |
|---|---|
| Title/author/date L11–15; abstract L16–20 | Page 1 |
| Frozen target, L22–26 | Page 1 |
| Exact result, L28–37: theorem, proof and missing theorem | Page 1 |
| Scoped stop and claim firewall, L39–47 | Page 1 |
| Reproducibility, L49–52 | Page 1 |
| Bibliography invocation L53–54; references.bib L1–5 | Page 2, References and sole entry |

There are no source subsections, appendices or section continuations.
Every page 2 contains only the References heading and its TPC182 entry.
All five bibliographies have the same bytes. README reproduction commands
at L23–32 are not reproduced literally in the PDFs; PDF section 4 gives
only the higher-level artifact description. These manual locations are
extraction-based, not rendered-page inspection or synchronization proof.

## Bounded prerequisite and source-wording qualifications

All five main.tex files L23–26 require the same six axes: actual fixed-h0
packet, named fixed atom, deterministic every prefix and every scale,
fixed-X power and actual active support. They state h0=2 as a source-backed
data fact, but its upstream backing was not independently verified here.
None supplies the complete literal coefficient/sign/mask/outer-label
formula, actual support construction, numerical atom, physical prefix
enumeration, full X/N/q ranges, uniform constants or full physical-loss
ledger. Lines 42–47 explicitly retain zero endpoint charge and the unpaid
strict 1/400 budget. The JSON/mutation claims at L50–52 were not rerun.

- **TPC185, finite prefix/block interface:** main.tex L30 states P <= B <=
  2P for general complex sequences; L33 retains signed differences S_s-S_r
  and S_0=0. The maximum index limits and inclusion of r=0 are not explicit
  in the theorem sentence, with the prefix-as-block convention appearing
  in the proof. No physical ordering or scale range is provided. The
  missing named-atom consecutive-block power-saving theorem at L37 stays
  missing; this REDUCTION_L1 identity is not a physical cumulative saving.
- **TPC186, boundary plus local increments:** main.tex L30 and L33 retain
  the separate boundary term and the identical endpoint family. The proof's
  statement that two maxima are equivalent up to factor two does not name
  both maxima or explicitly delimit the boundary contribution. Boundary
  control must not be silently dropped. The TPC159 input at L17 is neither
  stated locally nor included in the sole-entry bibliography. Concrete
  dyadic scales, normalization and uniformity remain unspecified.
- **TPC187, size-only obstruction:** main.tex L30/L33 use a_j=1 as a
  synthetic extremizer for length L, not physical coefficients. The q/T
  normalization mentioned in the abstract is not defined in the theorem,
  and q/T/X ranges and the saving exponent's positivity/growth conditions
  are not locally laid out. Text-mode exponent notation is preserved as
  written. Only SIZE_ONLY_LOCAL_OSCILLATION_METHOD is stopped at L40;
  arithmetic cancellation remains the missing input at L37.
- **TPC188, historical route decision:** main.tex L30/L33 rely on the
  declared TPC185–187 methods and assertions about TPC169/170 and TPC181,
  without locally providing every imported theorem or artifact inventory.
  The latter upstream premises were not expanded; bibliography contains
  only TPC182. The abstract's inherited stopped methods and L40's no-new-
  stop sentence do not close the pointwise theorem. Its historical switch
  to another frontier is not current GO authorization.
- **TPC189, direct-twist contract:** main.tex L17 names a q/N-normalized
  determinant-two twist but does not print the coefficient/mask/support
  formula or parameter ranges. L30's point evaluation on L2([0,1]) needs
  a distinction between equivalence classes and a pointwise-defined
  polynomial/representative domain. L33's Dirichlet polynomial convention,
  frequencies and phase sign are not given, nor is the transfer from zero
  to the unspecified prescribed atom. TPC167's Parseval input is invoked,
  not locally supplied or bibliographically located. No singleton decay
  theorem is certified by this CONTRACT_L0_L1 note.

All qualifications above refer to PDF page 1 and the source lines stated;
no original wording is repaired. Reliable full-content/semantic review,
source/PDF reconciliation and upstream prerequisite verification remain
separate future tasks. TPC418 STOP, arithmetic advance NO, fixed-power
credit 0 and full Gate B OPEN are unchanged.
