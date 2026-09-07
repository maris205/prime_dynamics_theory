# TPC-391 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `46480bc66366188408a8f9979b1023e71244fc57b26096a3403accb50df076a7`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `a17026aa1d2d9365ee81ab8774f7c040b7b301ec7a7ca40032009fd563bfa50d`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `67fee3b7506b91f6124f2bf42215c222c0a6f39a19fb4b89af71da7354a25a98`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Finite proxy` | 57 | 1 | `HEADING_TEXT_MATCH` |
| `Forecast trajectory` | 73 | 2 | `HEADING_TEXT_MATCH` |
| `Certification and finite result` | 102 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next clue` | 156 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 169 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `57` before writing and `57` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `33615ddcb5a504731ff5ea08f707935d5fc8f65f0fb1a72916e28a78970099a5`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–40 | `d3f4fb8f401d2792fee672908d15e995f99373c15b981ebf9280e89db9c36a3c` |
| D02 | \[...\] | 49–53 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D03 | align* | 60–64 | `56f851d416802d2953adc2c69573c54ab07ea8f03b0d1239ac208f52ce06bb72` |
| D04 | \[...\] | 78–81 | `0ce11fa965bda150c01aac02b5bdeb6d0d37019fa5f91891d98f6a69e726b3b1` |
| D05 | \[...\] | 84–89 | `557d44a6d621c8780580fe59150ad8cae0a82b101ec413f2ecdb59188b3be453` |
| D06 | \[...\] | 91–95 | `6af8844bb0d6dec2cd48edab8df4bc6d072cc9753c0d86dc93f81daf4a0ba4a0` |
| D07 | \[...\] | 163–165 | `a50a5f0c6264e171196a166165fc48f3c43d147d677ed252404255fb5395efec` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `TPC-390 located a finite recursive forecast failure but did not identify its`
- TeX line 27: `identity has residual at most $4.44\times10^{-16}$.  This is a finite`
- TeX line 52: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 57: `\section{Finite proxy}`
- TeX line 65: `The row geometry is the finite square energy`
- TeX line 98: `its declared forecast, minus one.  A finite pass requires absolute error at`
- TeX line 102: `\section{Certification and finite result}`
- TeX line 106: `the same finite matrices in descending shell order, recomputes row metrics,`
- TeX line 113: `certificate; all decimal values are finite diagnostics, not claimed limits.`
- TeX line 117: `\caption{TPC-391 finite horizon-localization census.}`
- TeX line 145: `and its terminal maximum error is $0.0166412350$.  Thus the finite evidence`
- TeX line 147: `on this family.  It does not identify a universal source of the mismatch:`
- TeX line 148: `band, law, normalization, and origin uniformity remain open questions.`
- TeX line 153: `fixed-three-block, pooled, alternating-index $Q=8192$ cell.  The finite`
- TeX line 166: `No arithmetic power credit is assigned, and Route-A/Route-B reassembly and`
- TeX line 167: `the twin-prime endpoint remain open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
