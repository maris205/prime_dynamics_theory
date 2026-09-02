# TPC-352 computational protocol

The panel is the Cartesian product of 3 origins, 3 lengths, 4 shell anchors,
2 exponents, and 2 source laws: `144` rows.  Each row constructs the literal
physical and unmasked matrices in double precision, forms their defect, and
computes the reciprocal and balanced incidence responses and spectral norms.

The reciprocal coefficients are computed as `Fraction` values and converted
to floating point only for matrix-vector evaluation.  The exact anchor uses
`Fraction` matrices at `I=[193,206]`, `Q=4`, exponent 1, all-plus signs.
Normal and optimized Python runs must have empty stderr and identical stdout.
The independent checker reverses shell accumulation order and rebuilds all
rows without importing the producer.  The stress checker applies eight
mutations and requires each to fail closed.

Environment controls:

```text
PYTHONDONTWRITEBYTECODE=1
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
```
