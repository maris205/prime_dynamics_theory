# TPC-325 derivation package

## 1. Literal blocks

For a source interval `I_N` and a prime `p` in `(Q,2Q]`, let

\[
B_{p,N}^{(s)}(u,t)=p\,\frac{H^{2s}}{(H^2+(u-t)^2)^s}
\left(1_{p\mid u-t}-\frac1{p-1}\right)
1_{u\ne t}1_{p\nmid u}1_{p\nmid t}.
\]

The direct Gram and signed coherent Gram are

\[
G_0(N)=\sum_p (B_{p,N}^{(s)})^*B_{p,N}^{(s)},\qquad
G_e(N)=\left(\sum_p e_pB_{p,N}^{(s)}\right)^*
       \left(\sum_p e_pB_{p,N}^{(s)}\right).
\]

## 2. Scale ladder

The source origin is fixed at `12001`, while `|I_N|=N/2` grows through four
nested values.  Thus a comparison between adjacent rungs changes the source
space and is not silently identified with a translated copy.

## 3. Profile and majorization

For a positive-trace Gram matrix, write

\[
\pi(G)=\left(\frac{\lambda_1(G)}{\operatorname{tr}G},\ldots,
\frac{\lambda_n(G)}{\operatorname{tr}G}\right),
\quad \lambda_1\ge\cdots\ge\lambda_n.
\]

The signed profile majorizes the direct profile when every interior cumulative
difference `sum_{j<=k}(pi_j(G_e)-pi_j(G_0))` is nonnegative and at least one is
strictly positive.  TV and the maximum cumulative difference are diagnostic
shape distances; trace ratio is an amplitude diagnostic and is kept separate.

## 4. Envelope readout

For each rung, take the minimum over its eight `(Q,s)` rows of the outward TV
lower endpoint for the all-plus law.  Separately take the maximum over those
rows of the outward energy-ratio estimate.  The certificate only records the
strict descending pattern observed on these four finite envelopes; it does not
promote the pattern to a monotone sequence theorem.
