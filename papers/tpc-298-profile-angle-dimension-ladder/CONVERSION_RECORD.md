# TPC-298 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `aa6a797b49ed462881998abf696440d164a0f74c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `4c6588146ebe20e35a2ebb0e890616b2479fca01d467bd5010c682361f0c7f65`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `96ac0298cf03c8536d89926304a8537b822ea1004e239728664b4ccc9a8aacbf`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `1e6f08b34516bdcd863b791c0a1c5daea6a76516b81a21799fad10b0ed17fbc2`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7541623b6789846b5a12d63556510f467b9313dbf56d29e9125213da4698ed84`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC295_299.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position on the route` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `Literal profiles and the physical map` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `Projection, angle, and dimension theorem` | 100 | 2 | `HEADING_TEXT_MATCH` |
| `Finite audit and validation` | 153 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and obstruction` | 223 | 3 | `HEADING_TEXT_MATCH` |
| `Claim boundary and conclusion` | 238 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 257 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 274 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `77` before writing and `77` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `863633e9121bd7302108c82a5c28063c051a7f6a1f03a590f3d487610465efb6`.
- Source theorem/proof environment starts: remark at TeX line 93, theorem at TeX line 108, proof at TeX line 121, proposition at TeX line 133, proof at TeX line 139.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 66–70 | `9cfff7298dfdcad4b304fdd5f2e95452832fbbac3f4fba2b8b9c6c8872a54647` |
| D02 | \[...\] | 72–74 | `e92193628a6a9b7867ee2710e4ad5bdbeb6c850cf279679542c7e2384a0b204a` |
| D03 | \[...\] | 77–83 | `e426c88478957f6fc660ea0771e2bf7ca62fa38f9af33b81456918ea5f202026` |
| D04 | \[...\] | 86–88 | `3712edf34ef44a9172e9943e7903bbb7c662c4af99d9c14cb26bdc690b8f5f4c` |
| D05 | \[...\] | 103–106 | `c232e84a3fe649a44f1120e10ffaaaf4f4ce501beb3045ca41fb4f93602c6f8e` |
| D06 | \[...\] | 110–112 | `dc6781f3e477989abdbb6682afb38c5ace93a9a1d032b4ad6b7b221b913c0b6e` |
| D07 | \[...\] | 115–118 | `1301384c14a7ed571253a3975f92a6aec765aa96e9b2b745027734070ddb7ab9` |
| D08 | \[...\] | 125–127 | `ad2b9ecf6be9aa82a73330a5aa60b9097b1ea343ee01ebb94f798409877e3383` |
| D09 | \[...\] | 146–148 | `81a454157eeb904c9b2cc2c862bf4314114e6322855905b029ad5a2de1db6a4c` |
| D10 | \[...\] | 248–253 | `07a9981383ee03d2e4a9f860aa0e9a3ca26908f452292592a196184a0bf7bf0e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 17: `for Finite Twin-Prime Shells}`
- TeX line 29: `left open how much source dimension is needed to approach a physically`
- TeX line 41: `same threshold in at most six profiles on every row.  The final finite prefix`
- TeX line 42: `spans every registered target space.  This is a finite dimension/angle atlas,`
- TeX line 43: `not an asymptotic native-profile theorem or a twin-prime result.`
- TeX line 48: `The finite prime-shell line has separated ambient image existence from native`
- TeX line 51: `hit every finite target when the shell Gram is full rank; and TPC-296 found`
- TeX line 90: `weighted minimum, unit-edge max-cut, and all-positive vectors are only finite`
- TeX line 94: `The term literal refers to the finite cutoff formula and its source-side`
- TeX line 95: `origin.  It does not claim that this seventeen-element list is the complete`
- TeX line 96: `native profile class, nor that its dimension or conditioning is uniform in`
- TeX line 108: `\begin{theorem}[Finite profile-angle identity]`
- TeX line 145: `For a threshold $\tau$, the finite dimension statistic is`
- TeX line 151: `$|S|$, then $P_{|S|}=I$ on the target space and the finite residual is zero.`
- TeX line 153: `\section{Finite audit and validation}`
- TeX line 173: `\caption{TPC-298 finite profile-dimension headline.}`
- TeX line 184: `full-prefix finite target capture & 18 / 18\\`
- TeX line 211: `The minimum weighted dimension fraction is exactly the declared finite floor`
- TeX line 215: `prefix, the rank certificate makes all three finite target controls exactly`
- TeX line 220: `approximately $4.24\times10^4$.  This number is recorded as a finite`
- TeX line 229: `This is a geometric statement about the finite map $A^{\mathsf T}U_k$.`
- TeX line 231: `The result also explains why the final-prefix zero is not a paradox.  Once`
- TeX line 233: `finite image is all of $\R^{S}$, just as TPC-295's unrestricted image was.`
- TeX line 235: `least-norm source cost, and condition number before that trivial finite`
- TeX line 240: `The projection, principal-angle, and nested-prefix statements are exact finite`
- TeX line 242: `certified finite observations for the declared grid and two moduli.  The`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
