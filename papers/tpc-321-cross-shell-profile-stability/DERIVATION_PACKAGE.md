# TPC-321 derivation package

## 1. Literal operator

Let (I_X=(X/2,X]capmathbb Z), let (S_Q={p:Q<pleq2Q, p {m
prime}}), and let (sin{1,2}).  With (h=66), define

\[
 K_s(u-t)=\frac{h^{2s}}{(h^2+(u-t)^2)^s},
 \qquad
 c_p(u,t)=\mathbf 1_{u\equiv t\pmod p}-\frac1{p-1}.
\]

The literal block has entries

\[
 B_{p,s}(u,t)=pK_s(u-t)c_p(u,t)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t},
 \qquad G_{X,Q,s}=\sum_{p\in S_Q}B_{p,s}^{\mathsf T}B_{p,s}.
\]

The matrix is PSD by construction.  TPC-321 changes no entry and no source
interval; it changes only the cross-shell readout.

## 2. Ordered normalized profile

Write the eigenvalues of (G) as

\[
 \lambda_1(G)\geq\cdots\geq\lambda_N(G)\geq0,
 \qquad p_j(G)=\frac{\lambda_j(G)}{T(G)},
 \qquad T(G)=\operatorname{tr}(G)>0.
\]

Then (p_jgeq0) and (sum_jp_j=1).  For (c>0),

\[
 p_j(cG)=\frac{c\lambda_j(G)}{cT(G)}=p_j(G).
\]

This exact identity is the normalization firewall: a result based only on
the profile cannot be credited to global amplitude growth.

## 3. Profile distances

For two same-dimensional ordered profiles (p,q), put

\[
 d_r(p,q)=\sum_{j=1}^r(p_j-q_j),\quad 1\leq r<N,
\]

and define

\[
 D_{\rm TV}=\frac12\sum_{j=1}^N|p_j-q_j|,\qquad
 D_{\rm L}=\max_{r<N}|d_r|,\qquad
 D_{\rm int}=\frac1{N-1}\sum_{r<N}|d_r|.
\]

The first is the l1 distance of rank masses; the latter two measure the
partial-sum (Lorenz/Ky Fan) discrepancy.  We call the relation (p\succeq q)
majorization when (d_r(p,q)geq0) for all (r<N).  A sign tolerance
(\tau=10^{-8}) is used only for finite numerical classification; a pair is
`MIXED` when both signs exceed (\tau).

## 4. Outward finite intervals

For each comparison, the producer computes the metrics for every combination
of its forward/reverse shell profiles and its NumPy/SciPy profiles.  If the
resulting scalar values are (v_1,ldots,v_m), the stored interval is

\[
 [\max(0,\min_i v_i-10^{-12}),
  \min(1,\max_i v_i+10^{-12})].
\]

This is a finite numerical enclosure around path spread plus a declared
rounding guard.  It is not an interval theorem for arbitrary (X) or (Q).

## 5. Panel conclusion

The certificate has 18 comparisons.  Every TV lower endpoint exceeds (0.03)
and every Lorenz lower endpoint exceeds (0.02).  The smallest endpoints are
`0.03212981290619634` and `0.02339722207455566`, respectively.  The
majorization census is (3) forward, (2) reverse, (13) mixed.
