# TPC-386 conversion record

## Conversion identity

- **Repository source commit:** `a8e14036a6516d08a787b6e0af53141e3dc26b13`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `566221aa309937a64049f1d631a68b67afcd67821787917611ad02969ca74e92`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `08c60631cf26c6797fdbb347d77975312e57aa470cac27917aef48507bd3c3c4`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and claim boundary` | 33 | 1 | 4 |
| `Finite proxy and frozen protocol` | 49 | 1 | 5 |
| `Certificate and exact anchor` | 81 | 2 | 4 |
| `Results` | 94 | 2 | 1 |
| `Interpretation and next step` | 133 | 2 | 4 |
| `Reproduction` | 152 | 2 | 1 |

The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audit

- Source has `4` displayed-equation environment markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
- The converted claim was checked against the paper README and `PROOF_PACKAGE.md`; no stronger theorem, asymptotic conclusion, physical identification, arithmetic advance, fixed-power credit, Route-B closure, or twin-prime conclusion was added.
- Proof package present: `PASS`.
- README scope boundary present: `PASS`.
- Source proof/claim symbols represented: `PASS` (displayed inequalities, sums, roots, and named quantities are retained in the Markdown math).
- Finite-only boundary preserved: `PASS` (source and proof package both state the finite synthetic scope).

### Declared prerequisites

- **Domain/premises:** use the finite synthetic assumptions stated in the source manuscript and its proof package; do not silently generalize them.
- **Exact/computational evidence:** certificate, independent checker, and stress commands remain linked by the package README; this conversion does not reclassify computation as an arithmetic proof.
- **Scope gate:** the source’s finite-only and open-gate language is preserved verbatim in substance.

## Audit note

This record audits provenance and theorem-boundary preservation. It is not an independent proof certificate; the TeX manuscript, proof package, code, certificate, and Bridge-B checks remain the authoritative release chain.
