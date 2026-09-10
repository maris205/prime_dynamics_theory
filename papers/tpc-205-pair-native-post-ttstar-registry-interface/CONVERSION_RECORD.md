# TPC-205 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `f5586627671e99323e924875a1c066c49ca1a1bb8c210e65b2b3f185887b19d7`.
- Bibliography: [references.bib](references.bib), SHA-256 `075ea70cddc268f03916d603f0c0a1e7d11f0a459b4d9ce153d2f138c9b48fba`.
- Preserved PDF: [tpc-205-pair-native-post-ttstar-registry-interface.pdf](tpc-205-pair-native-post-ttstar-registry-interface.pdf), SHA-256 `b3596e207943132ad48e6a17cfd107421f02b521bc02f617615c860816a1dc1e`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b29ee4cae1eeaa89cbd403f7fb84ab5bbdbe945f8ea2efa24eedf4984f9a69ee`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC205_209.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Authorization and level boundary` | 43 | 1 | `HEADING_TEXT_MATCH` |
| `The ordered post-TT-star carrier` | 58 | 1 | `HEADING_TEXT_MATCH` |
| `Conditional source--child composition` | 119 | 2 | `HEADING_TEXT_MATCH` |
| `Registry contract and finite nonvacuity` | 158 | 2 | `HEADING_TEXT_MATCH` |
| `Normalization and physical-loss firewall` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `H1 type separation and final verdict` | 246 | 3 | `HEADING_TEXT_MATCH` |
| `Machine certificate and trust boundary` | 302 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 320 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `56` before writing and `56` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `d99f8208e68af7807c27489f2b30f0eb937fdc83494b25f0b5bc302ea479992f`.
- Source theorem/proof environment starts: theorem at TeX line 81, proof at TeX line 92, theorem at TeX line 139, proof at TeX line 151, theorem at TeX line 266, proof at TeX line 281.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 65–69 | `0917fe494a84f75c29d01a5098d38ba81dc315e026a35acdfa7f8a23e82ca4af` |
| D02 | equation | 73–79 | `88980b9a9ef65163092de770feb178bdb0d09fa72b995a160a8c2f120a3acaed` |
| D03 | align | 100–110 | `bc479aa4c33f792059e6dd7bde9defca816f453b04691026fb5ccd48fe33ca9e` |
| D04 | \[...\] | 122–124 | `8b42ce4ffc75d17be83f1a3d7898c0eab956fda2a73ad09fba0c3941d644ff1b` |
| D05 | equation | 128–132 | `74d1a1c5eddbb986608177ad16b0a11c49cd7987c3258e70cec23c3e420d7f01` |
| D06 | \[...\] | 181–183 | `ec11ea372fa58097749705a1dfac978a1347fb9307b02edcaa66358d7996efe3` |
| D07 | \[...\] | 185–189 | `206185687502423646a58212bf9c347c70765e1a4a874d3c292d7d047624d444` |
| D08 | \[...\] | 196–199 | `0fda3c55b382a004d329d44c499cd93621dd3a76a8c08a9c5e4dc8bff995fd6a` |
| D09 | \[...\] | 201–204 | `796dbcb1c01f684197deecca8ab3313692437f28bb695c24f779c0237e43cd12` |
| D10 | equation | 219–224 | `fed83dc2c7cd9d705b7a55d7677f889468e886b80e89f321118c14d0ab063ce6` |
| D11 | \[...\] | 233–239 | `5131a494e65b0bc9cfbb643c81b7fe70a63351d7acaa0d3dbd255354f0bf24ed` |
| D12 | equation | 250–257 | `13e0b8d3addc3c2c6f74bd7952d255532e7cdb5bb71d49346fc04dd4661b2bde` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `We freeze the exact finite interface for a pair-native route beginning after`
- TeX line 36: `fail-closed registry contract, two strictly finite non-production fixtures,`
- TeX line 38: `survives only as an open architecture-reroute candidate.  This is an L0/L1`
- TeX line 39: `interface theorem, not a structural reopen, an L2 estimate, or a prime-pair`
- TeX line 45: `The authorized object is the finite interface`
- TeX line 48: `\code{FINITE_PAIR_NATIVE_POST_TTSTAR_REGISTRY_AND_}\\`
- TeX line 55: `\(L0\) for exact finite identities, schemas, and fixtures; \(L1\) for`
- TeX line 60: `Fix one TPC-18 opened-\(D\) packet.  Write`
- TeX line 63: `\(N_\alpha(j)=\ell_\alpha d_\alpha j+h_0\).`
- TeX line 88: `unsupplied; membership in the formal summation domain does not prove an`
- TeX line 94: `the TPC-18 opened-\(D\) formula.  Its support restrictions are stated as`
- TeX line 111: `Opening \(C_{m_\alpha}\) produces`
- TeX line 113: `Thus \(u\) is not a field of the parent \((\alpha,\gamma,j)\).  TPC-32 also`
- TeX line 133: `A single child does not restore the source.  The projector identity is a`
- TeX line 134: `finite identity.  On TPC-93's physical squarefree and target-primitive`
- TeX line 158: `\section{Registry contract and finite nonvacuity}`
- TeX line 167: `packet/identity scope & 16 & \(X,h_0,\delta\), scales, packet and source IDs\\`
- TeX line 182: `((103,1),(107,1),5),\qquad h_0=2.`
- TeX line 195: `For finite algebraic nonvacuity, the committed TPC-32 primitive fixture has`
- TeX line 197: `L=100,\ R=12,\ T=50,\ U_0=200,\ h_0=2,\ j=1,\quad`
- TeX line 211: `The integer \(\sigma=1\) here is not an analytic saving exponent.`
- TeX line 216: `archived string \code{nu_X} is only a scope label and not a scalar`
- TeX line 241: `hypotheses; the ledger does not compose these rows onto a production TPC-18`
- TeX line 258: `Its conceptual entries may be signed or complex.  The finite TPC-174`
- TeX line 260: `one, but its committed fixture is synthetic \citep{WangTPC174}.  By contrast,`
- TeX line 277: `its production and structural reopen triggers fail.  The pair-native`
- TeX line 278: `architecture-reroute candidate remains open.`
- TeX line 293: `architecture remain open.  The scoped cell`
- TeX line 299: `source atom or H1 edge; it does not stop a new registry, theorem crosswalk,`
- TeX line 305: `registry fields, two finite fixtures, 17 loss rows, and 23 gates.  A separate`
- TeX line 313: `The manifest is a repository review pin, not an external signature or theorem`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 9 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:carrier` → `../main.tex#L78` (existing project target or original TeX label line).
- Link relocation: `#eq:projector` → `../main.tex#L131` (existing project target or original TeX label line).
- Link relocation: `#eq:projector` → `../main.tex#L131` (existing project target or original TeX label line).
- Link relocation: `#eq:ttstar` → `../main.tex#L68` (existing project target or original TeX label line).
- Link relocation: `#thm:carrier` → `../main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#thm:conditional` → `../main.tex#L140` (existing project target or original TeX label line).
- Link relocation: `#eq:h1` → `../main.tex#L256` (existing project target or original TeX label line).
