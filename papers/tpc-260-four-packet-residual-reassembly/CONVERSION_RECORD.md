# TPC-260 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9cf4bbca7c15ceef4df54d5fbb6b48cae1715545c7260907c70cb6f49c5cf4e1`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `45e0d850c52aab0999b95a46ddff4d0c2dd32cd583d529d2cf06c4b16c50262b`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `4c66ec84f98b124c177dbed25adae65b56427dd8623a5797938a180c05bba2c1`.
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
| `Scope and motivation` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `The four-block interface` | 89 | 2 | `HEADING_TEXT_MATCH` |
| `A sharp null-compatible completion theorem` | 132 | 2 | `HEADING_TEXT_MATCH` |
| `The missing DFT mode` | 193 | 3 | `HEADING_TEXT_MATCH` |
| `Finite audit and route consequence` | 245 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 307 | 5 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 324 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `55` before writing and `55` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1eb31cbf54f84163b2a5aeb3a5b2dadd69299b27ac2e31d141f56b5b3085ab2d`.
- Source theorem/proof environment starts: theorem at TeX line 139, proof at TeX line 161, corollary at TeX line 176, proof at TeX line 182, theorem at TeX line 203, proof at TeX line 214.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 55–62 | `e68a0ef670ac2be32dada2c203718c5a65b3021561fd1a9c109090594d300f5d` |
| D02 | \[...\] | 94–96 | `34826024aa2059c3a83619048b08ef3f795f2bcf71a4e2202e3e6290c0655991` |
| D03 | align* | 99–106 | `bd8fd34cc00a9540c3cebc57a3b3b6cf32ba561fa66c73db3e247f502f52c40e` |
| D04 | equation | 108–112 | `cc1a373f1110210fc8476ba002a8c2f497838aaee34b42198962309781253886` |
| D05 | equation | 116–121 | `c3f06a78e784fa81f89e5f36b1a8d8673f01b8ce6d848a2e49fa89a36f6c0e7a` |
| D06 | \[...\] | 141–144 | `a77b9202597269add56a61899f89beec1edf77d9d49e545952c115f26521beef` |
| D07 | \[...\] | 146–148 | `2919d622b5f908fce3390f3b50eeb42933cd8c6079995a1c0c8b05a8f26f834b` |
| D08 | \[...\] | 150–152 | `dd1f4cf526d411c9685d708da68fa099dfc2acfc50f37f5bd0476bbb18aaae01` |
| D09 | equation | 154–157 | `77b8ac48d5ed140a594b19f93be2326e24933aa674f3f9a09e55258501d44550` |
| D10 | equation | 197–201 | `364b6e2f40a159b8098900b733b22c8fb58a454c222d447caf1a4e3a255540d6` |
| D11 | align | 205–209 | `63aaebeba8b40d3b278c37c3d6a28b804c0e9cf5882b463e8c9edf58de3c5796` |
| D12 | align* | 221–224 | `ba044311efe10abc25435e41ff234647d6eeccea1d50987ee80f5d47805b3849` |
| D13 | \[...\] | 227–231 | `39a95ee04a5ad37762fc06c9f3b48386ec65ae72745ba3bbcd9789d691b19f8f` |
| D14 | equation | 237–241 | `bc4dedfc2a648d6d530c9f6179d4352538173bb85c04ab39f359f1a7bcbdcc67` |
| D15 | \[...\] | 298–302 | `91dac0e7f7da01f0fc49f38f31abf39002c582ee046ba26f9a4db243b109a0ce` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 35: `the signed V59 coupling, but leaves an orthogonal residual.  We give an exact finite`
- TeX line 43: `$0$.  The result is a structural obstruction, not a prime-shell counterexample.`
- TeX line 65: `question: can the residual be recovered from packet norms and the finite Haar`
- TeX line 68: `The answer is no at the level of finite Hilbert-space algebra.  The obstruction is`
- TeX line 69: `useful because it does not merely repeat a generic Gram example.  It keeps the`
- TeX line 83: `refutes uniform promotion from these marginals to full reassembly.`
- TeX line 86: `All statements below are finite and structural.  In particular, no finite record`
- TeX line 123: `zero weighted sums in \eqref{eq:haar}; it does not use numerical values for the`
- TeX line 127: `general packet Gram matrix is positive semidefinite and that diagonal/trace data`
- TeX line 189: `the same finite Haar geometry used to select the null direction supplies a concrete`
- TeX line 245: `\section{Finite audit and route consequence}`
- TeX line 255: `\caption{Finite exact audit counts.  These are reproducibility checks, not`
- TeX line 276: `promotion of a finite witness to a prime theorem; they do not estimate the literal`
- TeX line 285: `Haar complement and polygon completion & PROVED\_EXACT\_FINITE\\`
- TeX line 289: `Arithmetic $L^2$ and full Gate B & NONE / OPEN\\`
- TeX line 304: `diagonal, unit masks, and both boundary lanes.  The finite completion result gives`
- TeX line 317: `in the growing prime shell, and it pays no arithmetic $L^2$ or endpoint credit.  Its`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:haar` → `main.tex#L111` (existing project target or original TeX label line).
- Link relocation: `#eq:polygon` → `main.tex#L156` (existing project target or original TeX label line).
- Link relocation: `#eq:haar` → `main.tex#L111` (existing project target or original TeX label line).
- Link relocation: `#eq:null` → `main.tex#L120` (existing project target or original TeX label line).
- Link relocation: `#eq:tpc259-split` → `main.tex#L61` (existing project target or original TeX label line).
- Link relocation: `#eq:parseval` → `main.tex#L206` (existing project target or original TeX label line).
- Link relocation: `#eq:inverse` → `main.tex#L207` (existing project target or original TeX label line).
- Link relocation: `#eq:modezero` → `main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#tab:checks` → `main.tex#L257` (existing project target or original TeX label line).
