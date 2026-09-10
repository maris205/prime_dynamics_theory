# TPC-180 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `796db52a1bd3e11ff9dc829cea8420ea2041d720d67635c0fec648aebce9faed`.
- Bibliography: [references.bib](references.bib), SHA-256 `ab72266f5264dd21d3f73935accec014523e0060c6e2fb9a6e4c8379676a5e85`.
- Preserved PDF: [tpc-180-production-phase-registry-census.pdf](tpc-180-production-phase-registry-census.pdf), SHA-256 `ede66f496c40c2c6498675987f22dceb3185f7172cf835ed7e73c4145ff7a110`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `6765c80b2652aee7ac39684e783d5d5f2b42d6130afd98bb4cffa9351b339ce5`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC180_184.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The exact question` | 82 | 1 | `HEADING_TEXT_MATCH` |
| `\texorpdfstring{Fixed \(h_0=2\)}{Fixed h0=2} is present and is not a phase` | 126 | 2 | `HEADING_TEXT_MATCH` |
| `Packet coordinates required by TPC-170` | 161 | 2 | `HEADING_TEXT_MATCH` |
| `Frozen source census` | 212 | 3 | `HEADING_TEXT_MATCH` |
| `Decision and typed progress` | 293 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducible artifacts and next gate` | 323 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 345 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 356 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `51` before writing and `51` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `13b5c08c2273cca8fa0cd8700327346c7dad3b50ea9194003592d65adb8ce982`.
- Source theorem/proof environment starts: definition at TeX line 107, proposition at TeX line 139, proof at TeX line 145, theorem at TeX line 256, proof at TeX line 271, remark at TeX line 283.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 85–88 | `de220d87a5d1d8c283080aafa6027381b433a333f30a91c1bcdf5ffffdc6d95a` |
| D02 | \[...\] | 90–102 | `39e2f015ae741d6e9334d406f22f0bfbe185972725ea35d97dbd0f07fef634c4` |
| D03 | \[...\] | 129–132 | `2f582f921dd6392aab76711642ad23f51770c31ec1433616e483a572fb3052d9` |
| D04 | \[...\] | 164–168 | `6aff3b5cacb0a48003e3731cac1262506af9d1dafd70832948ed1ca79defabe4` |
| D05 | \[...\] | 170–173 | `e4c5bfafa198319a2a08a7b0b7d14382031507ff4cec24c93d061eef31027e89` |
| D06 | \[...\] | 178–185 | `b9d461b1ad4acea23d1fed01a34692716eecc3ad81450475109474c71d10ad0f` |
| D07 | \[...\] | 187–194 | `a1750b43ec9faf978bef61e367404615bbe46f6a7defb892075372eb00bdfc34` |
| D08 | \[...\] | 200–203 | `5ac935d5f5e491f58ccffdcd471f41690934fb930277ced4b99263270dbc0fdc` |
| D09 | \[...\] | 296–306 | `ae8e16c247edf2400acd9ad2f6a5ca093919511df98be22d0732917c6e8b03c9` |
| D10 | \[...\] | 337–340 | `5c9c7e8c13fe0101f30a5147c1577c6788bee26f721f119de112e38d6aeff637` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `pdfkeywords={production phase registry, named atom, fixed h0, packet coordinates, source lock}`
- TeX line 39: `\textbf{Fixed-\(h_0=2\) Data, Missing Named-Atom Values,}\\`
- TeX line 59: `\(h_0=2\), and they specify the type of the missing H9 phase record.`
- TeX line 68: `global nonexistence theorem, does not synthesize phase zero or any`
- TeX line 75: `The fixed-\(h_0=2\) fact and the phase registry are separate data`
- TeX line 103: `The node has no arithmetic parent.  This direction is deliberate:`
- TeX line 114: `\item a separate source lock for \(h_0=2\);`
- TeX line 124: `not a record in the sense of \cref{def:record}.`
- TeX line 126: `\section{\texorpdfstring{Fixed \(h_0=2\)}{Fixed h0=2} is present and is not a phase}`
- TeX line 130: `h_0=2`
- TeX line 131: `\tag{3}\label{eq:h0}`
- TeX line 135: `marks the fixed physical \(h_0\) gate as proved on the relevant actual`
- TeX line 141: `The source-backed fact \eqref{eq:h0} does not instantiate any of the`
- TeX line 146: `The integer \(h_0\) is the prescribed physical shift, while`
- TeX line 150: `\texttt{fixed\_h0} or fixed-physical-\(h_0\) field.  None gives a`
- TeX line 157: `This proposition does not weaken the fixed-\(h_0\) result.  It only`
- TeX line 174: `At ambient scale \(X_n\), a prescribed finite list`
- TeX line 209: `\eqref{eq:representative} does not select the actual production`
- TeX line 225: `fixed physical \(h_0\) & \(2\), source-backed &`
- TeX line 234: `A metric quantifier, not a named atom.\\`
- TeX line 243: `\caption{The fixed-\(h_0\) fact survives the census; the production`
- TeX line 260: `\item \(h_0=2\) is source-backed on the relevant actual core;`
- TeX line 275: `fixed-\(h_0\) records and four phase-obligation records.  It is not a`
- TeX line 279: `source.  By \cref{def:record}, the mapped evidence does not construct`
- TeX line 285: `\Cref{thm:census} is not a theorem that no physical phase description`
- TeX line 319: `The fixed-\(h_0=2\) field is a proved literal data fact, but it creates`
- TeX line 332: `as a phase value, an unsourced locator, a synthetic packet row, H9`
- TeX line 334: `the fixed-\(h_0\) fact promoted to \(\Ltwo\).`
- TeX line 348: `\(h_0=2\) and the determinant-two Fourier interface are present; the`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:h9` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#def:record` → `../main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:h0` → `../main.tex#L131` (existing project target or original TeX label line).
- Link relocation: `#def:record` → `../main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:sum` → `../main.tex#L184` (existing project target or original TeX label line).
- Link relocation: `#eq:fiber` → `../main.tex#L167` (existing project target or original TeX label line).
- Link relocation: `#eq:representative` → `../main.tex#L202` (existing project target or original TeX label line).
- Link relocation: `#tab:census` → `../main.tex#L245` (existing project target or original TeX label line).
- Link relocation: `#eq:coordinates` → `../main.tex#L193` (existing project target or original TeX label line).
- Link relocation: `#eq:h9` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#eq:signature` → `../main.tex#L101` (existing project target or original TeX label line).
- Link relocation: `#eq:representative` → `../main.tex#L202` (existing project target or original TeX label line).
- Link relocation: `#eq:coordinates` → `../main.tex#L193` (existing project target or original TeX label line).
- Link relocation: `#def:record` → `../main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#def:record` → `../main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#thm:census` → `../main.tex#L257` (existing project target or original TeX label line).
- Link relocation: `#eq:decision` → `../main.tex#L305` (existing project target or original TeX label line).
