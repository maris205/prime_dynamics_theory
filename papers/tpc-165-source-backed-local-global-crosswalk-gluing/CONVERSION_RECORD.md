# TPC-165 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `4fd8af1eba622c4197d3aaa7e11d33846d0b77439865a2888e91445d9796bb93`.
- Bibliography: [references.bib](references.bib), SHA-256 `ae0ed1235a7651c72f80f5ac60cd41308daa1db3ac55942b5ff546b4c08c8bff`.
- Preserved PDF: [tpc-165-source-backed-local-global-crosswalk-gluing.pdf](tpc-165-source-backed-local-global-crosswalk-gluing.pdf), SHA-256 `6839c64eca8b44cf36d959e9a36ea98e3e1736c97ac0cf72de50ba59ca566777`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `25b16b7c76946441258ccd288780436c4f5e835131861098affd608d03aa2fb1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC165_169.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `From a monolithic blocker to a descent problem` | 96 | 1 | `HEADING_TEXT_MATCH` |
| `Typed local patch system` | 120 | 2 | `HEADING_TEXT_MATCH` |
| `Local-to-global gluing theorem` | 169 | 2 | `HEADING_TEXT_MATCH` |
| `Why the cocycle is indispensable` | 254 | 3 | `HEADING_TEXT_MATCH` |
| `Synthetic nonvacuity certificate` | 271 | 3 | `HEADING_TEXT_MATCH` |
| `Three gates that gluing must not merge` | 295 | 4 | `HEADING_TEXT_MATCH` |
| `Current production evaluation` | 333 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 360 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 369 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `69` before writing and `69` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7663c1966a13519fcdcaaf173b32a72ded7d4d23d91e5f6fb2acf277d8a298b7`.
- Source theorem/proof environment starts: definition at TeX line 122, definition at TeX line 147, theorem at TeX line 171, proof at TeX line 195, corollary at TeX line 238, proof at TeX line 248, definition at TeX line 297, proposition at TeX line 311, proof at TeX line 316.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 103–106 | `d8b638fee8af4f8cb6b133de1725cfc413b2363eb9baac3a9f0e49cc2be1dd6d` |
| D02 | \[...\] | 112–115 | `00b2570aaae0c3b191efc0bf284c5a050a06bae8f53ae225a37ba58460ff9204` |
| D03 | \[...\] | 135–139 | `e3eaded040ab63191be0470ffffa9b8b3cbef0aff99f4e60a03435156221e4ce` |
| D04 | \[...\] | 149–152 | `86a799e11e41689860365aef12843e5e1fbd37b54c12561423d187a831f71963` |
| D05 | \[...\] | 154–158 | `d2682f1b6a4d86c5bac6c001e30cabe690351f5748d99cee0bade4233c7ad209` |
| D06 | \[...\] | 160–165 | `dac5b5be00fea85b6052431d229fcbb86cda72aeb302e8076f0a58fe81be7013` |
| D07 | \[...\] | 187–191 | `2d72a67bf27b2909090d36c31de30db50e49cba84bc90e7b2b4bbf31df04ca08` |
| D08 | \[...\] | 197–199 | `38b22540c59dcae5a85af1521fccd20e49a94eeb3bbdfb8318ef2f2bc7dc082b` |
| D09 | \[...\] | 203–207 | `5c664889b192ae1ac802398237a40acf0dbe8cc527f4b621672c51d88e7eac5f` |
| D10 | \[...\] | 214–216 | `4165505ea8fca6e7ba82fcc983bb7ee9eb29ded5d2a71207986016e6813d0f29` |
| D11 | \[...\] | 222–224 | `e3031e61af18b0be549a6f5703604f5f003698b26f218aeb09a1b1c5dd1dd45c` |
| D12 | \[...\] | 231–234 | `d58b9f15ad9049f0cb0fe71f9f0039a206a6ade36c00abfe63fe9b1f3af1ffa5` |
| D13 | \[...\] | 242–245 | `cca0da4e11d3b7c17427fcb08553c5438d61e7bbd1ce17b304c1b40b1230a5c3` |
| D14 | \[...\] | 274–276 | `436132f31412fa8965c1544f7487f3e6b0921be828cddfddc78e83169940c915` |
| D15 | \[...\] | 280–290 | `c3ee0921467277948ac08a3a1a6b53189e01154dd82046ddc509262dd6ea47ee` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `pdfsubject={A finite descent theorem with exact column conservation},`
- TeX line 54: `monolithic table.  This paper proves the finite descent theorem needed`
- TeX line 55: `to construct it from local patches.  Let a finite family`
- TeX line 57: `finite nonempty local formal row family, and suppose exact typed,`
- TeX line 66: `This theorem is formal and conditional.  A synthetic two-patch fixture`
- TeX line 81: `\noindent\textbf{Keywords:} fixed shift; finite descent; gluing;`
- TeX line 90: `Synthetic fixtures have no theorem semantics.  We prove no actual`
- TeX line 107: `This key does not create actual occurrences, but it lets independent`
- TeX line 116: `The answer is yes, by an elementary finite quotient theorem.  This`
- TeX line 117: `does not solve the source problem; it isolates exactly which local`
- TeX line 123: `Let \(\Cuts\) be a finite set of archived cut addresses, and let`
- TeX line 124: `\(\{U_i\}_{i\in I}\) be a finite cover.  For every \(c\in U_i\), let`
- TeX line 125: `\(\Rows_i(c)\) be a finite nonempty set of local formal rows.  A row`
- TeX line 144: `as data to be preserved; it does not assert that they are true of an`
- TeX line 171: `\begin{theorem}[Finite typed gluing]\label{thm:gluing}`
- TeX line 175: `\item there is a global finite nonempty row family \(\Rows(c)\) for`
- TeX line 256: `Pairwise compatibility alone does not force consistent identifications`
- TeX line 271: `\section{Synthetic nonvacuity certificate}`
- TeX line 293: `\(\mathsf{SYNTHETIC\_REACHABILITY}\) with theorem semantics false.`
- TeX line 317: `The construction in \eqref{eq:quotient} uses only finite sets, typed`
- TeX line 322: `parents, so it cannot imply G3.  Synthetic systems satisfying all`
- TeX line 351: `are not currently instantiated.  This is not a negative existence`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:local-conservation` → `../main.tex#L138` (existing project target or original TeX label line).
- Link relocation: `#eq:preserve` → `../main.tex#L157` (existing project target or original TeX label line).
- Link relocation: `#eq:global-conservation` → `../main.tex#L190` (existing project target or original TeX label line).
- Link relocation: `#thm:gluing` → `../main.tex#L171` (existing project target or original TeX label line).
- Link relocation: `#eq:global-conservation` → `../main.tex#L190` (existing project target or original TeX label line).
- Link relocation: `#eq:matrix-conservation` → `../main.tex#L244` (existing project target or original TeX label line).
- Link relocation: `#thm:gluing` → `../main.tex#L171` (existing project target or original TeX label line).
- Link relocation: `#eq:quotient` → `../main.tex#L206` (existing project target or original TeX label line).
