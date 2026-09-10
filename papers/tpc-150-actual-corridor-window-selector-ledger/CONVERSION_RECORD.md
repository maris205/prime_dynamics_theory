# TPC-150 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `be071ded9daff31d02ce74b6e07df49d7fb8f905be597d4740661e192fc7354e`.
- Bibliography: [references.bib](references.bib), SHA-256 `e027872f465cb8e20b022e26ae468a0d1ac5662d68b1eff72fad6d216e7df64a`.
- Preserved PDF: [tpc-150-actual-corridor-window-selector-ledger.pdf](tpc-150-actual-corridor-window-selector-ledger.pdf), SHA-256 `98265926af07f90fe69b22b446c565efb8cc43a8e63051f27c9870eb4fa823ac`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `5fedd06cf2acac6bee83ecc218367c4b803f8c3c0d72e16a7bb433a3e6d5b67d`.
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
| `The sourced core and the missing occurrence lift` | 81 | 1 | `HEADING_TEXT_MATCH` |
| `A local exceptional set on a terminal window` | 120 | 2 | `HEADING_TEXT_MATCH` |
| `A sharp deterministic-prefix firewall` | 182 | 2 | `HEADING_TEXT_MATCH` |
| `The power-of-log return ledger` | 238 | 3 | `HEADING_TEXT_MATCH` |
| `The separate fixed-\texorpdfstring{\(X\)}{X}-power ledger` | 304 | 3 | `HEADING_TEXT_MATCH` |
| `Actual status and machine contract` | 337 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 382 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `74` before writing and `74` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `80373afba75309240e935712814a5b5f6a5570a8b66878d019fa24e5d2c0886b`.
- Source theorem/proof environment starts: proposition at TeX line 139, proof at TeX line 165, remark at TeX line 174, theorem at TeX line 184, proof at TeX line 198, corollary at TeX line 218, proof at TeX line 224, theorem at TeX line 266, proof at TeX line 288, proposition at TeX line 306, proof at TeX line 317.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 60–62 | `5720d35714c8e8bfdd43a82519141a717e3bd117dfffe2ec7718a5d316664bb8` |
| D02 | \[...\] | 85–87 | `07378eb22ab550b33ab71e505065de953911faf8c5b35abb53be021339561b56` |
| D03 | equation | 89–93 | `4fdf70f4110c1f9f0c3f11b41322c2a27c7af8c63f0efb1ab08524600c842e9f` |
| D04 | \[...\] | 108–111 | `dc8dd09143abf19b3913ad13dc7001316783163bd61ec4c26f57f5b3da988dcb` |
| D05 | equation | 113–116 | `be40c355d95d5bd757367b4bd703d21082b8ad4dab516b6c9a655f63385df863` |
| D06 | \[...\] | 123–129 | `05aec1b2a727dd67b9a598ad5838a66f907486e71e4b1fedc9e3ef5302bde6a2` |
| D07 | equation | 131–135 | `8981f942a00d05e7c02d074cb4207dc7c8175860d2699ee9a85f5ec59f8e2ded` |
| D08 | equation | 142–150 | `7fecc9170102295a98d75423b5f7a20e1061858cdbccfe436740b44ed2ae43f0` |
| D09 | equation | 152–155 | `71677afac35e36b43d7b4a625fe6ee2ce6cfdf768abe404caac922b929abdc4f` |
| D10 | equation | 157–161 | `3ff5ba4c45f3d1a69788d070862f4035f92b7d202e2384174f1c7ca7c3f36967` |
| D11 | \[...\] | 188–192 | `a94ef9b68b115717c7829b5c5bf3f3d46d463f6f56fd0aa51e13c876392a07b4` |
| D12 | equation | 212–215 | `90b2986da0353ee129233eada818a0342ab90ba1f1aeaf29ab88b25273d435ff` |
| D13 | align | 242–248 | `17071dc91d2c650e146502d8d3ffbfba9d71f1ae601b8e49c3ac48a8a1e83429` |
| D14 | equation | 250–255 | `0d6ab20948b679f6a55da950576f94ed8e19f597009725daaf8c1cf9a2680d75` |
| D15 | equation | 270–282 | `6a4a4cbc3895c3905a31c4a18084564d17adfe110fbee8e55423a361cb765194` |
| D16 | \[...\] | 310–313 | `ef3210a7cb7691b228215db0bd6bfba04f01a13d83ba9dc427c2233c37ab53a7` |
| D17 | \[...\] | 319–321 | `8e264d64747d1ad8c6615c5a3f01a6ee45aab3b414f391f4186aac41a8cea590` |
| D18 | equation | 327–330 | `50ceafc748eb94735a765629a5469d38c41a137cbec424aa862f151339d3593b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 36: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 67: `finite list of requested endpoints to an exceptional set does not`
- TeX line 78: `\(\Ltwo\) and not a prime-pair result.`
- TeX line 99: `This core theorem is uniform under a small-polylogarithmic bound on`
- TeX line 101: `It does not include a nonperiodic physical multiplier, a generic`
- TeX line 186: `Let \(T_X\subset[\sqrt X,X]\) be any finite set of deterministic`
- TeX line 199: `Every finite set has Lebesgue, hence logarithmic, measure zero.`
- TeX line 205: `This is a logical nonimplication, not a claim that the arithmetic`
- TeX line 221: `finite \(K_X\) satisfies \eqref{eq:selector}.`
- TeX line 231: `\item a pointwise theorem uniform in every actual prefix;`
- TeX line 300: `The displayed exponent is a guaranteed ledger output, not a claim`
- TeX line 334: `This is a scale comparison, not a theorem that a future stronger`
- TeX line 363: `\(\OPEN\) after occurrence lift.\\`
- TeX line 376: `obstruction, not an H3 or endpoint certificate.`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:source-density` → `../main.tex#L92` (existing project target or original TeX label line).
- Link relocation: `#eq:containment` → `../main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#eq:source-density` → `../main.tex#L92` (existing project target or original TeX label line).
- Link relocation: `#eq:theta` → `../main.tex#L154` (existing project target or original TeX label line).
- Link relocation: `#eq:exception-exponent` → `../main.tex#L160` (existing project target or original TeX label line).
- Link relocation: `#eq:window` → `../main.tex#L149` (existing project target or original TeX label line).
- Link relocation: `#eq:selector` → `../main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#eq:selector` → `../main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#eq:aff` → `../main.tex#L254` (existing project target or original TeX label line).
- Link relocation: `#eq:first-missing` → `../main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:window` → `../main.tex#L149` (existing project target or original TeX label line).
- Link relocation: `#eq:log-ledger` → `../main.tex#L281` (existing project target or original TeX label line).
