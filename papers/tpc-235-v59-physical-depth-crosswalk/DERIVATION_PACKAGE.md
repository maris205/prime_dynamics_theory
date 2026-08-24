# TPC-235 derivation package

## Frozen physical row

V59 and TPC-218 freeze

\[
H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400},
\]

and, for each physical denominator `h`, prime `Q<q<=2Q`, and common profile `psi`,

\[
B_{h,q}(a)=\sum_{0<|m|\le\lfloor hq/H\rfloor}
\psi\!\left(\frac{Hm}{hq}\right)
\mathbf1_{mq^{-1}\equiv a\pmod h}. \tag{D1}
\]

The full source also contains

\[
C_h=\sum_{d\in\mathcal D_x:\,h\mid d}\frac{\mu(d)\log d}{d},
\qquad
K_q(n)=\sum_{h,a}C_hB_{h,q}(a)e(na/h). \tag{D2}
\]

## Exact physical depth

Define

\[
\lambda_h=\frac{hQ}{H}. \tag{D3}
\]

Then (D1) becomes exactly

\[
B_{h,q}(a)=\sum_{0<|m|\le\lfloor\lambda_h q/Q\rfloor}
\psi\!\left(\frac{mQ}{\lambda_hq}\right)
\mathbf1_{mq^{-1}\equiv a\pmod h}. \tag{D4}
\]

This is a two-parameter row: depth `lambda_h` and modulus `h=(H/Q)lambda_h`.

Active denominators satisfy `h>=H/(2Q)` and `h<=U`, so

\[
\frac12\le\lambda_h\le\frac{UQ}{H}=x^{23/2400}. \tag{D5}
\]

One unit of depth contains about `H/Q=x^(31/96)` available integer-denominator grid
points.  This does not assert that every corresponding coefficient `C_h` is nonzero.

## Single-clock compatibility theorem

TPC-226 uses surrogate scales

\[
H_{\rm mod}=4Q^2,\qquad h_{\rm mod}=4LQ,
\]

which yield cutoff `floor(Lq/Q)` and profile argument `mQ/(Lq)`.  Exact equality with
one physical row requires both

\[
h=4LQ,\qquad \frac{H}{h}=\frac{Q}{L}. \tag{D6}
\]

For nonzero `L`, (D6) holds if and only if

\[
H=4Q^2. \tag{D7}
\]

At V59 scales,

\[
\frac{4Q^2}{H}=4x^{1/96}, \tag{D8}
\]

so the exact attachment fails by a growing factor.  Matching depth makes the modeled
modulus too large by (D8); matching modulus makes the modeled cutoff too shallow by
the same factor.

## Packet normalization firewall

V59 uses one common linear transform `T` and

\[
\langle T\beta,Tw\rangle
=\frac14\sum_{j=0}^3i^j\|T(\beta+i^jw)\|^2. \tag{D9}
\]

Output normalization `N(z)=z/||z||` is nonlinear.  Whenever all four outputs are
nonzero,

\[
\frac14\sum_{j=0}^3i^j\|N(T(\beta+i^jw))\|^2
=\frac14\sum_{j=0}^3i^j=0. \tag{D10}
\]

For `T=1`, `beta=1`, `w=2`, the right target in (D9) is `2`, while (D10) is zero.
Thus per-output unit normalization cannot be inserted into V59 polarization.

## Correct next object

Retain the complete weighted family `(h,q)` with `C_h`, one common transform for all
four source packets, and all denominators in each physical depth band.  Any fixed
linear rescaling must be common across packet labels and its inverse weight must remain
explicit in reassembly.
