# TPC-210 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `acac5b7dd2e6d4b96bc292630cf8bae22d82dc00b8f08741c11662cc0002deba`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `4bc8b8f42e6244e15f3bb966531481c8f76e757d41cec8fa0aa5d3fb835ccc52`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `67a001c12baa42bd7534e9162f64ded7c199685908d5332ceadd60fd661fb036`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a756cf5e0149dc261fb556e089f802ebda1d1e03b028c8d1a67241e3ffaacbb9`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC210_214.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction and claim ceiling` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `The profile interface` | 107 | 2 | `HEADING_TEXT_MATCH` |
| `Exact finite profile interpolation` | 141 | 2 | `HEADING_TEXT_MATCH` |
| `Mobius-weighted aligned profiles` | 194 | 3 | `HEADING_TEXT_MATCH` |
| `The exact missing object: a cross-divisor Gram theorem` | 243 | 4 | `HEADING_TEXT_MATCH` |
| `Finite certificate` | 298 | 5 | `HEADING_TEXT_MATCH` |
| `Source boundary and route decision` | 336 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 358 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 373 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `89` before writing and `89` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `20`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a7a281a1d6f3840443407f078173988c3e7b1baf1c610ce89dc9423ae0da9ff8`.
- Source theorem/proof environment starts: theorem at TeX line 153, proof at TeX line 175, remark at TeX line 187, proposition at TeX line 209, proof at TeX line 228, proposition at TeX line 253, proof at TeX line 270.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 70–72 | `04b5c0e7edfb997e243256c11643e6de8114ca7cb0e97ef4834cad6ef5bd677b` |
| D02 | \[...\] | 94–96 | `cd3186d073321544c4513c3725f545d5b76cb56067ab5298063cfd89724e191a` |
| D03 | \[...\] | 110–114 | `4cf6c0562e0716de29cd65e9839950cc144bafdb43ac45e4afdaaaf74396633a` |
| D04 | \[...\] | 117–123 | `166f38076c9c015a47540314a3f5235c870c3a1f52c7ca7316b49e0ab16db589` |
| D05 | \[...\] | 126–129 | `5c072984f42c06645cd33d642524d4c2e94f50bad0c0a79c7d46243ba7720911` |
| D06 | \[...\] | 133–137 | `6ebda1eefe9a031d95ccf3414e81afcc1a75f677dc601adafad55a7bbd27ecc2` |
| D07 | \[...\] | 144–148 | `9d44181520f9647b21a1b01427e336b50ea51aea393ff4ebabb7422dbb66a918` |
| D08 | \[...\] | 156–161 | `3c0a59e753927e3a39dd21a7b9a2b1d16280563c8023c2eb5477acbb6017cc38` |
| D09 | \[...\] | 164–169 | `ac987a59142f35d0973267e080aacb16c791c330fcd1c3ef6349597eafe8c72d` |
| D10 | \[...\] | 197–200 | `1096b44f6426cfd8b37be2fef1974996cda82dd386d6c00910ea28b118e4930a` |
| D11 | \[...\] | 202–205 | `119090590c24e0b2b577f92bd736d5050668d2fd7d71296a5f765fa3d7a89d41` |
| D12 | \[...\] | 212–215 | `4b4c328ac70966595d5eea1bb9185ce6b8ab5cdfd431afdca0fc812d40a0ee02` |
| D13 | \[...\] | 217–224 | `d8358cf986aa2a8e69668ae970a254dc7686b678dfdf3a822fce25b0ba2e86d1` |
| D14 | \[...\] | 230–232 | `c6fe7e47c8420a93e4432431837d59657c717ce05910aa0213c1629f619954f1` |
| D15 | \[...\] | 246–251 | `1b590ce2266e4674260d8549ee02e8a264c07fa997f19b97a4e5cdce94c98fa7` |
| D16 | \[...\] | 257–261 | `85c392ae7a6fad72ca62255d429cb4732b1c9af2621249535dd822b02b20ae4a` |
| D17 | \[...\] | 263–266 | `3c9a0f015139edf81f6087ddb876d2a472f32e3c010057a5ffeda8484dac4c9a` |
| D18 | \[...\] | 278–281 | `2344360187708fe7ce2b76bbff5981a7f5416dc75529e9ebe9c899f6fea962b7` |
| D19 | \[...\] | 290–294 | `e9a557af22633d47712eee8c5acc9d48891cfc70ef4766f7c0ae109282316f69` |
| D20 | \[...\] | 347–356 | `5894f024d7e0f5d5597d125a15c68bf1be45005b94cd0131830fbbaf3f708328` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `pdfsubject={Finite profile interpolation, Mobius alignment, and the TPC-210 scoped obstruction}`
- TeX line 47: `finite residue profiles, leaving open whether Schwartz regularity and the`
- TeX line 49: `structure.  We prove that they do not at finite modulus.  For every prime`
- TeX line 56: `profile-aware energy as a positive-semidefinite cross-divisor Gram quadratic`
- TeX line 61: `the strict $1/400$ gate, and the twin-prime endpoint remain open.`
- TeX line 99: `\item finite residue-profile interpolation is proved exactly;`
- TeX line 141: `\section{Exact finite profile interpolation}`
- TeX line 153: `\begin{theorem}[finite profile interpolation]`
- TeX line 171: `$\C^{\Gq}$, and any finite family of target profiles is realized by choosing`
- TeX line 188: `The theorem is finite and exact.  It does not say that a single physical`
- TeX line 196: `Let $\cD$ be a finite set of squarefree integers coprime to $q$, and put`
- TeX line 255: `The matrix $G=(G_{D,E})_{D,E\in\cD}$ is Hermitian positive semidefinite and`
- TeX line 272: `Hermitian positive semidefinite.  Finally, $U_D^*P_qU_D=P_q$, so (5.3)`
- TeX line 284: `arithmetic target is not a profile-norm estimate.  It is a theorem that uses`
- TeX line 298: `\section{Finite certificate}`
- TeX line 307: `\caption{TPC-210 finite certificate.}`
- TeX line 333: `The certificate is a finite QA artifact.  It verifies the exact construction;`
- TeX line 338: `TPC-209 left open a profile-aware prime-only estimate after the exact return to`
- TeX line 350: `\texttt{ACTUAL\_PHYSICAL\_PROFILE\_BOUND=OPEN},\\`
- TeX line 351: `\texttt{FULL\_GATE\_B=OPEN},\quad`
- TeX line 361: `packets can interpolate arbitrary finite residue profiles, and literal Mobius`
- TeX line 367: `This does not settle the twin-prime problem and does not negate the possibility`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#thm:interpolation` → `main.tex#L154` (existing project target or original TeX label line).
