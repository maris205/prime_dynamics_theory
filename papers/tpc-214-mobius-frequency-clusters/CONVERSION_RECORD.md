# TPC-214 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `7d7224eb573154c866c99e61555a46de997fdbe8fc1f957d2de8f203020a3193`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `fb9570e3d3e3b69ceec931139427f763a4dd90505ffb69b444fa61f2b40b7900`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `0b4bc620d765a889ed07478e56d18279c82c16b4e327519fb1d61a405b90b741`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d590aaa5c0a2e4144a155e183d8256682c1b2789ba1bf98f63af294a97d3188a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC210_214.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 67 | 1 | `HEADING_TEXT_MATCH` |
| `The literal emitter and its reduced frequencies` | 110 | 2 | `HEADING_TEXT_MATCH` |
| `The cluster factorization theorem` | 171 | 3 | `HEADING_TEXT_MATCH` |
| `Four-packet compatibility` | 240 | 4 | `HEADING_TEXT_MATCH` |
| `Exact finite certificate` | 272 | 4 | `HEADING_TEXT_MATCH` |
| `Route evaluation and limitations` | 321 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 352 | 1, 5 | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | 364 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `91` before writing and `91` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `4589014ead161edbb886dc64c2b491c6a6f00ac3f0500853e362bb3a15bd33af`.
- Source theorem/proof environment starts: lemma at TeX line 139, proof at TeX line 148, corollary at TeX line 160, proof at TeX line 166, theorem at TeX line 186, proof at TeX line 199, corollary at TeX line 218, proof at TeX line 234, proposition at TeX line 246, proof at TeX line 259, remark at TeX line 266.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 72–78 | `53e7b03741e3f309b0dbea195e724d418216b14fe31b28714701f31d793493f0` |
| D02 | equation | 116–122 | `004d763271a46e7a2604dc86a43331eb9bb90a43bb09a0b46d7d47269b5b2846` |
| D03 | equation | 124–127 | `73402927b29d7b3b7812fc005d2dd007b9f0f8474c9b2448a5ade68502446bb2` |
| D04 | equation | 129–133 | `cd36d2783147856d92b19fd9ac89004fe469ce398cc1b6b148de778010e2996e` |
| D05 | equation | 142–145 | `e85a0caef761f9c1b0039364cdace19b009d4b57d0e2fa9c6300ec44cbb698d1` |
| D06 | \[...\] | 154–156 | `ceda0f5d574abe70cde2add5591b1d128f232ef0c89b3b80130b70f43c461a52` |
| D07 | equation | 174–179 | `3572b770bd601edad5cc1280e37f92d8613755eccf77279776bc0d01fae88a3b` |
| D08 | equation | 181–184 | `d0f1a2e3c411cf58ad74eb6e27270bd41e27493a3a10e82f47451f31c6a00023` |
| D09 | equation | 189–194 | `f83c4fe4a9370704c68c07ec566bfc7dbda609c511fbf18bd4944959546f8d0f` |
| D10 | \[...\] | 203–205 | `54a2e17e2d910b027800ae78893670a4201d5739866bd29731c3fbd9c44f4ab3` |
| D11 | \[...\] | 207–211 | `70cc67466e139390d695105bbb51929a06104f31d70d57511d1d26544e88232e` |
| D12 | equation | 222–228 | `5623f51f263543cf98528f2b764522a79d58dc89e99431dbbdcfd1ade5efb75a` |
| D13 | equation | 249–252 | `beae3958977fdf1efe9c35837c3c32fac36d8cd30b199d7932b79a4f8a68457c` |
| D14 | equation | 275–279 | `35c22fa91ca7b7fe611afa57429c1f119d8d0a70a1f99e561260cb24d2043ca9` |
| D15 | \[...\] | 301–304 | `2c72fe3efe26693175ce1f28e7c3621d952661272df59cafadfeeb145b5b4815` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 63: `The finite sign directions are exact; the displayed ratios are numerical`
- TeX line 65: `the literal V46 asymptotic cluster bound remains open.`
- TeX line 84: `kernel is not an orthogonal direct sum.  On a complete period, only equal`
- TeX line 95: `Second, the coefficient tail is not sign-definite.  The nested family`
- TeX line 96: `$\{5,7,35\}$ produces a substantial finite reduction, while the family`
- TeX line 97: `$\{3,5,7,105\}$ produces a finite enhancement.  The examples do not model the`
- TeX line 106: `\item two independently checked finite coefficient ledgers with opposite`
- TeX line 112: `Let $\Dd$ be a finite family of squarefree positive integers.  Let $\QQ$ be a`
- TeX line 113: `finite set of integers coprime to every member of $\Dd$, let $H\ge 1$, and let`
- TeX line 114: `$\psi$ be any function on the finite set of arguments that occur below.  Define`
- TeX line 188: `Assume the hypotheses of Lemma~\ref{lem:dilation}.  On one complete period,`
- TeX line 268: `emitter.  It does not delete the multiplicative principal character, a local`
- TeX line 272: `\section{Exact finite certificate}`
- TeX line 280: `The profile is smooth and even, and all finite row entries are rational.  The`
- TeX line 312: `observations.  This is a finite sign obstruction, not a lower bound`
- TeX line 332: `finite cancellation/enhancement signs & \texttt{PROVED\_EXACT\_FINITE\_SIGN} \\`
- TeX line 333: `finite energy ratios & \texttt{NUMERICAL\_OBSERVATION} \\`
- TeX line 335: `literal V46 asymptotic cluster bound & \texttt{OPEN} \\`
- TeX line 336: `prime-shell reassembly & \texttt{OPEN} \\`
- TeX line 344: `does not estimate the coefficient tails uniformly in the transition band`
- TeX line 345: `$Y_0<d\le U$.  It also does not perform the prime-only shell reassembly or`
- TeX line 347: `The finite profile is one explicit Schwartz choice, not the proof of an`
- TeX line 349: `advance only: no arithmetic $L^2$ credit, fixed-atom credit, strict`
- TeX line 357: `reusable structure for the next arithmetic step.  The two finite certificates`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:v46-row` → `main.tex#L77` (existing project target or original TeX label line).
- Link relocation: `#eq:emitter` → `main.tex#L121` (existing project target or original TeX label line).
- Link relocation: `#lem:dilation` → `main.tex#L140` (existing project target or original TeX label line).
- Link relocation: `#lem:dilation` → `main.tex#L140` (existing project target or original TeX label line).
- Link relocation: `#cor:zero` → `main.tex#L161` (existing project target or original TeX label line).
- Link relocation: `#eq:cluster` → `main.tex#L193` (existing project target or original TeX label line).
- Link relocation: `#eq:cluster` → `main.tex#L193` (existing project target or original TeX label line).
- Link relocation: `#lem:dilation` → `main.tex#L140` (existing project target or original TeX label line).
- Link relocation: `#eq:polarization` → `main.tex#L251` (existing project target or original TeX label line).
- Link relocation: `#eq:polarization` → `main.tex#L251` (existing project target or original TeX label line).
