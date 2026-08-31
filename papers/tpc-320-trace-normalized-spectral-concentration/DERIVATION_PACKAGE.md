# TPC-320 derivation package

## 1. Frozen operator

For \(I_X=(X/2,X]\cap\mathbb Z\), \(H=66\), and
\(\mathcal S_Q=\{p: p\ {\rm prime},\ Q<p\leq 2Q\}\), set

\[
K_{p,s}(u,t)=
\mathbf 1_{u\ne t}\mathbf 1_{p\nmid ut}
\frac{pH^{2s}}{(H^2+(u-t)^2)^s}
\left(\mathbf 1_{u\equiv t\pmod p}-\frac1{p-1}\right).
\]

The finite matrix \(A_{Q,s,X}\) has rows \((p,u)\) and columns \(t\), and
\(G=A^*A\) is real symmetric positive semidefinite.

## 2. Trace-normalized spectral measure

Write the eigenvalues in descending order:

\[
\lambda_1(G)\geq\lambda_2(G)\geq\cdots\geq\lambda_N(G)\geq0,\qquad
T(G)=\operatorname{tr}G.
\]

For \(T(G)>0\), let

\[
p_j(G)=\frac{\lambda_j(G)}{T(G)},\qquad
C_k(G)=\sum_{j=1}^k p_j(G)
=\frac{F_k(G)}{T(G)}.
\]

The vector \(p(G)\) is a probability distribution on the finite spectral
indices.  Thus \(C_k\) is a cumulative spectral mass and not a source-count
normalization.

## 3. Exact scale-invariance identities

For \(c>0\), the spectrum of \(cG\) is \(c\lambda_j(G)\), while
\(T(cG)=cT(G)\).  Consequently

\[
C_k(cG)=C_k(G),\qquad
r_{\rm st}(cG)=r_{\rm st}(G),\qquad
r_{\rm part}(cG)=r_{\rm part}(G),
\]

where

\[
r_{\rm st}(G)=\frac{T(G)}{\lambda_1(G)},\qquad
r_{\rm part}(G)=\frac{T(G)^2}{\operatorname{tr}(G^2)}
=\frac1{\sum_jp_j(G)^2}.
\]

The normalized Shannon entropy

\[
h(G)=-\frac1{\log N}\sum_{j:p_j>0}p_j\log p_j
\]

is invariant as well.  We use it as an adversarial control, not as a claimed
monotone observable.

The relation to the preceding source-count readout is exact:

\[
\frac{F_k(G)}{N}=\frac{T(G)}{N}\,C_k(G).
\]

Therefore a source-normalized or trace-normalized trend cannot be promoted to
an arithmetic power law without a separate law for \(T(G)/N\) and the signed
prime-shell reassembly.

## 4. Finite enclosure

The producer evaluates the top 17 eigenvalues in SciPy and the full spectrum in
NumPy, each in forward and reverse shell order.  The declared finite entry
bound is \(\lvert K\rvert\leq160\).  A binary64 entrywise Gram guard and Weyl's
inequality give a finite spectral guard.  The top-\(k\) mass interval is divided
outward by the positive trace interval:

\[
\left[\frac{F_k^-}{T^+},\frac{F_k^+}{T^-}\right].
\]

The comparison certificate only promotes strict interval separation on the
declared finite panel.  It does not claim exact eigenvalues or an asymptotic
limit.
