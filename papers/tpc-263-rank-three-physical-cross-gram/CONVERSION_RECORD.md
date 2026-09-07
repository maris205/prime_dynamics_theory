# TPC-263 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `d5e4403dd84d5a428364e125f1ba0b655a091f2c539900d4e4b786f2fac79709`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `fd3c482f7764c946f04b5c4707b3716a2300d36874572f5ab2874744bead7361`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `bd44b3d1dcf7ced1da7739d01649e1118897241c48c957f3466de74ce1de7a7e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC260_264.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `The source-only rank-three frame` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `Three hybrid moments` | 89 | 2 | `HEADING_TEXT_MATCH` |
| `Exact physical channel split` | 106 | 2 | `HEADING_TEXT_MATCH` |
| `What the theorem does not pay` | 149 | 3 | `HEADING_TEXT_MATCH` |
| `Finite certificate and route evaluation` | 168 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 197 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 212 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `54` before writing and `54` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b6dfc72997ba6dff3b6b4e6abd5def93f7862864f4afd0d5dfc764305c0bcf9f`.
- Source theorem/proof environment starts: lemma at TeX line 69, proof at TeX line 77, theorem at TeX line 122, proof at TeX line 128.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–40 | `63ca0e94a744966584303437c27d0a9ded11088ee4c55b2bb52a93fb38103c58` |
| D02 | equation* | 47–50 | `89b3ce9054945c425d335ce4dd240d30f7e30c407ac37c3d22228bed1280ab2f` |
| D03 | \[...\] | 60–62 | `9630d848010632fa0c40738b5bd50f78bcaea0ca8aa711a11cabe654c992d32a` |
| D04 | \[...\] | 64–67 | `26e1ac73381275d0ea26c88097c5ba20016cb3c1c7a199ae62804658cdd67104` |
| D05 | \[...\] | 72–74 | `632b9b8c3539c205b61fd10b8cca142371e449b01ddba59eb808800aa5c94eac` |
| D06 | \[...\] | 81–83 | `3f07d04d21b152707565fcb5af06f40a3a38b18d2a251c62a3affd2ba8c2c9ed` |
| D07 | \[...\] | 93–95 | `9a976c511fa2f440d085e3d05f679c3a08a1dc5b0d638073c741b93beb836034` |
| D08 | equation | 98–101 | `e677a4e83fb7b11bcb4bd0c975a7537d0f90525d581d7cb2f37f36920fdd3dba` |
| D09 | equation | 108–111 | `349e4cf4810c0e4c924e5397fbf61780aa89a35a3351ddc27ce3cbeb3dfc91bb` |
| D10 | equation | 114–117 | `ef5acfcb55fd99cc9c600db7a87ecca6be5ccfca0bbaed3e4ccf48143d6a29a5` |
| D11 | \[...\] | 124–126 | `184ef5174c40c9c6198ac4172c07c4ababf581611b7efdf1d513de1b3aa9b10a` |
| D12 | \[...\] | 130–133 | `78a9e998a6eaa862dd86ed5e7c9a73b3ce6faaf9777b5ddd502e27a329eaa7b7` |
| D13 | \[...\] | 135–139 | `c436865d8ffdb435866f1f2d5029ef91aa8f0e2c083038155d7da23be370259b` |
| D14 | \[...\] | 142–144 | `72e49a27dad5058a871f3079b94d2c0d79f7b876aed3cfdd34bafa1d277e4a59` |
| D15 | \[...\] | 151–153 | `9361bea11135fd2c949a7111a6d9fa5cd45c079ddac3001bce23a6aa9cc1504f` |
| D16 | \[...\] | 161–164 | `3058a9531c84ff128aebbe6483abda208d88a0310a38db20497c65ae7433045c` |
| D17 | \[...\] | 172–175 | `f686d726473170e172608d236b52f228922f5d8061acedfdccbec9611e697fe4` |
| D18 | \[...\] | 201–207 | `5c00e19ab3f73a7d0fa30a81cac1a6abad84232412e438b0fe2f52f92e77b7de` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 29: `channel advance, with zero fixed-power credit; it is not a full \(L^2\) bound,`
- TeX line 44: `full coupling by a finite diagonal surrogate.`
- TeX line 53: `claimed uniform in either parameter.`
- TeX line 145: `and the logarithmic orders add to \(M+3\).  The finitely many \(o(1)\) factors`
- TeX line 149: `\section{What the theorem does not pay}`
- TeX line 154: `TPC-263 supplies no estimate for it.  This is not a cosmetic qualification:`
- TeX line 155: `TPC-260 showed that finite packet marginals and a finite list of null/Haar`
- TeX line 168: `\section{Finite certificate and route evaluation}`
- TeX line 190: `Orthogonal residual & open\\`
- TeX line 192: `Arithmetic \(L^2\), Gate B, twin primes & none / open\\`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:w` → `main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:w` → `main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:channel` → `main.tex#L116` (existing project target or original TeX label line).
- Link relocation: `#eq:split` → `main.tex#L110` (existing project target or original TeX label line).
