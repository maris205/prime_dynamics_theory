# TPC-234 derivation package

## Invariant geometry

For `L<Q/4`, TPC-232 proves that every residue of the modeled clock `h=4LQ` belongs
to at most two distinct prime-row supports.  Let `v_q` be any nonzero scalar- or
Hilbert-valued row supported on `S_{q,L}`, and put

\[
u_q=v_q/\|v_q\|,\qquad \|u_q\|=1.
\]

Define the synthesis operator

\[
Tc=\sum_q c_q u_q,
\qquad G=T^*T.
\]

## Pointwise theorem

At a coordinate `x`, at most two summands occur.  Therefore

\[
\left\|\sum_{q:x\in S_q}c_qu_q(x)\right\|^2
\le2\sum_{q:x\in S_q}|c_q|^2\|u_q(x)\|^2. \tag{D1}
\]

Summing `x` and using `||u_q||=1` gives

\[
\|Tc\|^2\le2\sum_q|c_q|^2. \tag{D2}
\]

Since `G` is a Gram operator and has diagonal one,

\[
0\le G\le2I,
\qquad -I\le K:=G-I\le I,
\qquad \|K\|\le1. \tag{D3}
\]

No coefficient, profile, or depth factor appears.

## Exact residual identity

For scalar rows, write the one or two contributions at a coordinate as `a_x,b_x`,
with `b_x=0` for a singleton bucket.  Then

\[
2\sum_x(|a_x|^2+|b_x|^2)-\sum_x|a_x+b_x|^2
=\sum_{x:\,|B_x|=1}|a_x|^2+
\sum_{x:\,|B_x|=2}|a_x-b_x|^2\ge0. \tag{D4}
\]

This is the finite exact certificate identity.

## Sharpness and non-saving

Two identical singleton unit rows attain ratio `2`, so the constant is sharp in the
ambient multiplicity-two class.  The literal clock `Q=39,L=7,h=1092` has rows
`p=67,r=71`, each with six atoms and shared coordinates `277,815`.  Their normalized
inner product is `2/6=1/3`; hence

\[
\frac{\|u_p+u_r\|^2}{2}=\frac43,
\qquad
\frac{\|u_p-u_r\|^2}{2}=\frac23. \tag{D5}
\]

Thus unit normalization removes the TPC-233 condition-number growth but does not choose
the sign of the collision correction.

## Boundaries

- Normalization is not yet derived from actual V59 weights.
- `G<=2I` is stability, not a strict saving below `I`.
- No arithmetic cancellation, `L2`, fixed-atom credit, strict `1/400`, or full Gate B
  is proved.
