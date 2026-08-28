# TPC-295 paper plan

## Question

TPC-294 found ambient equal-sign weighted minimizers but left “source image”
open.  What exactly is the finite source-side image, and are the minimizing
sign targets attainable under a natural linear correlation map?

## Claim spine

1. Treat the physical shell vectors as columns of a rational matrix $A$.
2. Define the source-correlation map $A^{\mathsf T}$ and prove the full-rank
   surjectivity lemma with explicit witness $A(A^{\mathsf T}A)^{-1}b$.
3. Certify full column rank of the inherited 18 Gram matrices by independent
   modular determinants.
4. Transfer the result to every TPC-294 weighted minimizer and max-cut/all-
   positive target using exact modular residual checks.
5. Record the remaining native-profile and norm-budget obstruction without
   claiming an arithmetic or asymptotic result.

## Claim ceiling

The linear-algebra implication is exact.  Modular full rank and target
feasibility are finite certificates.  The unrestricted source space is an
explicit modeling choice; the original source class, growing-shell
uniformity, arithmetic $L^2$, and Gate B remain open.
