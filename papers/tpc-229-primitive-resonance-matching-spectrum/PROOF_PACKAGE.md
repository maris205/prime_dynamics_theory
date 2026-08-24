# TPC-229 proof package

## Theorem

For every integer `Q>=8`, let `G_Q` have as vertices the primes in `(Q,2Q)` and an
edge `p<r` whenever the primitive dilation-four resonance

$$
7p+3r=16Q
$$

holds. Then:

1. `G_Q` is a matching and every edge satisfies
   `10Q/7<p<8Q/5<r<2Q`.
2. The two-coordinate collision operator on each edge has spectrum
   `(-1,-1,+1,+1)`; the global operator is their orthogonal direct sum plus zeros.
3. For symmetric source vectors `u,v`,
   `E_diag=E_sym+E_anti`, `E_collision=E_sym-E_anti`, `E_AP=2E_sym`, and
   `0<=E_AP/E_diag<=2` sharply.
4. For `0<=delta<1`, AP saving by `delta` is equivalent to
   `(1+delta)E_sym<=(1-delta)E_anti`.
5. The TPC-228 bilinear edge block is bounded sharply by half its four-source mass.

## Proof

Let `(p,r)` be an edge. Since `r<2Q`,

$$
7p=16Q-3r>10Q,
$$

so `p>10Q/7`. Since `p<r`, the resonance equation gives
`10p<16Q<10r`, hence `p<8Q/5<r`. The shell supplies `r<2Q`.

The endpoint intervals are disjoint. Moreover, a low endpoint determines
`r=(16Q-7p)/3`, and a high endpoint determines `p=(16Q-3r)/7`. Thus a vertex cannot
occur in two edges, proving the matching theorem.

Each edge has two sign-symmetric shared coordinates. In the ordered basis consisting of
the two coordinates on the p-row followed by those on the r-row, the collision adjacency
is

$$
J=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix}.
$$

The symmetric subspace `(u,u)` has eigenvalue `+1` and the antisymmetric subspace
`(u,-u)` has eigenvalue `-1`, both of dimension two. Matching makes different edge
supports orthogonal, so the global statement follows.

For one symmetric source channel put `s=(u+v)/sqrt(2)` and
`d=(u-v)/sqrt(2)`. Parallelogram identities give

$$
\|u\|^2+\|v\|^2=\|s\|^2+\|d\|^2,
\qquad
2\langle u,v\rangle=\|s\|^2-\|d\|^2,
$$

and therefore `E_AP=||u+v||^2=2||s||^2`. Nonnegativity gives the sharp ratio range;
`v=u` and `v=-u` attain its endpoints. Rearranging
`2||s||^2<=(1-delta)(||s||^2+||d||^2)` proves the saving criterion.

Finally,

$$
|\langle\beta_p,w_r\rangle|\le
\tfrac12(\|\beta_p\|^2+\|w_r\|^2)
$$

and the exchanged inequality prove the bilinear bound. Taking
`w_r=beta_p` and `w_p=beta_r` attains equality. ∎

## Boundary

The theorem removes graph-combinatorial amplification but does not prove that the
physical source occupies the antisymmetric modes or that matched resonance mass is a
fixed proportion of total diagonal mass. Those are arithmetic inputs.
