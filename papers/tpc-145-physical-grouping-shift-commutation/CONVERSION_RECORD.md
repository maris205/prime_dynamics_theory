# TPC-145 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `40652c61a4f042ec7d47f48e0a1e452411ee6b33eeded302d8c7c8ef41b88ff6`.
- Bibliography: [references.bib](references.bib), SHA-256 `a4aa3709994ff123fa8592ca949b8b577699a8b4b38382b552854dbdeadb33fb`.
- Preserved PDF: [tpc-145-physical-grouping-shift-commutation.pdf](tpc-145-physical-grouping-shift-commutation.pdf), SHA-256 `aea86385fd0b9ef2f973bfeeafd8cdd985c3f968a5f756f3cd664da09a359ddc`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `70f91129dbbec2596f63e5c9818030b024e5601fadfddef541731c4da5cd4c29`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC143_146.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Cut selection versus downstream selection` | 76 | 1 | `HEADING_TEXT_MATCH` |
| `Physical occurrence grouping` | 110 | 2 | `HEADING_TEXT_MATCH` |
| `Why aggregate commutation is not lineage` | 166 | 2 | `HEADING_TEXT_MATCH` |
| `The current field boundary` | 229 | 3 | `HEADING_TEXT_MATCH` |
| `Executable regression` | 261 | 3 | `HEADING_TEXT_MATCH` |
| `Claim boundary` | 301 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 323 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `61` before writing and `61` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e8139dfd5e87a06778f3609641d8afd20fa5a7533e1a0f1f40c8f59d92de9ae6`.
- Source theorem/proof environment starts: definition at TeX line 103, theorem at TeX line 139, proof at TeX line 153, definition at TeX line 180, theorem at TeX line 190, proof at TeX line 196, proposition at TeX line 211, proof at TeX line 216, corollary at TeX line 246, theorem at TeX line 303.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 56–58 | `b97547caeb7cc11bf464e3b2f977a929ece1f3bea91a98a365fe0198bef383dc` |
| D02 | \[...\] | 82–89 | `738c36ef4c9e7a274888ebe5386cc8406da00b3a4595aa4ede84fc2c7272ea0c` |
| D03 | equation | 91–94 | `d34dc5eab04a1977b9e9a09545258f9c3d6e950f85becc694006406a10b7954d` |
| D04 | \[...\] | 115–117 | `e878d76ea144697ccea9c62d6ee56cc0d797bfe537c692247fa02522dba2473f` |
| D05 | equation | 142–145 | `b300012740b82524874d976b051be0c97eaef7142cde84786346c021cb2039d1` |
| D06 | \[...\] | 147–149 | `313c6e23406abe84e6a978e3a6ced93fc2cc7f6d3c764f5dbfffcf2d7588cf50` |
| D07 | \[...\] | 155–157 | `b8e5f49dbe4bd51d147589bc0702a8952b110a8094f6aa72ba9a81dabbc97ba6` |
| D08 | \[...\] | 159–161 | `1ebb87d6e552b97c739b0b630e9ccaf7cfefc8f0f54bf0b390ddeef0d09b99a3` |
| D09 | \[...\] | 170–174 | `00b8f53e40ddd684e0241dc34dabc6cc69695e9faa80df5c798b000de1231e5d` |
| D10 | \[...\] | 183–187 | `2bde73e7920e49e821c95d13f750eb6fa934306e07826f7fe1778f4290cd89e7` |
| D11 | \[...\] | 199–205 | `63866e6949be9a5447023be561e0eae3105cc01a4ca20d064f08c0b1a16f7074` |
| D12 | \[...\] | 234–237 | `a288568c627908397c60d49fedd51d03a582b79da88d410d637fa80cf7fc7444` |
| D13 | \[...\] | 249–256 | `92df64b57a04ada4dbde254a76c738e0858ddcf155aeb02224f9984ae7caada9` |
| D14 | \[...\] | 292–297 | `f59d3f518ed8cd0330b892fdad4b466bdb0d46c1ce5320de9c4441b18891c93b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 60: `operator identity is still not a pathwise provenance certificate:`
- TeX line 64: `the prescribed-\(h_0\) slice.  We prove this exact criterion and a`
- TeX line 67: `\(P_{h_0}^{\rm cut}=I\), already supported by cut metadata`
- TeX line 78: `Fix a prescribed nonzero shift \(h_0\).  TPC-136 proves that every`
- TeX line 83: `P_{h_0}^{\rm cut}e_c`
- TeX line 86: `e_c,&h(c)=h_0,\\`
- TeX line 87: `0,&h(c)\ne h_0.`
- TeX line 90: `Every row in the fixed-\(h_0\) archive has the first case, whence`
- TeX line 92: `\boxed{P_{h_0}^{\rm cut}=I_{E_{\rm cut}}.}`
- TeX line 95: `This is a literal \(\Lone\) fact, not a localization estimate.`
- TeX line 104: `We write \(P_{h_0}^{\rm cut}\) only for the proved cut selector and`
- TeX line 105: `\(P_{h_0}^{\rm down}\) only for a selector on a completed downstream`
- TeX line 106: `archive.  Equality of their names or numerical \(h_0\)-values is not`
- TeX line 136: `projections onto records tagged by \(h_0\) in the source and target,`
- TeX line 150: `whenever exactly one of \(h(p),h(o)\) equals \(h_0\).`
- TeX line 156: `\mathbf1_{h(p)=h_0}G_{p,o},`
- TeX line 160: `G_{p,o}\mathbf1_{h(o)=h_0}.`
- TeX line 181: `The grouping is pathwise shift preserving at \(h_0\) when every edge`
- TeX line 184: `\mathbf1_{h(o(e))=h_0}`
- TeX line 186: `\mathbf1_{h(p(e))=h_0}.`
- TeX line 201: `\mathbf1_{h(p(e))=h_0}`
- TeX line 203: `\mathbf1_{h(o(e))=h_0}`
- TeX line 213: `Aggregate commutation does not imply the pathwise condition.`
- TeX line 217: `Take a source \(o\) tagged \(h_0\) and a target \(p\) tagged`
- TeX line 218: `\(h_1\ne h_0\).  Add two occurrence edges \(o\to p\), with`
- TeX line 238: `No finite sample census can replace that typed domain.`
- TeX line 242: `and reconnection destinations.  For \(P_{h_0}^{\rm down}\), they lack`
- TeX line 252: `\mathsf{H1.cut\_Ph0}&=\PROVED_{\Lone},\\`
- TeX line 254: `\mathsf{H1.frontier\_Ph0\_downstream\_totality}&=\NT.`
- TeX line 257: `The occurrence-level \(G/P_{h_0}\) commuting square is also`
- TeX line 266: `no physical or downstream stage edge.  Separate synthetic fixtures`
- TeX line 276: `Cut selector \(P_{h_0}^{\rm cut}\)`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:cutidentity` → `../main.tex#L93` (existing project target or original TeX label line).
- Link relocation: `#eq:square` → `../main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:square` → `../main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:cutidentity` → `../main.tex#L93` (existing project target or original TeX label line).
- Link relocation: `#thm:aggregate` → `../main.tex#L140` (existing project target or original TeX label line).
- Link relocation: `#thm:pathwise` → `../main.tex#L191` (existing project target or original TeX label line).
- Link relocation: `#prop:hidden` → `../main.tex#L212` (existing project target or original TeX label line).
- Link relocation: `#eq:cutidentity` → `../main.tex#L93` (existing project target or original TeX label line).
