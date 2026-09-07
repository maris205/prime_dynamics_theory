# TPC-278 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `72d57e5e22fbbc319c79c41dfed3725614dbf043d4a9146d779d1d6bf7eebaa3`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `b6fb674a8326a21e3df3486bfb552b73f8412c8f6d0c9e0ed6f42086929440e1`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ed8b56de7de3550e770f75b536f2fd2c6e2512742eae8bba07e5e945571ff504`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC275_279.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and frozen source` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Exact sign/gain relation` | 52 | 1 | `HEADING_TEXT_MATCH` |
| `The twelve-row audit` | 71 | 2 | `HEADING_TEXT_MATCH` |
| `What the obstruction says about the route` | 129 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and route evaluation` | 144 | 2 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 162 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `37` before writing and `37` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `98aebccea1ce07528424820887a956884233edf05ed728c4fa1529f7164ecb37`.
- Source theorem/proof environment starts: proposition at TeX line 54, proof at TeX line 62, theorem at TeX line 104, proof at TeX line 117.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–41 | `c6006e70d7f6856a92efea85b143940c4d07cefdc696dd8946d4e667ecf04bfe` |
| D02 | \[...\] | 56–59 | `591f68cc74545092f553698044be259a3d6da9ef165635721af67b6a6b831797` |
| D03 | \[...\] | 107–114 | `d1e24e623be6ddd329a9535d3ce3bdb60c88ed90e0eba14b3b02a2b1d1c61e9d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 31: `finite statement $D/G\geq1$ is not stable on this declared interface.  The`
- TeX line 32: `result is a scoped obstruction, not an asymptotic counterexample.`
- TeX line 42: `Then $G=D+2E$.  TPC-277 found $E<0$ on a natural finite scan, which is`
- TeX line 100: `\caption{Exact finite source replay at $s=2$.  Displayed decimals are not`
- TeX line 104: `\begin{theorem}[finite shell/clock instability]`
- TeX line 126: `This is a direct finite attack on interface stability, not a claim that the`
- TeX line 127: `same perturbations occur infinitely often in the intended growing schedule.`
- TeX line 133: `identify the natural shell/clock choice with nearby finite choices: the sign`
- TeX line 139: `The finite flips do not refute the natural growing sequence, and the natural`
- TeX line 140: `three controls do not prove its uniform stability.  Accordingly the release`
- TeX line 141: `assigns zero fixed-power credit and makes no arithmetic $L^2$ or twin-prime`
- TeX line 154: `\texttt{ROUTE-A} & not applicable to this finite stability audit\\`
- TeX line 157: `\texttt{ARITHMETIC-L2 / FULL-GATE-B} & open\\`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
