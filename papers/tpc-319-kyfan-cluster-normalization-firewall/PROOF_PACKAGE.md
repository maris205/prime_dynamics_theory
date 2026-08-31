# TPC-319 proof package

## Theorem 1 (finite Ky Fan cluster envelope)

Let (G=A^*A) be the Gram matrix of any finite real matrix (A), and let
(lambda_1\ge\cdots\ge\lambda_N\ge0).  For (1\le k\le N),

\[
 F_k=\sum_{j=1}^k\lambda_j
   =\max_{\operatorname{rank}P=k}\operatorname{tr}(PG),
 qquad 0\le F_k\le\operatorname{tr}G.
\]

### Proof

Diagonalize (G=U\operatorname{diag}(\lambda_1,\ldots,\lambda_N)U^*).  For a rank-(k)
projection (P), put (q_j=(U^*PU)_{jj}).  Then (0\le q_j\le1) and
(sum_jq_j=k), while

\[
 \operatorname{tr}(PG)=\sum_j\lambda_jq_j
 \le\sum_{j=1}^k\lambda_j.
\]

Equality is obtained by projecting onto the first (k) eigenvectors.  Positivity of
the eigenvalues gives the final inequality.  \(\square\)

## Theorem 2 (normalization-flip identity)

If (N_2=2N_1) and (F_k(N_i)>0), then

\[
 \frac{F_k(N_2)/N_2}{F_k(N_1)/N_1}
 =\frac12\frac{F_k(N_2)}{F_k(N_1)}.
\]

Hence (1<F_k(N_2)/F_k(N_1)<2) is exactly the regime in which the unnormalized
mass rises while the normalized mass falls.

### Proof

Cancel (N_1) and use (N_2=2N_1).  \(\square\)

## What is certified here

The producer and its independent replay certify a declared finite panel of 24 rows,
five (k)-values, and 16 adjacent scale pairs.  All 80 normalized intervals are
strictly decreasing and all 80 unnormalized intervals are strictly increasing.  The
cluster gap and effective-rank fields are finite numerical observations supported by
the same dual eigenspectrum, not uniform spectral theorems.

No step in this package reassembles prime-shell signs into a twin-prime estimate.
