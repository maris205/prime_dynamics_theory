# TPC-229 derivation package

## 1. Endpoint separation

For an edge `p<r` satisfying `7p+3r=16Q`, shell bound `r<2Q` gives
`p>10Q/7`; ordering gives `p<8Q/5` and `r>8Q/5`. Hence

$$
\frac{10Q}{7}<p<\frac{8Q}{5}<r<2Q.
$$

The low/high endpoint sets are disjoint. The equation uniquely gives
`r=(16Q-7p)/3` and `p=(16Q-3r)/7`, so every vertex has degree at most one.

## 2. Edge block

After ordering the two shared coordinates, an edge couples two vectors `u,v in R^2`.
The swap operator is

$$
J=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix}
$$

with spectrum `{-1,-1,+1,+1}`. Put

$$
s=(u+v)/\sqrt2,\qquad d=(u-v)/\sqrt2.
$$

Then

$$
D=\|s\|^2+\|d\|^2,\quad
C=\|s\|^2-\|d\|^2,\quad
E_{AP}=D+C=2\|s\|^2.
$$

Consequently `0<=E_AP/D<=2`, sharply.

## 3. Saving criterion

For `0<=delta<1`,

$$
E_{AP}\le(1-\delta)D
\iff
(1+\delta)\|s\|^2\le(1-\delta)\|d\|^2.
$$

This is exact for each block and after summing blocks with the corresponding total
symmetric/antisymmetric energies.

## 4. Bilinear source block

TPC-228's edge value is

$$
B_e=\langle\beta_p,w_r\rangle+\langle\beta_r,w_p\rangle.
$$

Two applications of `2|<x,y>|<=||x||^2+||y||^2` give

$$
|B_e|\le\frac12(\|\beta_p\|^2+\|\beta_r\|^2+\|w_p\|^2+\|w_r\|^2),
$$

with equality on the exchanged aligned fixture.

## 5. Census

The exact replay over 4089 scales finds 2268 edge-bearing scales, 13,754 total edges,
maximum 18 edges first at `Q=3440`, and maximum degree one throughout. The replay
validates implementation boundaries; matching itself is proved for all `Q>=8`.
