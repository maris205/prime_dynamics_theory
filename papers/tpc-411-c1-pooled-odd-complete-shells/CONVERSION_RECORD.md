# TPC-411 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `43403dc5ddc8eeec037bdd316725f5929dd7616bc7fcdc913acd347e127b46d0`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `1e55bf1dacd4ba2589c657651064dee02c59eb9163b76ef7d7b07c88c2ffb39e`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `eb6e34fded6b33fb0addab23704a58fc140a6e647a1385e357d008a692af78df`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Pooled complete-shell profile` | 22 | 1 | `HEADING_TEXT_MATCH` |
| `Finite pooled theorem` | 47 | 1 | `HEADING_TEXT_MATCH` |
| `Exact certificate and observation` | 69 | 2 | `HEADING_TEXT_MATCH` |
| `Route boundary` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 93 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `47` before writing and `47` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c0fa0ce9a8d7d26da8d1034ed4e9acbe94a8ff3d65d54b8b56425369828f47fd`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 27–30 | `196c71e0d3f11021e718a739789907af05d60b36fa6f664752b4a0c690a7ea5e` |
| D02 | \[...\] | 32–35 | `a158af3c9c0d6e46f31e83fa7b4577bb61ec4821a3777b9cf0b3c88b96039925` |
| D03 | \[...\] | 37–40 | `80fc41f28fe2baa248235d5483252cf89c96f91c22670a07a35a11b9d5d6a7aa` |
| D04 | \[...\] | 42–44 | `117e3d90a4573521a043f829c143ed1810f871ef776a54ca2c6adb7a960bbf16` |
| D05 | \[...\] | 50–53 | `4335c200a8d658f3af0e8ad83df93f6ee8e38978ed287a16b97f2444228c29e7` |
| D06 | \[...\] | 60–63 | `3603fa5fb8e6247765e7e2535b2698aa9f5952906aa21099e09d997a25976f25` |
| D07 | \[...\] | 72–77 | `d43475eee5f763bef84da6781b7be8dd1b04def097c80c9864384a08ac41f06c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `the pooled row.  This is a synthetic finite proxy result, not an arithmetic`
- TeX line 45: `The parameter $H$ is a proxy height, not the physical $h_0$.`
- TeX line 47: `\section{Finite pooled theorem}`
- TeX line 78: `and the finite observation $Hz=0.344313597135425$.  This decimal is derived`
- TeX line 79: `from an exact rational square and is not an asymptotic claim.  The independent`
- TeX line 85: `This is one finite pooled synthetic adjacent normalized proxy entry.  It does`
- TeX line 86: `not prove a full normalized operator estimate, identify physical $h_0$ or`
- TeX line 88: `or imply a twin-prime result.  The exact finite pooled odd complete-shell`
- TeX line 91: `\texttt{OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
