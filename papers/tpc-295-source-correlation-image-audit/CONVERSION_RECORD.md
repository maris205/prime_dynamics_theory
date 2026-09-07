# TPC-295 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `aa6a797b49ed462881998abf696440d164a0f74c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2c5700f589913ee1ba166b976c4996c310c20e82cfe231fc1af9c247c30b1e82`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `64070066ebb5512436d32b322d8f21123a47c77ba7602c90b978244deab0c52d`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `821396d1b379289905623bf128924a5931f38a2dca7106f49757a2f5e53afc1c`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `affb0304eca86c224d4408adaaaef6d470c5d0042d681718891a73a8f7c5c768`.
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
| `Position on the route` | 47 | 1 | `HEADING_TEXT_MATCH` |
| `Finite physical shell and source map` | 67 | 1 | `HEADING_TEXT_MATCH` |
| `Exact image theorem` | 101 | 2 | `HEADING_TEXT_MATCH` |
| `Modular rank certificate` | 140 | 2 | `HEADING_TEXT_MATCH` |
| `Inherited finite atlas` | 168 | 2 | `HEADING_TEXT_MATCH` |
| `What this does and does not close` | 242 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and conclusion` | 273 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 300 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `79` before writing and `79` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ed8f75b5f26a6d8caa4b539e04ab5d70ab3a910d357e48999161ea1c4f57c4b2`.
- Source theorem/proof environment starts: theorem at TeX line 105, proof at TeX line 115, proposition at TeX line 123, proof at TeX line 128, lemma at TeX line 146, proof at TeX line 151.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 71–75 | `a1a3b131961932f06b381198ae8b88ec7b1c24e7cb895633655cde5c4ef491bd` |
| D02 | \[...\] | 78–83 | `b062aae7cce741cd70c74e8f3c832130beff5a7941798945d37705016f9c29e5` |
| D03 | \[...\] | 85–89 | `30edc1903e8642ab7ea93a907acd2024fb0b34887d31a5b7d03b325946260fc5` |
| D04 | \[...\] | 92–96 | `15065821c725cfc4bbfd0dfcd0acb7f76f16dfa26e138f66454e0604b81634a1` |
| D05 | \[...\] | 109–112 | `567d5a76adadfd432a85e49937ecadecd61f4482947c8ab7942ff42295c921ab` |
| D06 | \[...\] | 117–119 | `ca1ccff2a6a8c95c740cbedcaf064214b78f2e03c521d36c5e7151341597f230` |
| D07 | \[...\] | 159–161 | `b1b3fa35a93465890372780f386bdd5d256568b097d11ae2a88e4d330f8433b5` |
| D08 | \[...\] | 232–236 | `875df628278ecb961ecb9ca2fde6efbd65dabc91b83fbe7add3e635f428656c2` |
| D09 | \[...\] | 267–270 | `dd4b34569af435f4b01668de4447b5e110ecb12bc93c1b70ed61ec56238e5907` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `\title{Source-Correlation Image and Finite Signed Feasibility\\`
- TeX line 33: `isolates that finite linear-algebra question.  Let the physical shell`
- TeX line 41: `has an exact witness in the declared unrestricted finite rational source`
- TeX line 42: `space.  This closes only the broad finite image question: admissibility in`
- TeX line 44: `$L^2$, and the twin-prime endpoint remain open.`
- TeX line 61: `perturbation?  The present paper answers the finite question for an`
- TeX line 67: `\section{Finite physical shell and source map}`
- TeX line 84: `For a finite shell $S=\{q:Q<q\le 2Q\}$, set`
- TeX line 97: `The source space in this release is the full finite rational coordinate`
- TeX line 105: `\begin{theorem}[Full Gram rank gives a full finite source image]`
- TeX line 136: `attainability does not imply that the least source cost is small enough for`
- TeX line 142: `All entries in \eqref{eq:physical} are rational on the declared finite grid.`
- TeX line 168: `\section{Inherited finite atlas}`
- TeX line 172: `The resulting finite image statement is summarized in`
- TeX line 178: `\caption{Finite source-image audit inherited from TPC-294.}`
- TeX line 242: `\section{What this does and does not close}`
- TeX line 244: `The finite atlas closes a genuine branch of the map: an ambient signed`
- TeX line 245: `target cannot be rejected merely because the finite linear correlation map`
- TeX line 247: `weighted directions are now known to possess explicit finite source`
- TeX line 263: `The first issue is an image-of-a-profile problem, not a rank problem.  The`
- TeX line 268: `\texttt{PROVED\_EXACT\_FINITE}\quad+\quad`
- TeX line 269: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE},`
- TeX line 284: `finite record is`
- TeX line 290: `checker as the available fail-closed evidence; it does not declare an`

## Conversion limitations

- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:physical` → `main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#tab:headline` → `main.tex#L179` (existing project target or original TeX label line).
- Link relocation: `#tab:rows` → `main.tex#L205` (existing project target or original TeX label line).
