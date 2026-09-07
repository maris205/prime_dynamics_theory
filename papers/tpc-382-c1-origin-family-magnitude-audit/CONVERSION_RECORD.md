# TPC-382 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f1b2e8f52496c7a698b5bb281ba5b28691be833e52f902c8e2fe7d014766e187`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `c95539aaef4b8b8f9588f10a36c271e31f8893ea3c50271d270388328ca0b438`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `39b1bdd40261dc2be3e091f0fb7db29716103d7ed2847760752bf1a592de2025`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 29 | 1 | `HEADING_TEXT_MATCH` |
| `Locked protocol` | 44 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Verification and claim firewall` | 106 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `34` before writing and `34` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `eee6c7ea5134a511978064c05dd220168af19c960dd16712c44f8334e36190d7`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 49–51 | `a7b8b38449e710c043ddff3162093972a0a540e5df926867116649c23676e6cc` |
| D02 | \[...\] | 67–71 | `4dd48667dee8ba09ab9b5fa6bef08bc514e487a05e7749b365cdd4ae3a6951a6` |
| D03 | \[...\] | 97–100 | `770c663d4ac6a5193f813f364ec520b4d7a92d8d66b281b8fb9abe2f51905380` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{TPC-382: A Finite \(c=1\) Origin-Family Magnitude Audit}`
- TeX line 16: `We audit the magnitude, rather than only the threshold profile, of a finite`
- TeX line 25: `finite certificate results.  They do not establish source validity, an`
- TeX line 26: `asymptotic uniformity theorem, arithmetic power saving, or a twin-prime result.`
- TeX line 31: `The preceding origin-family replay preserved the finite band failure profile`
- TeX line 32: `but left magnitude stability as an explicit open diagnostic.  We ask two`
- TeX line 33: `finite questions:`
- TeX line 103: `is a finite refutation of that narrowly stated hypothesis, not a theorem of`
- TeX line 104: `scale non-uniformity.`
- TeX line 110: `The finite proof package therefore certifies the arithmetic transformation of`
- TeX line 111: `the locked parent rows and the stated finite comparisons.  The official`
- TeX line 121: `parent locks and row census & PROVED\_EXACT\_FINITE\\`
- TeX line 122: `all-plus high-\(Q\) one-percent stability & NUMERICALLY CERTIFIED, FINITE SCOPED\\`
- TeX line 123: `law-dependent spread census & NUMERICALLY CERTIFIED, FINITE SCOPED\\`
- TeX line 124: `matched-count one-percent scale hypothesis & REFUTED, FINITE SCOPED\\`
- TeX line 125: `source-valid normalization, growing bound, arithmetic \(L^2\) & OPEN\\`
- TeX line 126: `Route-A / Route-B gates & OPEN\\`
- TeX line 133: `\texttt{FIXED\_POWER\_CREDIT}=0.  The next finite test is the predeclared`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
