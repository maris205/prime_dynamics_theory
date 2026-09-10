# TPC-140 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `3c5e967a3159c19febe280e84c96c4f11dee6cfdb7b3448bccc203a7bd99a6be`.
- Bibliography: [references.bib](references.bib), SHA-256 `d2c9b3133ed0d2761b317bf6d9ebd8af5b693569c05c0a643987c5603387f3a8`.
- Preserved PDF: [tpc-140-exceptional-scale-selector-power-gate.pdf](tpc-140-exceptional-scale-selector-power-gate.pdf), SHA-256 `322d82548d495fb448a6259a6820e25b4e774d68faa7339ae47441f5645903f4`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2b9340acb2c0ce1adf990bff5ef7b9be659beff62a05720fc18712da490a9daf`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC140_142.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Why almost all scales are not all prefixes` | 76 | 1 | `HEADING_TEXT_MATCH` |
| `Two legal return interfaces` | 127 | 2 | `HEADING_TEXT_MATCH` |
| `Power transport` | 254 | 3 | `HEADING_TEXT_MATCH` |
| `The logarithmic corridor and its separate ledger` | 327 | 4 | `HEADING_TEXT_MATCH` |
| `Certificate schema and current verdict` | 408 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 463 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `104` before writing and `104` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `23`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `00305996e9eedf989b815bdc82ae4a7d194a2c006bc21b37f091492dc269e7cb`.
- Source theorem/proof environment starts: proposition at TeX line 108, proof at TeX line 117, proposition at TeX line 136, proof at TeX line 161, remark at TeX line 169, definition at TeX line 181, definition at TeX line 195, theorem at TeX line 207, proof at TeX line 219, proposition at TeX line 226, proof at TeX line 232, remark at TeX line 244, theorem at TeX line 273, proof at TeX line 294, corollary at TeX line 303, proof at TeX line 322.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 46–48 | `d6cb5370fab215e1c33376090f6f166aaf7a91b4f0422a34083971aadd42de53` |
| D02 | \[...\] | 53–58 | `6a2732dfe0ad6ca874e83296e0505d7b6583cc08e41a1ce7de62fe94b27bc5be` |
| D03 | \[...\] | 79–81 | `d44aeeb4f10664441d12c458214dd96c99b4da48080b92450e7ec6962b5da3fa` |
| D04 | equation | 83–88 | `9b198c5781da637140ea895d7b6479a0c90063ed5a049c4d8e5e24907d344568` |
| D05 | \[...\] | 111–113 | `1e7af1e932ac56076f92493598c688c45518828322f2f332712b793958fcdfb6` |
| D06 | \[...\] | 130–133 | `e20b9d4ffee84e47b9d6b0248a6552a9a97752de218d361c57eed4d1ce40b2de` |
| D07 | equation | 139–145 | `cf22a87e1f9f50f2b663416f26385d23a3d490ddcfba953039d1f3e245232ba1` |
| D08 | equation | 147–155 | `164f11d5ce6af6011af9cb34d3e1cf7180861ba598a8294e36b067cca0adf3c5` |
| D09 | \[...\] | 185–190 | `7a02be9d7969465255eb9cdf95af5dd6080f8dc3f7f0dee62c100880651aabf9` |
| D10 | equation | 200–203 | `feebe79194a1304a368a367c01a2634bf9eb07ad2305fd1754fc62b1ac1140c7` |
| D11 | equation | 211–216 | `90670e763571d74a7cdb9d8bc2a3168cdb3b9ec857406ec37e908dd1c6548b1f` |
| D12 | \[...\] | 257–259 | `f447bc29c85586414d0b5281b549a97d57e356755f2d8ee96f159c787f5ca020` |
| D13 | \[...\] | 262–264 | `f2fb07ce4b2f98a28dc62e5eb32306b13ee430ed45ecdeedee603bd95a1c0174` |
| D14 | equation | 277–289 | `c844d70c5e69859148016cf9a63146748bce2171a972e52c4dca4f440aa67cc5` |
| D15 | equation | 308–311 | `d5a611b77f16b9daacb248f3d395ff7a824d9655faeffc0dd9ad145bb96f7133` |
| D16 | \[...\] | 315–319 | `7cdcb23e121adbb98c8a90ba4d899f9ee7a7fedfd59986262f678cb8af6c1799` |
| D17 | \[...\] | 342–344 | `48e7437b1afce10ce0d72f1f558b33b4f23c873e9f70114783ecadd1314c3d8b` |
| D18 | \[...\] | 347–349 | `22bc5515afeb7b53df3c4ef31c1ee326eaf81b45ed525cfe61cba647a5c99e98` |
| D19 | \[...\] | 363–368 | `4478b1f520a8e6b9ecb5b5f8784743d398b23c1c04eea6ec88c1295daf9afb73` |
| D20 | equation | 371–376 | `a34d8a72e06f37e6e5002956e7e097ac049920347f7d1d377c426dd1e268a9f8` |
| D21 | \[...\] | 382–384 | `dabe9eb0f586957b1e95e4bf43c3cf2dd015026987708525281cbac2e96315b4` |
| D22 | equation | 389–399 | `e6c16a105277a3526eabdd59efbcaa01bbf7a4e6de468a8e6694879600bae662` |
| D23 | \[...\] | 411–421 | `870eda779a7eeaf1cfe443e64993a571ad08aa1ca0e04a3ccb1f37494978fc3e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 43: `first is a direct uniform all-prefix theorem.  The second requires`
- TeX line 72: `The actual selector and all-prefix gates remain open; no positive`
- TeX line 98: `small exceptional set is still not a deterministic all-prefix`
- TeX line 123: `This counterexample is analytic, not a construction of Liouville`
- TeX line 156: `In particular, \eqref{eq:global-exceptional} alone does not give`
- TeX line 229: `\eqref{eq:domination} fails for every finite \(K_X\).`
- TeX line 247: `nonnegative error; it does not control a supremum.  For a component`
- TeX line 248: `family, one needs either a uniform arithmetic error and uniform`
- TeX line 256: `Assume now that every input is expressed at amplitude scale.  Let`
- TeX line 339: `one of the eligibility checks, not an automatic property of the`
- TeX line 419: `\texttt{evidence}:&\text{proved, conditional, finite, or open}.`
- TeX line 443: `& Open.\\`
- TeX line 445: `& Open / not supplied.\\`
- TeX line 446: `Positive fixed-\(h_0\) L2, H3, or \(1/400\)`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 6 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:almost-scale` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#eq:almost-scale` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#eq:almost-scale` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#eq:global-exceptional` → `../main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:global-exceptional` → `../main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:almost-scale` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#def:selector` → `../main.tex#L196` (existing project target or original TeX label line).
- Link relocation: `#eq:domination` → `../main.tex#L202` (existing project target or original TeX label line).
- Link relocation: `#eq:almost-scale` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#eq:domination` → `../main.tex#L202` (existing project target or original TeX label line).
- Link relocation: `#def:pointwise` → `../main.tex#L182` (existing project target or original TeX label line).
- Link relocation: `#thm:selector` → `../main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#eq:raw` → `../main.tex#L288` (existing project target or original TeX label line).
- Link relocation: `#eq:almost-scale` → `../main.tex#L87` (existing project target or original TeX label line).
- Link relocation: `#thm:raw` → `../main.tex#L274` (existing project target or original TeX label line).
- Link relocation: `#eq:return` → `../main.tex#L215` (existing project target or original TeX label line).
- Link relocation: `#eq:raw` → `../main.tex#L288` (existing project target or original TeX label line).
- Link relocation: `#eq:log-ledger` → `../main.tex#L398` (existing project target or original TeX label line).
