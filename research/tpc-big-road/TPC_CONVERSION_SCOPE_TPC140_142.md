# TPC140–142 conversion and bounded prerequisite audit

Updated 2026-09-09. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Three existing manuscripts only;
no new paper, original-source repair, theorem, or publication release.

## Mechanical evidence and limits

Preflight retains 254 math nodes and 49 raw displayed-equation blocks over
18 preserved PDF pages. Source locks and full abstract/body formula and
normalized-text roundtrips pass. Original hashes and automated heading
matches remain in each conversion record. TPC142's Conclusion heading
at source L503 retains automatic matches on pp1 and 6; the complete
manual read locates the actual conclusion on p6. The automatic ambiguity
is preserved alongside that supplement, not rewritten as a unique match.

All three use root main.tex and an exact-basename original PDF. Reading
layers stay at paper/main.md; no source is copied or moved. Complete
invoked bibliographies are retained, not externally verified or formatted
into invented entries. No separate PROOF_PACKAGE.md is present.

The converter and maintenance helpers are unchanged. All 24 targeted
coverage/inventory/source-link tests pass in normal and optimized modes.
Neither full semantic verification nor reliable-full-md is earned.

## Independent original-source audit

Read-only task `tpc-maintenance-source-scope-140-142-20260909` completed
all required original text and full PDF-extraction reads. No required
file or PDF page remains unread; first fatal is NONE and supported level
is SCOPED_ARCHIVE_REVIEW_ONLY. Nine README/main.tex/references.bib texts
total 2,116 raw LF characters and 75,210 bytes. Three exact PDFs total
18 pages and 1,275,559 bytes; all 12 originals total 1,350,769 bytes.
Each manuscript invokes only its local references.bib, without a local
TeX child. Original proof/derivation packages and notes are absent;
these are expected discovery results, not failed reads.

All 12 originals matched baseline Git blobs by direct raw-byte and
SHA-256 equality at start and finish. The canonical ledger's unchanged
SHA-256 is
`43a409061f55bb48f16c28bb1e6f8289fe824dca6704f459a49f919bc24b60a2`.
It contains all and only the three papers' README, main.tex,
references.bib and exact-basename PDF, as repository-relative path, TAB,
lowercase SHA-256 and LF, LC_ALL=C ordered with final LF. Controls are
excluded; binary PDF LF bytes are not counted as textual source lines.

HEAD and cached origin/main stayed at the declared commit, the index
was empty and the same nine declared tracked paths remained dirty.
AGENTS.md was read completely and matched its baseline Git blob.
Handoff SHA-256 stayed
`f8ee2801e45b26b080a406c7548aa852cfa865d3e24deb09f0d868ad147510e8`.
Untracked counts rose from 591 to 614: exactly twenty allowed conversion
outputs and three scope reports, with no removed status entry. Generated
contents were not read; the primary owns the broader untracked-byte
comparison. Cached remote equality is not a fresh live-remote observation.

All 17 reported shell invocations exited zero: initial Git/status/hash/
control reads, complete AGENTS reread, scoped rg discovery, restricted
numbered handoff read, five complete numbered original-text invocations,
three pdfinfo and three complete pdftotext calls, and two in-memory
Node preservation audits. The initial compound control display was
truncated and recovered by complete control/status reads. No original
read remains truncated. Compound/pipeline component exit codes were not
separately observed and are not invented. No source edit, network,
scientific script/JSON/schema review, reproduction, build or render ran.

## Original counts and complete manual PDF locations

| Original source | Text files / raw LF / bytes | PDF pages / bytes |
|---|---:|---:|
| [TPC140](../../papers/tpc-140-exceptional-scale-selector-power-gate/main.tex) | 3 / 622 / 20,043 | 5 / 415,189 |
| [TPC141](../../papers/tpc-141-source-locked-cut-arithmetic-integration/main.tex) | 3 / 763 / 27,989 | 6 / 464,040 |
| [TPC142](../../papers/tpc-142-mvp4-source-locked-route-decision/main.tex) | 3 / 731 / 27,178 | 7 / 396,330 |

Lines below refer to the linked root main.tex. Actual PDF page and
printed numbering agree in the complete layout-text reads. This is
text-page location evidence, not rendered-PDF QA. No subsection headings
occur. README, preamble, bibliography and document endings were also read.

