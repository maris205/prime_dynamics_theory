# TPC-354 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `1d8c547e0f9dcd4be0d6678ae197e2441c3ee66ab96465109bce7831712117d1`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `bbad18df4e3092eebb7dfe32a121272577394d3a0a58391df459590f4c33dd69`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `5372849fb1aaee41e3c4d548a2250724c2d763aa336c633b29152ced420f21c6`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 36 | 1 | `HEADING_TEXT_MATCH` |
| `Finite object and exact identities` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `Protocol and independent audit` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 170 | 2 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 191 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `58` before writing and `58` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `45b7cf715ab773bed01d0aceed1a85ac7e9218f5fc06070ba9942c88e4704adb`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 55–60 | `9cdf2cd86073fa35f25ca665261540fa17e1cc20ba1bf2343f5bc5a6366ce311` |
| D02 | equation | 63–67 | `2a94f4bf18625243f7632778f34596f0cef6dca9561963d5fb102e32ed18b4d1` |
| D03 | equation | 73–76 | `e5024e8dc51e39002d4c6d68889096ac52cd5a7f008a8ba68b430557ae1b3fd9` |
| D04 | equation | 81–85 | `e05b68087be6a837ad72986d176a67f6ee0f035c9b57de9d19c159e05cf8b1c0` |
| D05 | equation | 87–92 | `a165c93cbe55508c9cc8cec12516c39fa6ba99a451233695de7e6edbd647af40` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `Finite Transfer and Floor-Stability Firewall}`
- TeX line 25: `other protocol choice fixed.  For every finite row the identity`
- TeX line 32: `finite floor is not stable.  This is a scoped holdout result, not an`
- TeX line 38: `TPC-352 subjected a reciprocal-shell finite repair to a disjoint holdout and`
- TeX line 46: `Throughout, all conclusions are explicitly classified as finite, declared`
- TeX line 47: `model statements or numerically certified finite observations.  In particular,`
- TeX line 48: `the finite V59 convention used below is not identified with an asymptotic`
- TeX line 51: `\section{Finite object and exact identities}`
- TeX line 53: `Let $I$ be a finite interval and let $S_Q=\{p: p$ prime, $Q<p\leq 2Q\}$.`
- TeX line 62: `finite declared model`
- TeX line 68: `with the inherited finite Euler-tail enclosure and logarithm midpoint rule.`
- TeX line 71: `For any real finite matrix $A$ and finite vectors $L,b$, putting $\beta=L-b$`
- TeX line 77: `This follows by expanding the finite Euclidean square; no limit or`
- TeX line 86: `Then $R_A=1-\kappa_A$.  Cauchy--Schwarz gives the exact finite envelope`
- TeX line 93: `The envelope is an interface for a specified finite source and operator, not`
- TeX line 94: `a source-uniform operator theorem.`
- TeX line 117: `accumulates shell primes in reverse order.  It does not import the producer.`
- TeX line 161: `preserves finite positive alignment while refuting a uniform all-plus floor`
- TeX line 172: `The exact claims are the finite operator identity and Cauchy envelope.  The`
- TeX line 176: `The narrow obstruction is that positive finite transfer does not stabilize the`
- TeX line 178: `Source-level polarization also does not determine operator-level polarization;`
- TeX line 182: `No source-uniform arithmetic $L^2$ bound, uniform masked-operator bound,`
- TeX line 188: `controlled sign-law subspace; adding the same finite panel again would not pay`
- TeX line 189: `the open theorem.`
- TeX line 193: `Standard finite-dimensional Cauchy--Schwarz and polarization identities are`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:polar` → `main.tex#L75` (existing project target or original TeX label line).
- Link relocation: `#tab:summary` → `main.tex#L137` (existing project target or original TeX label line).
- Link relocation: `#tab:summary` → `main.tex#L137` (existing project target or original TeX label line).
- Link relocation: `#eq:polar` → `main.tex#L75` (existing project target or original TeX label line).
- Link relocation: `#eq:cauchy` → `main.tex#L91` (existing project target or original TeX label line).
