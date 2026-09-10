# TPC-152 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `126a7fee713954f0e3bec43df2320a604419d05407d8c2fd86416d285f8d88f2`.
- Bibliography: [references.bib](references.bib), SHA-256 `052c1cab103a7180f95f3a859a413b3211dfc5c0d58ce7b5f3913e0ea46d0a20`.
- Preserved PDF: [tpc-152-mvp5-frontier-occurrence-lift-route-decision.pdf](tpc-152-mvp5-frontier-occurrence-lift-route-decision.pdf), SHA-256 `6f31aa468dcad399579e13cd393a60534003200a39f39bf222f81880465afd22`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `21f2a7387e2eb55ece8ccefbfba8b3f194b1ac585271d6472f6ccd39d2244080`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC150_152.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `From MVP4 to MVP5` | 106 | 1 | `HEADING_TEXT_MATCH` |
| `A valid source-locked snapshot` | 152 | 2 | `HEADING_TEXT_MATCH` |
| `The minimal missing antichain` | 178 | 2 | `HEADING_TEXT_MATCH` |
| `Eight outcomes and their precedence` | 219 | 3 | `HEADING_TEXT_MATCH` |
| `Strengthened stop and reroute rules` | 265 | 3 | `HEADING_TEXT_MATCH` |
| `Three evidence labels` | 289 | 3 | `HEADING_TEXT_MATCH` |
| `The split \texorpdfstring{\(1/400\)}{1/400} endpoint` | 322 | 4 | `HEADING_TEXT_MATCH` |
| `H9 arithmetic independence` | 352 | 4 | `HEADING_TEXT_MATCH` |
| `Frozen gate projection` | 366 | 4 | `HEADING_TEXT_MATCH` |
| `MVP5 decision` | 406 | 4 | `HEADING_TEXT_MATCH` |
| `Regression suite and next forced step` | 440 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 487 | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 497 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `87` before writing and `87` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `11154ad6c599e70f2327532afff335f238efc269ea2ff27b5e3f0c35e0e8c289`.
- Source theorem/proof environment starts: definition at TeX line 154, proposition at TeX line 197, proof at TeX line 207, definition at TeX line 224, theorem at TeX line 247, proof at TeX line 257, proposition at TeX line 309, proof at TeX line 315, theorem at TeX line 408, proof at TeX line 421, corollary at TeX line 431.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 80–82 | `4a46ebf2ac1a46f3570179821dd0b1c0ba36832e500fc48437d8d1a4f6ce295b` |
| D02 | \[...\] | 113–117 | `f4b8ea56938e9e3410bcad6d6e04a0217e3d68c7bd727e7107c134973d613942` |
| D03 | \[...\] | 119–123 | `c825eb3ce95be920e659f1b7c5928eff3eea4f5ee5ab567083278e5d39c5cd14` |
| D04 | \[...\] | 182–187 | `df77871fc328fc130272abeda703218a15418bbba1995a4cc275841aec042e48` |
| D05 | \[...\] | 189–193 | `053c22c66a567cf2f86398490306f391f4c9c4df6837cfa36873f23b987e1fd0` |
| D06 | \[...\] | 200–204 | `f1016ad45f5e3122819ac36527c7bba914f9b3d60b2a7d2dbedf1e2958766228` |
| D07 | \[...\] | 249–254 | `36176dcbde25ed37d8751e9bcc5cf938c9c556da62e2f14fafd1111a48c3600b` |
| D08 | \[...\] | 269–273 | `3bfc451ae0d65cb2bed02b6756380d4e365f9184454ecc8e10591c41f2e34ae8` |
| D09 | \[...\] | 292–301 | `d6fe4f829e33dedba94740a40dc94aeb334cbe9f3182732b6c0d73cc8724b831` |
| D10 | \[...\] | 325–334 | `d890792ae175116a6b18195689994fd43c5cc79bf82609d6d75fb5f67d8f1096` |
| D11 | \[...\] | 411–417 | `d8b45a55778314bd19f79fcb2b391054b0a560e030509097fcbcf40abd68ef68` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 39: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 41: `\newcommand{\Bhard}{B_{h_0,\delta}}`
- TeX line 99: `below are narrower architectures, not a complete impossibility`
- TeX line 129: `\item \(P_{h_0}^{\rm cut}=I\), with an explicit prohibition against`
- TeX line 131: `\item field-descent, \(Q_D/Q_Z\) kernel and \(G/P_{h_0}\)`
- TeX line 140: `It does not construct \(L_X\).  The independent scalar route is not`
- TeX line 143: `Thus the empty ETO class in the finite fixture and a frontier scalar`
- TeX line 176: `certificate stale; it does not refute a theorem.`
- TeX line 210: `\(P_{h_0}\), H1 carrier, H5--H9 and physical-return missing node is a`
- TeX line 232: `\item \(\REROUTE\): the selected route is stopped and a distinct open`
- TeX line 241: `unresolved active node is an open scope-matched positive-\(\Ltwo\)`
- TeX line 243: `\item \(\OPEN\): every remaining valid case.`
- TeX line 252: `\STOPR,\quad \NT,\quad \AF,\quad \OPEN.`
- TeX line 258: `Validation either fails or provides a well-typed finite snapshot.`
- TeX line 279: `obstruction does not stop an occurrence-augmented quotient route; an`
- TeX line 280: `aggregate-commutator counterexample does not stop a row-separated`
- TeX line 281: `lift; and an atomic-prefix obstruction does not stop every possible`
- TeX line 284: `Finally, a reroute is not a change of a string identifier.  The`
- TeX line 285: `alternative must be open, use a distinct registry and possess a`
- TeX line 305: `synthetic model.  It remains below the third line because its scope is`
- TeX line 317: `\(\OPEN\), evidence type \(\Ltwo_{\rm target\mbox{-}positive}\), exact`
- TeX line 336: `the first as an open arithmetic target.  The \(\GO\) verdict requires`
- TeX line 380: `H2 & \(\OPEN\) & positive \(\Ltwo\) &`
- TeX line 382: `H3 & \(\OPEN\) & positive \(\Ltwo\) &`
- TeX line 385: `H4 & \(\OPEN\) & positive \(\Ltwo\) &`
- TeX line 392: `Actual downstream fixed-\(h_0\) totality.\\`
- TeX line 404: `route-universe completeness status is \(\OPEN\).`
- TeX line 423: `\(\INVALID\).  The selected route is open, and no theorem proves the`
- TeX line 426: `\(\NT\) occurs before \(\AF\) and \(\OPEN\).  Independently, H6--H9`
- TeX line 436: `are forward moves, but neither closes a fixed-\(h_0\) physical`
- TeX line 443: `synthetic typed snapshots and rejects:`
- TeX line 467: `The distinct scalar-plus-ETO route remains open under its own complete`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#prop:missing` → `../main.tex#L198` (existing project target or original TeX label line).
