# TPC-352 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `129df4a020d0af3b86d9de7984bfb78b418746b638cc0a835b56e6f3c100924a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `ce0fe54b111675f3103ca15d92c87080d278598659fc372bafab25362bae63cb`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `02cc6ec3f9732407d0d5c2c8a8aaeacbfe6669b66208ce3bc1e6f636dde70bfb`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and literal defect` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Exact reciprocal-shell witness` | 62 | 1 | `HEADING_TEXT_MATCH` |
| `Adversarial holdout protocol` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 122 | 2 | `HEADING_TEXT_MATCH` |
| `Exact rational anchor` | 174 | 3 | `HEADING_TEXT_MATCH` |
| `Validation and claim boundary` | 191 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 208 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 218 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `65` before writing and `65` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `884b5557b7de8c70f2f0b6511b89cfe7b143ef54e30014396c4eabb8043338ed`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 45–47 | `01b37f8b4a6af2d1ccf324ebcb05bd9438a59ad840e4434b52cb8194268a409c` |
| D02 | \[...\] | 49–53 | `2606c422fe461f9b1878b6d9c61771f1daa1c9a3d583587ecfb20e55d0a0a590` |
| D03 | equation | 65–69 | `9285ac01a51fab6f72a0325a11039286afab189f23613f3c159f875a9949b20c` |
| D04 | equation | 71–74 | `ae2718d27ec5d805262a0a07eff34afe5a22469016b2b778b32aa8f8b478308d` |
| D05 | \[...\] | 80–86 | `475363cac4bdc44474fc4e92514a213ba4d0e89354a4039724390831dd9f3dad` |
| D06 | equation | 88–92 | `e1d68edbd06d49843d34b476e0d41e48ac824c8b0763d73291971d99f151c240` |
| D07 | \[...\] | 99–107 | `0371a337733c8a7ea774efdeb534800b36511bfba5062508f3ef016a6696e1f8` |
| D08 | \[...\] | 178–181 | `ba3c9b499dc8905731d723b858f69d403df671744a997ffb7aaa32a40824f76d` |
| D09 | \[...\] | 183–187 | `441250659a15387f92dd7c3baa981fbdf49eb48388edad8653dffbbc1baee89d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 35: `finite scale repair partially transfers but no uniform repair theorem is`
- TeX line 36: `supported.  No arithmetic $L^2$ estimate, fixed-power credit, or twin-prime`
- TeX line 57: `TPC-350 found that a fixed balanced shell contrast had positive finite`
- TeX line 75: `exactly.  The rule is fixed by the shell alone; it does not depend on $o$,`
- TeX line 93: `Equations~\eqref{eq:balance}--\eqref{eq:witness} are exact finite linear`
- TeX line 122: `\section{Finite results}`
- TeX line 129: `\caption{TPC-352 paired finite holdout audit.}`
- TeX line 148: `$1.09769598704$, so the comparison is plainly not uniform.  The scale`
- TeX line 172: `scale-specific finite observation, not a scale-uniform repair.`
- TeX line 197: `text before rerunning the finite checks.`
- TeX line 201: `official evaluator pass.  The exact statements proved here are finite`
- TeX line 204: `In particular, this paper does not prove a source-uniform arithmetic $L^2$`
- TeX line 205: `estimate, a uniform masked-operator bound, a growing lower bound, a fixed-power`
- TeX line 210: `The reciprocal-shell rule transfers as a useful but non-uniform finite witness:`
- TeX line 214: `uniform shell-scale principle.  We therefore freeze this finite incidence`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:balance` → `main.tex#L73` (existing project target or original TeX label line).
- Link relocation: `#eq:witness` → `main.tex#L91` (existing project target or original TeX label line).
- Link relocation: `#tab:overall` → `main.tex#L130` (existing project target or original TeX label line).
- Link relocation: `#eq:gamma` → `main.tex#L68` (existing project target or original TeX label line).
