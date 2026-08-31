# TPC-320 proof package

## Theorem 1 (finite spectral readouts)

Let \(G=A^*A\) be a finite real Gram matrix, with eigenvalues
\(\lambda_1\geq\cdots\geq\lambda_N\geq0\), and let \(T=\operatorname{tr}G>0\).
Then

\[
0\leq C_k=\frac{\sum_{j\leq k}\lambda_j}{T}\leq1,\qquad
1\leq r_{\rm st}=\frac{T}{\lambda_1},\qquad
1\leq r_{\rm part}=\frac{T^2}{\operatorname{tr}(G^2)}.
\]

### Proof

The spectral theorem gives \(T=\sum_j\lambda_j\), so the
\(p_j=\lambda_j/T\) are nonnegative and sum to one.  The first assertion
follows immediately.  Since \(T\geq\lambda_1>0\), \(r_{\rm st}\geq1\).
For the participation rank, expand the square:
\[
(\sum_j\lambda_j)^2=\sum_j\lambda_j^2+
2\sum_{i<j}\lambda_i\lambda_j\geq\sum_j\lambda_j^2.
\]
Thus \(r_{\rm part}\geq1\).  \(\square\)

## Theorem 2 (exact positive-scalar invariance)

For every \(c>0\),

\[
C_k(cG)=C_k(G),\quad r_{\rm st}(cG)=r_{\rm st}(G),\quad
r_{\rm part}(cG)=r_{\rm part}(G),\quad h(cG)=h(G).
\]

### Proof

The eigenvalues of \(cG\) are \(c\lambda_j\).  Thus both the numerator and
denominator of \(C_k\) acquire a factor \(c\); the stable-rank numerator and
denominator acquire the same factor; and the participation numerator and
denominator acquire \(c^2\).  The probabilities \(p_j\) do not change, so
neither does \(h\).  \(\square\)

## Theorem 3 (outward quotient enclosure)

Suppose \(0\leq F^-\leq F\leq F^+\) and
\(0<T^-\leq T\leq T^+\).  Then

\[
\frac{F^-}{T^+}\leq\frac FT\leq\frac{F^+}{T^-}.
\]

### Proof

All quantities are nonnegative and the denominator interval is positive.
The quotient is increasing in its numerator and decreasing in its
denominator, so the two endpoint choices give the stated bounds.  \(\square\)

## What is certified here

The producer and independent replay certify 24 finite rows, five \(k\)-values,
120 trace-normalized intervals, and 80 strict adjacent decreases.  The
stable-rank and participation-rank growth counts, entropy range, and all
reported metric values are finite numerical observations.  No statement here
reassembles prime-shell signs into a twin-prime estimate.
