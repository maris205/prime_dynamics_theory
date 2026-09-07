# TPC-386 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `566221aa309937a64049f1d631a68b67afcd67821787917611ad02969ca74e92`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `08c60631cf26c6797fdbb347d77975312e57aa470cac27917aef48507bd3c3c4`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `08ce8aac7f6333cdcfc4faca319e3b7be99f604f8edb3b9210a4f144731d2fa8`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `Finite proxy and frozen protocol` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Certificate and exact anchor` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 94 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next step` | 133 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 152 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `64` before writing and `64` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9e040993826f29a29949d036bd53879790389bded5b8a5c14f5479f5dcf9a93d`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 40–44 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 52–56 | `53f8042701001239a26c5943d04cbe21892fe5640fbb65ec0f9b96b101be0d31` |
| D03 | \[...\] | 59–61 | `251511bb23d9b66defbfc68016bc8cc8476073a99c2cf49a7f079a55d63c2f8a` |
| D04 | \[...\] | 145–147 | `a408e1260edefbbc21892a4c096cd422267d795ee006af1ce2088b8d213aeeac` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{TPC-386: A Count Holdout for the Finite $c=1$ Bandwidth Proxy}`
- TeX line 18: `The preceding TPC-385 experiment transferred a finite high-bandwidth phase`
- TeX line 25: `$1.0652$ to $1.1295$, while the inherited finite spectral diagnostic`
- TeX line 28: `The result is a finite count-transfer observation and a scoped obstruction`
- TeX line 29: `to promoting the old cap to a count-uniform statement.  It proves no`
- TeX line 30: `growing operator bound and makes no arithmetic claim about twin primes.`
- TeX line 35: `We work in one fixed finite dynamical-system family.  The question is whether`
- TeX line 38: `The distinction matters: a finite origin holdout and a bound uniform in the`
- TeX line 43: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 49: `\section{Finite proxy and frozen protocol}`
- TeX line 79: `declared finite audit threshold, not a theorem.`
- TeX line 91: `four signed matrices on this anchor.  This exact check validates the finite`
- TeX line 118: `All four ratios lie inside the declared $20\%$ finite audit envelope, but`
- TeX line 119: `that observation does not establish count uniformity.  Relative to the`
- TeX line 127: `The signed laws remain controls rather than a uniformity certificate.  For`
- TeX line 136: `transfer inside a broad finite envelope.  The strongest obstruction is the`
- TeX line 148: `Any resulting statement must remain finite until a genuine growing-$N$`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
