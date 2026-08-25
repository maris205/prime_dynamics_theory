# Paper Plan

**Title:** Binary Refinement Calculus and Singleton Degeneracy for
Declared-Block V59 Margins
**Author:** Liang Wang
**Affiliation:** School of Electronic Information and Communications,
Huazhong University of Science and Technology (HUST), Wuhan, China
**Date:** August 25, 2026
**Type:** finite Hilbert-space structural theory note
**Page target:** 4--6 pages

## One-sentence contribution

Binary block refinement is an exact rank-one orthogonal range extension that
transfers one covariance from the transverse to the longitudinal term,
decreases the exact transverse radius, and culminates at a singleton
partition whose TPC-251 margin equals---but cannot improve---the direct
external bound.

## Claims--evidence matrix

| Claim | Evidence | Status | Paper location |
|---|---|---|---|
| `M_P'=M_P+z tensor z` | Orthogonal range decomposition after one binary split | Proved exact | Theorem 1 |
| Exact `C_long` and `Q_trans` covariance updates | Orthogonality and conjugate-first expansion | Proved exact | Theorem 1 |
| `R_trans(P')<=R_trans(P)` | Residual Pythagoras plus Cauchy--Schwarz on the two child blocks | Proved exact | Theorem 1 |
| Fixed-family projected Gram has rank-one subtraction | Apply `I-M_P'=(I-M_P)-z tensor z` to unchanged probes | Proved with fixed-family scope | Proposition 2 |
| Native common repartition is not that matrix update | Input/output probe labels and vectors change | Scope firewall | Proposition 2 discussion |
| Singleton projected probes, Gram, `D,L,mu,U,Q_trans,R_trans,R_coh` vanish | `M_singleton=I` | Proved universal finite | Corollary 3 |
| `kappa` remains undefined at singleton `D=0` | TPC-250 domain convention | Proved/recorded | Corollary 3 |
| Maximum declared-partition margin equals direct external bound | TPC-251 enclosure for the upper bound; singleton attainment | Proved universal | Theorem 4 |
| Resulting decomposition metrics for one fixed `A,beta,w` can change under refinement | Exact two-coordinate swap replay | Verified existential synthetic | Proposition 5 |
| Every source changes under refinement | Stable same-source fixture and zero contrast increment | Refuted | Proposition 5 discussion |
| Actual V59 coarse nonzero contrast or arithmetic gain | No source estimate supplied | Open/not claimed | Limitations |

## Structure

1. Abstract: refinement law, radius monotonicity, singleton collapse, and
   margin optimality.
2. Source lock and definitions: import only the finite TPC-247/TPC-251 scalar
   and TPC-250 total conventions.
3. Binary refinement theorem: projector, covariance, and radius calculations.
4. Fixed-family projected Gram and native-indexing firewall.
5. Singleton degeneracy and global partition-margin optimization.
6. Two-coordinate non-invariance witness and stable-source counterexample.
7. Exact verification, limitations, and conclusion.

## Figure and table plan

`NO_FIGURE_REQUIRED`. The central relation is one orthogonal direct sum. A
compact table compares the coarse and singleton values of the same synthetic
two-coordinate source.

## Citation plan

Use only the verified project-local TPC-247, TPC-250, and TPC-251 papers. No
external priority, historical, venue, DOI, or literature-survey claim is made.

## Audit plan

The mathematical pass checks conjugation, contrast normalization, residual
Pythagoras, the difference between `R_trans` and `R_coh`, fixed-family Gram
scope, singleton `D=0`, and the maximization quantifiers. The release pass
checks canonical JSON, mutation rejection, 192 exact-rational families,
normal/optimized byte identity, a warning-free 4--6 page PDF, embedded fonts,
and rendered-page visual integrity.
