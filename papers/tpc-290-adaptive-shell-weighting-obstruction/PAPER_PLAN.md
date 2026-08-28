# TPC-290 paper plan

## Question

Can an adaptive choice of nonnegative coefficients on the literal prime
components turn the physical output shell from amplification into decay?

## Claim spine

1. Define the weighted physical ratio
   `R(w)=||sum_q w_q g_q||_2^2 / sum_q w_q^2 d_q` and the effective support
   `kappa(w)=(sum_q w_q)^2/sum_q w_q^2`.
2. Prove the exact weighted Gram identity.
3. Prove that nonnegative weights cannot produce decay when all off-diagonal
   Gram entries are nonnegative.
4. Prove the conditional diffuse lower bound
   `R(w)>=1+eta*delta*(kappa(w)-1)` under the TPC-289 coherence and diagonal
   balance hypotheses.
5. Use equal two-component nonnegative supports to expose the precise sparse
   escape created by a negative cross term.

## Finite test

Replay the TPC-289 18-row grid with three full-support policies: uniform,
inverse-diagonal, and linear shell taper.  Also audit every equal two-prime
support and every leave-one-prime-out uniform support.

## Claim ceiling

The weighted lemmas are exact.  The 54 policy rows and sparse support census
are finite numerical certificates.  No growing-shell weighted theorem,
source-uniform arithmetic `L2` estimate, or twin-prime conclusion is claimed.
