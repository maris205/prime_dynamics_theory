# Paper Plan

**Title:** Source-Frozen Rank-Midpoint Contrasts for the Literal V59 Scalar
**Author:** Liang Wang
**Affiliation:** School of Electronic Information and Communications,
Huazhong University of Science and Technology (HUST), Wuhan, China
**Date:** August 25, 2026
**Type:** finite Hilbert-space structural theory note
**Page target:** 4--6 pages

## One-sentence contribution

The ordered physical interval supplies a coefficient-independent rank
midpoint whose normalized Haar contrast gives exact rational-projector,
partial-sum, longitudinal/transverse covariance, literal TPC-247 kernel, and
safe-adjoint formulas without deciding the arithmetic sign or scale.

## Claims--evidence matrix

| Claim | Evidence | Status | Paper location |
|---|---|---|---|
| The rank split depends only on ordered `I_x` and `x` | Definition before all coefficients and margins | Proved source-only deterministic | Definition 1 |
| `rho^2=ell*r/N`, zero sum, unit norm, and uniqueness with positive sign on `L` | Direct cardinality and normalization calculation | Proved exact | Proposition 1 |
| `M_mid=M_coarse+z tensor z` | Orthogonal child-flat decomposition | Proved exact | Proposition 1 |
| Integer split ends at `floor(3k/4)` | Four residue classes `k mod 4` | Proved exact | Proposition 2 |
| Exact partial-sum moments and both longitudinal formulas | Direct summation and block averaging | Proved exact | Theorem 3 |
| Conjugate-first covariance transfer and opposite `Q` update | Rank-one projector identity | Proved exact | Theorem 3 |
| Midpoint residual equals within-child covariance | Childwise centering | Proved exact | Theorem 3 |
| Literal TPC-247 kernel expansion retains every factor | Direct substitution of `A_x(u,t)` | Proved exact formal compiler | Proposition 4 |
| `<z,A_x beta>=<A_x^*z,beta>` without self-adjointness | Finite adjoint definition | Proved exact | Proposition 4 |
| Constant factors annihilate; `w=z,g=+-z` give both signs | Exact finite controls | Verified nonliteral synthetic | Proposition 5 |
| Midpoint sign, nonzero value, scale, or arithmetic gain | No source estimate of both literal contrasts | Open/not claimed | Limitations |

## Structure

1. Abstract: exact compiler, integer crosswalk, literal kernel, and claim ceiling.
2. Introduction and frozen source scope.
3. Rank midpoint, normalization, projector, and integer crosswalk.
4. Partial-sum longitudinal/transverse compiler and within-child covariance.
5. Literal TPC-247 kernel expansion and safe adjoint orientation.
6. Sharp nonliteral controls, exact verification, limitations, and conclusion.

## Figure and table plan

`NO_FIGURE_REQUIRED`. A compact four-row table records the `x mod 4`
crosswalk. The main object is an exact rank-one identity, so a diagram would
not improve precision.

## Citation plan

Use only the verified project-local TPC-247 and TPC-252 papers. TPC-247 fixes
the literal source operator; TPC-252 supplies the general binary rank-one
transfer that is specialized here. No external priority, venue, DOI, or
literature-survey claim is made.

## Audit plan

The mathematical pass checks quantifier order, arbitrary real clocks with
`N>=2`, the integer-only threshold crosswalk, first-slot conjugation, the
opposite transverse update, exact rational projector products, every literal
kernel factor, adjoint orientation, and synthetic/nonliteral labels. The
release pass checks strict canonical JSON, at least 25 mutations, 192 exact
families, normal/optimized byte identity, a warning-free 4--6 page PDF,
embedded fonts, and every externally rendered page.
