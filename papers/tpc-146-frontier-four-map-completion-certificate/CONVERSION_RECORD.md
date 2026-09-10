# TPC-146 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `1e003023c5720a3af1a26007f60b06a1cd54b40071982a4db9929722bbc3f0cc`.
- Bibliography: [references.bib](references.bib), SHA-256 `70e4e986edb6a55a6ecea9176cb42833b3814122de75c6130f80cc2270aa1830`.
- Preserved PDF: [tpc-146-frontier-four-map-completion-certificate.pdf](tpc-146-frontier-four-map-completion-certificate.pdf), SHA-256 `c945330180d7882a44be26f19b1ca999c3990f1bd5ea54ad289138f98ff268a6`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ffb81b4a83ea1ed755336d56e0103cd3accf59dd944911672fc05441aa5fa0fc`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC143_146.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The disjunctive frontier contract` | 75 | 1 | `HEADING_TEXT_MATCH` |
| `The literal map route` | 124 | 2 | `HEADING_TEXT_MATCH` |
| `The zero-defect vector` | 169 | 2 | `HEADING_TEXT_MATCH` |
| `Two aggregation firewalls` | 248 | 3 | `HEADING_TEXT_MATCH` |
| `Source-locked current evaluation` | 283 | 3 | `HEADING_TEXT_MATCH` |
| `Verdict and claim boundary` | 334 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 379 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `64` before writing and `64` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `17`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `02f3b60852d7a57027665270e15ff40821bf0e9c371de913f67a9eb8f5d3afc5`.
- Source theorem/proof environment starts: definition at TeX line 200, theorem at TeX line 215, proof at TeX line 226, remark at TeX line 241, proposition at TeX line 250, proof at TeX line 256, proposition at TeX line 265, proof at TeX line 271, theorem at TeX line 336, proof at TeX line 355.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 82–92 | `bb80f3eeb8348250eb2535111ed01b8170ddaeff951ac18f81a64d4cf74bdbff` |
| D02 | \[...\] | 94–96 | `9b91f380286269cb5c9a1cc70f995f9c1f6bca27ff5f4fd190cfeefb17b3ac9c` |
| D03 | \[...\] | 98–100 | `edbd44d6dffceedfbcf578f501e8305cccc1d7f112e3790e59f0666f457a2793` |
| D04 | equation | 112–119 | `b00cd8fbbb50df67eaa859e27743708dbc72c82172e726056196df48e025b8c1` |
| D05 | \[...\] | 128–131 | `ac2b4fd47e4b7030248ca162048eab0f33406f7006f80a5ecac1377310c8adfd` |
| D06 | equation | 133–136 | `2980c9533b0b494c7dc9b53fa4b7ddb845c1d8af9c105c4af71fc5756efde1df` |
| D07 | \[...\] | 143–145 | `d0534b932e4a886a2b3315d59d9d5588326c756b2a2d5666b6ceb56e226ea201` |
| D08 | \[...\] | 150–152 | `6b3161f27714d7448388487104673cc3a32a9923711cfda920927643a79c8d2d` |
| D09 | align* | 173–183 | `e60f428fae2d7676c8f879654da5d8efe0656baa04d8d6ce570a5073b576b313` |
| D10 | \[...\] | 186–188 | `c2ef67c946dcf8d2d9c343840ebf87b296b76210b2e5525e6cfc3804d4f9a2a2` |
| D11 | \[...\] | 190–192 | `44b94e60b9d7ee73b11c3ae30d9e4a3ad43c79e4bccdc2a802a42aef6741eafd` |
| D12 | \[...\] | 194–196 | `3d51dc5270d2b30a41e8062c6554bb02df71e7ba4eb31b077c3415fca3058326` |
| D13 | equation | 208–213 | `d8d539ebc04b872cc59ed21e6a7e955eb9f314ae6eb6810507f701d4226cd326` |
| D14 | \[...\] | 219–222 | `639ec2ac6c80f8eecf90c5de17b7f477b2087806e5b9fde40cabfce1b8fbd9fe` |
| D15 | \[...\] | 305–309 | `27cffdd726272cb2b7d2e741c0cad92f044939732b6afcd1e48adf02a82e3327` |
| D16 | \[...\] | 339–342 | `dcadf6a3f91b9a778189a04a3acdbd17ee8fb1d89c4f7ee41ccb5eb84701aa35` |
| D17 | \[...\] | 344–349 | `3d5c1dd728f3e6ee43a8f89ce05a7ceb3cee689ece1975d7e9fdaa1e9b4582f0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 33: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 57: `total downstream prescribed-shift selector \(P_{h_0}\), two`
- TeX line 67: `proved cut-stage identity \(P_{h_0}^{\rm cut}=I\) is not the missing`
- TeX line 72: `route and a scalar-plus-eligible-tail route remain open.`
- TeX line 101: `for the \emph{complete} original frontier sum.  A finite regression,`
- TeX line 103: `does not satisfy this clause.`
- TeX line 106: `every eligible-tail-open path, or a separate theorem that makes their`
- TeX line 108: `finite fixture happens to contain no such row.`
- TeX line 151: `G,\qquad P_{h_0}^{\rm down}`
- TeX line 178: `D_P&:\ \text{path-domain defect of }P_{h_0}^{\rm down},\\`
- TeX line 217: `Assume all literal source matrices and the complete occurrence`
- TeX line 237: `The assumed complete registry then attaches every map edge to one`
- TeX line 243: `certificate.  It does not create \(L_X,Q_D,Q_Z,G\), or`
- TeX line 244: `\(P_{h_0}^{\rm down}\).  In particular, no defect can be evaluated`
- TeX line 265: `\begin{proposition}[Cut selection does not erase \(D_P\)]`
- TeX line 267: `The proved equality \(P_{h_0}^{\rm cut}=I\) does not certify`
- TeX line 272: `\(P_{h_0}^{\rm cut}\) acts before the missing occurrence lift and all`
- TeX line 297: `\item promotion of the empty finite eligible-tail sample;`
- TeX line 298: `\item substitution of \(P_{h_0}^{\rm cut}\) for \(D_P\);`
- TeX line 304: `The committed finite census is`
- TeX line 310: `This is a regression fixture, not an asymptotic support theorem.`
- TeX line 322: `\(G,P_{h_0}^{\rm down}\)`
- TeX line 352: `route remain \(\OPEN\).`
- TeX line 367: `The result sharpens one structural pointer.  It does not advance the`
- TeX line 368: `route to a purely arithmetic frontier.  No positive fixed-\(h_0\)`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 8 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:defectvector` → `../main.tex#L212` (existing project target or original TeX label line).
- Link relocation: `#eq:disjunction` → `../main.tex#L91` (existing project target or original TeX label line).
- Link relocation: `#thm:criterion` → `../main.tex#L216` (existing project target or original TeX label line).
