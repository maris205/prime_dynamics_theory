# TPC-360 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `b5c36960b7ec3250d584b0c565e90115bde34fd04c0db9b9090e6e89f01fb681`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `25404832447873d08db71c6cfa0ae99b1cb7602aad587dda9305b8b3f596d03f`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a74c6477b2e3c15f21fc411c6fc876e533aa4d0927b230e6ccb879f7aee351eb`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md), [experiments/protocol.md](experiments/protocol.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Operator and finite protocol` | 45 | 1 | `HEADING_TEXT_MATCH` |
| `Finite envelope facts` | 68 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `Audits and claim firewall` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 134 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `27` before writing and `27` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `bf72b5c8a845c5e26385bedf4ef6472f83bbf0540988daa1fd0c3db17f449b55`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 49–54 | `463b07bcd825c9c5f39b96744a93bcec005dffec45306073985fcf5e93307670` |
| D02 | equation | 57–61 | `2e8657b4873251f3dcc136f216b5ac98dbcff131d75aa993358ced345eea3841` |
| D03 | equation | 71–76 | `f19ed74f092540f230bc104e7f2c2738d4064549e1f616c7e69b0aee7c4dc1a7` |
| D04 | equation | 100–105 | `56b11c20aa602386b69cfc964c6c2e576facff11b911c68d8dee1d2c3cce56b6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{Schur Slack and Sign-Law Uniformity in a Normalized Prime-Shell Operator}`
- TeX line 21: `We audit two possible weaknesses in a finite normalized operator certificate:`
- TeX line 29: `law wins 6.  These are finite, scoped observations: they quantify envelope`
- TeX line 36: `TPC-359 transferred a finite normalized cap to a high-origin panel selected`
- TeX line 40: `ask whether the envelope is tight and whether a law-uniform spectral maximum`
- TeX line 45: `\section{Operator and finite protocol}`
- TeX line 68: `\section{Finite envelope facts}`
- TeX line 70: `For every finite real symmetric matrix $T$,`
- TeX line 77: `The inequalities are exact finite statements.  We use the ratios`
- TeX line 106: `Thus, within this finite panel, the Schur envelope has at least`
- TeX line 108: `Frobenius envelope has at least 0.37889122745866566.  This does not mean that`
- TeX line 114: `win.  Consequently all-plus is a useful finite stress law, but the winner`
- TeX line 128: `The maximum justified claim is therefore a numerically certified finite`
- TeX line 129: `Schur-tightness and law-uniform audit.  The exact envelope inequalities are`
- TeX line 130: `proved only for finite matrices.  Source-uniform arithmetic $L^2$, a growing`
- TeX line 132: `twin-prime endpoint remain open.`
- TeX line 136: `The finite normalized cap is not close to saturation by either elementary`
- TeX line 140: `all four laws in the spectral audit.  Nothing in this finite diagnostic pays`
- TeX line 146: `\texttt{TPC360\_FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