| Paper | Complete heading/page coverage and continuations |
|---|---|
| TPC140 | Title L30–37 and abstract L39–74: p1. §1 Why almost all scales are not all prefixes L76–125: pp1–2, continuing from L99 on p2. §2 Two legal return interfaces L127–252: pp2–3, L127–193 p2 and L195–252 p3. §3 Power transport L254–325: pp3–4, Endpoint gate L303–325 p4. §4 The logarithmic corridor and its separate ledger L327–406: p4. §5 Certificate schema and current verdict L408–457 and references L459–464: p5, seven printed references. No paragraph headings. Complete README L1–100, TeX L1–466 and BibTeX L1–56 read. |
| TPC141 | Title L43–53, abstract L55–96, keywords L98–100 and claim boundary L103–113: p1. §1 The inherited target and the two new branches L115–153: pp1–2, continuation from L127 p2. §2 Source-locked records L155–215: p2. §3 The complete cut and the frontier L217–260 and §4 What the arithmetic shadow proves L262–315: p3. §5 Cut-aware synthesis L317–363 and §6 The nonduplicated 1/400 ledger L365–416: p4. §7 The source-locked manifest L418–475, including Table 1: p5. §8 Deterministic audit and claim boundary L477–513: pp5–6, list continuation from L489 p6. Established L499–504, Not established L506–513, §9 Conclusion L515–530 and references L532–538: p6, fourteen printed references. Complete README L1–89, TeX L1–540 and BibTeX L1–134 read. |
| TPC142 | Title L48–58, abstract L60–114, keywords L116–118 and snapshot boundary L120–131: p1. §1 What changed after MVP3 L133–171 and §2 A frozen source-locked snapshot L173–202: p2. §3 Statuses, evidence and active requirements L204–237: pp2–3, L210 onward p3. §4 Eight total audit outcomes L239–290: p3. §5 The strict endpoint and stop directions L292–320, §6 H9 must be arithmetically independent L322–348 and §7 Projection of TPC-133–141 L350–391: p4, except Table 1 L352–384 floats to p5; narrative L386–391 stays p4. §8 First missing and current verdict L393–430: heading/box p4, theorem/proof/corollary L406–430 p5. §9 Publishable outcomes and next branch L432–469: pp5–6, numbered-list continuation from L458 p6. §10 Deterministic regression and claim boundary L471–501, Established L492–495, Not established L497–501 and §11 Conclusion L503–518: p6. References L520–526: p7, fourteen printed entries. Complete README L1–94, TeX L1–528 and BibTeX L1–109 read. |

## Bounded prerequisites and source qualifications

These are attributed source statements and archive-reading qualifications,
not independent proofs of their analytic inputs. Missing literal physical
coefficients, growing uniformity and loss payments are not filled by
conversion success or a historical certificate description.

- **TPC140:** main.tex L78–81 (p1) uses generic bounded b(n) and
  C(t)=t^(-1)*sum_(t<n<=2t)b(n), without expanding a physical Mobius
  product, masks, phase or outer-label tuple. Components f, sums S_f
  and masses V_f require every mask/weight/phase/origin/prefix to be
  covered (L181–193, p2). No physical h0 or identifying map is supplied.
  The dyadic block, scale window J_X=[x/omega,x] and normalized prefix
  supremum sup_f sup_(T in I_f)|S_f(T)|/V_f(T), after zero-mass discharge,
  are distinct domains. Selector averaging is not that pointwise supremum
  (L244–252, p3). The global exceptional premise holds for y>=2,
  K_X>=1 and nonnegative power-loss exponents; no physical x-to-X map
  or N,q range is supplied. Domination must hold on every Borel set;
  growing families require uniform component bounds or joint domination.
  Positive atoms defeat every finite selector constant. Global-to-window
  loss is min{1,(log x)^(1-c0)/log omega}, and required endpoint dilates/
  CRT pullbacks must be union-controlled (L136–252, pp2–3). Block 1/t,
  logarithmic probability dt/(t*log omega), and prefix mass V_f(T) do
  not automatically become physical original-X normalization. The ledger
  (L254–406, pp3–4) is sigma_raw=min{eta_tail,
  sigma_aff-ell_sel-ell_cen-ell_BV} and
  sigma_final=sigma_raw-Lambda_phys, requiring strict positive difference.
  All upstream costs precede raw 1/400 recording. Separately,
  kappa_aff=min{kappa_corr,kappa_exc} and
  kappa_raw=min{kappa_tail,kappa_aff-kappa_sel-kappa_cen-kappa_BV}.
  Positive logarithmic saving is not fixed-X-power saving; K_X=X^o(1)
  and epsilon_X=o(1) alone do not make their product vanish. The indicator
  counterexample is not constructed Liouville values (L123–125, p2).
  The source distinguishes exact selector implication L0 from conditional
  physical transport L1; positive fixed-h0 L2 remains unproved.
