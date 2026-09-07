# TPC-281 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `54a03c2525e07bea8d30d26053f4577a208fa9dd5e26d9d77a6d3737affbf35d`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `0c2b6a5a07cf56231b63c2b214f47bdb296edb47053dedbddae21cecefb2dfa5`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `71c76a23f19af6fe40811791e07e5ec1cff141741129a8230dfe71d7cfcb9cbe`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC280_284.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Typed source interface` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `The exact interface theorem` | 78 | 2 | `HEADING_TEXT_MATCH` |
| `Attachment is an independent input` | 135 | 2 | `HEADING_TEXT_MATCH` |
| `Exact audit and finite transfer` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `Claim firewall and conclusion` | 214 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 235 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `92` before writing and `92` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `30b09c62389dc12de176d9ccda01927f5a552504e5233824bdbd1f7891c39c2f`.
- Source theorem/proof environment starts: theorem at TeX line 80, proof at TeX line 102, corollary at TeX line 112, proof at TeX line 121, proposition at TeX line 141, proof at TeX line 159, remark at TeX line 170.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 31–33 | `2abc1aa2e4b6ada2005c7781b8e3a1f59818a621ee78fa0047993776e7481ca1` |
| D02 | \[...\] | 52–54 | `9faee7de4e4ff308cc0458561a1566f71eca0f47d7a76437cbc72ad75579b5de` |
| D03 | \[...\] | 57–62 | `1f6979200bc7c9bb6c01dbf99c69ffde92f8c63f64f4320754415cf0c81b193f` |
| D04 | equation | 70–74 | `d0015b29e057cc6233d5872203aa2e9f671aef7fc1f437e832bfde291762527f` |
| D05 | equation | 82–86 | `bc270c9e6af2d51b068e5365b52e023be794ad4c544f08e1b26ee13c6d7ce303` |
| D06 | \[...\] | 88–92 | `f4107e3762bbb10df6f1803caeade955a9178aae1bf79944ab10b8a88745d14c` |
| D07 | equation | 94–99 | `0b4916ff8a107a4995644fceb67e81003c9ba0b28d4fadc5f44e6f680cccd3a2` |
| D08 | \[...\] | 104–107 | `0c745a35485765ab588399b4d2feedb44df2fb30f92ffc494b81a8b4579e0c08` |
| D09 | equation | 114–118 | `b5ee060c992dfa7f94c5714971befd1668b6b5a5adebc585fb373dc3b563793c` |
| D10 | \[...\] | 144–146 | `d012222c7809a9660970e8470135d6855b26a938cb9dcd11f9ac4e7509a83d9f` |
| D11 | \[...\] | 148–150 | `e86789e3a662bc6ead529cc8a329e324eb8ab09c0c709f75898b080ab5da12ef` |
| D12 | \[...\] | 152–154 | `6e45e5557b95126eed3da874b3be80ac1917a48524e52775ef4bc451e7458351` |
| D13 | \[...\] | 162–165 | `301a8adac8b85209c5f055da53a20e045c7f4367fb6a9a4b18872104abe70789` |
| D14 | \[...\] | 221–224 | `d93bb89af8aa2a71116916665e8ee2102276ff517376f16f1bec2efed9c13726` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 44: `nondegenerate attachment for the literal growing prime source remain open;`
- TeX line 68: `available, what does it actually buy at the Gate-B output?  We assume the`
- TeX line 76: `statement.  It is not inferred from a finite matrix experiment.`
- TeX line 81: `Assume \eqref{eq:hyp}.  Then`
- TeX line 109: `assumption and $D\le d_+X^a$ yield \eqref{eq:collapsed} by substitution.`
- TeX line 127: `it does not assert that the literal prime/Möbius operator has norm`
- TeX line 171: `The perpendicular functional is an information-model adversary, not a claim`
- TeX line 177: `\section{Exact audit and finite transfer}`
- TeX line 202: `Four finite interface cases instantiate the theorem with $X\in\{8,16\}$,`
- TeX line 211: `schema and coordinates only; it cannot turn a finite parent table into a`
- TeX line 229: `Gate B, and the twin-prime conclusion remain open.  The fixed-power credit is`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:hyp` → `main.tex#L73` (existing project target or original TeX label line).
- Link relocation: `#eq:two` → `main.tex#L85` (existing project target or original TeX label line).
- Link relocation: `#eq:collapsed` → `main.tex#L98` (existing project target or original TeX label line).
