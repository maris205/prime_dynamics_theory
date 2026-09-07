# TPC-336 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `938d8c8d7a447846e99018ca8e1dc65c523041e672cfc5168310620a88d1c4ab`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `890dcc16076e4267d7d275b1934d43f827776435d7cb4774da996f0d84408d1e`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c571ce52f5bb0d14d551d7a8402ea5314e51c8a89bc5db59470d40134268d9a0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC335_339.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question` | 39 | 1 | `HEADING_TEXT_MATCH` |
| `Source masks and operator` | 52 | 1 | `HEADING_TEXT_MATCH` |
| `Finite output-Gram identity` | 78 | 2 | `HEADING_TEXT_MATCH` |
| `Protocol and exact anchor` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and batch endpoint` | 152 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `36` before writing and `36` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `3de707c2a7551d9fecc87fee1a4f80b4b075afe17ccad9f32928f9e971c7dbd6`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 26–29 | `97709d08689ee65ca7dcf2478d49fd52a97832e9db6f7d3adb6774983b8915ba` |
| D02 | \[...\] | 54–57 | `b23f80747162c5c95f0fc6afd0cb56779ad4dc028ef15b938dc798fb1f92f521` |
| D03 | equation | 62–65 | `9fee4c19bd26fa29604705816d676bb54b35695d8a3314443c1758147133d87e` |
| D04 | \[...\] | 68–70 | `eaee1a80712e0f7a47e95ce3dd35525d00f12321968f3a0a3f12b88516084fa6` |
| D05 | \[...\] | 74–76 | `2c6bdfbe6540b88ce36d127ee90221b3c94c09c5e27447c98774dc2a36c952b7` |
| D06 | equation | 80–83 | `e9196f752d015452945e90add0cd5a64e4ce8716506711e1e99a9955d198d90c` |
| D07 | \[...\] | 89–92 | `28e32928b621d62dde7e1949ac0dc2faeb436488aa948c0141b8d7b808ef313f` |
| D08 | \[...\] | 106–109 | `2abc3f96bd0f1b2f0d631c17eb2c8520cca338d891e75bd362f7a0414eeb2cae` |
| D09 | \[...\] | 112–114 | `213be4907d6db5a1af7243618e0404ee05845fcb8cbdabceaaf04eedbc0c6530` |
| D10 | \[...\] | 137–139 | `01453bab4eacf2659dc78bb2b46acc7fbe7d3ee978051ec0feea68ce970a7202` |
| D11 | \[...\] | 162–166 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `TPC-335 separated the finite source residual into twin, non-twin prime-shift,`
- TeX line 35: `unchanged through the operator.  This is a finite fixed-operator obstruction,`
- TeX line 36: `not a uniform bound or a twin-prime theorem.`
- TeX line 48: `We answer this for one predeclared operator and six finite windows.  The`
- TeX line 50: `shell-uniform theorem.`
- TeX line 78: `\section{Finite output-Gram identity}`
- TeX line 79: `Since $C\beta=\sum_Cy_C$, finite bilinearity gives`
- TeX line 115: `This anchor certifies the finite output-Gram algebra only.`
- TeX line 144: `positive, but it does not overcome the larger destructive interactions.`
- TeX line 149: `overestimate the full response.  A future uniform argument must control the`
- TeX line 153: `The finite expansion \eqref{eq:response} is`
- TeX line 154: `\texttt{PROVED\_EXACT\_FINITE} for the declared model.  The six-row fixed`
- TeX line 156: `checker, and stress suite are \texttt{NUMERICALLY\_CERTIFIED\_FINITE}.  The`
- TeX line 158: `ordering transfers to all operators is \texttt{REFUTED\_SCOPED}.  A uniform`
- TeX line 160: `official route pass, and twin-prime conclusion remain \texttt{OPEN} or`
- TeX line 165: `\texttt{FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:gains` → `main.tex#L122` (existing project target or original TeX label line).
- Link relocation: `#eq:response` → `main.tex#L80` (existing project target or original TeX label line).
- Link relocation: `#eq:response` → `main.tex#L80` (existing project target or original TeX label line).
