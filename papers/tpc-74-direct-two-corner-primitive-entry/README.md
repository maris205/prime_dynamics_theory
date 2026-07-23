# TPC-74: Direct Two-Corner Primitive Planes

This paper attaches the primitive cofactor coordinates of TPC-70 directly
to every off-diagonal entry of the literal atomic-normalized
missing-native Gram on the frozen TPC-61/68 missing-high carrier.

For active rows \(m<n\), write \(d_m=ga\), \(d_n=gb\), \((a,b)=1\).
At a complete common-output key,
\[
mj+h_0=Q_mS_m,\qquad nj+h_0=Q_nS_n,
\]
and define
\[
q=(S_m,S_n),\qquad S_m=qu,\qquad S_n=qv.
\]
Then \((u,v)=1\), \(q\mid |h_0(n-m)|\), and equality of the two residual
labels is equivalent to the single primitive direction
\((u,v)=(b,a)\).

The exact gauged entries are
\[
\widetilde H_{mn}
=\sum_{(u,v)=1}\mu(u)\mu(v)L_{mn}(u,v),
\]
\[
\widetilde R_{mn}
=\mu(a)\mu(b)L_{mn}(b,a),
\qquad
\widetilde E_{mn}
=\sum_{\substack{(u,v)=1\\(u,v)\ne(b,a)}}
\mu(u)\mu(v)L_{mn}(u,v).
\]
The kernel \(L_{mn}\) retains every complete key and the physical
normalization \(1/\sqrt{W_mW_n}\).  This is a literal two-corner operator
carrier, not a four-corner trace surrogate.

The paper also gives exact per-entry Abel majorants and a nonnegative
Perron matrix \(P^H\) satisfying \(\|H\|\le\rho(P^H)\).  No estimate
proving that \(\rho(P^H)\) is small is obtained.

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archival PDF is `direct-two-corner-primitive-entry.pdf`.
