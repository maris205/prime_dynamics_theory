# TPC-295 — Source-correlation image and finite signed feasibility

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

Let $A=[g_q]$ be the finite physical shell matrix from TPC-294.  On every one
of the 18 inherited rows, two independent modular determinant certificates
give full column rank for $G=A^{\mathsf T}A$.  Consequently the source-side
correlation map $A^{\mathsf T}:\mathbb Q^{I}\to\mathbb Q^{S}$ is surjective:
every TPC-294 sign target, including each weighted Rayleigh minimizer, has an
exact finite source-coordinate witness
$h=A G^{-1}a$.

This closes the broad unrestricted finite source-correlation question.  It
does not prove that the witnesses lie in the original low-complexity source
profile, satisfy interval-valued arithmetic constraints, or remain controlled
as the shell grows.

## What advances

- proves the exact linear-algebra implication
  `rank(A^T A)=|S| => im(A^T)=Q^S`;
- gives the explicit witness formula `h=A G^{-1}b` for any target `b`;
- certifies full rank on all 18 TPC-294 rows using the independent moduli
  `1000000007` and `998244353`;
- shows that all 18 weighted minimizer sign patterns are realizable in the
  unrestricted finite rational source space;
- moves the real open question from sign attainability to source-class
  admissibility and witness-norm/budget control.

## Finite headline

```text
rows = 18
shell edges = 1,380
full rank mod 1000000007 = 18 / 18
full rank mod 998244353 = 18 / 18
unrestricted source-correlation surjective = 18 / 18
TPC-294 weighted minimizers source-realizable = 18 / 18
restricted native profile theorem = OPEN
source witness norm budget = OPEN
```

The largest shell has 17 columns.  At the representative late row
`(N,H,Q,z,s)=(512,58,90,5,2)`, the determinant residues are
`98453757 mod 1000000007` and `233740651 mod 998244353`, both nonzero.

## Claim ceiling

```text
PROVED_EXACT_FINITE = full-rank implication and explicit source witness formula
NUMERICALLY_CERTIFIED_FINITE = two-modulus full-rank atlas on 18 rows
NUMERICALLY_CERTIFIED_FINITE = unrestricted source-correlation surjectivity 18/18
NUMERICALLY_CERTIFIED_FINITE = TPC-294 weighted minimizer feasibility 18/18 in Q^I
MODELING_CHOICE = unrestricted finite rational source-coordinate space
OPEN = restricted native source profile / interval-weight image
OPEN = source witness norm and growing-shell control
OPEN = arithmetic L2, fixed-power credit, Gate B
TWIN_PRIME_RESULT = NONE
```

The word “source-realizable” is deliberately qualified: it means realizable
under the explicitly declared finite map $A^{\mathsf T}$ with unrestricted
rational source coordinates.  It is not a theorem about the frozen Mobius or
comparison-weight profile.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc295_source_correlation_image_certificate.py --write
python -B code/tpc295_source_correlation_image_certificate.py --check
python -B experiments/tpc295_independent_checker.py
python -B experiments/tpc295_source_image_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent from this checkout; the local
proof package, canonical certificate, independent replay, stress test, and
Bridge-B checker are the available fail-closed validation path.
