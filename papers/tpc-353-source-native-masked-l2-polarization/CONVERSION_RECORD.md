# TPC-353 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `fb33baf2c557c8d4dff1066afa6268d6b2178a1cc34e1b0d5a41a15f307d8a8e`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `76382ed910887321bbc562f022e67b8fa20f6fed92cb4ec0e6c2a9a48282795c`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2201206623d8f9fb83e6ac124dfe5fb9b5aaf4207516ea40c37dfdac4647f966`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `Finite object and exact identities` | 52 | 1 | `HEADING_TEXT_MATCH` |
| `Protocol and independent audit` | 97 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 125 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 164 | 2 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 182 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `54` before writing and `54` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `dd6c33738cfc3e300eb3a35266c80a83aaacd120da3ec2b6dd4ec13ecd854ef5`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 56–61 | `9cdf2cd86073fa35f25ca665261540fa17e1cc20ba1bf2343f5bc5a6366ce311` |
| D02 | equation | 64–68 | `2a94f4bf18625243f7632778f34596f0cef6dca9561963d5fb102e32ed18b4d1` |
| D03 | equation | 74–77 | `e5024e8dc51e39002d4c6d68889096ac52cd5a7f008a8ba68b430557ae1b3fd9` |
| D04 | equation | 82–86 | `f0de171d96ed0f7391d577d5e24f532f1ad2be91c26d4a5d2b68e361a1e5c09b` |
| D05 | equation | 88–93 | `a165c93cbe55508c9cc8cec12516c39fa6ba99a451233695de7e6edbd647af40` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `Exact Operator Attachment and Finite Firewall}`
- TeX line 24: `operator-only envelopes.  We attach the declared finite residual to the`
- TeX line 26: `every finite row the identity`
- TeX line 33: `geometry substantially.  This is a finite attachment and a scoped obstruction`
- TeX line 40: `TPC-352 subjected a reciprocal-shell finite repair to a disjoint holdout and`
- TeX line 44: `the source or the masks?  The answer here is yes at the finite algebraic`
- TeX line 47: `Throughout, all conclusions are explicitly classified as finite, declared`
- TeX line 48: `model statements or numerically certified finite observations.  In particular,`
- TeX line 49: `the finite V59 convention used below is not identified with an asymptotic`
- TeX line 52: `\section{Finite object and exact identities}`
- TeX line 54: `Let $I$ be a finite interval and let $S_Q=\{p: p$ prime, $Q<p\leq 2Q\}$.`
- TeX line 63: `finite declared model`
- TeX line 69: `with the inherited finite Euler-tail enclosure and logarithm midpoint rule.`
- TeX line 72: `For any real finite matrix $A$ and finite vectors $L,b$, putting $\beta=L-b$`
- TeX line 78: `This follows by expanding the finite Euclidean square; no limit or`
- TeX line 87: `Then $R_A=1-\kappa_A$.  Cauchy--Schwarz gives the exact finite envelope`
- TeX line 94: `The envelope is an interface for a specified finite source and operator, not`
- TeX line 95: `a source-uniform operator theorem.`
- TeX line 116: `accumulates shell primes in reverse order.  It does not import the producer.`
- TeX line 156: `is a finite observation, not a law-independent source theorem.`
- TeX line 166: `The exact claims are the finite operator identity and Cauchy envelope.  The`
- TeX line 170: `polarization does not determine operator-level polarization; consequently a`
- TeX line 173: `No source-uniform arithmetic $L^2$ bound, uniform masked-operator bound,`
- TeX line 179: `position-aware masked bound; adding the same finite panel again would not pay`
- TeX line 180: `the open theorem.`
- TeX line 184: `Standard finite-dimensional Cauchy--Schwarz and polarization identities are`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:polar` → `main.tex#L76` (existing project target or original TeX label line).
- Link relocation: `#tab:summary` → `main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#tab:summary` → `main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#eq:polar` → `main.tex#L76` (existing project target or original TeX label line).
- Link relocation: `#eq:cauchy` → `main.tex#L92` (existing project target or original TeX label line).
