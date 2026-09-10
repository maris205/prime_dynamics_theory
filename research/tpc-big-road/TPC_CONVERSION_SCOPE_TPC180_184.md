# TPC180–184 conversion and bounded prerequisite audit

Updated 2026-09-08. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Five existing manuscripts only;
no new paper, original-source repair, theorem, or publication release.

## Mechanical evidence and limits

The conversion preflight retains 172 math nodes and 43 raw displayed-
equation blocks over 19 preserved PDF pages. All five source locks and full
abstract/body formula and normalized-text roundtrips pass. Original TeX,
invoked bibliography and PDF hashes, display catalogues and original-line/
PDF-heading matches are retained in the per-paper conversion records.
All automatic source-section headings have unique PDF text matches.
This is location evidence, not source/PDF synchronization certification.

All five originals use root main.tex, references.bib and exact directory-
basename PDFs. Reading layers remain at paper/main.md with relative links
back to those originals; nothing is copied, moved or silently corrected.
All five lack a separate PROOF_PACKAGE.md. Bibliographies are retained as
full original BibTeX, not externally verified or reconstructed references.

The source-input helper, batch checker and inventory generator are unchanged.
The converter receives the narrow multi-target-reference repair below.
Full semantic validation and reliable-full-md status remain unearned.

## Multi-target-reference repair and regression scope

The first new-batch link check failed on TPC181's original main.tex line
371: Pandoc interpreted the three-label cref as one combined anchor that
does not exist. The source command is unchanged. The reading layer now
retains the original visible label list and order, with independent links
to original label lines 208, 246 and 331. No theorem numbering is guessed
and no target is dropped.

The repair handles only Pandoc's exact unresolved-label reference shape,
with all target labels present exactly once in the source. Unsupported
shapes and missing or duplicate source labels fail closed. A real literal
comma-containing label has priority; ordinary links and images are not
split. Original included-file/line maps are preserved when applicable.

All 126 named maintenance tests pass in normal and optimized modes,
including 15 new reference tests. These test order, repeated references,
source locations, failure cases, idempotence, visible-text/math preservation
and the actual TPC181 conversion. Independent QA initially found that a
malformed in-memory Link with an extra payload field could lose that field
during replacement. The parent added exact outer/target payload lengths
and node-key checks, plus rejection-without-mutation tests for embedded
extra math. This was an adverse AST fixture, not observed content loss in
the actual manuscript. The independent finite follow-up returned
`ACCEPT_SCOPED`: 26 selected unit tests and 10 additional in-memory case
groups pass in each of normal and optimized modes. Tests and case groups
are separate counts. The original failing case and additional target-list/
top-level math payloads now raise ValueError without object or math loss.
Real TPC181 retains 61 math nodes and all three original label targets;
its 25 Markdown and 7 conversion-record links pass. These checks do not
certify source mathematics or rendered PDFs.

QA verified the bounded code changes against its prior hashes in memory;
the final converter hash is
`a3af367bc6c87a22c2b8968e33ceeba3ba5992f768caf012bee67b1b8ccfc687`,
and the reference-test hash is
`4bbd2d17f38933cb7989417ac457c9448cff9275b8d3d4a349fb626220e67cae`.
All four assigned TPC181 originals matched Git bytes at follow-up start
and end. QA retained the declared handoff hash, nine dirty tracked paths,
empty index and 524 untracked paths, with no writes. Its acceptance is
limited to the specified converter repair, not the parent's full-suite,
prior-pair replay or whole-untracked preservation evidence.

After the final shape guard, all 229 prior TPC190–418 Markdown/provenance
pairs were replayed in memory and remained byte-identical, with 14,646
math nodes and passing source-lock/text roundtrips. No prior artifact was
rewritten. The ten new pairs also pass their source/formula/text checks;
no math, original-proof or reliable semantic-review credit follows.

## Independent source-reading scope

Read-only task `tpc-maintenance-source-scope-180-184-20260908` returned
`ARCHIVAL_SOURCE_REVIEW_COMPLETE_WITH_RECORDED_LIMITATIONS`, supported at
`SCOPED_ARCHIVE_REVIEW_ONLY`, with no archive-level fatal mismatch and no
writes. It fully read five READMEs, five complete root main.tex files and
five invoked references.bib files: 15 original texts with 1,817 raw LF
characters. Five preserved exact-basename PDFs were fully extracted to
stdout and read across all 19 physical pages. No invoked local TeX child,
separate proof/derivation package or relevant source/theorem/route/claim
note exists in these five directory inventories. There are no source
subsections or appendices.

