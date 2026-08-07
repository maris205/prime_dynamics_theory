# RH Program Roadmap after RH-384

## Completed within the frozen branch

RH-384 pays the prime-scale translation budget left open by RH-383. It source-locks a prime-counting theorem, proves the fixed-r Abel constant, converts each fixed partition to a precise `p_y`/log scale, and locates the independent `P_2` contribution strictly between `T_y^2` and `T_y^3`.

The new closed chain is:

1. RH-374 supplies square-clock Euler products and run arithmetic.
2. RH-379 freezes the phasewise Chowla-free memory class.
3. RH-380 proves square-clock monotonicity and finite-clock nonattainment.
4. RH-381 gives the leading `T_y` gap and a quadratic remainder.
5. RH-382 separates `T_y^2` and `P_2(y)` with an `O(T_y^3)` remainder.
6. RH-383 supplies the exact all-order partition normal form.
7. RH-384 proves `P_r(y)` for fixed `r`, the fixed-partition scale compiler, and five normalized gap limits.

## Route decisions

- Route A: `GO`. The fixed-r/fixed-partition prime-scale theorem and gap normalization are complete.
- Route B: `STOP_SCOPED`. Nothing here supplies a spectral operator, completed zeta divisor, or new RH implication.

## Closed local questions

- The Abel constant is `1/(2r-1)`, including the negative strict-endpoint boundary.
- The fixed-partition `p_y` exponent is `2d-ell`; its log exponent is `ell`.
- `T_y^3=o(S_y)` and `S_y=o(T_y^2)`.
- The twice-subtracted residual has positive `S_y` coefficient and is logarithmically larger than `T_y^3`.
- The interval quantity is explicitly `Y_infinity-2*m_infinity`, while `C` is that quantity divided by `pi^2`.

## Still unpaid

The following are separate theorem budgets, not continuations licensed by RH-384:

- any effective PNT remainder or computable eventual-sign threshold;
- uniformity when `r`, partition degree, or partition length grows with `y`;
- a nonzero phasewise `c11` correlation theorem;
- a growing-clock or exchanged-limit theorem;
- an intrinsic determinant or scattering completion;
- a self-adjoint generator;
- von Mangoldt weighted prime-power trace identities;
- equality with the divisor of a completed zeta function.

Gates A–E remain false/open. The next valid successor must introduce and source-lock one of these missing edges explicitly. Finite certificate rows cannot pay that budget.
