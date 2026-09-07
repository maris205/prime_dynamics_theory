# TPC-393 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2e1301947de763f61dd96a9c57539b58765bb09b80614ba9a424762225e60726`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `84b6fd580dbe003bbba87f72affa8943bcabffbd2354180f7b4f70bfc69dca5e`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d86bd2aeb88d7105c0e7d417875ec849aec5f0f3692c2773fb6a807d569dc089`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Finite proxy and predeclared panel` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Certification protocol` | 97 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 113 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next clue` | 156 | 3 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 177 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `38` before writing and `38` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b3390d0cd792f30dbd731abc767397bfb4ef5b5bba8e74416b9ed78c468b3956`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 40–44 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 53–57 | `1523c178a1e7cea0660f3469721d0ba97a206c9acc487e57603ea1c06cdbd611` |
| D03 | \[...\] | 59–62 | `259cffaae82fc6234bd75e96f8b32e37600857e4899c46f9fe46002628b15cfb` |
| D04 | \[...\] | 66–68 | `ece914f570cd9d11d5436c02b0f84a9c5a6b4df9e9c24f0fb8091583be26bb28` |
| D05 | \[...\] | 86–89 | `f8eb584e2dd9ed3d01d7f11105888c440f5c84bc057ca0c70e8c143dee9e8684` |
| D06 | \[...\] | 93–95 | `858a6708d403387728e80099c468512110d847cbce00b3af68c2b4e0d56c4ab4` |
| D07 | \[...\] | 137–139 | `fc415d3ff153055b018f63e719eba37fa677f7309a9d3b003bbbedf5d3ac2b9c` |
| D08 | \[...\] | 170–172 | `c70d1b7374cd6e13d5415181ff88fd9a9e08511fada89138a283d9900fbec30e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `TPC-392 found one finite calibration-to-holdout forecast failure in a`
- TeX line 23: `target.  The 64-row certificate shows that the forecast failure does not`
- TeX line 27: `fails the Schur cap.  These are finite $c=1$ proxy observations with explicit`
- TeX line 28: `claim firewalls, not an arithmetic, asymptotic, or twin-prime theorem.`
- TeX line 43: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 47: `of finite consistency only; they cannot declare an official Route-A or`
- TeX line 50: `\section{Finite proxy and predeclared panel}`
- TeX line 52: `For $p\in(Q,2Q]$, $H=66$, and $u,v$ in a finite interval, define`
- TeX line 85: `origins available at count $N$.  The finite forecast is`
- TeX line 100: `does not import the producer: it rebuilds the same matrices in descending`
- TeX line 113: `\section{Finite results}`
- TeX line 142: `level effect remains measurable even though the forecast separation does not.`
- TeX line 146: `and all four alternating-index cells fail.  This is a finite observation on`
- TeX line 147: `five selected origins, not a source-uniform origin theorem.`
- TeX line 151: `failures occur in 0 of 32 rows.  The latter is only a finite Schur diagnostic,`
- TeX line 152: `not a growing-family Schur bound.  Conversely, the universal spectral failure`
- TeX line 153: `is a scoped obstruction to the particular $0.64$ finite envelope, not a`
- TeX line 162: `anomaly does not, together with the universal failure of the declared finite`
- TeX line 171: `\texttt{ROUND2\_CLUE=TEST\_C1\_ORIGIN\_UNIFORMITY\_AFTER\_REPLICATION}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
