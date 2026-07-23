# TPC-70 - Primitive Cofactor Coordinates

**Title:** *Primitive Cofactor Coordinates for Two-Key Erasure Rectangles:
Divisor Compression, Frozen Prime Rays, and the Residual Mobius Plane*

This paper continues the exact cross-key rectangle analysis of TPC-69.
It makes no arithmetic cancellation assumption and no twin-prime claim.

## Main exact results

For two distinct primitive rows \(m,n\), a fixed nonzero shift \(h_0\),
same-residual time \(j_R\), and erasure time \(j_E\), put
\[
H=h_0(n-m),\qquad \Delta=j_E-j_R.
\]
The four targets satisfy
\[
nA_m-mA_n=nB_m-mB_n=H,\qquad
A_mB_n-B_mA_n=H\Delta.
\]

Write
\[
d_m=ga,\qquad d_n=gb,\qquad (a,b)=1.
\]
At the same-residual anchor,
\[
d_mR_m=d_nR_n
\quad\Longrightarrow\quad
R_m=bt,\quad R_n=at,\quad t\mid |H|.
\]
For fixed \(t\), every physical anchor lies on one candidate prime ray:
\[
j_R=j_{R,0}+abt z,\quad
P_m=P_{m,0}+ma z,\quad
P_n=P_{n,0}+nb z.
\]

At the erasure key, write
\[
q=(S_m,S_n),\qquad S_m=qu,\qquad S_n=qv,\qquad (u,v)=1.
\]
Then
\[
q\mid |H|,
\qquad
d_mS_m\ne d_nS_n
\Longleftrightarrow
(u,v)\ne(b,a),
\]
and every fixed-\((q,u,v)\) solution lies on
\[
j_E=j_{E,0}+quv z,\quad
Q_m=Q_{m,0}+mv z,\quad
Q_n=Q_{n,0}+nu z.
\]

The exact rectangle sign is
\[
\mu(a)\mu(b)\mu(u)\mu(v).
\]
It is constant along each \(z\)-ray.  Keeping every physical mask, native
label, coefficient, phase, and normalization inside
\(K_{\mathfrak a,q}(u,v)\), the anchored rectangle sum is exactly
\[
\mu(a)\mu(b)
\sum_{q\mid |H|}
\sum_{\substack{(u,v)=1\\(u,v)\ne(b,a)}}
\mu(u)\mu(v)K_{\mathfrak a,q}(u,v).
\]

## Claim boundary

The paper proves exact finite algebra (L0) and an exact reindexing of the
complete fixed-\(h_0\) native rectangle carrier (L1). It does **not**
prove:

- cancellation in the primitive cofactor plane;
- a local-star, mixed-moment, or native operator bound;
- missing-mass, represented-frame, or nuisance-shorting estimates;
- a fixed-shift parity-breaking estimate;
- a prime-pair or twin-prime theorem.

Brun-Selberg bounds thin each prime ray only unsignedly. The next
falsifiable gate is a two-dimensional Abel/Mertens certificate that
retains every boundary and variation term of the actual ragged kernel.

## Build

Run:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The archival PDF is `primitive-cofactor-plane.pdf`.
