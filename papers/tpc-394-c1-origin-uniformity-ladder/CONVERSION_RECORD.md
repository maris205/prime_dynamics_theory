# TPC-394 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `8bc3f4dd764b73ca9666e29c085bbf5e1d4ebd99935efc99c5ef5ad2f700458e`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `2f7f8ab1b07971752d2cb27251d1e382054a52f2ac137b8c28baa6f644c3b999`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `63d534923d0c8e214116c1fc7326104df29b52e24f0946c60264dc5d6e956125`.
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
| `Finite proxy and frozen origin ladder` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `Certification protocol` | 89 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 106 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next clue` | 159 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 179 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `28` before writing and `28` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `962e6d29fdffa9854ba1dc50fb656c677c716433e8f1a5f5a64f064df96447e0`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 41–45 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 54–58 | `1523c178a1e7cea0660f3469721d0ba97a206c9acc487e57603ea1c06cdbd611` |
| D03 | \[...\] | 60–63 | `259cffaae82fc6234bd75e96f8b32e37600857e4899c46f9fe46002628b15cfb` |
| D04 | \[...\] | 66–69 | `73d29dbb5c4e2cf78f724239e56355ea81dc5383ed6f48af596b5de92e3587bb` |
| D05 | \[...\] | 78–80 | `2d3bb6786e14202880fa624c8eea7c0ef0144cdac96085628298ee385c428b6d` |
| D06 | \[...\] | 82–85 | `9b46d04abad37d9c8660f10cf7e120b4190045e34e907041f6a13f92829f13f7` |
| D07 | \[...\] | 129–134 | `c7a343798ac1ad6834d72451a9c270799c9f31ce57dbf6218ae3078241cca0b4` |
| D08 | \[...\] | 136–143 | `811c342206fffee35fce711585dff7394e0c91a42cf558b7764c55b27b9a4149` |
| D09 | \[...\] | 172–174 | `63fab31d44766774824c1dd8f4214456a86d55333f2237d0a55280bdfc3cf00f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{TPC-394: A Same-Count Origin-Uniformity Ladder for a Finite $c=1$ Proxy}`
- TeX line 26: `eight cells.  The finite $0.64$ spectral cap fails on all 32 all-plus rows and`
- TeX line 27: `the Schur cap fails on no row.  These are certified finite $c=1$ proxy facts;`
- TeX line 28: `they do not establish source validity, a growing origin-uniform estimate,`
- TeX line 44: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 48: `of finite consistency only; they cannot declare an official Route-A or`
- TeX line 51: `\section{Finite proxy and frozen origin ladder}`
- TeX line 53: `For $p\in(Q,2Q]$, $H=66$, and $u,v$ in a finite interval, set`
- TeX line 92: `checker does not import the producer: it rebuilds the matrices in descending`
- TeX line 100: `The producer and checker use float64 only for the finite matrix calculation;`
- TeX line 106: `\section{Finite results}`
- TeX line 144: `Thus the finite split is strongly law-dependent and is not removed by any of`
- TeX line 151: `this records finite cancellation in the selected proxy only.`
- TeX line 155: `Schur cap.  The Schur result is a finite diagnostic and not a growing Schur`
- TeX line 157: `finite cap, not an asymptotic statement.`
- TeX line 166: `nine percent.  This supports a finite law-dependent obstruction hypothesis,`
- TeX line 167: `not a source-uniform theorem.`
- TeX line 177: `argument exists, no arithmetic power credit is assigned.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
