# TPC-324 computational protocol

## Frozen source panels

```text
training union (TPC-323): [321,640] U [641,1280] U [1281,2560]
continuation: [2561,2880], [2881,3520], [3521,4800]
gap_offset:   [5001,5320], [6001,6640], [8001,9280]
H = 66
Q = {24,36,54,80}
s = {1,2}
rows = 2 * 3 * 4 * 2 = 48
```

## Numerical paths

The producer retains forward matrix multiplication, reverse `einsum`
accumulation, and SciPy/NumPy spectral paths.  The independent checker uses
a separately written reverse `einsum` reconstruction and NumPy
`eigvalsh`.  Negative eigensolver noise is clipped at zero; profile labels
use tolerance `1e-10`; scalar intervals expand path extrema by `1e-12`.

Long profile digests are provenance hints.  The independent checker validates
recomputed metrics, labels, geometry, and outward interval containment rather
than demanding byte equality of last-bit LAPACK eigenvectors/eigenvalues.

## Falsification rule

Any all-plus reverse/mixed/unresolved row, any panel overlap, or any mismatch
with the frozen per-panel census fails the certificate.  No row is removed
after computation.
