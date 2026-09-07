# TPC-296 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `aa6a797b49ed462881998abf696440d164a0f74c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9bbe206d8640d4bab034b7a443d33b04c8f0f2496a242a5fd83fefe60e319fa4`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `944f1434091ae3b3bce33737626b6367a33da9ab1c5b150650612fee734da5f4`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `140c7de888dcb510a3c08ce999985715408efaa4951e139e50c039a89da20416`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `558ba83745c64b7148c4be2f401984933325a6d833b444b7c553e5fbe6ecc69b`.
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
| `Physical shell and source correlation` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `Exact source-budget theorem` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `A declared native-ray diagnostic` | 143 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol` | 169 | 2 | `HEADING_TEXT_MATCH` |
| `Cost and profile atlas` | 193 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and route boundary` | 256 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and conclusion` | 284 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 307 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `85` before writing and `85` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `aea45091553b158a39d431dc44076524d95cac81ef75f88d90994c86bc874f1f`.
- Source theorem/proof environment starts: theorem at TeX line 93, proof at TeX line 107, proposition at TeX line 120, proof at TeX line 133, proposition at TeX line 153, proof at TeX line 164.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 65–69 | `a1a3b131961932f06b381198ae8b88ec7b1c24e7cb895633655cde5c4ef491bd` |
| D02 | \[...\] | 72–76 | `2d3078a47396587dee9721a610ed5fca742aa092e53b34140c7433b51b196f65` |
| D03 | \[...\] | 78–82 | `5f5b31b57dd29f685868368ef5ed0f9088b7ad455b684a0083ca79a533e7a016` |
| D04 | \[...\] | 84–87 | `a81be974a617b405927c42f432dabc5dfcf03460d9bf50a4f6f28ed3ac598a7c` |
| D05 | \[...\] | 97–101 | `62f320db493b77bc43fd5f0ada8d08346670cfe7ad596e43a07a9fe121946044` |
| D06 | \[...\] | 112–114 | `91bb1d1346e87cd1f40abc40a30016ecdddefb71d8a3e1da0d109df641cfe72f` |
| D07 | \[...\] | 122–124 | `6984a619747d095bc544b74a49d75b53922f3997c38eb328f420a88557cc947b` |
| D08 | \[...\] | 126–129 | `ce8dda41f97f6a447a70f3e8e9e6da7b00bf738ec56cf7b30ac82d3bd37ad012` |
| D09 | \[...\] | 146–148 | `2ebc010a32c0d523e904b894a8b9d69fd3bf574a6ad4e26ed80b3fdca27e77e2` |
| D10 | \[...\] | 155–159 | `fd14526752491e2667ba4d468987962ebd48060133fdd476b0487552c06eca02` |
| D11 | \[...\] | 186–190 | `d937134c039ab5fc8dda9c720426e567797fc526ad7ccc0c0ce9f43572154a74` |
| D12 | \[...\] | 276–280 | `4912b7ff3faf717b95e568dfd12715a494d9534056d37eb087049c6943a3e32d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 30: `TPC-295 proved that the unrestricted finite source-correlation map attached`
- TeX line 31: `to a physical prime shell is onto, but existence alone does not measure its`
- TeX line 41: `weighted targets.  The finite evidence therefore moves the obstruction from`
- TeX line 52: `then proved that these ambient targets have finite rational source`
- TeX line 58: `declared one-dimensional proxy, so that a finite obstruction is not`
- TeX line 88: `The finite source domain in this paper is the full rational coordinate space;`
- TeX line 141: `target.  It is exact linear algebra, not an arithmetic estimate.`
- TeX line 151: `the proxy does not say that a richer source family fails.`
- TeX line 169: `\section{Finite protocol}`
- TeX line 180: `column source-first and does not import the producer.  It checks the source`
- TeX line 191: `They are finite modeling choices and carry no exponent credit.`
- TeX line 200: `\caption{Finite source-budget and one-ray audit.}`
- TeX line 223: `uniformly for the weighted targets.  The largest observed Gram condition`
- TeX line 251: `ratio reaches the finite maximum $0.0005840565446\ldots$, but the ray RMS`
- TeX line 259: `unrestricted least-norm witness on this finite grid.  This is a useful`
- TeX line 269: `calculation does not determine its dimension or image.  The source-control`
- TeX line 272: `boundary, not cutoff-uniform arithmetic evidence.  Finally, a finite`
- TeX line 273: `condition-number range is not a growing-shell bound.`
- TeX line 277: `\texttt{PROVED\_EXACT\_FINITE}\quad+\quad`
- TeX line 278: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}\quad+\quad`
- TeX line 282: `profile theorem, Gate B, and the twin-prime endpoint remain open.`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:headline` → `main.tex#L201` (existing project target or original TeX label line).
