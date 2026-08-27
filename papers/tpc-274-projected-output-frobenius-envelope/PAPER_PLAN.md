# TPC-274 paper plan

## Question

After TPC-273 showed that the normalized margin can move across finite cutoff
bands, can a cancellation-free norm estimate still control the output residual
lane on the same literal V59 operator?

## Frozen object

- TPC-268's released finite operator, prime shell, masks, deleted diagonal,
  exact beta source, and three four-block Haar contrasts;
- TPC-269's registered growing-cutoff schedule on
  `N=64,96,128,192,256,384`;
- kernel exponents `s=1,2` as a matched control;
- no synthetic source vector and no replacement of the physical output.

## Claim-bearing contributions

1. Prove the projected Frobenius inequality
   `G_perp <= ||(I-P_3)A||_F^2 ||beta||_2^2`.
2. Construct the projected matrix exactly over rational arithmetic and verify its
   multiplication against the released output engine.
3. Certify all 12 rows: the envelope-to-actual output-energy ratio is above 50,
   while the margin proxy obtained by inserting the envelope is below `1/8`.
4. Interpret this as a scoped insufficiency of cancellation-free output control,
   not as a source-level counterexample or an asymptotic statement.

## Evaluation policy

The Route-B local fallback evaluates the exact inequality, independent matrix
replay, five hostile mutations, PDF, and normal/optimized reproducibility.
Route A is not claimed: no arithmetic `L2`, growing theorem, or signed
four-packet reassembly is supplied.
