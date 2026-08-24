# TPC-239 Paper Plan

## One-sentence contribution

Primitive physical buckets compile into reduced prime progressions, so a
source-backed Brun--Titchmarsh estimate improves the TPC-237 finite-window packet
trace by `log x/loglog x` while leaving its fixed-power exponent `1/48`
unchanged.

## Claim--evidence matrix

| Claim | Evidence | Classification | Paper location |
|---|---|---|---|
| A primitive bucket is bounded by a sum of reduced prime AP counts | Exact congruence `m q^(-1)=a mod h`, unit propagation, and TPC-236 internal row injectivity | Analytic theorem | Section 3 |
| The AP census is at most the factor-16 envelope | Standard Brun--Titchmarsh bound and `#M_h^x<=2M_h<=4hQ/H` | Source-backed analytic theorem | Section 3 |
| The V59 maximum row is `<<x^(1/96)loglog x/log x` | `Q/U=x^(1/1200)`, maximal order of `h/phi(h)`, and exact Fraction arithmetic | Analytic corollary | Section 4 |
| The finite-window trace is `<<JM^2x^(1/48)(log x)^4loglog x` | Exact TPC-237 composition with its direct-energy and reduced-frequency large-sieve interfaces | Analytic theorem | Section 4 |
| The improvement over TPC-237 is logarithmic only | Side-by-side loss ledger | Exact comparison | Sections 1 and 4 |
| The fixture has a three-row primitive collision and obeys both upper bounds | Complete finite enumeration and an independent reconstruction | Numerical finite illustration only | Section 5 |

## Narrative

The paper begins with the one new arithmetic interface: primitivity turns the
physical congruence into a reduced prime progression. It then proves the factor
`16` without hiding constants, specializes the result at V59, and substitutes it
at the same point in the TPC-237 composition. The closing sections separate the
logarithmic route advance from the unchanged fixed-power obstruction.

## Section plan

1. **Abstract.** State the compiler, factor `16`, packet-trace bound, and
   logarithmic-only status.
2. **Introduction.** Explain why the row factor is the only modified interface;
   preview the strongest result and claim ceiling.
3. **Frozen source and setup.** Restate the exact TPC-237 kernel, TPC-236 row
   incidence, and the locally verified Brun--Titchmarsh source boundary.
4. **Primitive AP compiler.** Prove the `h=1` branch, reduced classes, AP census,
   and factor `16`.
5. **V59 composition.** Derive the maximum row, insert it before the large
   sieve, and compute the exact exponent and logarithm ledgers.
6. **Finite certificate.** Describe deterministic JSON, strict types,
   independent reconstruction, stress grid, and mutation firewalls.
7. **Route evaluation.** State the obstruction, open theorem, reusable
   structure, and next-round clue.
8. **Conclusion.** Summarize the honest advance.
9. **Status appendix.** Give machine-readable vocabulary and declarations.

## Comparison table plan

The paper uses one compact table comparing TPC-237 and TPC-239 at the row,
normalized trace, and fixed-power levels. A plot would not clarify this exact
symbolic comparison, so no figure is planned.

## Citation plan

The bibliography contains only `MontgomeryVaughan2007`, the sole cited source.
The local TPC-61 source explicitly invokes its interval Brun--Titchmarsh theorem.
No page-level scan of the book is stored in the repository; that boundary is
stated verbatim in the paper and audit note.

## Claim ceiling

No sentence may imply `C_h` signed cancellation, an actual signed four-packet
projection, arithmetic `L2`, fixed-atom credit, strict `1/400`, Gate B, a
twin-prime result, a fixed-power saving over TPC-237, or sharpness.
