# TPC-321 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `88c46824c79e9c202a698cf4db36fcaf98260537`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `d11718e7b80813a1f48ade6c01be903f4d73db7f24f7224480e46953450f24ab`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `9307c4d6fd02d55f50470cb94466221a9ea9570be3d6553968a93a22e017292a`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `de0e786e174413ba7bd0b4535675a8bc2a77e4f31d521798b113d43a6e9d8dc8`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC320_324.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen operator and normalized profile` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Profile distances and the majorization firewall` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `Protocol and finite enclosure` | 142 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 168 | 2 | `HEADING_TEXT_MATCH` |
| `Route status and conclusion` | 219 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 242 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `74` before writing and `74` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `90137b6f1b397e2124420e85c0f5aab2ac57e77c168a23c1505bdd364abb5987`.
- Source theorem/proof environment starts: proposition at TeX line 88, proof at TeX line 93, proposition at TeX line 124, proof at TeX line 129, remark at TeX line 207.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 69–74 | `334b8cc24cd73655088e45ab807c93d25097090e1fc729dfa0f2f0b2a20d8314` |
| D02 | equation | 77–80 | `f7c7d6029be8b4eca482a447f9e4755771f1392bfe4431be885205460d1934eb` |
| D03 | \[...\] | 82–85 | `b9f5d93ad7666d62806b42d9d5db0003058efa5be7da585b646a75ca51a91b14` |
| D04 | \[...\] | 101–103 | `d82aa9eda0a0ea203b3c7d5076a25785a9bc737e4e336edfe9d8f1975517fe17` |
| D05 | equation | 105–109 | `af0201f44bba948f687d22cf3bcfc452c38cde1fc6a7cd8e74d22f45bc73cc1d` |
| D06 | equation | 110–113 | `b35eb0dfbf7bd0586541d08580e0a92d4e1eb629f3b893c2357f27c4f66ce393` |
| D07 | \[...\] | 145–148 | `f467f27b70b35170b3cdf41d35e2be77df4a1b00f2461a41da240acbb49be133` |
| D08 | \[...\] | 157–160 | `28cc420582c417d0eae50687ee53cde5584502a737c12ad8cbadc037045722f7` |
| D09 | \[...\] | 197–200 | `3f90795becd3e321a0f292749d5e87ba69368d813a2b705e4ac9c1e75be3d0be` |
| D10 | \[...\] | 210–212 | `86983d3bea8635a3d130613a874c11defbea65d8ddca65fcbeddf39d77b0074b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `We continue a finite structural audit of a deleted-diagonal, centered`
- TeX line 31: `stable when the prime shell changes.  For a positive-semidefinite Gram matrix`
- TeX line 39: `single shell-monotone profile law is a finite-panel obstruction, not an`
- TeX line 43: `remain open.`
- TeX line 60: `eigenvalue masses in rank order.  The result is deliberately finite.  It is`
- TeX line 62: `18 numerical comparisons into a uniform statement about the primes.`
- TeX line 81: `It is positive semidefinite by construction.  Write $N=|I_X|$ and`
- TeX line 104: `We use three finite diagnostics:`
- TeX line 120: `all $r<N$.  A finite sign tolerance $\tau=10^{-8}$ is used only to classify`
- TeX line 124: `\begin{proposition}[finite metric facts]`
- TeX line 131: `absolute value and the finite $\ell^1$ norm.  Since $p$ and $q$ are probability`
- TeX line 142: `\section{Protocol and finite enclosure}`
- TeX line 161: `This is an outward finite numerical guard, not an interval theorem for`
- TeX line 203: `finite panel refutes both a universal forward direction and a universal`
- TeX line 209: `the finite-panel status`
- TeX line 211: `\texttt{REFUTED\_FINITE\_PANEL}.`
- TeX line 213: `It is not a theorem that all larger shells`
- TeX line 216: `model, not a replacement theorem.`
- TeX line 228: `The arithmetic gates remain open.  The Gram construction squares an unsigned`
- TeX line 230: `bilinear estimate.  Consequently this paper supplies no arithmetic`
- TeX line 233: `checkout; the local Bridge-B checker is a fail-closed record of the finite`
- TeX line 239: `does (or does not) survive the arithmetic step.  Neither should be inferred`
- TeX line 240: `from this finite audit alone.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:dist` → `main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:integrated` → `main.tex#L112` (existing project target or original TeX label line).
- Link relocation: `#tab:distances` → `main.tex#L180` (existing project target or original TeX label line).
