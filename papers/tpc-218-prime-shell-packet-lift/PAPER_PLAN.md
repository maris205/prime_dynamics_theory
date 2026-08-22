# TPC-218 Paper Plan

## Title

Prime-Shell Hilbert Lift and the Sharp Collapse Barrier

## Research question

Can the TPC-217 finite-window large-sieve attachment retain the literal prime
label and four-packet label long enough to expose, rather than hide, the exact
cost of scalar prime-shell reassembly?

## Main structural theorem

For fixed packet count J and bounded packet profiles,

~~~
N^(-1) sum_(n in I_x)||K_vec(n)||_2^2
  << J M^2 x^(1/96)(log x)^5.
~~~

The proof is the standard additive large sieve tensored with
ell^2({q,j}), fixed-q cutoff injectivity, and an elementary harmonic bound for
the literal cluster coefficients.

## Scalar corollary

Pointwise Cauchy over P=#Q_x gives

~~~
N^(-1) sum_(n in I_x)sum_j|K_j(n)|^2
  << J M^2 x^(11/32)(log x)^5.
~~~

The P factor is explicit and is not arithmetic progress.

## Adversarial controls

1. Exact q alignment with four labels gives coherent/diagonal ratio P=4.
2. Parallel four-packet vectors give unit-projection ratio 1.

## Claim classes

~~~
PROVED_STRUCTURAL_L1 = Hilbert lift, label preservation, exponent ledger, PSD packet bound
NUMERICALLY_CERTIFIED = finite dilation and large-sieve fixtures
REFUTED_SCOPED = free q orthogonality and geometry-only packet cancellation
OPEN = signed prime-shell reassembly, four-packet arithmetic cancellation, full Gate B
ARITHMETIC_ADVANCE = NO
~~~
