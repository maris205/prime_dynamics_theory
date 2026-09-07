# TPC-320 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `88c46824c79e9c202a698cf4db36fcaf98260537`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `53da473b5b5c02df7760be9ef778c2987a3397b268517acfc7f60bf06fe80151`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `6c6a370a9ee409772ebeb66c9a2ccf8a7f5e465abf6dd45de988415c51b5b1b2`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d217ca3abcc6f2f133a1430132d4e8c8a1974b9180c837746f1d2357b40386d3`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC320_324.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen operator and readouts` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Exact algebraic firewall` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol` | 152 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 174 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route status` | 223 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 248 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 259 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `61` before writing and `61` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ceb5f0da237ca1b01ec337944faa822ca17309bd33633b3563a2df830822d12b`.
- Source theorem/proof environment starts: proposition at TeX line 97, proof at TeX line 104, theorem at TeX line 115, proof at TeX line 127, proposition at TeX line 135, proof at TeX line 142.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 64–69 | `3af391dda1f7076eab449557b6eb510219181ce42a1f824acc38dcf47d163fb0` |
| D02 | \[...\] | 73–76 | `67541793a66e54411f0e1689ce0a2b007b075c5abc18e4e94ee6f23bf451ed0c` |
| D03 | \[...\] | 78–82 | `dbdfc0935bfa841ac873df30deb2d8e6ac2de149d047f204fbd0237e013626a0` |
| D04 | \[...\] | 84–88 | `0c72bacd255995f78469a5d2ba2cc91a7c8b9f8b7ee7a3eca0cc60d4928d4e67` |
| D05 | \[...\] | 90–93 | `bf793a9ebab61014bfa01713e52e863441bd6620fd2fd6ed4e9c0cf5aa9c140f` |
| D06 | \[...\] | 99–102 | `793c1519384c8bf93edd604d4e77d3f19fd388913493df00cffe4f677578fdac` |
| D07 | \[...\] | 108–112 | `d438f8da763ade1b5310e43836fe85429b8f4308035896de9957918ab060e8e4` |
| D08 | \[...\] | 117–120 | `953939269af87e2421e211142b8e231c17c14eeebb394cbc11b938ee0181dcf7` |
| D09 | \[...\] | 122–124 | `8714990d854cb4a3b8506b7a88ac6e8f6512847b79d6c538597aac0b43dcc2d3` |
| D10 | \[...\] | 138–140 | `5a5df87b8480dee16107b07082c690f7d9f04aef49d87366b864aadedb2c74c0` |
| D11 | \[...\] | 155–157 | `654305d04897f3807fa198a1515744a4d6f1d8b79cb18cda575e7a97cce93e50` |
| D12 | \[...\] | 209–217 | `f44a58df73ef154678e942ed1fc6a92638c2191a11c3c67d17619269799b19d8` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 25: `We continue a finite audit of a deleted-diagonal, centered prime--shell`
- TeX line 31: `$k\in\{1,2,4,8,16\}$, a dual-path finite enclosure on 24 rows and 80`
- TeX line 34: `finite observations, while normalized entropy is mixed (14 increases and`
- TeX line 36: `are finite and do not provide signed prime-shell cancellation, an asymptotic`
- TeX line 45: `unchanged from the preceding finite audits.  TPC-319 read`
- TeX line 55: `We answer this question only on a declared finite panel.  The answer is`
- TeX line 57: `obstruction without silently turning a finite slope into an arithmetic`
- TeX line 97: `\begin{proposition}[finite spectral bounds]`
- TeX line 98: `For a finite PSD Gram matrix with $T(G)>0$,`
- TeX line 152: `\section{Finite protocol}`
- TeX line 176: `Table~\ref{tab:concentration} reports the finite point ranges and the`
- TeX line 204: `NUMERICALLY CERTIFIED FINITE decreases.  The smallest ratio is about`
- TeX line 205: `0.3976 and the largest is about 0.9001, so the effect is not a numerical`
- TeX line 211: `\text{quantity} & \text{finite range} & \text{growth transitions}`
- TeX line 228: `than the source-count-normalized plot: the finite trend is not explained only`
- TeX line 231: `The strongest negative result is equally important.  The panel does not`
- TeX line 233: `edge gaps can be small, and the certificate is tied to fixed $H$, finite`
- TeX line 234: `$Q$-anchors, and three source scales.  No uniform concentration theorem,`
- TeX line 241: `advance for a finite scale-invariant spectral readout, with the full Gate-B`
- TeX line 242: `arithmetic endpoint still OPEN.  The exact identities are labeled`
- TeX line 244: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}; ranks and entropy are`
- TeX line 245: `\texttt{NUMERICAL\_OBSERVATIONS}; the uniform and arithmetic claims are`
- TeX line 246: `\texttt{OPEN}.`
- TeX line 253: `sizes, while stable and participation ranks increase as finite observations.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:sourcefactor` → `main.tex#L92` (existing project target or original TeX label line).
- Link relocation: `#tab:concentration` → `main.tex#L187` (existing project target or original TeX label line).
