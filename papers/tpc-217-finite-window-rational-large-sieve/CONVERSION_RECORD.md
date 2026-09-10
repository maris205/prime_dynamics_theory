# TPC-217 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `73ec5ee1770adbe554d20d3f08b6c3b335eb65adef629841fc8b725c745109f9`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `17e19613a409dd8ab29214b394d65ff4337f62ba1351a37ee8d13673cbb546ee`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `4165b8112c02aca14996834a759856c906547ac955e52b7d161e43cd24c5a544`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `0d05f8d6610a173262277c97021a1ec082b631ad61f55fc1facee46bf7165505`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC215_219.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 71 | 1 | `HEADING_TEXT_MATCH` |
| `Literal source and inherited complete-period bounds` | 114 | 2 | `HEADING_TEXT_MATCH` |
| `Exact reduced-frequency representation` | 171 | 3 | `HEADING_TEXT_MATCH` |
| `Finite-window large-sieve theorem` | 217 | 3 | `HEADING_TEXT_MATCH` |
| `Finite certificates and the crowding obstruction` | 286 | 4 | `HEADING_TEXT_MATCH` |
| `Route evaluation and open gates` | 324 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 341 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 354 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `106` before writing and `106` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `22`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `95b233babc388fd61d13ba5ee8142be321b677fd6b7010ca82ac1bc87be15ac2`.
- Source theorem/proof environment starts: lemma at TeX line 173, proof at TeX line 181, theorem at TeX line 191, proof at TeX line 207, lemma at TeX line 230, proof at TeX line 239, theorem at TeX line 245, proof at TeX line 262, remark at TeX line 279.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 53–56 | `6af59958ff8556040943624d2f92e239348dcd8273c964a59ea392f65899e047` |
| D02 | \[...\] | 81–84 | `3662cf777db5c3d0e0b2f53c4b99dc4fa6d8b8b046ba24e4831aa7909c28312b` |
| D03 | \[...\] | 89–92 | `1fc1c5afd2203b3be07630cf0587bb8d866e2680fd0e6670ac2f3f5f9b6a53ea` |
| D04 | equation | 117–121 | `e67c1eb96cc6ba77445458f42012fc4250941b09da7f127b45e098e864139e0a` |
| D05 | equation | 123–127 | `705690235f1fa7c004a7bb6c5b2837b68200f31dfb57d361a30e927df584aebd` |
| D06 | equation | 129–134 | `9ea5c9f589b43ab1d2c97040d987b3925627f94222577ff892a3a46e48fa0615` |
| D07 | equation | 136–140 | `81ac12ea3ba5bcfbd09a950fdfca1236209aa76c45ddfdcfdfc60a2f77b5a497` |
| D08 | equation | 144–148 | `8b1396b4ecdda6f21629553f192e99d7420f51593a5eba4a767dcb375b66692f` |
| D09 | equation | 150–154 | `538680a07a5ff3c2a1fbe60e9aeabf92342d2ea0bcbf3d992df542f658925708` |
| D10 | equation | 156–162 | `c77f350f0730054d95a10b5fb2beacf1d0fe6c10a83555d523bbdd80b50378b8` |
| D11 | equation | 164–167 | `a0feb3f9b54948a3d53cd1014492ccdcb8a6ff611f1ba1ea409a7f9c350b16a6` |
| D12 | \[...\] | 176–178 | `3f08666cc9b54477437425b960c142a7d3d4f2adff5f2a95e8e2b7e34f26d8e0` |
| D13 | \[...\] | 183–185 | `8bf67ed2548352fa852f82420d27f0810f5224cd9512e67cddba5c1d8afdf0bf` |
| D14 | equation | 194–197 | `b9c2374e210adb66ab1dc9c8f519ea5bdc74009d1c7fb196f382f878048e62e1` |
| D15 | equation | 199–204 | `e4e64ddccb3a2e66d46f02b2ce757816494dd3fd88a1b817f17bb439a1b4a833` |
| D16 | equation | 222–226 | `df25efba9e200ab3268d5bb8da4ce345dd7c551a19ec81c1f19decf3b411df3e` |
| D17 | \[...\] | 233–235 | `d7419ee46bfc95aae20a44895a7713d931605ca9915f71c448168c3feb949126` |
| D18 | equation | 248–252 | `9e4f09cce35cffdc4d990eba341cdb3a99ccd4e7a68ba2f664325482154416f8` |
| D19 | equation | 254–258 | `7ba84d6e4093ad130cf77c57fb1bff60dd8d72d71135e1cf612220d32ef9a4d3` |
| D20 | align | 265–271 | `8e575cc1872324a1a280de475bc1e69137fb3aff9602206852ca26c166a7291f` |
| D21 | \[...\] | 314–317 | `bfe853b6f70872b7a796a7f53b3b0a8c9cacc250768106e8ea8e449b661b48c6` |
| D22 | align* | 328–335 | `713159adc4aad83074d173d6d6f43957694c6956a22cb6870133ace1ef463af6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 34: `\title{\textbf{Finite-Window Attachment by Reduced Rational-Frequency Large Sieve}}`
- TeX line 45: `reciprocal emitter but left the physical interval open.  This paper attaches`
- TeX line 51: `additive large sieve gives a finite-window factor $N+U^2$, where`
- TeX line 58: `unnormalized exponent $43/32+o(1)$.  A finite aligned-shell fixture has exact`
- TeX line 60: `by free finite-window orthogonality.  This is a structural result only: prime-`
- TeX line 62: `twin-prime endpoint remain open.`
- TeX line 66: `\texttt{PROVED\_STRUCTURAL\_L1 / FINITE\_WINDOW\_ATTACHMENT}.\\`
- TeX line 68: `is a standard named input.  Finite fixtures are reproducibility checks, not`
- TeX line 101: `unchanged.  The result does not exploit signs of $\mu$, cancellation among`
- TeX line 102: `primes, or the four-packet polarization.  It establishes the finite-window`
- TeX line 107: `\item an exact finite-window regrouping of the literal common-source kernel;`
- TeX line 110: `\item an independent finite certificate and a one-point aligned-shell`
- TeX line 111: `adversary showing why free finite-window orthogonality is invalid.`
- TeX line 217: `\section{Finite-window large-sieve theorem}`
- TeX line 228: `large sieve; no arithmetic property of the coefficients is required here.`
- TeX line 245: `\begin{theorem}[finite-window attachment]`
- TeX line 246: `\label{thm:finite}`
- TeX line 251: `\label{eq:finite-bound}`
- TeX line 273: `\eqref{eq:tpc216} to obtain \eqref{eq:finite-bound}.  Finally,`
- TeX line 280: `The proof controls the finite-window off-frequency Gram by spacing.  It does`
- TeX line 282: `four-packet reassembly.  The result is consequently structural and does not`
- TeX line 286: `\section{Finite certificates and the crowding obstruction}`
- TeX line 288: `The reproducible finite fixture uses $Q=\{11,13,17\}$, $H=40$, the full`
- TeX line 292: `three translated windows of lengths 1, 17, and 60.  The finite checks use exact`
- TeX line 297: `\caption{Finite-window certificate.  The right column is the coarse`
- TeX line 312: `uniform envelope, not a sharp finite fixture estimate.  The separate`
- TeX line 320: `finite-window Gram is not freely diagonal even in this small admissible model.`
- TeX line 321: `The statement is scoped: it does not contradict the long-interval large sieve`
- TeX line 322: `and is not an asymptotic lower bound for the V46 prime shell.`
- TeX line 324: `\section{Route evaluation and open gates}`
- TeX line 330: `&\texttt{TPC217\_FINITE\_WINDOW\_ATTACHMENT`
- TeX line 333: `&\texttt{TPC217\_PRIME\_SHELL\_REASSEMBLY = OPEN},\\`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:emitter` → `main.tex#L133` (existing project target or original TeX label line).
- Link relocation: `#lem:dilation` → `main.tex#L174` (existing project target or original TeX label line).
- Link relocation: `#eq:regroup` → `main.tex#L203` (existing project target or original TeX label line).
- Link relocation: `#eq:large-sieve` → `main.tex#L225` (existing project target or original TeX label line).
- Link relocation: `#lem:spacing` → `main.tex#L231` (existing project target or original TeX label line).
- Link relocation: `#eq:tpc215` → `main.tex#L161` (existing project target or original TeX label line).
- Link relocation: `#eq:tpc216` → `main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#eq:finite-bound` → `main.tex#L251` (existing project target or original TeX label line).
- Link relocation: `#eq:normalized-bound` → `main.tex#L257` (existing project target or original TeX label line).
- Link relocation: `#tab:certificate` → `main.tex#L299` (existing project target or original TeX label line).
