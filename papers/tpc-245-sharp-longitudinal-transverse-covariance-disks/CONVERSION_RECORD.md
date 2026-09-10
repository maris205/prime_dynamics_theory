# TPC-245 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `df78be47f3f5ad6260bb38a96644cc0706603eb9d27a678d9c9972ed1ebaa577`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `1493bd4eaa5a8d8149dabf7026f7441b148ed787bed412b9cb3d9239f70a9241`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `9cbc17293f7d05b36a164b7d01280034c37b39aa5f464049ee10d6e38f42c51b`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC245_249.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 12 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `df78be47f3f5ad6260bb38a96644cc0706603eb9d27a678d9c9972ed1ebaa577` |
| [paper/math_commands.tex](paper/math_commands.tex) | `0c509b321f40ecba4c72f96699b9bfa358bf7189cfe3e02c143d1cc36853e77e` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `d895ce81fec8eff9547fb73dbabbd6678264aab038c2592d50913c186cc990e8` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `e817b39f1a67c8261dd67f8b00ab6ba16ad2f604ad4e9d9ea55bace496ed39c5` |
| [paper/sections/2_source_lock.tex](paper/sections/2_source_lock.tex) | `9b4d83ad5197f3b2b0bedec04f0f9d1449a63bf2cb078390ddfc69ff9bcee74f` |
| [paper/sections/3_classification.tex](paper/sections/3_classification.tex) | `ed9f6305bfdbf029d7e1643d486cea3f01f92b9f72f283380a6c43b15b676336` |
| [paper/sections/4_proof.tex](paper/sections/4_proof.tex) | `7837f952355011c6da41d851763c1d3641ca288acce51b68a0e4053dccbe126b` |
| [paper/sections/5_sharp_corollaries.tex](paper/sections/5_sharp_corollaries.tex) | `91aec0317a1ae703f4230010511a0263247c388fe09268566943a3dba681ae57` |
| [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) | `8ec7f8280e27faa40f3ff5f517a231b35bd49570b04b9d0e26b5ae269c1d0117` |
| [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) | `f9ed85daebb9c2e201ed60d7e40ec28ec876b70f16f31af436d95779b6130673` |
| [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) | `3a47cf1a8f92b82d9ab5ac833416c36a60b92b000445d35139509dbc167409dc` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `2e4c97dd5d4311451d9826503bc2d07aa9fe9fec46dd868ccffb45642c06caaf` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L17](paper/main.tex#L17) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L45](paper/main.tex#L45) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L48](paper/main.tex#L48) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/2_source_lock}` | [paper/sections/2_source_lock.tex](paper/sections/2_source_lock.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/3_classification}` | [paper/sections/3_classification.tex](paper/sections/3_classification.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/4_proof}` | [paper/sections/4_proof.tex](paper/sections/4_proof.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/5_sharp_corollaries}` | [paper/sections/5_sharp_corollaries.tex](paper/sections/5_sharp_corollaries.tex) |
| [paper/main.tex:L53](paper/main.tex#L53) | `\input{sections/6_certificate}` | [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) |
| [paper/main.tex:L54](paper/main.tex#L54) | `\input{sections/7_route_boundary}` | [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) |
| [paper/main.tex:L55](paper/main.tex#L55) | `\input{sections/8_conclusion}` | [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) |
| [paper/main.tex:L58](paper/main.tex#L58) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Source lock and object boundary` | [paper/sections/2_source_lock.tex:L1](paper/sections/2_source_lock.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Exact covariance classification` | [paper/sections/3_classification.tex:L1](paper/sections/3_classification.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Proof of Theorem~\ref{thm:classification}` | [paper/sections/4_proof.tex:L1](paper/sections/4_proof.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `Cancellation margin and phase sector` | [paper/sections/5_sharp_corollaries.tex:L1](paper/sections/5_sharp_corollaries.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Exact finite certificate` | [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Route consequence and boundary` | [paper/sections/7_route_boundary.tex:L1](paper/sections/7_route_boundary.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/8_conclusion.tex:L1](paper/sections/8_conclusion.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Status ledger` | [paper/sections/A_status_ledger.tex:L1](paper/sections/A_status_ledger.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `95` before writing and `95` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `777177c9b9065cee73702eaac5d6809ae32c3d99a88d743efef62b6df565c226`.
- Source theorem/proof environment starts: theorem at [paper/sections/3_classification.tex:L17](paper/sections/3_classification.tex#L17), corollary at [paper/sections/5_sharp_corollaries.tex:L3](paper/sections/5_sharp_corollaries.tex#L3), corollary at [paper/sections/5_sharp_corollaries.tex:L19](paper/sections/5_sharp_corollaries.tex#L19).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/3_classification.tex:L7](paper/sections/3_classification.tex#L7) – [paper/sections/3_classification.tex:L11](paper/sections/3_classification.tex#L11) | `d709c3b56669f98cdfe7e2abe72778513521d6d8082840386451af7fc861f320` |
| D02 | \[...\] | [paper/sections/3_classification.tex:L13](paper/sections/3_classification.tex#L13) – [paper/sections/3_classification.tex:L15](paper/sections/3_classification.tex#L15) | `84ca074e1b7729a583814536387efcd0d8504056c7cc84afb1d35f700adcfe93` |
| D03 | \[...\] | [paper/sections/4_proof.tex:L4](paper/sections/4_proof.tex#L4) – [paper/sections/4_proof.tex:L8](paper/sections/4_proof.tex#L8) | `8a5ba9e7cd401956df476960c7bd72fb451b256105b495beb8409d61bb462654` |
| D04 | equation | [paper/sections/4_proof.tex:L12](paper/sections/4_proof.tex#L12) – [paper/sections/4_proof.tex:L14](paper/sections/4_proof.tex#L14) | `efd2d1b0056117c6ae47e78f8ccff122ff5ccbcbcd84b7d1a1bb27ae07eab900` |
| D05 | equation | [paper/sections/4_proof.tex:L16](paper/sections/4_proof.tex#L16) – [paper/sections/4_proof.tex:L18](paper/sections/4_proof.tex#L18) | `324e36368912c80e627a8501ad3f027f78458272759f3f735126608ac49505d6` |
| D06 | \[...\] | [paper/sections/4_proof.tex:L24](paper/sections/4_proof.tex#L24) – [paper/sections/4_proof.tex:L30](paper/sections/4_proof.tex#L30) | `1961981e1f759d01421858eec1234b6824af00e869df7fcedd26c50911f13629` |
| D07 | \[...\] | [paper/sections/4_proof.tex:L38](paper/sections/4_proof.tex#L38) – [paper/sections/4_proof.tex:L43](paper/sections/4_proof.tex#L43) | `f7dddd4aad467c0b6ecab2c81d20b0f751e779e4e21c3c02d810e748b5530a5d` |
| D08 | \[...\] | [paper/sections/5_sharp_corollaries.tex:L5](paper/sections/5_sharp_corollaries.tex#L5) – [paper/sections/5_sharp_corollaries.tex:L8](paper/sections/5_sharp_corollaries.tex#L8) | `39aea6132437a8677dd144df0e5148770a1fde222fb836cb0980289fdf3f3115` |
| D09 | \[...\] | [paper/sections/5_sharp_corollaries.tex:L21](paper/sections/5_sharp_corollaries.tex#L21) – [paper/sections/5_sharp_corollaries.tex:L24](paper/sections/5_sharp_corollaries.tex#L24) | `3ec7dbf392a02c12f24991bd2384ae93d58dbc7bbe5a1959242d0b0f6e00c58c` |
| D10 | \[...\] | [paper/sections/5_sharp_corollaries.tex:L31](paper/sections/5_sharp_corollaries.tex#L31) – [paper/sections/5_sharp_corollaries.tex:L33](paper/sections/5_sharp_corollaries.tex#L33) | `f57652845b369e0780274d6472ef71ff8e3b36a690676317f7065bb130da4212` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L12](paper/sections/0_abstract.tex#L12): `V59 two-lane attachment remain open.  No arithmetic cancellation or twin-prime`
- [paper/sections/1_introduction.tex:L20](paper/sections/1_introduction.tex#L20): `vectors with fixed data; it does not assert that the actual arithmetic vectors`
- [paper/sections/2_source_lock.tex:L15](paper/sections/2_source_lock.tex#L15): `of $V^P$, generally of dimension $\dim V$.  It is not a previously defined`
- [paper/sections/3_classification.tex:L27](paper/sections/3_classification.tex#L27): `No finite-dimensionality or separability hypothesis is required.`
- [paper/sections/4_proof.tex:L21](paper/sections/4_proof.tex#L21): `Assume first that $m\ge2$.  If $r=0$, one transverse vector vanishes and the`
- [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1): `\section{Exact finite certificate}`
- [paper/sections/6_certificate.tex:L16](paper/sections/6_certificate.tex#L16): `and $625$ in dimension one.  These computations are finite illustrations and`
- [paper/sections/7_route_boundary.tex:L14](paper/sections/7_route_boundary.tex#L14): `inside each attached block.  TPC-219 does not supply this second field: its`
- [paper/sections/7_route_boundary.tex:L17](paper/sections/7_route_boundary.tex#L17): `Accordingly, the maximum claim here is structural L1.  We claim no arithmetic`
- [paper/sections/7_route_boundary.tex:L18](paper/sections/7_route_boundary.tex#L18): `advance, no fixed-atom credit, no arithmetic L2 estimate, no payment of the`
- [paper/sections/A_status_ledger.tex:L15](paper/sections/A_status_ledger.tex#L15): `Canonical block direction & open \\`
- [paper/sections/A_status_ledger.tex:L16](paper/sections/A_status_ledger.tex#L16): `Literal V59 two-lane attachment & open \\`
- [paper/sections/A_status_ledger.tex:L18](paper/sections/A_status_ledger.tex#L18): `Strict $1/400$ / full Gate B & unpaid / open \\`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- The preamble-only glyphtounicode input was resolved with kpsewhich and checked against the audited SHA-256; its non-content mapping table was not expanded. The original command, source line, and dependency hash are retained in the reading layer.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#thm:classification` → `sections/3_classification.tex#L17` (existing project target or original TeX label line).
- Link relocation: `#thm:classification` → `sections/3_classification.tex#L17` (existing project target or original TeX label line).
