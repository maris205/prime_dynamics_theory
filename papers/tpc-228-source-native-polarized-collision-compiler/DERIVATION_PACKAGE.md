# TPC-228 derivation package

## 1. Common-profile rows

Let `U_q=T_q beta` and `V_q=T_q w`, where the transform used for packet `j` is the
same transform for every `j`. Define

$$
W_q^{(j)}=U_q+i^jV_q.
$$

For each packet put

$$
E_{\rm AP}^{(j)}=\left\|\sum_qW_q^{(j)}\right\|^2,
\qquad
E_{\rm diag}^{(j)}=\sum_q\|W_q^{(j)}\|^2.
$$

## 2. Exact compiler

Expanding before any absolute-value estimate,

$$
E_{\rm AP}^{(j)}-E_{\rm diag}^{(j)}
=\sum_{q\ne r}\langle U_q+i^jV_q,U_r+i^jV_r\rangle.
$$

Four-phase polarization term by term yields

$$
\boxed{
\frac14\sum_{j=0}^3i^j
(E_{\rm AP}^{(j)}-E_{\rm diag}^{(j)})
=\sum_{q\ne r}\langle U_q,V_r\rangle.}
$$

No self-prime term survives because it was removed at the quadratic level.

## 3. Q25 block

At residues `119,281 mod 400`, the p-row atoms have multipliers `3,-3` and the r-row
atoms have `-7,7`. If their common-profile source amplitudes are denoted by
`beta_(q,m)` and `w_(q,m)`, the block is

$$
\frac1{400^2}\bigl(
\beta_{37,3}w_{47,-7}+\beta_{47,-7}w_{37,3}
+\beta_{37,-3}w_{47,7}+\beta_{47,7}w_{37,-3}
\bigr).
$$

This is the minimal arithmetic object whose sign must be controlled.

## 4. Exact controls

All source amplitudes equal to `+1` give `1/40000`; changing all `w` amplitudes to
`-1` gives `-1/40000`; opposite signs on the two prime rows give zero; a directed
`beta_p`/`w_r` source gives `1/80000`; one shared coordinate gives `1/160000`.
The checker also validates a three-row/two-collision graph and a no-collision graph.
