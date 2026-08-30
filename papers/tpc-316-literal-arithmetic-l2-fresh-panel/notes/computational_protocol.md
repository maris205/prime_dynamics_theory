# TPC-316 computational protocol

## Locked inputs

* Physical engine: `papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py`.
* Engine normalized-LF SHA-256:
  `e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3`.
* Height `H=66`.
* Shells `S_Q={p prime: Q<p<=2Q}` for `Q=24,36,54,80`.
* Kernel exponents `s=1,2`.
* Source panels `I_640={321,...,640}` and `I_1280={641,...,1280}`.

## Exact calculation

The producer uses Python `Fraction` values.  It computes the Hilbert--Schmidt
mass by summing the exact signed-difference count and computes each coordinate
column directly from the matrix formula.  Exact rational values are sealed by
numerator/denominator SHA-256 digests; decimal strings are display views only.

The five coordinate offsets are `0`, `floor((N-1)/4)`,
`floor((N-1)/2)`, `floor(3(N-1)/4)`, and `N-1`.  The best probe is selected by
exact comparison, with the smallest column index breaking ties.

## Independent and hostile checks

The independent checker has its own sieve, count implementation, direct
small-panel mass replay, and direct coordinate calculation.  The stress suite
checks 155 signed differences, a nontrivial signed-vector Frobenius
inequality, kernel symmetry, deleted-diagonal behavior, and certificate
firewall fields in normal and optimized Python modes.

No floating-point value participates in a pass/fail decision.