All 20 text/PDF originals matched the declared Git blobs and were unchanged
at completion. The canonical 20-original ledger SHA-256 is
`4b5885bf86ec09d8f51d9c7d3f5cf4d4f929014aba0759ef324eedbb43b7c61c`.
Serialization is repository-relative path, TAB, lowercase SHA-256 and LF,
sorted with LC_ALL=C, including the final LF. Source, bibliography and
PDF hashes are also in each conversion record. HEAD/origin/main matched
the declared commit; the observed/closing handoff hash was
`32a1eae462e9914a4b9ad3416390be56dd2019bf7ab83890e1eb21102f5c09a9`.
The original-path diff and index were empty. The same nine dirty tracked
paths were retained. The reviewer's detailed status snapshots covered
503–523 untracked files: the first included the primary's two scope notes,
the second the 20 new reading/provenance files. No path disappeared. These
snapshots precede the additional reference-test file and do not rehash the
primary's entire original untracked collection.

The reviewer recorded 74 command invocations: 71 individually retained
zero statuses and three initial statuses lost to aggregate-output
truncation, each repeated with observed zero status. No nonzero status was
observed; unrecorded pipeline-component statuses are not inferred. Commands
covered complete original/policy reads, inventories, status/index/HEAD,
SHA-256/Git-blob/tree checks, pdfinfo and full pdftotext. No science script,
schema or JSON contents, upstream paper or external theorem was used as a
substitute proof receipt. There was no reproduction, build or render.

## Original text counts and manual PDF locations

| Existing paper and original source | README raw LF | main.tex raw LF | BibTeX raw LF | PDF pages |
|---|---:|---:|---:|---:|
| [TPC180](../../papers/tpc-180-production-phase-registry-census/main.tex) | 79 | 358 | 69 | 5 |
| [TPC181](../../papers/tpc-181-metric-fixed-atom-selector-gate/main.tex) | 91 | 405 | 48 | 5 |
| [TPC182](../../papers/tpc-182-mvp8-source-phase-route-decision/main.tex) | 86 | 391 | 106 | 5 |
| [TPC183](../../papers/tpc-183-pointwise-parent-interface-comparison/main.tex) | 32 | 55 | 5 | 2 |
| [TPC184](../../papers/tpc-184-bad-endpoint-literal-target-contract/main.tex) | 32 | 55 | 5 | 2 |

The manual maps below come from complete extraction and page boundaries,
not the automatic heading table. Line numbers refer to each linked original
main.tex. Printed page numbers match extraction order; no rendered-page
inspection or source/PDF synchronization proof is inferred.

| Paper | Complete source-section and continuation map |
|---|---|
| TPC180 | Title L38, abstract L50 and claim boundary L73: p1. §1 The exact question L82: pp1–2, including Definition 1.1 continuation. §2 Fixed h0=2 is present and is not a phase L126: p2. §3 Packet coordinates required by TPC-170 L161: pp2–3; equations 4–7 p2, interface/representative rule p3. §4 Frozen source census L212: pp3–4; table/theorem/proof p3, scope remark continues p4. §§5–7 Decision and typed progress L293, Reproducible artifacts and next gate L323, Conclusion L345: p4. Bibliography L356: p5, entries 1–10. |
| TPC181 | Title L40, abstract L52 and claim boundary L77: p1. §1 The imported metric theorem L87: pp1–2; equations 1–4 p1 and 5–8 p2. §2 The two independent missing inputs L160: p2, including Definition 2.1. §3 The singleton obstruction L205 and §4 Selector verdict and sufficient bridge hypotheses L274: p3. §5 Return to the two pointwise routes L304 and §6 Level ledger and reproducible audit L365: p4. §7 Conclusion L390 and bibliography L403: p5, entries 1–7. |
| TPC182 | Title L39, abstract L51 and §1 Dynamic imported state L83: p1. §2 The scoped structural stop L114 and §3 Vacuity is not a certificate L165: p2. §4 The production phase registry L205 and §5 The selector obstruction L236: p3. §6 Typed routes and endpoint ledger L274: pp3–4, table p3 and ledger/axis comparison p4. §7 MVP8 decision L341 and §8 Claim firewall L375: p4. Bibliography L389: pp4–5, entries 1–3 p4 and 4–13 p5. |
| TPC183 | Title L11, abstract L16, §1 Frozen target L22, §2 Exact result L28 and §3 Scoped stop and claim firewall L39: p1. §4 Reproducibility L49 and bibliography L54: p2, one entry. |
| TPC184 | Title L11, abstract L16 and all §§1–4 at L22/L28/L39/L49: p1. Unlike TPC183, Reproducibility is on p1. Bibliography L54: p2, one entry. |

