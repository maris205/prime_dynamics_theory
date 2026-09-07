# TPC-327 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `4f178335dce229a5ded67fe9851407eb5c150e4d6d60d52f32da0681f993925e`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `3a20d08be08fe0d70a6439d2d7fda7639f8dcad2bbda07fd76a482d59a789373`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d135fed4497fbaee75be2930e9cc028ea8cb0f5b0e0e728e59873f22271458a1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC325_329.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and frozen object` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Triangulation protocol` | 67 | 1 | `HEADING_TEXT_MATCH` |
| `Finite results` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limitations` | 154 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 173 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 190 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `44` before writing and `44` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e0ab77ea234562fbbbe2d27b5965eae160bcbece5d4fdea9a4f52d624d2da0a0`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–41 | `1b1f37136300e91417915e943d5bf9342b6ac9e821d9a8ac5ddcc6b371a2d6c9` |
| D02 | equation | 43–47 | `7675b8c74671a6c7da8b4aa087e0dd55512a4f735a6ddeff8c4ef23776c07987` |
| D03 | \[...\] | 49–53 | `ec93802632bcc58f2bcb02703e4ae7f4a148f96cb01ea39439b9919f5e74210a` |
| D04 | \[...\] | 58–62 | `b27e9ebbddad4f9dffd2c352d4dc1a4eb588a9542a32fc47b64a3729b4bc4a7a` |
| D05 | \[...\] | 70–73 | `5cea9cb28014fd62e4b5c33684140f09e95474303784965067231d63370af577` |
| D06 | \[...\] | 77–80 | `7bf0c3cb0bedd164e94b022c747f63c84cbc6c5154880ea97396cfa583e971f0` |
| D07 | \[...\] | 109–117 | `46a5dcaca7ec09265c7bdf67722494314f362e679fb2bb5e3fd47f2e21836310` |
| D08 | \[...\] | 145–147 | `281dd3c7ae5695f7d477f4ffe7958052f37e4322c36151687a8db119273d7729` |
| D09 | \[...\] | 148–150 | `ac0f5f002e25eb8ba6d6c3a34fa97e6774221a9ae1fa1afd225ac2cd3e2e5c19` |
| D10 | \[...\] | 157–159 | `9bb2cc1309062fa7930466577c67bdb982a0d1d0425e23f5b19553b58ffbf4a9` |
| D11 | \[...\] | 164–168 | `408ee08c5572ba79f7bb0fc9228f12dab6c865c41d209d57ee495534c3eb07c0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{Three-Origin Triangulation of a Finite Prime--Shell Spectral Ladder}`
- TeX line 17: `Finite spectral experiments can be tied to one residue environment even when`
- TeX line 28: `finite triangulation evidence only: it does not prove a source-uniform limit,`
- TeX line 34: `TPC--325 and TPC--326 used the same finite prime-shell operator at origins`
- TeX line 36: `finite readout survives a third residue environment and whether the agreement`
- TeX line 63: `Finite Gram positivity and trace normalization give the basic spectral typing`
- TeX line 87: `\section{Finite results}`
- TeX line 141: `range is positive.  Thus the result is a finite three-point triangulation,`
- TeX line 142: `not a copied equality.  At the exact rational anchor $[20001,20016]$ with`
- TeX line 158: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_THREE\_ORIGIN\_SCALE\_TRIANGULATION}.`
- TeX line 160: `The third origin does not falsify the earlier finite profile readout, and the`
- TeX line 161: `pooled ranges quantify its finite source sensitivity.  It does not establish`
- TeX line 162: `uniformity over source origins or over a growing scale ladder.  In particular,`
- TeX line 167: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 171: `not an official evaluator pass.  No twin-prime conclusion is asserted.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
