# TPC-273 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `13a27783522489bc584c4733a361d58811a75d350b22dda9ddf6f8d02c09d62a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `32576350e0e9e38f4cc0a32ccc385d6fec8f0b6b3a9f6a9b4a5a48001cd848b2`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8e6a2dce2891fb630cf30bd6bca1046138b9e764a73cf51c67e62dd90ded9736`.
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
| `Question and claim ceiling` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen finite object` | 59 | 1 | `HEADING_TEXT_MATCH` |
| `The 32-row matrix` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Phase census and kernel control` | 156 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and limits` | 185 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 205 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 214 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `54` before writing and `54` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `208cac97ffa1b9d9b856a00edb446afe37f663f3247e4f0b5390994ceb08fe4c`.
- Source theorem/proof environment starts: lemma at TeX line 80, proof at TeX line 87, theorem at TeX line 132, proof at TeX line 141, theorem at TeX line 171, proof at TeX line 177.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 51–54 | `715c3e1cf638bbcf1b8d74ed8005eaa08aced1d507b94f7269c6422df3debf94` |
| D02 | \[...\] | 65–67 | `5f2f65e0416d707d6e1d35fce2ebed9408c12c737656402880db41c5d00ba452` |
| D03 | \[...\] | 74–76 | `df8165e46d13a14a0af229655ec0050dc559bd9b938783ee5614cf65a31533e6` |
| D04 | \[...\] | 82–84 | `5481e47c7befe6daa63b62d2a12cb711e4ac7212704b95e8cadba58ab0abea38` |
| D05 | \[...\] | 99–102 | `5515721e44d7ec5230e96a231410f179ea556f2d510bb5096667ceef1708ab99` |
| D06 | \[...\] | 105–110 | `97940689d2ff84afdfce1fc7749791537dd1620f609a7e018a720abfe7c663b3` |
| D07 | \[...\] | 161–163 | `609a1d89da95796cd300496236f9fe8f65e044ca5ee2c8d43f7cf017bfe0e348` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 16: `\title{A Finite Margin-Stability Matrix for the Literal V59 Residual}`
- TeX line 28: `We now test whether that margin is stable under the declared finite cutoff,`
- TeX line 36: `is a certified finite stability obstruction for the declared interface, not`
- TeX line 45: `\(\sigma-\eta\) endpoint budget.  A finite phase label is not such a lower`
- TeX line 52: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE},\qquad`
- TeX line 56: `does not represent a proved growing sequence.  Fixed-power credit,`
- TeX line 59: `\section{Frozen finite object}`
- TeX line 61: `For each \(N\) we use the same finite literal operator as the parent`
- TeX line 63: `masks, deleted diagonal, exact finite beta, and the four consecutive equal`
- TeX line 70: `synthetic random vector.`
- TeX line 132: `\begin{theorem}[finite margin-stability obstruction]`
- TeX line 137: `separated by its stored outward intervals.  Therefore uniform margin`
- TeX line 138: `stability for this declared finite parameter family is \texttt{REFUTED\_SCOPED}.`
- TeX line 148: `declared cutoff changes in each comparison, the asserted finite instability`
- TeX line 153: `\(0.969\), respectively.  They are finite transition diagnostics, not`
- TeX line 171: `\begin{theorem}[finite phase census]`
- TeX line 173: `positive-real, and 0 zero-crossing intervals.  This census does not imply an`
- TeX line 174: `eventual phase sector and does not imply a positive margin lower bound.`
- TeX line 189: `does not claim that the finite cutoff values are the source-level growing`
- TeX line 190: `rule, nor that a finite crossing supplies an asymptotic subsequence.  In`
- TeX line 201: `The next legitimate source-level question is uniformity on the registered`
- TeX line 203: `the actual source family rather than inferred from this finite matrix.`
- TeX line 207: `TPC-273 supplies a hostile finite test of the new TPC-272 margin coordinate.`
- TeX line 208: `The same literal finite operator exhibits both low and high correlation bands`
- TeX line 210: `result is a useful obstruction to treating a declared finite interface as`
- TeX line 212: `strict \(1/400\) payment, arithmetic \(L^2\), and the twin-prime problem open.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