There are 33 source bibliography entries and 32 printed entries. TPC182's
uncited Durrett2019 entry at references.bib L100–106 is retained in full
BibTeX but is not printed; this is not a missing-PDF-page finding. Original
bibliographic title variants are preserved, not silently normalized.

## Bounded prerequisite and source-wording qualifications

- **TPC180, registry census:** main.tex L163–195 prints su-ad=2, q=as,
  t_d(z)=ad+qz and c(z)=mu(d+sz)mu(u+az), with ordered-prefix summand
  c(z_j)rho(z_j)e(-alpha z_j), j<=k. The negative phase sign and multiplier
  are retained. It is a consumer interface, not an actual production row:
  physical masks, multiplier values, atom, schedule and coordinate rows are
  absent. Positivity/coprimality, detailed ordering/ranges and natural
  normalization are not fully specified locally. The all-solutions
  representative statement at L198–210 (p3) does not locally state the
  needed coprimality premise on a,s. The seven-field frozen-corpus census
  at L256 (pp3–4) is a source assertion, not a census of arbitrary archives
  or a nonexistence theorem. The first missing object stays the named atom
  and phase-value source locator; h0=2 at L126 is data, not a phase value.
- **TPC181, metric/selector separation:** main.tex L87–155 uses normalized
  G=(q/T)max|S| and V=D^2||rho||_infinity^2(q/T+q^2/T^2), with lambda_n>0,
  strict bad-set threshold G>lambda_n and summability of lambda_n^-2
  times the packet V sums. The packet list is prescribed before observing
  exceptional phases. T/q is the displayed packet scale, not established
  physical normalization. The eventual prefix-bound wording at L133 must
  retain normalized G; it is not an additional raw-S estimate. Literal S,
  phase sign, masks, D definition and detailed dyadic/polylogarithmic
  envelope are imported, not restated. The printed power range delta<1/4
  lacks an explicit positive lower bound. Named phase, exact schedule/bad
  sets, a same-atom limsup-avoidance theorem and complete production cover
  remain independent missing bridge inputs (L160–202, p2). Only uncontrolled
  atomic promotion is stopped; metric credit does not become fixed-atom
  credit. The constant-coefficient example at L239 is explicitly not the
  literal Mobius packet. The separate reference repair above changes no
  original-source mathematical statement.
- **TPC182, historical MVP8 decision:** main.tex L114–164 (p2) imports zero
  local edges, zero covered cuts and 2,988 unmatched cuts; these counts are
  not rerun. A two-edge synthetic fixture and empty eligibility cannot
  supply nonempty local totality. Three structural certificates and four
  physical registries remain distinct (L93, L165). Named phase, locator,
  schedule, literal coefficient/masks, actual order/ranges and physical
  normalization are not instantiated. Shell prefixes versus all prefixes
  and eventual prescribed schedules versus all scales stay separate.
  Endpoint Ledger V5 at L311 (p4) records metric delta<1/4, named credit 0
  and required 1/400, not a paid full-loss ledger. The historical verdict
  remains NOT_TESTABLE; first missing is the source-backed local occurrence
  edge family. Bibliography title variants do not establish source identity.
- **TPC183, conditional specialization:** main.tex L28–33 (p1) allows N=T
  only with identical summand, uniform constants/exponent, atom, scale and
  endpoint ranges. Each bad endpoint must lie in the direct-prefix domain.
  That common literal summand, masks/signs, bad-endpoint set, order, ranges
  and named atom are not displayed locally. Equality q/N=q/T does not
  establish the missing physical identification or saving. The reverse
  implication is not established, not declared false. Mutation assertions
  in L49–52 (p2) remain source claims, not new testing receipts.
- **TPC184, cumulative target contract:** main.tex L17 (p1) specifies the
  q/T-normalized cumulative target, without a literal sum, masks/signs,
  cumulative domain/order, ranges, atom value or dyadic-shadow definition.
  No block-to-cumulative substitution follows. At L30 the theorem says
  strictly weaker, whereas L33 records a required-axis mismatch; this
  archival pass supplies neither a strictness argument nor the imported
  TPC171/159/169 hypotheses. Only TPC182 appears in the bibliography. The
  named-pointwise-axis wording does not identify the missing production
  atom. The named-atom bound inside the TPC159 shadow remains missing.

All originals remain unchanged. The last two manuscripts state h0=2 as
data and retain zero endpoint charge and the unpaid strict 1/400 budget.
Reliable full semantic review, physical identification, original proof
correctness and rendered-PDF QA are not certified. TPC418 STOP, arithmetic
advance NO, fixed-power credit 0 and full Gate B OPEN remain unchanged.
