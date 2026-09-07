# TPC-408 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `dfa9755da88919c5162d214355ca6dd135f3823284e8f9c622ecb048007a027a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `411761c4ece08f6d5ec712f2bf10d6372677a6e458945110281fcd7ad37b528e`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `be79b8366e2ab02080f949cf4f56387986d8f6b2494bd976352010718ad0b434`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Odd complete-shell extension` | 24 | 1 | `HEADING_TEXT_MATCH` |
| `Finite theorem` | 45 | 1 | `HEADING_TEXT_MATCH` |
| `\,Exact certificate` | 66 | 2 | `HEADING_TEXT_MATCH` |
| `\,Route boundary` | 83 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 92 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `47` before writing and `47` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7d97143e2d8f15abad6e84dc6ef36961cefe4610b2005534971bbe8f09807fc1`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 28–31 | `a158af3c9c0d6e46f31e83fa7b4577bb61ec4821a3777b9cf0b3c88b96039925` |
| D02 | \[...\] | 33–36 | `80fc41f28fe2baa248235d5483252cf89c96f91c22670a07a35a11b9d5d6a7aa` |
| D03 | \[...\] | 40–42 | `117e3d90a4573521a043f829c143ed1810f871ef776a54ca2c6adb7a960bbf16` |
| D04 | \[...\] | 48–51 | `29388c58274db6bafda747d59456837beefcec2ba2a2f32834e305318d11209a` |
| D05 | \[...\] | 58–61 | `3603fa5fb8e6247765e7e2535b2698aa9f5952906aa21099e09d997a25976f25` |
| D06 | \[...\] | 69–75 | `b07f0eea632040fc2d05a0dc3515365b8b3eca8a16222d49de91327b6a2cb402` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `complete prime shells.  This note extends the finite audit to the next two`
- TeX line 20: `replay verify both rows.  This remains one synthetic proxy entry and makes`
- TeX line 21: `no arithmetic or twin-prime claim.`
- TeX line 43: `The height $H$ here is a proxy parameter, not the physical $h_0$.`
- TeX line 45: `\section{Finite theorem}`
- TeX line 77: `$0.344391172918121$.  These decimals are finite float64 observations only;`
- TeX line 84: `This is a finite extension of one synthetic adjacent normalized proxy entry.`
- TeX line 85: `It is not a full normalized operator estimate, a physical $h_0$ theorem, an`
- TeX line 87: `closure, or a twin-prime result.  The claim status is the exact finite`
- TeX line 90: `is \texttt{OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
