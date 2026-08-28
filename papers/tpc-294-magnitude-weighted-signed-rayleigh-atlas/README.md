# TPC-294 — Magnitude-weighted signed Rayleigh cancellation in finite prime shells

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

After restoring the exact Gram magnitudes discarded by TPC-293, exhaustive
equal-sign optimization gives a strict finite contraction on all 18 inherited
prime-shell rows: the globally optimal trace-normalized quotient is below one
in every row, while the all-positive vector is above one in every row.  The
unit-edge signed max-cut label is not the physical optimizer in any of the 18
rows.

This is an exact finite optimization and a numerical certificate for a frozen
literal source.  It is not a growing-shell theorem, a source-image theorem,
an arithmetic $L^2$ estimate, or a twin-prime result.

## What advances

- proves the exact trace-normalized Gram identity
  $R(a)=a^{\mathsf T}Ga/\operatorname{tr}G$
  $=1+2\sum_{i<j}a_i a_jG_{ij}/\operatorname{tr}G$;
- proves that common-denominator integerization plus Gray traversal visits
  every equal-sign labeling exactly once, so the finite sign optimum is global;
- restores Gram magnitudes and certifies all 18 finite rows with exact
  rational arithmetic;
- separates the unit-weight sign objective from the physical weighted
  Rayleigh objective: the two optima differ in 18/18 rows;
- records a strong finite atlas signal without assigning any asymptotic or
  arithmetic credit.

## Finite headline

```text
rows = 18
shell edges = 1,380
global weighted minima below 1 = 18 / 18
all-positive quotients above 1 = 18 / 18
unit-edge max-cut candidates below 1 = 18 / 18
weighted optimum differs from max-cut = 18 / 18
weighted optimum <= 1/4 = 13 / 18
weighted optimum <= 1/10 = 8 / 18
```

The strongest contraction in the declared grid is
`R_min = 0.0496374497659` at
`(N,H,Q,z,s)=(512,58,90,5,2)`.  The largest all-positive amplification is
`R_plus = 16.4393131994` at the same row.  At the earlier exceptional
exponent-crossover row `(256,38,27,5,1)`, the unit-edge max-cut label has
`R=0.988974603760`, whereas the exact weighted optimum has
`R=0.519059163428`.  Thus sign compatibility and energy compatibility are
different finite objects.

## Claim ceiling

```text
PROVED_EXACT_FINITE = trace-normalized signed quadratic identity
PROVED_EXACT_FINITE = exhaustive finite sign-domain enumeration protocol
NUMERICALLY_CERTIFIED_FINITE = exact weighted atlas on 18 frozen rows
NUMERICALLY_CERTIFIED_FINITE = 18/18 minima below one and 18/18 plus states above one
NUMERICALLY_CERTIFIED_FINITE = 18/18 weighted optima differ from unit-edge max-cut
MODELING_CHOICE = frozen literal source, shells, kernel, and 18-row grid
OPEN = source-native coefficient image
OPEN = growing weighted-shell theorem
OPEN = arithmetic L2 estimate and Gate B
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```

The finite sign vectors are chosen in the ambient equal-coefficient sign
domain.  They are not asserted to be images of any admissible source
coefficient vector.  The next natural question is therefore whether the
weighted minimizers can be reached by the source map, rather than whether
another unconstrained sign search is useful.

## Reproduction

From this project directory:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py --write
python -B code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py --check
python -B experiments/tpc294_independent_checker.py
python -B experiments/tpc294_magnitude_weighted_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent from this checkout; the local
proof package, canonical rational certificate, independent replay, stress
test, and Bridge-B checker are the available fail-closed validation path.
