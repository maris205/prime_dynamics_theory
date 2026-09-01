# TPC-323 computational protocol

## Frozen panel

```text
H = 66
X = {640, 1280, 2560}
Q = {24, 36, 54, 80}
s = {1, 2}
rows = 24
```

## Paths

The producer accumulates blocks in increasing and decreasing prime order.  It
retains SciPy-forward, NumPy-forward, and NumPy-reverse profiles for the
direct Gram and each of four coherent Grams.  The independent checker uses a
fresh reverse-order `einsum` reconstruction and NumPy eigensolver.

## Numerical rules

- negative eigensolver noise is clipped at zero before normalisation;
- profile classification tolerance is `1e-10`;
- reported scalar intervals expand extrema by `1e-12`;
- all profile dimensions are `X/2` and all traces must be positive;
- floating profile digests are retained as producer provenance hints, while
  the independent checker validates numerical metrics and labels rather than
  requiring byte equality of last-bit eigensolver output.

## Stored observables

For each law and row the certificate stores energy-ratio intervals, TV,
Lorenz/Ky-Fan cumulative discrepancy, integrated discrepancy, minimum and
maximum interior prefix difference, path labels, and profile digests.  It does
not store a claim-bearing asymptotic extrapolation.
