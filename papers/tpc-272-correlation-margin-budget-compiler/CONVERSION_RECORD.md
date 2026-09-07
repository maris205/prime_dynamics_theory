# TPC-272 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `1f803d9a145563c07e068fd15d5731a946d2419b564e45ead770d6a0f4604c71`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `0de29c8a5f18080d5fb33f0b0ff8ef82d10fed71d7c58188ff564ff29654d4e5`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `52ce12de62c73082863cc78962f2f4dde258188081e1f1665213cf6a04605de1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC270_274.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position and scope` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `The correlation coordinate` | 74 | 1 | `HEADING_TEXT_MATCH` |
| `The endpoint budget` | 107 | 2 | `HEADING_TEXT_MATCH` |
| `Sharp sign-only converse` | 157 | 3 | `HEADING_TEXT_MATCH` |
| `Finite margin audit` | 183 | 3 | `HEADING_TEXT_MATCH` |
| `Route status and limitations` | 226 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 243 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 255 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `83` before writing and `83` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1ac97e1670c826966049ddafa35ecf06d332be6c52ceeccedb5996022a469f46`.
- Source theorem/proof environment starts: lemma at TeX line 84, proof at TeX line 92, theorem at TeX line 115, proof at TeX line 141, proposition at TeX line 159, proof at TeX line 166.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 52–55 | `00f7209158882ccf9cc3bccc1654cd95865a0f65a23018d6f106f2d977552819` |
| D02 | \[...\] | 56–60 | `7b5c2efdcbe5898a94419f9c5420301e446e9a2da9fc6b61485342990ff5e558` |
| D03 | \[...\] | 66–70 | `d918bbb136fae305b1ff5cdae69f94012ad7ca742f71ab8dda1dd11116a36a8c` |
| D04 | \[...\] | 77–79 | `2a03cf661714a2ee8089b086ce1475fa9e2f69d3df3b971db43152d3e48c1cd9` |
| D05 | \[...\] | 86–89 | `c174b05a11d9df226204723deb50e4d7047fe816f0bc0632f39d3388c59de070` |
| D06 | \[...\] | 94–98 | `363491f308809878959a3ac86097a5c336b4d55e35dba37e655b5f60004d56b0` |
| D07 | \[...\] | 111–113 | `76d38ef9ee643ef90631f6045596ec65a7fdfa06314553c086a4938a5ea642d1` |
| D08 | \[...\] | 118–123 | `dd28e3b57e54deeb5a6da40a693f0176726cf2fe90b44fc53a77f1bf4ed3985b` |
| D09 | \[...\] | 125–129 | `75fdd21402ccead3028b763fbca1a85049a761c8eaf87a2074e94cac7b8d43d1` |
| D10 | \[...\] | 132–135 | `fc0d401ddf3e63a4b7147164a0fec4e9e7600b7a960897186705ed3e8a335945` |
| D11 | \[...\] | 143–145 | `858071015a3169c7a87cce8a345726dd0373aa844073f00aa8b08ae8843f742b` |
| D12 | \[...\] | 168–171 | `b12d3bd4818390f1c908b2f23ec6ad21fc497dfcad4f85063b579baca14f1224` |
| D13 | \[...\] | 210–213 | `8b85f7d7e5b33fc20ee649811681a4dda8acdeb1f900873678b5be638604e59c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 40: `we convert the TPC-271 finite certificate to exact rational \(m^6\) intervals:`
- TeX line 43: `finite numerical audit, not a source-level estimate or a twin-prime proof.`
- TeX line 48: `The TPC chain studies a literal finite V59 operator with prime shell, unit`
- TeX line 72: `twin-prime conclusion all still open.`
- TeX line 109: `We now state the new analytic bridge independently of the finite experiment.`
- TeX line 179: `The proposition is a structural obstruction, not a counterexample to the`
- TeX line 183: `\section{Finite margin audit}`
- TeX line 216: `strictly above \(4^6\).  Thus the finite data provide a particularly clean hostile`
- TeX line 233: `still open for the source-level V59 sequence.`
- TeX line 234: `\item The nine-row margin table is a numerically certified finite audit.`
- TeX line 237: `No finite ratio supplies fixed-power credit.  In particular, the observed`
- TeX line 238: `negative phase is not an eventual phase sector, the finite margin collapse is`
- TeX line 239: `not an asymptotic lower-bound refutation, and the compiler is not an`
- TeX line 241: `conditional sense; full Gate B and the twin-prime conclusion remain open.`
- TeX line 249: `the sign census from TPC-271 cannot fill this gap.  The finite certificate`
- TeX line 253: `lower-bound audit, not a phase-only promotion.`
- TeX line 260: `L. Wang, ''Phase--Radius Decoupling in a Finite V59 Residual,'' TPC-271`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
