# Real-vector version of the growing-rank obstruction

Date: 2026-09-09. Parent addendum; independent round-4 audit passed with
no necessary corrections, at the scoped real-witness claim level.
Dependencies: the exact \(A=U-\Delta\), symmetric Fourier band, uniform
positive-form trace bound, \(D_*(x)\), \(\tau_x\), \(d_x\), \(k_x=d_x-35\),
and common threshold from GROWING_RANK_PROOF.md.

The complex spectral-cutoff subspace in that proof need not be invariant
under conjugation. This addendum constructs a **different real subspace**;
it does not reinterpret the complex subspace as a real one.

## R1. Real orthonormal coordinates on the same band

For \(f_j(n)=N^{-1/2}e(jn/N)\), \(-J\le j\le J\), use
\[
 v_0=f_0,\qquad
 c_j=(f_j+f_{-j})/\sqrt2,\qquad
 s_j=(f_j-f_{-j})/(i\sqrt2),\quad 1\le j\le J.
\]
These \(d=2J+1\) columns are real and orthonormal on the same \(N\)
consecutive physical integers. Let \(V\) be their real \(N\)-by-\(d\)
matrix. Its complex column span is the original symmetric Fourier band,
so its orthogonal projector equals \(FF^*\), where \(F\) is the
complex Fourier-basis matrix in the growing-rank proof.

Put
\[
 C=V^TUV,\qquad C_{\mathbb R}=\operatorname{Re}C.
\]
Here \(C\) is complex Hermitian positive semidefinite;
\(C_{\mathbb R}\) is real symmetric. For real \(y\),
\[
 y^TC_{\mathbb R}y=(Vy)^*U(Vy)\ge0.
\]
The right side is real because \(U\) is Hermitian. Thus \(C_{\mathbb R}\)
is positive semidefinite as a real matrix. Moreover
\[
 \operatorname{tr}C_{\mathbb R}
 =\operatorname{tr}C
 =\operatorname{tr}(UFF^*)
 =\operatorname{tr}(F^*UF).
                                                               \tag{R1}
\]
The same proved trace bound therefore applies with no factor of two.

## R2. A real negative subspace with the same dimension bound

Let \(E_{\mathbb R}\) be the real spectral subspace of
\(C_{\mathbb R}\) for eigenvalues in \([0,D_*/2]\), and define
\[
 W_{\mathbb R}=V E_{\mathbb R}\subset\mathbb R^{I_x}.
\]
By R1 and the common threshold
\(2\operatorname{tr}(F^*UF)<35D_*\), at most 35 dimensions are discarded.
Consequently
\[
 \dim_{\mathbb R}W_{\mathbb R}\ge k_x.
\]
For \(f=Vy\) in this real subspace, the imaginary antisymmetric part of
\(C\) contributes zero to \(y^TCy\). Using
\(\Delta(n)\ge D_*\ge\tau_x\) on every physical row gives
\[
 \boxed{
 f^TAf=f^T(\operatorname{Re}A)f
 \le-\frac{\tau_x}{2}\|f\|_2^2
 \quad(f\in W_{\mathbb R}).}                                  \tag{R2}
\]
Thus the real symmetric matrix \(\operatorname{Re}A\) has at least
\(k_x=(1/4+o(1))Q^2\) eigenvalues at most \(-\tau_x/2\).
The complex matrix \(A\) itself is not declared real.

## R3. Real-linear constraints and deflations

For a real-linear map \(L\) out of \(\mathbb R^{I_x}\), rank is understood
as real dimension of its image. Rank-nullity gives
\[
 \dim_{\mathbb R}(W_{\mathbb R}\cap\ker L)
       \ge k_x-\operatorname{rank}_{\mathbb R}L.
\]
In particular, for a real-linear correction
\(R:\mathbb R^{I_x}\to\mathbb C^{I_x}\) of real rank \(r<k_x\), choose
a real unit vector \(f\in W_{\mathbb R}\cap\ker R\). Then
\[
 \boxed{
 \|A-R\|_{\mathbb R^N\to\mathbb C^N}
 \ge |f^*(A-R)f|
 = |f^TAf|
 \ge \tau_x/2.}                                             \tag{R3}
\]
Real matrices of ordinary real rank \(r<k_x\) are included.
For a general complex matrix, its rank over \(\mathbb C\) is not to be
substituted for this real rank. The earlier complex theorem separately
handles complex-linear corrections of complex rank less than \(k_x\);
the two statements use different witness and rank conventions.

If the independently proved positive real row weights obey
\(G(n)\le C_GH\tau_x\), then \(D_G^{1/2}W_{\mathbb R}\) is real, of the
same dimension, and its quadratic bound for
\(Z=D_G^{-1/2}AD_G^{-1/2}\) is \(-1/(2C_GH)\).

## R4. Physical scope and no-GO boundary

This is a coefficient-blind real-witness strengthening, not arithmetic
cancellation. It identifies neither \(\beta\), \(w\), nor their weighted
versions with the constructed spectral subspace. The real subspace depends
on the positive-form compression of the actual operator; it is not claimed
to equal a predeclared coordinate or physical-prefix subspace.
The equality \(f^TAf=f^T\operatorname{Re}(A)f\) uses the same real
vector in both slots. It does not justify replacing
\(w^TA\beta\) by \(w^T\operatorname{Re}(A)\beta\) for the two
different real arithmetic lanes.

All source data are unchanged: \(x=2X\), full
\(I_x=(x/2,x]\cap\mathbb Z\), \(Q=x^{1/3}\), \(H=x^{21/32}\),
complete prime shell, fixed shift \(h_0=2\), exact unit masks, outer \(q\),
deleted diagonal, literal signed arithmetic lanes, and inherited fixed
nonnegative profile supported in \([-1,1]\). No evenness or new smoothness
hypothesis is needed here. Threshold and exceptional-set quantifiers are
exactly those in the growing-rank theorem; all physical rows are retained.
No maximal-prefix assertion is made.

The scalar scale remains \(xQ^2\); the required \(\delta>1/400\), the
critical-array loss \(\ell<19/2400\), and Gate A are still unpaid.
The terminal bound \(0<\eta<\min(\eta_A,\delta-1/400,419/2400)\) is not
activated. Island 2 / image Bridge A / Gate B; formal endpoint TPC418.
No numbered-paper or publication GO. This is elementary finite-dimensional
realification of the trace argument, not a claimed novelty theorem.
