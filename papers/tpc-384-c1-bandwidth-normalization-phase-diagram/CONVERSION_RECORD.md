# TPC-384 conversion record

## Conversion identity

- **Repository source commit:** `75e23fe44efae6c677b440ed8149eaacd31e2323`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `30f23e31aafb8793f25e8992b6a8de0f8e1b8e9eb8b7c5e084288e483f1e2c08`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `f8fe10a8f9a2051c636a759d34baa855dfcdbd345085ac47b18261ad43920ac1`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and frozen protocol` | 28 | 1 | 4 |
| `Matrix construction` | 53 | 1 | 2 |
| `Results` | 75 | 2 | 1 |
| `Verification and claim boundary` | 119 | 2 | 4 |

The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audit

- Source has `5` displayed-equation environment markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
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
