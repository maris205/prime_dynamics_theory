# TPC-319 derivation package

## 1. Frozen operator

For (I_X=(X/2,X]\cap\mathbb Z), (H=66), and
(mathcal S_Q=\{p: p\text{ prime}, Q<p\le 2Q\}), set

\[
 K_{p,s}(u,t)=
  \mathbf 1_{u\ne t}\mathbf 1_{p\nmid ut}
  \frac{pH^{2s}}{(H^2+(u-t)^2)^s}
  \left(\mathbf 1_{u\equiv t\pmod p}-\frac1{p-1}\right).
\]

The block operator (A_{Q,s,X}) has rows indexed by ((p,u)) and columns by
(t\in I_X); (G=A^*A) is real symmetric and PSD.

## 2. Ky Fan readout

Write the eigenvalues in descending order

\[
 \lambda_1(G)\ge\lambda_2(G)\ge\cdots\ge0,
 \qquad F_k(G)=\sum_{j=1}^k\lambda_j(G).
\]

For every rank-(k) orthogonal projection (P), the finite Ky Fan principle gives

\[
 \operatorname{tr}(PG)\le F_k(G),
 \qquad F_k(G)=\max_{P^2=P=P^*\atop \operatorname{rank}P=k}
 \operatorname{tr}(PG).
\]

Consequently (F_k) is a cluster mass, not a sum of arbitrary coordinates, and

\[
 0\le F_k(G)\le\operatorname{tr}(G),
 \qquad \lambda_1(G)\le F_k(G)\le k\lambda_1(G).
\]

## 3. Normalization lemma

For a scale doubling (N\mapsto 2N), let

\[
 R_k=\frac{F_k(2N)}{F_k(N)}.
\]

Then

\[
 \frac{M_k(2N)}{M_k(N)}=\frac{R_k}{2}.
\]

Thus (1<R_k<2) implies unnormalized cluster growth and normalized cluster decay
simultaneously.  This is an exact algebraic firewall: it cannot be interpreted as a
power saving without a separately proved normalization law.

## 4. Finite numerical enclosure

Each row is evaluated in forward and reverse shell order, with SciPy's symmetric
top-(17) solver and NumPy's full symmetric solver.  The declared literal bound

\[
 |K_{p,s}(u,t)|\le160
\]

produces an entrywise binary64 guard.  For a top-(k) sum, Weyl's inequality is
applied to each of the (k) eigenvalues, so the spectral guard is multiplied by (k).
Solver spread, residual, and an outward pad are included.  This is a finite numerical
certificate, not an exact algebraic eigenvalue calculation.
