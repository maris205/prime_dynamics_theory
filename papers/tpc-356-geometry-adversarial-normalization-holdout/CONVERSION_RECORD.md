# TPC-356 source-to-Markdown conversion

## Conversion identity

- **Repository source commit:** `642a0314e9c2a8dd7eb8a83d0bbd3e22d903b18e`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `9b2bd6205eb483cf1b971a8d61edeaeed9e63fc9c21ba4b4483fabf52c947a60`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `bbbc18b2abc402f664d08fb6b90fda7e760d49179a512ea63cfa1be0ef39c5d0`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and scope` | 40 | 1 | 3 |
| `Finite model` | 58 | 1 | 3 |
| `Geometry-only adversarial selection` | 99 | 1 | 3 |
| `Results` | 128 | 2 | 3 |
| `Exact and independent checks` | 168 | 2 | 3 |
| `Claim firewall and conclusion` | 185 | 2 | 3 |

The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audit

- Source has `4` displayed-equation markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
- The converted claim was checked against the paper README and available proof/application materials; no stronger theorem, asymptotic conclusion, physical identification, arithmetic advance, fixed-power credit, Route-B closure, or twin-prime conclusion was added.
- Proof package present: `PASS`.
- README scope boundary present: `PASS`.
- Source proof/claim symbols represented: `PASS` (displayed formulas, inequalities, sums, masks, and named quantities are retained in the Markdown math).
- Finite-only boundary preserved: `PASS` (source and available package materials state the finite synthetic scope).

### Declared prerequisites

- **Domain/premises:** use the finite synthetic assumptions stated in the source manuscript and available package materials; do not silently generalize them.
- **Exact/computational evidence:** certificate, independent checker, and stress commands remain linked where present; this conversion does not reclassify computation as an arithmetic proof.
- **Scope gate:** the finite operator, predeclared panel, computed profile, and audit language remain finite-scope objects; no scale/origin uniformity, arithmetic estimate, fixed-power credit, Route-B closure, or twin-prime conclusion is inferred.

## Audit note

This record audits provenance and theorem-boundary preservation. It is not an independent proof certificate; the TeX manuscript, proof package or available notes, code, certificate, and Bridge-B checks remain the authoritative release chain.
