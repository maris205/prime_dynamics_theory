# TPC-323 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `88c46824c79e9c202a698cf4db36fcaf98260537`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `7a12b337d235bb312dccd6fee87b3d80909f85cd2788e658636bd8ed3a421fe4`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `888998d2a0354ae021699b5e95efe7332cbbc4fa4f8e070e5565aa3df8905107`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7544ae36acbbdf6b7b1cabc24136ac55e04df3cc7c10ff8c82fdba788c5bc97c`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC320_324.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Operator and two profile coordinates` | 68 | 1 | `HEADING_TEXT_MATCH` |
| `Finite protocol and certification` | 136 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 157 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route status` | 213 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `55` before writing and `55` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b898002563ac427b1fb98c8d31fbeb5d4dd5c5ee9abe3020615ad9bbb698808f`.
- Source theorem/proof environment starts: proposition at TeX line 103, proof at TeX line 113.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 73–78 | `e168cf6b59287e8a1edd6baa034e640d1b6b709927240aa598a64334ea1e9795` |
| D02 | equation | 80–86 | `f87a0952a024703bdb69f26325b182225993fb342e54c46c575913a4ea96675c` |
| D03 | equation | 89–94 | `87806aaeada32aea4b9793d23b71ec64b5f57d7ddfa4d53336fc1fed40f19178` |
| D04 | equation | 96–101 | `662239c227266a92c56bfe9531c3bca43d91a6d6d1889fd5ef214e59739446ad` |
| D05 | \[...\] | 105–108 | `b8bae3c2c1615f151897450ff8bcf9e9592aafcb53e4a4a83f4780e95aa6ca94` |
| D06 | \[...\] | 123–125 | `d82aa9eda0a0ea203b3c7d5076a25785a9bc737e4e336edfe9d8f1975517fe17` |
| D07 | \[...\] | 130–134 | `531480ee471a2b30c569155746cc41b66020a8def89f517ae76adbae7d272d2c` |
| D08 | \[...\] | 139–141 | `4353ec3b75643e62529a31eadee274c4c71cbc00c21d5c6f03cd0909c357d611` |
| D09 | \[...\] | 190–194 | `eeaea8d67c0f99dd2e4420986d98a017bbfac6de0bdca2990f2d4e0e4d9f1188` |
| D10 | \[...\] | 226–233 | `f57f1d1132cb61e20832653b3cb3ceb70eb235d19468d0b7f9915a435d2ebbb4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `A Finite Profile-Majorization Audit}`
- TeX line 29: `We study the next finite interface in a twin-prime research route based on a`
- TeX line 41: `respectively 7, 3, and 6 mixed profile rows.  Thus finite profile selection`
- TeX line 44: `not an arithmetic cancellation theorem, a power saving, or a twin-prime`
- TeX line 54: `\(C_e=\sum_pe_pB_p\).  Its finite energy ratio can be either below or above`
- TeX line 66: `means unique among those four laws on the declared finite panel.`
- TeX line 79: `All matrices below are finite real matrices on \(\ell^2(I_X)\).  Define`
- TeX line 87: `Both Gram matrices are positive semidefinite.  Write their eigenvalues in`
- TeX line 104: `For every finite block family with positive traces,`
- TeX line 111: `knowledge of one does not determine the other.`
- TeX line 136: `\section{Finite protocol and certification}`
- TeX line 148: `The independent checker does not import the producer.  It rebuilds the`
- TeX line 159: `Table~\ref{tab:law} reports the complete finite census.  The first number in`
- TeX line 185: `profile is never below \(0.1701\).  Thus the finite shape signal is not a`
- TeX line 197: `ratio; the label is therefore not an energy-threshold restatement.`
- TeX line 203: `the only predeclared law with a uniform profile label on the full panel.  This`
- TeX line 204: `is a panel observation, not a canonical arithmetic selection theorem.`
- TeX line 215: `The strongest positive result is an operator-level finite profile readout:`
- TeX line 216: `all-plus coherent reassembly has a uniform majorization relation to the`
- TeX line 220: `prefix-sign patterns, so finite profile geometry alone does not choose a`
- TeX line 224: `weight.  The PSD Gram and finite sign laws do not reassemble the arithmetic`
- TeX line 230: `\texttt{TPC323\_FULL\_GATE\_B} &= \texttt{OPEN},\\`
- TeX line 236: `arithmetic $L^2$ interface.  Neither should be inferred from this finite`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:law` → `main.tex#L168` (existing project target or original TeX label line).
