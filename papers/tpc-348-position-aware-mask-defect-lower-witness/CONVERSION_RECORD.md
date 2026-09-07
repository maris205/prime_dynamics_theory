# TPC-348 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `1de1964aa411aa631587da690524beadf1127d3c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `20cc2fb200e48a98dbf01b3bdb66818eb33333f3a7b5c35b5da67bb257251a75`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `232662c33a62f8c6501952d675e588ff044a2eb3273698e5ba19d464b906524b`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `41d12937565a55f8f20e7d51ef7b57699409abe71ee16bd2a8fb81d12093a137`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `972f06ed1d252260098b91f49e3a7bef3f5eb7aa168d5434fda4af761bd22d26`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC345_349.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `The literal object` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Exact position formula and lower witness` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Frozen audit protocol` | 143 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 164 | 3 | `HEADING_TEXT_MATCH` |
| `Exact rational anchor` | 198 | 3 | `HEADING_TEXT_MATCH` |
| `Adversarial checks and claim boundary` | 211 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 238 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 250 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `72` before writing and `72` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2d0a8518dba0f21e8ad5f5089cda1a0974801a9172f5671377866a215e40292e`.
- Source theorem/proof environment starts: theorem at TeX line 116, proof at TeX line 126, remark at TeX line 136.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 36–39 | `e5799e4001e77c1aaf64e9fa59840dd52ad3853008a70db553d297d56348eadd` |
| D02 | \[...\] | 68–70 | `558e315b25511c3d2ba1617edd2add2511b4e94fe6a75f7081ba7b3d11873922` |
| D03 | align* | 74–78 | `d01df2cfde099d496bf364628363cc01be5b8181b2b3272ddaace9bf616ba56e` |
| D04 | equation | 84–87 | `c0057c308ae33430892b38cda5882b39d7ac41dbc8d0d98db9ce4a830f749e8f` |
| D05 | equation | 89–93 | `a0fa2a800e7e974e8d446c30e9b86ada09ef648b0fa2639608b85b0014255a95` |
| D06 | equation | 101–105 | `417afe6ce55f595e469738b68c100c196c3358e2c1b4c4d1db2a306418c2f5ef` |
| D07 | \[...\] | 110–114 | `82342b4fbc2840381652d29c44be6fab9921ed04b89a6f94a659e0eed90cabfc` |
| D08 | equation | 118–121 | `03941520ef906ec62b3fa92bb37beac6d12ff7ac86ebc3a31b321a862ac32f66` |
| D09 | \[...\] | 129–131 | `bc7e86f7874a42a3479fac1c5f74c1352f52ce587df3040a3a0db23a307842eb` |
| D10 | \[...\] | 147–150 | `8f4f4e448a859b21bc890f9171db81fe1d793796783681a8f233e1a9c71c2496` |
| D11 | \[...\] | 203–207 | `38a4f8255059d7735d182526a6698e25096a0b92dad6405faee1ee005bd8c588` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 35: `finite-dimensional lower bound`
- TeX line 40: `This witness uses only declared mask-hit positions and does not fit a leading`
- TeX line 44: `norm.  These are finite observations, not growing lower bounds.  The result`
- TeX line 46: `the source-uniform arithmetic $L^2$ problem open.`
- TeX line 51: `The twin-prime route currently contains a literal finite prime-shell operator`
- TeX line 54: `hide a sizeable finite defect.  The present paper asks a narrower question:`
- TeX line 58: `Our answer is yes in a precise finite sense.  The main theorem is elementary`
- TeX line 62: `a source-uniform arithmetic theorem, or a proof of the twin-prime conjecture.`
- TeX line 117: `For every finite matrix $D_I$ and every nonempty $J_I$,`
- TeX line 123: `without any positivity, symmetry, or cancellation assumption.`
- TeX line 137: `The selector is not an eigenvector optimization: $J_I$ is fixed by the`
- TeX line 159: `shell accumulation order and does not import the producer.  It recomputes all`
- TeX line 164: `\section{Finite results}`
- TeX line 168: `operator.  The ratios are reported only to describe the finite panel.`
- TeX line 177: `Quantity & Certified finite readout\\`
- TeX line 223: `finite identities;`
- TeX line 228: `\item mask deletion is refuted only as a uniformly negligible operation on`
- TeX line 229: `that finite panel.`
- TeX line 232: `We do \emph{not} claim a source-uniform arithmetic $L^2$ estimate, a uniform`
- TeX line 240: `TPC-348 turns the mask-defect observation into a reusable finite interface:`
- TeX line 243: `cannot be dismissed by an unstructured finite remainder argument on the`
- TeX line 247: `arithmetic $L^2$ gate remains open.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:defect` → `main.tex#L86` (existing project target or original TeX label line).
- Link relocation: `#eq:global-defect` → `main.tex#L92` (existing project target or original TeX label line).
- Link relocation: `#eq:witness` → `main.tex#L120` (existing project target or original TeX label line).
- Link relocation: `#eq:column-formula` → `main.tex#L104` (existing project target or original TeX label line).
- Link relocation: `#tab:summary` → `main.tex#L174` (existing project target or original TeX label line).
