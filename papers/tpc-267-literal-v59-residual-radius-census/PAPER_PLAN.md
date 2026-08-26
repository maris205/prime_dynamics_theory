# TPC-267 paper plan

## Question

What does the exact rank-three residual look like on finite, physically
instantiated V59 data once the prime shell, unit masks, deleted diagonal,
beta coefficient, and shifted-prime comparison are all present?

## Contribution

Freeze the coarse source comparison (b_x^{(2)}), an explicit normalized
Fourier kernel family

\[
 K_{H,s}(h)=\bigl(1+(h/H)^2\bigr)^{-s},\qquad s\in\{1,2\},
\]

and the four consecutive-block Haar frame.  A rational interval replay then
certifies, for twelve natural finite clock rows, the exact decomposition

\[
 C=C_3+C_\perp,
 \qquad |C_\perp|/\bigl(\|(I-P_3)w\|\|(I-P_3)A\beta\|\bigr)<1/4.
\]

This is the first finite replay in this branch using the physical prime shell
and the source-shaped coefficients rather than a synthetic Schur witness.

## Evidence package

1. `code/tpc267_literal_residual_radius_certificate.py` computes the exact
   rational operator and outward rational intervals for logarithms and the
   Euler-product tail.
2. `experiments/tpc267_independent_checker.py` independently replays all
   twelve rows and performs mutation tests.
3. `experiments/tpc267_kernel_stress.py` checks the interval/radial guards.
4. The proof and theorem ledgers separate finite certification from an
   asymptotic V59 estimate.

## Non-claim

The chosen finite Fourier profile and rounded clocks are explicit modeling
choices.  The certificate does not prove a uniform sector theorem, a power
saving for the asymptotic residual radius, arithmetic `L2`, full Gate B, or
the twin-prime conjecture.
