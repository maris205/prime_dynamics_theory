# TPC-376 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `aab0c41888af0737120aeb5f3c8c79e7e34126e4f206d598544e3b07f63d044e`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `fa467b50ba3a40590eeda3fefb080c3997c88facfaf3c0abbf332cac6f0ccfa7`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `349335d14306ab9ab808e18a236f4595e56c93360ef67e50874115cbe968d521`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `Finite normalized object` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `Response-blind holdout protocol` | 98 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 133 | 2 | `HEADING_TEXT_MATCH` |
| `Audit and reproducibility` | 179 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 195 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `65` before writing and `65` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `bc664b6dfff102da08f6875760fe80305ec9bda65ed715342778343207e35975`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 67–72 | `082b630fb88393592d133ec55b1ca9ffc9315655f0094b4bdf44297d2bf7920e` |
| D02 | equation | 74–77 | `c9de90680d18353f2873d222faa87fb640e32993a5a1724641c515617b09d3c3` |
| D03 | equation | 79–81 | `526825d7cfdbb60784887e63394f7c114c37a81805d1a31affc55c14370bec42` |
| D04 | equation | 83–86 | `a471cedfb0280eaa51ab741867fa6f09e0726dd13c8cf52b1dd28f6bb1bcbc2a` |
| D05 | equation | 92–95 | `3cf99f918547388eba257ee982130b1e61f5988594414190e8116a450db784eb` |
| D06 | \[...\] | 101–103 | `56a57c691da83ea3911785f4cb52e410fefc10c8da2946e3ab8675e2e9759dc1` |
| D07 | \[...\] | 106–108 | `8a17ddbd01ace32f372c5d93c590194883972585857d53da1bd2d85f34b7efd1` |
| D08 | \[...\] | 167–171 | `1022429ddad18a36edfbfddc738f18a6b12f7ed89989cad69d205f75843b4f4c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 7: `for the Finite \(c=1\) Bandwidth Rule}`
- TeX line 21: `{\large for the Finite \(c=1\) Bandwidth Rule\par}`
- TeX line 31: `TPC-375 found that the first member of a finite block-band menu matching its`
- TeX line 40: `$0.93760019185559207$ and $0.976941204869197$.  The result is a finite`
- TeX line 42: `nearby training windows, and no origin-uniform, growing, arithmetic, or`
- TeX line 48: `The recent finite TPC audits locate a recurring high-$Q$ spectral signal in`
- TeX line 56: `The present result is deliberately finite.  The term \textit{holdout} means`
- TeX line 57: `a set of grid indices fixed independently of the signed response; it does not`
- TeX line 63: `\section{Finite normalized object}`
- TeX line 88: `The geometry is a finite sum of rational squares.  At the exact anchor`
- TeX line 96: `These are finite identities and carry no assertion about a growing family.`
- TeX line 116: `\caption{Frozen protocol and finite census.}`
- TeX line 174: `symmetry, and the finite Schur/Frobenius envelopes.  A separate checker`
- TeX line 184: `by LF-normalized SHA-256; the independent checker does not import the`
- TeX line 188: `The exact finite statements are the fixed grid protocol, the finite`
- TeX line 199: `This is a concrete finite transfer edge from TPC-375, while the overlap`
- TeX line 201: `sample-independence language.  Origin/window uniformity, cross-block`
- TeX line 202: `causality, a growing operator estimate, source-uniform arithmetic $L^2$,`
- TeX line 203: `fixed-power credit, and the twin-prime endpoint remain open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
