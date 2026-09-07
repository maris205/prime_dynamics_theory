# TPC-267 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `99811e2c135168ce97fa9d9170c7e607dec3f089a1a45ac25c332e8d5ad29f41`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `9f6f3b32ccb9cf83b36854a0f566f5e40b056d45480265765bbb5a95240c8cd4`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ba78602a01c4d740dbccb68471208b942520970671cafb725c02b9d7866e3eb1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC265_269.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position and claim firewall` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `The finite physical object` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `The rank-three residual` | 103 | 2 | `HEADING_TEXT_MATCH` |
| `Certified intervals` | 143 | 3 | `HEADING_TEXT_MATCH` |
| `What the census does and does not say` | 225 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next experiment` | 249 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 263 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `64` before writing and `64` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `17`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `087a258f15098194f3296097ee75be96f42dd7d25b13d42f1b1c83cd015088ab`.
- Source theorem/proof environment starts: proposition at TeX line 119, proof at TeX line 132, theorem at TeX line 168, proof at TeX line 188.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 63–66 | `9b06ad86f4d525a8a5efe41fb97464ab45c84020fe4ca9f383703bf958c9b6b0` |
| D02 | \[...\] | 68–70 | `b04b250897078ba6646aa50226a8ad5658ea09c15ae85462f901c2e870a79782` |
| D03 | \[...\] | 78–81 | `35e45fcd6f7b6af7a7c317770629b8c7750f5a501fbd0518b2267e1df0fdb903` |
| D04 | \[...\] | 85–89 | `60b96bd6f5de486d3837ac7853e780532a9f8db78fd18495ccf11e07c9627cf0` |
| D05 | \[...\] | 93–96 | `c67e95d583bbacc7e6b6720c26b41ea53de9808605fb0b514b1f87ab01de07ac` |
| D06 | \[...\] | 99–101 | `0af55981ead60031d19f50b5349e3b1690d8708f5b4286a67247d8d321b3d72c` |
| D07 | \[...\] | 107–110 | `5060937680541a9f41602c27d0399e17b0a58d27eda74d44f94b3eefb7fcef88` |
| D08 | \[...\] | 114–117 | `b06cb64feb6da8b7b6682abebcdf2d7637615a51e78c514f4a47509d40cf3901` |
| D09 | \[...\] | 122–124 | `f98939a2c71c89c58ef173a5d8a580b9130407449241702fd4f549edb36ea579` |
| D10 | \[...\] | 126–128 | `d18e155a8654de18e782c718a29300c20a6c9cf51119bbb597e9cbe9804768be` |
| D11 | \[...\] | 147–149 | `adc563f66ce214ac92f44b496b33c901a8144ada3e4bcb0f0dcfa94b8db8c2f2` |
| D12 | \[...\] | 151–154 | `6c23eba6a7ea757159620b0db936d4454278cbfd904a9671ffce800dfe821bd6` |
| D13 | \[...\] | 162–164 | `11a492a99e816248aca05000791a90d35277fdbdf42b9dda74db452d60de52fc` |
| D14 | \[...\] | 170–177 | `970bc78929881c54f0e821110d3309186aaf1950de7d3518c0326c38b4bf37c6` |
| D15 | \[...\] | 179–182 | `95b61e48d58c84c83a71d71fc6a7fba946fbfe32a069a29c7ea72685a85ca374` |
| D16 | \[...\] | 243–247 | `fe49906df8a2f4e9990bffb8f88af15cadd25c6d21d9e951ba3627b011cb243f` |
| D17 | \[...\] | 253–256 | `8f3df886f127bd1215a8ea757160f26d19901d9278ef5b62e5f8c758008b3d0d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `\title{A Finite Literal V59 Residual-Radius and Signed-Phase Census}`
- TeX line 29: `the first finite replay in which the residual is formed from the physical`
- TeX line 32: `For twelve natural finite representatives of the V59 clock and two explicit`
- TeX line 36: `\(0.2320126753\).  This is a finite signed-phase observation, not an`
- TeX line 38: `phase, arithmetic \(L^2\), and the twin-prime conclusion remain open.`
- TeX line 47: `paper takes a deliberately finite step toward that input.  It does not`
- TeX line 48: `pretend that a finite table is an asymptotic theorem.`
- TeX line 52: `\small\texttt{FINITE\_LITERAL\_V59\_RESIDUAL\_PHASE\_CENSUS}\\`
- TeX line 53: `\textit{numerically certified finite result}.`
- TeX line 55: `The exact operator and projection algebra are proved finite identities.  The`
- TeX line 57: `certificates.  The two kernel profiles and rounded finite clocks are explicit`
- TeX line 58: `modeling choices, so no uniform smooth-profile assertion is made.`
- TeX line 60: `\section{The finite physical object}`
- TeX line 75: `The profiles are used only to define a finite audit kernel.`
- TeX line 82: `The first term is rational on every finite input: it equals \(1/k\) when`
- TeX line 92: `The finite matrix is`
- TeX line 119: `\begin{proposition}[finite projection identity]`
- TeX line 120: `For every finite row, (7) is the cross-Gram of the orthogonal projection`
- TeX line 145: `The only infinite object in (3) is \(C_2\).  Let \(P=50000\) and multiply`
- TeX line 160: `The certificate does not take a square root to decide the phase contraction.`
- TeX line 168: `\begin{theorem}[twelve finite contractions]`
- TeX line 189: `The producer enumerates the finite prime shell, evaluates (2) exactly, forms`
- TeX line 202: `\caption{Selected finite residual phase bounds.  The displayed value is an`
- TeX line 225: `\section{What the census does and does not say}`
- TeX line 228: `the vectors entering the finite residual are generated by the physical prime`
- TeX line 229: `shell and source-shaped coefficients.  It is weaker than the open theorem in`
- TeX line 235: `finite kernel and comparison cutoff are declared choices.  Replacing them by`
- TeX line 237: `requires a new uniform theorem.`
- TeX line 239: `In particular, (12) is not a payment of the endpoint budget.  TPC-266`
- TeX line 241: `than \(1/400\) on the common asymptotic clock.  A finite ratio bounded away`
- TeX line 246: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 251: `TPC-267 establishes a reproducible physical finite interface for the object`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
