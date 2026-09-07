# TPC-325 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `cfb1c22951f76172000ceb8435f0b1b7f00443dc2089b9c3daa589c7cdb54963`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `ae2288f21b7f685ced7869f6f7a74ccfc9eff630c317fd784cfc1510fa92a22a`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `0a55be7f268effd8a6d0e3928093119be141c7afb284ba699d59d9b3370bce3d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC325_329.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Exact structure and protocol` | 66 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and obstruction` | 136 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 156 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 170 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `36` before writing and `36` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b9cf0ad2d3deb12023fc7bb29fafab34e05d0adef3379324933175baef76d334`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 37–42 | `4e18a0b31bfb3ab9d9aee6a1e2ad47878fc7b1f30517393797c8f8055508b466` |
| D02 | equation | 44–48 | `1842b68555a54f18476f7315fce336680e514b316afc1fdaad089e90e57cb222` |
| D03 | \[...\] | 53–57 | `a298a3d8339d423a70153b4f3e9f6d708ccfeb43454df1a7968e484bca7bdbb9` |
| D04 | equation* | 146–150 | `3f1494a0538048542d5e774accea947cdefdf0bd9dddaefff33996648b25cbf6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{A Finite Source--Scale Ladder for Signed Prime--Shell Spectral Profiles}`
- TeX line 17: `TPC--324 replicated a finite signed spectral-profile pattern at new source`
- TeX line 26: `rungs.  These are finite numerical certificates and observations, not an`
- TeX line 60: `The principal claim is deliberately finite:`
- TeX line 62: `\textbf{NUMERICALLY CERTIFIED FINITE:} all-plus majorization on $32/32$`
- TeX line 68: `Every Gram above is of the form $A^*A$ (or a finite sum of such matrices), so`
- TeX line 69: `positive semidefiniteness and positive spectral-profile typing are exact finite`
- TeX line 90: `strictly.  The numbers are outward-rounded finite diagnostics.`
- TeX line 94: `\caption{All-plus finite scale ladder.}`
- TeX line 139: `fixed-origin finite scale audit.  It does not establish that the four-rung`
- TeX line 140: `envelopes have a limit, or that a profile law is uniform for arbitrary source`
- TeX line 142: `dimension, so their comparison is not an identity under unitary translation.`
- TeX line 149: `\texttt{FULL\_GATE\_B = OPEN}.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#tab:ladder` → `main.tex#L95` (existing project target or original TeX label line).
