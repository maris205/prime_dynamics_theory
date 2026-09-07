# TPC-268 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `3852064cba5864cd53c94173bfd2e6440ddaae0b8e779d6f4a3dd834fd369f84`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `f6a3829dca58b6a387fe912125f98768f262e5596c032f51e59f461737fee527`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `54ad2c5dbca9aca45285ef4b82f653744b891254e7568968c819ff8bb4fc82f0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC265_269.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position and claim firewall` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `The finite physical operator` | 45 | 1 | `HEADING_TEXT_MATCH` |
| `Projection and interval decision` | 79 | 2 | `HEADING_TEXT_MATCH` |
| `The finite obstruction` | 125 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation` | 179 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 213 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 225 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `67` before writing and `67` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `66d459f2de32d055374cc8535d0703fd697b2bab413d3143f6eebd1dbd6f4a91`.
- Source theorem/proof environment starts: proposition at TeX line 98, proof at TeX line 103, theorem at TeX line 127, proof at TeX line 143.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 47–50 | `4dbe83cf7cd26419d60360f19ad197eb5a642b3ad21fc3e708249380437b7396` |
| D02 | \[...\] | 52–56 | `193f216ccaa959456b38e413df675eff97585d44276db7c5cea8abaab606e743` |
| D03 | \[...\] | 58–60 | `1b596ead0c9c511f3d66c0f158c9cc2c770400bacb891548f6ef86a205483e78` |
| D04 | \[...\] | 62–66 | `c74fecc52c250da5644aca82ccda36914aaaf3bd1c267cd13d1f107417776a48` |
| D05 | \[...\] | 68–70 | `4795ba7ddec4eae41b20e8d9f5ed00eebd53d50cbbf013771e101c344bb61e99` |
| D06 | \[...\] | 72–75 | `d1ff7e35a96c41d8bb4268a83800af2bb7aa9578d0c01a03d7c53b5d2aea4527` |
| D07 | \[...\] | 82–85 | `af23f673e715143c03c8dc11e46e33725402006aafebb7f7600ec61cb0487bb9` |
| D08 | \[...\] | 87–91 | `cc37e3114db2f998a09a4a75b74cad5ba9a4ba409c53b5165b3ad08b25fd4075` |
| D09 | \[...\] | 93–96 | `2624a842510f4dd53c4dc49dca3ba70e3371f7817d4fd56e46090c5634dab305` |
| D10 | \[...\] | 112–116 | `fca4c30155a62fb8dd2cc1e74f5937c7eec607d000debd5117601d2f56b10c12` |
| D11 | \[...\] | 121–124 | `1f956254a9da26ab3ff2e3d6360656d97d7684443470740bbae3a0aa089c5a31` |
| D12 | \[...\] | 130–136 | `2feeb706fd95c468d805db48b5719fc3c9e3068ca055a5118c94c476e4616205` |
| D13 | \[...\] | 187–189 | `5ea7d019943de398c17d086d91a02eaf19daf47afd0cc97afaef6fb80ed26da4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `\title{A Finite Cutoff-Sensitivity Obstruction for the V59 Residual Phase}`
- TeX line 20: `TPC-267 found a finite quarter contraction for a literal V59 residual using`
- TeX line 24: `rational intervals classify sixteen finite rows. Six matched \(z=2\)`
- TeX line 30: `over the declared finite parameter family, but it is not an asymptotic`
- TeX line 36: `TPC-267 supplied a reproducible finite interface and twelve \(z=2\) rows`
- TeX line 38: `radius and source-specified profile open. The present paper asks whether that`
- TeX line 39: `finite inequality is stable under the interface choices declared as modeling`
- TeX line 43: `\textit{numerically certified finite result}.`
- TeX line 45: `\section{The finite physical operator}`
- TeX line 98: `\begin{proposition}[finite identity]`
- TeX line 111: `The finite Euler product is multiplied through \(P=50000\). The tail uses`
- TeX line 125: `\section{The finite obstruction}`
- TeX line 137: `so changing only the finite cutoff from \(z=2\) to \(z=3\) flips the`
- TeX line 181: `The central pair gives a clean finite sensitivity statement. The physical`
- TeX line 191: `Consequently a universal quarter-sector lemma over this tested finite`
- TeX line 193: `show that the \(z=3\) obstruction is not a single rounded-clock accident,`
- TeX line 194: `and the \(z=5\) row supplies a stronger finite stress point. These are`
- TeX line 195: `finite statements about the explicitly enumerated rows.`
- TeX line 199: `cutoff, and this paper does not prove that its finite values are represented`
- TeX line 200: `by any fixed \(z\) in the table. Thus the result is not a source-level`
- TeX line 203: `threshold, while the \(N=96,z=3\) row with \(s=2\) is above it. A finite`
- TeX line 207: `The audit also does not pay any endpoint budget. It proves no bound for the`
- TeX line 208: `size of \(R\), gives no fixed-power saving, and supplies no arithmetic`
- TeX line 211: `remains open.`
- TeX line 215: `TPC-268 turns the finite residual census into an adversarial diagnostic. A`
- TeX line 216: `matched \(z=2\) control and \(z=3\) perturbation use the same finite physical`
- TeX line 219: `next question is not whether the most favorable finite profile can be made`
- TeX line 221: `profile admit a uniform interval theorem. Until that question is answered,`
- TeX line 222: `the observed phase contraction is evidence about a finite interface rather`
- TeX line 237: `L.~Wang, ''A finite literal V59 residual-radius and signed-phase census,''`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
