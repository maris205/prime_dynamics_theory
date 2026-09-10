# TPC-155 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `6401392d066e675e818509317fd5c3d950b4dfb924b4d76bf5be64d959ac7018`.
- Bibliography: [references.bib](references.bib), SHA-256 `cdeb7de91eb5e8c4ee407719a32a1bcd02338d21b123b15917c3a3159e11d90c`.
- Preserved PDF: [tpc-155-theorem-backed-occurrence-witness-verifier.pdf](tpc-155-theorem-backed-occurrence-witness-verifier.pdf), SHA-256 `a9ad976f4f188c8da55893fb8587ca9fa36737ca15eda6de17927f52b5318a6e`; 8 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2ef7bb7c67b43fa5d1a0b574e3e06bf942bcbc1655f8c9a3af5ee73ee41be428`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC153_156.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The exact verification problem` | 110 | 1 | `HEADING_TEXT_MATCH` |
| `Exact scalars and row separation` | 146 | 2 | `HEADING_TEXT_MATCH` |
| `\texttt{OccurrenceWitnessV1}` | 192 | 2 | `HEADING_TEXT_MATCH` |
| `Domain and source registry` | 194 | 2 | `HEADING_TEXT_MATCH` |
| `Native identity and support namespaces` | 227 | 3 | `HEADING_TEXT_MATCH` |
| `Parent, stage and multiplier chain` | 254 | 3 | `HEADING_TEXT_MATCH` |
| `The four downstream interfaces` | 282 | 3 | `HEADING_TEXT_MATCH` |
| `Three exports that cannot be merged` | 313 | 4 | `HEADING_TEXT_MATCH` |
| `Soundness of the finite verifier` | 350 | 4 | `HEADING_TEXT_MATCH` |
| `The provenance firewall` | 438 | 5 | `HEADING_TEXT_MATCH` |
| `A non-vacuous synthetic certificate` | 474 | 6 | `HEADING_TEXT_MATCH` |
| `Current production verdict` | 522 | 6 | `HEADING_TEXT_MATCH` |
| `Mutation audit and kill criteria` | 571 | 7 | `HEADING_TEXT_MATCH` |
| `What the verifier enables next` | 620 | 8 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 655 | 8 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 672 | 8 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `82` before writing and `82` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `326084c72cd773d52495dd2145a670337e66338dbeb7f82dd246c496eba5a8e3`.
- Source theorem/proof environment starts: definition at TeX line 148, theorem at TeX line 166, proof at TeX line 177, remark at TeX line 185, definition at TeX line 196, definition at TeX line 318, theorem at TeX line 356, proof at TeX line 376, proposition at TeX line 388, proof at TeX line 402, proposition at TeX line 408, proof at TeX line 414, theorem at TeX line 423, proof at TeX line 431, theorem at TeX line 443, proof at TeX line 456, corollary at TeX line 466, proposition at TeX line 504, proof at TeX line 510, theorem at TeX line 542, proof at TeX line 558.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 113–115 | `5427d1d4d4859d7e2dbed3d6080220bfe02e83d3ad6a448a646b441fc757d72f` |
| D02 | equation | 124–127 | `30e015b84a7fa84ebfe534fc1b69e14f9ddd95c10e387f34bdee084617c7a83a` |
| D03 | \[...\] | 150–152 | `0cb9716a04de69fe694ec01dc102edcfe6957564f12a12b62997ecc120979c43` |
| D04 | equation | 161–164 | `822bbe3b8f18762f4b289acdf04d90fbf0e68d877b8d27e813b115d2076f75e1` |
| D05 | equation | 169–174 | `453a50604ed02983e25ab9c76aeb86f39379e120e0a3b9972bf8fd793b20f747` |
| D06 | \[...\] | 201–205 | `5365d0210d65655869afd01e81bdfb8499a4b6f54b5ad62695c563ffebf70624` |
| D07 | \[...\] | 230–233 | `d949aa8b2f4fdac5c78d033448e37bf69d816684c1cba9618786b0b2a46f8a80` |
| D08 | \[...\] | 239–245 | `0ecf7fdf36ffec6ba9410d544783e1912de679a06d455168249cb370662c22c5` |
| D09 | equation | 274–276 | `79d6151fc6b5c0b9df91a664b1f21c3d4d384ef0ed83126be1f241ac53d44b73` |
| D10 | \[...\] | 305–307 | `663c22225165a81c83d2b4a037d3809b349431af574b5b305829928f6bda9cbe` |
| D11 | equation | 359–363 | `664af1c91861fecdc8faf9abed893252821ed8d8ffef31d5fc8457e5a275f33c` |
| D12 | equation | 394–397 | `37da73ae086a0563993db9ad499a237e5cb0b4d53a0b538c8077e489256b30af` |
| D13 | \[...\] | 526–540 | `4ef9ed3c1c48b3b868a289dbd21385cb54a5be97be171c18d10f4dd27ff069c5` |
| D14 | \[...\] | 545–550 | `1f6977b9d4ba1ea0234dae5e16c15bdbeb0c422b1e971e9cfa1467db252b7c3e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 42: `\newcommand{\Bhard}{B_{h_0,\delta}}`
- TeX line 60: `fully typed downstream occurrences.  The existing archive does not`
- TeX line 62: `what finite evidence would be sufficient to verify a proposed lift`
- TeX line 75: `We prove that the finite contract is equivalent to column conservation`
- TeX line 82: `one-to-many column.  It is explicitly synthetic \(\Lzero\) evidence.`
- TeX line 103: `\texttt{SYNTHETIC\_L0\_ONLY}; it is not a production occurrence`
- TeX line 116: `Here ETO denotes \texttt{ELIGIBLE\_TAIL\_OPEN} and FUM denotes`
- TeX line 117: `\texttt{FRONTIER\_UNMAPPED}.  The frozen finite archive used by`
- TeX line 123: `The desired object is a finite sparse matrix`
- TeX line 142: `remains open.  We do not fill that gap by fabricated labels.  Instead`
- TeX line 198: `\nolinkurl{SYNTHETIC_L0_ONLY} or`
- TeX line 213: `source-locked TPC-143 obligation domain.  In synthetic mode the`
- TeX line 222: `\texttt{CANONICAL\_UTF8\_LF\_V2} hash must match.  Synthetic mode uses`
- TeX line 223: `\texttt{SYNTHETIC\_AXIOM\_L0}, for which artifact path and hash are`
- TeX line 231: `(\text{native id},(\ell,k,d_{\rm native}),h_0,`
- TeX line 284: `The witness does not infer the four maps; it demands their`
- TeX line 299: `\item[\(P_{h_0}\), downstream selector]`
- TeX line 301: `domains, and a literal edgewise fixed-\(h_0\) preservation Boolean.`
- TeX line 346: `essential: a complete export on a synthetic or incomplete supplied`
- TeX line 347: `witness is not a complete physical cover of the unknown actual`
- TeX line 350: `\section{Soundness of the finite verifier}`
- TeX line 366: `\item identical native tuple, \(h_0\) and physical normalization to`
- TeX line 369: `\item internally consistent \(Q_D,Q_Z,G,P_{h_0}\) records;`
- TeX line 383: `\(P_{h_0}\); named multiplier factors against the recorded product;`
- TeX line 398: `In particular this holds for \(h_0\) and for any encoded scalar`
- TeX line 417: `\(h_0\).  The test precedes all aggregation.  Therefore an edge that`
- TeX line 424: `Within the declared finite schema, the verifier accepts exactly when`
- TeX line 433: `a finite conjunction of precisely the listed syntactic, arithmetic,`
- TeX line 457: `The verifier reads finite files.  Its source operation checks path,`
- TeX line 458: `hash and identifier equality; it does not contain a proof checker for`
- TeX line 474: `\section{A non-vacuous synthetic certificate}`
- TeX line 481: `\caption{Synthetic \(\Lzero\) conservation fixture.}`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 8 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:matrix` → `../main.tex#L163` (existing project target or original TeX label line).
- Link relocation: `#def:exports` → `../main.tex#L319` (existing project target or original TeX label line).
- Link relocation: `#thm:column` → `../main.tex#L167` (existing project target or original TeX label line).
- Link relocation: `#thm:soundness` → `../main.tex#L357` (existing project target or original TeX label line).
- Link relocation: `#tab:fixture` → `../main.tex#L482` (existing project target or original TeX label line).
- Link relocation: `#thm:soundness` → `../main.tex#L357` (existing project target or original TeX label line).
- Link relocation: `#thm:firewall` → `../main.tex#L444` (existing project target or original TeX label line).