- **TPC141:** main.tex L117–129 (pp1–2) uses B_(h0,delta)(X), prescribed
  nonzero even h0, fixed rational 0<delta<1/2 and fixed compactly supported
  smooth W. Arithmetic signs/masks/phases are imported, not expanded.
  The support-envelope archive's deterministic dyadic prefix cut gives
  B=S_soft+S_elig+S_front and three terminal classes, not full-carrier
  totalization; the low-L formal frontier column can have zero full
  arithmetic coefficient (L217–260, p3). The witness is for sufficiently
  large X; no N,q range is restated, and fraktur-q is a quantifier record,
  not a modulus bound (L157–169, p2). Imported defect error holds for
  each fixed A>0 with affine forms/modulus/cutoff frozen before the limit.
  Growing-family uniformity, containment, reassembly, local exceptional
  windows and deterministic-prefix return remain missing (L262–315, p3).
  Original amplitude scale is X; the eligible-prefix outer error is
  already o(X). Conditional synthesis keeps |B|<=o(X)+|S_front|+
  X^(1-sigma_elig+Lambda_elig+o(1)), so cannot discard the frontier
  (L317–363, p4). The ledger requires Lambda_phys<1/400, energy-to-amplitude
  e/2, disjoint primitive replacement and selector charge once. H3
  squarefree tail, H5 content remainder, physical high/ultra/boundary and
  frontier totalization are four different residual namespaces. Complete
  upper U<1/400 passes; lower/exact-dual L>=1/400 stops; upper U>=1/400
  alone does not. Frontier, cover, localization, reconnection and outer
  census costs remain unknown (L365–416, p4). Frozen-scope unconditional
  arithmetic statements do not remove the integration's conditional scope.
- **TPC142:** main.tex L133–171 (p2) imports the complete-carrier formula
  for B_(h0,delta), without expanding signs/masks/weights. The selected
  signed_native_frontier_augmented route is distinct from two stopped
  alternatives (L386–391, p4). Fixed physical h0 is required, but no
  numerical value/new identification is supplied and nonzero-even h0/
  rational-delta ranges are not restated. H7's total map is untestable
  (L210–214 p3, L376–377 p5). The three-class cut is not full-carrier
  totalization; physical L2 needs every mask, weight, phase, origin,
  prefix and residual sector. Classifier order is administrative, not
  arithmetic-prefix order. The decision is a frozen 27 July 2026 MVP1
  snapshot, without a growing X,N,q corridor (L123–130, p1). Frozen,
  logarithmic or almost-scale results do not prove complete-family
  uniformity; containment, reassembly, local windows and prefixes stay
  open (L204–237, pp2–3). Original-X amplitude normalization and physical
  endpoint are distinct from arithmetic saving; hash validity is not
  theorem validation. The strict Lambda_phys<1/400 ledger retains energy
  conversion, joint replacement and census. Unknown is not zero;
  determinant reserve cannot reduce physical cost. H9 must have no direct
  or indirect H2–H5 dependency (L292–348, p4). The snapshot is NOT_TESTABLE,
  first missing H1.frontier_totalization, with H6–H9/endpoint incomplete
  (L393–430, pp4–5). This historical verdict does not reopen TPC418.

## Preserved wording, references and remaining boundary

TPC142 main.tex L141–145 (p2) places eq:synthesis inside an unnumbered
display, while L286–289 (p3) uses eqref; extracted Remark 4.3 prints
reference (1). The primary separately inspected both literal source
fragments. This is a cross-reference issue, not a missing equation or
proof verdict. TPC140 README L81 groups selector/exponent implications
as conditional L1, while main L434–441 (p5) distinguishes the exact L0
selector implication from conditional L1 transport; the finer scope stays.

Full bibliography/printed counts are 7/7, 18/14 and 15/14. TPC141's
uncited entries occupy bibliography L29–36 and L45–64; TPC142's uncited
TPC141 entry occupies L104–109. Omission from printed references does
not mean unread BibTeX. TPC137–139 titles in TPC140 bibliography L37–53
(p5) vary from TPC141 L110/117/124 (p6) and TPC142 L78/85/92 (p7).
TPC140's title begins Exceptional-Scale Selection (main L30–32, p1),
but TPC141 L131/p6 and TPC142 L99/p7 cite a Selector and Power-Ledger
Interface title. These are preserved local variants, not established
source substitutions. Tao–Teravainen attribution in TPC141/142 is indirect
through the series; no upstream verification was performed.

Restricted arithmetic results are not relabeled synthetic or promoted
to full physical L2. Original-proof validation, upstream theorem review,
explicit future wording reconciliation, rendered-PDF QA and reliable-full
Markdown semantic review remain open. Finite historical validation was
read as source prose, not reproduced.

TPC418 STOP, arithmetic advance NO, fixed-power credit 0 and full Gate B
OPEN remain unchanged. No new research route or paper is authorized.
