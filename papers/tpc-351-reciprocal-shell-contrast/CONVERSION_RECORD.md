# TPC-351 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `688fe9fc74c13468588f93f62bac977ff65e68b79aa9cae5da98a43cbe1a7406`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `5f26d6b55a09fcefc12e05c45ee38efb1ba736f05fb7bc933d45006bf3fd3644`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e3bea76f9b80552fbfdc8728e4c679602275ad1015d3850539e77d528eefddc6`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `Literal masked defect` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Reciprocal-shell incidence interface` | 79 | 2 | `HEADING_TEXT_MATCH` |
| `Frozen paired protocol` | 132 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 152 | 2 | `HEADING_TEXT_MATCH` |
| `Exact reciprocal anchor` | 202 | 3 | `HEADING_TEXT_MATCH` |
| `Adversarial validation and claim boundary` | 219 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 234 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 244 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `63` before writing and `63` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `81935c9da5a954c2ccc08f239f4b0e4377a3a3fd481a08e29f107eecf3c1f879`.
- Source theorem/proof environment starts: proposition at TeX line 92, proof at TeX line 96, proposition at TeX line 101, proof at TeX line 109, theorem at TeX line 114, proof at TeX line 121, remark at TeX line 126.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | align* | 66–70 | `94d3c3fbd40844a8caf011a9570c738d1afd3a6554b2bd383004f6a417d4acaf` |
| D02 | \[...\] | 73–77 | `51fc783d285911aa67ba58d0d7b8538f6be76ba4e662b074a9df06a5bd3ef799` |
| D03 | equation | 82–85 | `b93145de1b5cb0bdb6632ce2c61db047fcd3b6dc56927671307923a2150e8b45` |
| D04 | \[...\] | 87–89 | `b93422b403094397c2692cdd68d0f27352a8751acde48dbd566e838d428be989` |
| D05 | equation | 103–107 | `3f047c32b0dcbc88d214c5fc0ea3f8f6e9a77b40e22ceefb467f3f4f401c5768` |
| D06 | equation | 116–119 | `89c9c57bd5628f5829e1ca54ffffff0aebf36eadf9591bd0af130a9c1747f859` |
| D07 | \[...\] | 135–139 | `acc5741e0ba6d29a9695a53cc87ff68f290941ced62bc1878f532f113839359b` |
| D08 | \[...\] | 206–209 | `45593ab22c173109e258e16561a735aa88d87276eb5d26cc961c090257e1de91` |
| D09 | \[...\] | 211–215 | `921d974c050d061fb7f26029aa84be351135bf4c951d55fcc1a88a553215e240` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `Finite Scale Repair for Prime-Incidence Defect Witnesses}`
- TeX line 30: `incidences has a positive finite response but a low floor on large prime`
- TeX line 42: `one quarter.  Thus the reciprocal rule gives a genuine finite scale repair,`
- TeX line 43: `not a uniform floor, arithmetic $L^2$ estimate, or twin-prime result.`
- TeX line 49: `finite interval lengths, yet its $Q=256$ block had no row reaching one half of`
- TeX line 57: `finite.  They do not imply a limit as $M$ or $Q$ grows, a source-uniform`
- TeX line 72: `coefficients.  The finite matrix entry is`
- TeX line 102: `For every finite matrix $D_I$,`
- TeX line 110: `Apply linearity to the finite sum defining $c_I$ and expand the Euclidean`
- TeX line 127: `Equations \eqref{eq:gamma}--\eqref{eq:lower} are exact finite algebra.  They`
- TeX line 152: `\section{Finite results}`
- TeX line 157: `\caption{TPC-351 paired finite audit.}`
- TeX line 161: `Quantity & Certified finite readout\\`
- TeX line 195: `The $Q=256$ block is a real finite repair: its minimum increases from`
- TeX line 197: `of zero.  It is not a universal repair, because eight high-shell rows lose to`
- TeX line 228: `These checks establish finite package integrity only.  No source-uniform`
- TeX line 229: `arithmetic $L^2$ estimate, uniform masked-operator theorem, fixed-power saving,`
- TeX line 240: `and shell scales.  If the repair does not transfer, the finite incidence branch`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:gamma` → `main.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#eq:gamma` → `main.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#eq:lower` → `main.tex#L118` (existing project target or original TeX label line).
