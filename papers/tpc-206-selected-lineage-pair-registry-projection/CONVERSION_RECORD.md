# TPC-206 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `5097a7aa858596abe90de3652cdf922933fb6959f7bbea3592159aac3aad9776`.
- Bibliography: [references.bib](references.bib), SHA-256 `d8f4a786b20d71731cefa05db8e2522ada7782438dab8b74be484d8b99e1e24a`.
- Preserved PDF: [tpc-206-selected-lineage-pair-registry-projection.pdf](tpc-206-selected-lineage-pair-registry-projection.pdf), SHA-256 `e6a3ee6df0492daa2aae86de47040e8b0d5f8c75a7abc91208601f945d3bb082`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2e32612b0544345b3a36c428367f6d14cbe5826c3b2951435a8f725ba5804bfe`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC205_209.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Authorization, contract, and theorem scope` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `The selected source lineage` | 89 | 1 | `HEADING_TEXT_MATCH` |
| `Four typed derivations and three notation firewalls` | 118 | 2 | `HEADING_TEXT_MATCH` |
| `Selected-graph closure` | 157 | 2 | `HEADING_TEXT_MATCH` |
| `Why this is not a corpus-wide maximum` | 220 | 3 | `HEADING_TEXT_MATCH` |
| `Route state and machine boundary` | 244 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 279 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 290 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `46` before writing and `46` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `cab49161c360a3e39fd09eaae8b0ccbe4aa8779f3b10cd131713b30d05bc88db`.
- Source theorem/proof environment starts: theorem at TeX line 177, proof at TeX line 191, proposition at TeX line 229.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 77–83 | `0e17044109c817a93dd21c5aeaa14e16bf7f12d1edcb05f1c5d1c9e65c304e6b` |
| D02 | \[...\] | 92–97 | `7b004b3051bfd43191e7d5147f70a4e5375db6cd6d09e0354daeaeba8bb0d773` |
| D03 | \[...\] | 101–103 | `1c6d8a9835318473d9598d92adb514b5dbf4c5cdfd4058d13e0af945f4646b17` |
| D04 | \[...\] | 121–125 | `ce3f339659535ee32f0659bc99b2f3f7538cfb5902088a9cf81310d0c43c0ebe` |
| D05 | \[...\] | 127–129 | `ab8e69ce8bd40fa222b7aea84e2d28f2cc0d18281c99cbf58e242616b0d2ddd0` |
| D06 | \[...\] | 132–134 | `d7387b1dac86cd2f8548b397e42a8860edd8c63227fff046065faa695fece418` |
| D07 | \[...\] | 138–140 | `723f2afe1b05e724d44e9249797adcae13142d34c3a43310a9bb5f5cb002d16b` |
| D08 | \[...\] | 142–144 | `5ebd43048bfbce99ae7ead7b9c88648cb96a1b4ec2de5f2b5e973c278af5d41c` |
| D09 | \[...\] | 146–149 | `46051520abc25d489d13631d29729a06b9ea97e4ee638981aaee3ad88a29d96c` |
| D10 | \[...\] | 151–155 | `b8ca8db4027b14e883ff0429b59f6f1e182d2c059a0f31670d041fea3c37421c` |
| D11 | \[...\] | 181–186 | `ce9ec382f8e9abbc580eeb8d738197631840276ad81bfb3e49a0c1bdbff9cfc8` |
| D12 | \[...\] | 203–208 | `47ed9a32f85d45d5171900e546eb3a73865a96e4f218e7d6fd386a8afc2e04a1` |
| D13 | \[...\] | 210–212 | `aa9e11dfdd64047df5f31342885926c600502b650ecc23f287ec07e691b7c6cf` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `\(X,h_0,\delta,R,V,D_0,L,K,\alpha,\gamma,j,N_\alpha,N_\gamma\).`
- TeX line 38: `The first unmaterialized field in contract order is the opened dyadic scale`
- TeX line 39: `\(D\), at index nine.  The row divisor \(d=1\) does not fill \(D\);`
- TeX line 43: `This is a finite \(\Lone\) selected-lineage obstruction.  It is not a`
- TeX line 45: `reopen, an \(L2\) estimate, or a prime-pair theorem.`
- TeX line 50: `The authorized object is the finite theorem`
- TeX line 53: `\code{FINITE_SELECTED_LINEAGE_13_OF_42_PROJECTION_AND_}\\`
- TeX line 94: `\alpha &: X=512\mid h_0=2\mid \ell=103\mid k=5\mid d=1,\\`
- TeX line 95: `\gamma &: X=512\mid h_0=2\mid \ell=107\mid k=5\mid d=1.`
- TeX line 113: `The manifest has \(X=512,h_0=2,\delta=1/4\); its certificate records 866`
- TeX line 166: `two row records & \(X,h_0,V,\alpha,\gamma\)\\`
- TeX line 183: `X,h_0,\delta,R,V,D_0,L,K,\\`
- TeX line 218: `\code{nu_X} is not a scalar normalization.`
- TeX line 220: `\section{Why this is not a corpus-wide maximum}`
- TeX line 239: `1,707 dot-JSON blobs parse and 17 files containing non-finite constants are`
- TeX line 240: `rejected.  This census is a reproducible context and reopen-trigger audit.`
- TeX line 241: `It is not a semantic census of every JSONL or \TeX{} formula and is not used`
- TeX line 262: `remain open.  Earlier route stops remain scoped; the new cell`
- TeX line 277: `not an external signature or theorem source.`
- TeX line 285: `therefore a source-backed opened-\(D\) attachment search for this selected`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#thm:selected` → `../main.tex#L178` (existing project target or original TeX label line).
