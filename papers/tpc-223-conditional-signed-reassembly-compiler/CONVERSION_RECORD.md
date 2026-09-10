# TPC-223 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `81693a79efb42dd74b8e4bda8977746ce57637df2008c7a9173dd608c9411644`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `6b0b57f46ae48dd8d36efaa859ce37f6ae948511010d41be5ad543747cdb991b`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `dcf3e756fb83867f952b6b311fd545909816084159bfb6fc88735220f02616f4`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC220_224.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Why a compiler is the next bridge` | 45 | 1 | `HEADING_TEXT_MATCH` |
| `The conditional two-channel interface` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `Exact compiler theorem` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Rational certificate and adversarial boundaries` | 122 | 2 | `HEADING_TEXT_MATCH` |
| `Route evaluation and claim firewall` | 162 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 180 | 2, 3 | `UNMAPPED_OR_AMBIGUOUS` |
| `References (thebibliography)` | 188 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `57` before writing and `57` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a95ebca292c4c159a9fcc5f83dc50fe9dd04a909c7627f66212b343fcc840b7c`.
- Source theorem/proof environment starts: remark at TeX line 79, theorem at TeX line 87, proof at TeX line 103.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 31–33 | `acf80a3c355a6dcd03dc4169d02753d8112765829ff237f9b568ce51a9e99174` |
| D02 | align | 67–71 | `ca9848e9cf6ccb146621b1072cfbe8c5271e3f71c5d193ad25b79004bd6d90d0` |
| D03 | \[...\] | 89–91 | `c032a11e9c7321e23df9297808a5960685f1960fd012851af5782e770f5048af` |
| D04 | \[...\] | 93–96 | `1a4c2d2412a945cab14fef83fac3f3901c908e0ef67fc060882520123dda503c` |
| D05 | \[...\] | 98–100 | `dc026f3138dfe79c93caa50e3454cd53ab141b03f0b4aae7b1689facc499730c` |
| D06 | \[...\] | 105–108 | `7512293de9c326393adae54778a95794021c9df73eeb94ff7b596bc50a8d51ca` |
| D07 | \[...\] | 126–130 | `072e9ac9b8ceaa4fb6b9b90afe21560248f5358f82baa1a5aeab03042988fbbc` |
| D08 | \[...\] | 135–137 | `0abc892fdd578a5c932366c9d98a798919c14470319706320133d0af7799c813` |
| D09 | \[...\] | 167–170 | `aca3def9b074d371d85a50dd4d10251ca0f7f881c3e07b76c787ed3818121d9f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 38: `interface remain conditional and open; no arithmetic $L^2$ advance or twin-prime`
- TeX line 43: `\texttt{CONDITIONAL\_THEOREM / FULL\_GATE\_B\_OPEN}.`
- TeX line 88: `Assume \eqref{eq:interface}.  Define`
- TeX line 117: `The theorem is an exact compiler implication, not an estimate of $A_x$ or`
- TeX line 159: `all rejected.  These are finite arithmetic checks; they do not certify the`
- TeX line 172: `the threshold cannot pass.  The next open theorem is to establish the two`
- TeX line 173: `conditional inputs on one literal prime shell, while retaining the finite-window,`
- TeX line 177: `\texttt{TPC223\_ARITHMETIC\_ADVANCE=NO; L2=NONE; FULL\_GATE\_B=OPEN.}`
- TeX line 183: `certificate.  It does not close a mathematical gate: the AP dispersion,`
- TeX line 185: `open inputs.  The result therefore belongs to`
- TeX line 196: `interface is exact but its literal arithmetic realization is open.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:interface` → `main.tex#L68` (existing project target or original TeX label line).
- Link relocation: `#eq:interface` → `main.tex#L68` (existing project target or original TeX label line).
