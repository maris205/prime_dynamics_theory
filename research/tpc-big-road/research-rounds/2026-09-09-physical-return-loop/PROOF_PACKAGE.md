# Proof package: literal operator, row energy, and norm scale

Date: 2026-09-09. Unnumbered proof; round-1 independent audit found no fatal
mathematical defect. Explicit definitions/notation are corrected for delta review.
Definitions and physical contract: DERIVATION_PACKAGE.md.
Claim ceiling: exact structural identities and coefficient-blind norm estimates;
no mixed arithmetic cancellation theorem.

## P1. Exact unit-residue projection identity

For one prime \(q>2\), on residues \(r,s\bmod q\) set
\[
 F_q(r,s)=q1_{r=s}-1,\qquad
 S_q(r,s)=a_q[(q-1)1_{r=s}-1]1_{r\ne0}1_{s\ne0}.
\]
Then
\[
 F_q-S_q=\frac{r_qr_q^*}{q-1},\qquad
 r_q(r)=q1_{r=0}-1.                                      \tag{P1}
\]
Proof: when both residues are nonzero, the difference is \(1/(q-1)\);
when exactly one is zero it is \(-1\); at \((0,0)\) it is \(q-1\).
These are exactly the three values of the right side. Also \(F_q\) is
\(q\) times the orthogonal projection onto the mean-zero residues, and
\(S_q\) is \(q\) times the projection onto the subspace that vanishes at
0 and sums to zero on the units. Thus \(0\le S_q\le F_q\).

Pulling the residue matrices back along \(I\to\mathbb Z/q\mathbb Z\)
preserves positive semidefinite order, regardless of unequal residue counts.
For \(D_v(n,n)=e(-vn/H)\),
\[
 [\kappa((u-t)/H)S_q(u,t)]_{u,t\in I}
   =\int\psi_+(v)D_vS_qD_v^*\,dv .
\]
Because \(\psi_+\ge0\), the same order is preserved after multiplication
by the kernel. This is an ordinary finite-matrix identity, with an
absolutely convergent integral. Summing P1 and deleting the exact diagonal
proves
\[
 A=T_{\mathcal Q}-R-\Delta,\quad R\ge0,\quad
 0\le A+\Delta\le T_{\mathcal Q}.                         \tag{P2}
\]
Here \(S_q(n,n)=a_q(q-2)1_{q\nmid n}\), which explains the diagonal
\(\Delta\) in the derivation package. This verifies all signs and masks.

## P2. Frequency-separation upper bound

The fractions
\(\mathcal F=\{a/q:q\in\mathcal Q,\ 1\le a<q\}\) are distinct on the unit
circle and separated by at least \(1/(4Q^2)\), including across 0.
Indeed every nonzero difference modulo 1 has numerator of absolute value
at least 1 over a denominator at most \(4Q^2\).

The convolution kernel
\(\kappa(h/H)\sum_{\lambda\in\mathcal F}e(\lambda h)\) is absolutely
summable for each fixed \(x\). Its Fourier multiplier, by Poisson
summation for the fixed Schwartz profile, is
\[
 m(\theta)=H\sum_{\lambda\in\mathcal F}\sum_{k\in\mathbb Z}
       \psi_+(H(\lambda-\theta-k))\ge0.                 \tag{P3}
\]
The real points in this sum have mutual spacing at least
\(s=H/(4Q^2)\). Every half-open interval of length 1 has at most
\(1+1/s\) points. Splitting positive and negative half-lines into unit
intervals yields
\[
 \sum_{\lambda,k}(1+|H(\lambda-\theta-k)|)^{-2}
 \le 2(1+1/s)\sum_{j\ge0}(1+j)^{-2}
 <4(1+1/s).
\]
Thus the convolution norm, and hence its compression to \(I\), is at most
\(4B_\psi(H+4Q^2)\). Also
\(\Delta_{\max}<\sum_{q\in\mathcal Q}q\le3Q^2\) for \(Q\ge2\).
Using P2 and the triangle inequality,
\[
 \|A\|\le4B_\psi(H+4Q^2)+3Q^2.                          \tag{P4}
\]
This is a classical frequency-separation mechanism derived here; no
novelty claim is attached to it. At the physical scales \(H<Q^2\).

## P3. Exact full-row-energy formula

Fix \(u\in I\), \(q\nmid u\). Define
\[
 S_q^{(2)}(u)=\sum_{\substack{t\in I\\t\ne u,\ q\nmid t}}
                  |\kappa((u-t)/H)|^2,\qquad
 C_q^{(2)}(u)=\sum_{\substack{t\in I\\t\ne u,\ q\mid u-t}}
                  |\kappa((u-t)/H)|^2.
\]
As \((q-2)^2-1=(q-1)(q-3)\), the exact identity is
\[
 G(u)=\sum_{\substack{q\in\mathcal Q\\q\nmid u}}
 a_q^2\{S_q^{(2)}(u)+(q-1)(q-3)C_q^{(2)}(u)\}.          \tag{P5}
\]
There are no cross-prime terms because of the declared definition of \(G\).

For the upper bound, extend both sums to the infinite lattice:
\[
 S_q^{(2)}(u)\le(2B_\kappa^2/3)H,\qquad
 C_q^{(2)}(u)\le(2B_\kappa^2/3)H/q.
\]
These follow from
\(\sum_{j\ge1}(1+j/a)^{-4}\le\int_0^\infty(1+t/a)^{-4}dt=a/3\).
Since \(1+(q-1)(q-3)/q\le q\) for \(q\ge3\), the per-prime
contribution is at most \((2B_\kappa^2/3)a_q^2qH\).

For a lower bound assume \(N-1\ge2\rho H\) and \(H\ge2Q/\rho\).
At least one side of \(u\) in \(I\) has length at least \(\rho H\).
That side contains \(\lfloor\rho H/q\rfloor\ge\rho H/(2q)\)
nonzero multiples of \(q\) from \(u\). All are units because \(q\nmid u\),
and all have \(|\kappa|\ge b\). Since \((q-2)^2\ge q^2/9\),
the per-prime contribution is at least
\((\rho b^2/18)a_q^2qH\).

Let \(S_Q=\sum_{q\in\mathcal Q}a_q^2q\). An integer \(u\le x=Q^3\)
has at most two distinct prime divisors in \((Q,2Q]\), since three such
primes have product strictly greater than \(x\). Each omitted term is at
most \((3/2)^2(2Q)\), so their sum is at most \(9Q\).
The prime number theorem and partial summation give
\(S_Q\sim(3/2)Q^2/\log Q\). Consequently, eventually \(S_Q\ge18Q\)
and the above interval assumptions hold. Uniformly for every \(u\in I\),
\[
 \frac{\rho b^2}{36}HS_Q\le G(u)\le
       \frac{2B_\kappa^2}{3}HS_Q.                       \tag{P6}
\]
In particular the normalization is defined at every physical row
eventually. This is not a statement about intervals of arbitrary huge
origin at the same length; the bound \(u\le x=Q^3\) is essential.

## P4. Constant-mode lower bound, fixed compact profile

Set \(f=N^{-1/2}1_I\). By V59 (4.2)--(4.4), or directly by P1,
\[
 \langle f,Af\rangle=R_0-D_0,\qquad
 R_0=\frac1N\sum_q q\int\psi_+(v)V_q(v/H)\,dv,
\]
\[
 D_0=\frac1N\sum_q\frac{q(q-2)}{q-1}N_q,\qquad
 N_q=|\{n\in I:q\nmid n\}|,
\]
where the variance is the unnormalized sum
\[
 S_r(\alpha)=\sum_{n\in I,\ n\equiv r(q)}e(\alpha n),\quad
 \bar S^\times(\alpha)=\frac1{q-1}\sum_{r\ne0}S_r(\alpha),\quad
 V_q(\alpha)=\sum_{r\ne0}|S_r(\alpha)-\bar S^\times(\alpha)|^2 .
\]
It is not divided by the number of unit residues.

Write \(I=\{a+1,\ldots,a+N\}\), \(N=mq+s\), \(0\le s<q\).
Relabel residues by \(j=1,\ldots,q\), with
\(S_j^{\#}=S_{(a+j)\bmod q}\). The excluded nonunit label depends
on \(a\); the following bound holds for every label and hence for
the unit subset. Suppressing the superscript in this one display:
\[
 S_j(\alpha)=e(\alpha(a+j))
   \{G_m(\alpha q)+1_{j\le s}e(\alpha mq)\},\quad
 G_m(y)=\sum_{k=0}^{m-1}e(ky).
\]
If \(0<|\alpha|q\le1/2\), then
\(|G_m(\alpha q)|\le1/(2|\alpha|q)\) and
\(|e(\alpha j)-1|\le2\pi|\alpha|q\).
Hence all \(S_j\) are within \(\pi+1\) of the common value
\(e(\alpha a)G_m(\alpha q)\). At \(\alpha=0\), they are within 1
of \(m\). Subtracting the mean minimizes squared distance to a constant,
so \(V_q(\alpha)\le q(\pi+1)^2\).

Here \(\psi_+\) is supported on \([-1,1]\); eventually
\(2Q/H<1/2\). Thus the preceding bound applies throughout the entire
integral, without a tail cutoff or an \(x\)-dependent profile:
\[
 0\le R_0\le\frac{(\pi+1)^2}{N}\sum_q q^2
       =O_\psi(Q^3/(N\log Q))=O_\psi(1/\log Q).
\]
Also \(N_q=N(1-1/q)+O(1)\), uniformly, so
\[
 D_0=\sum_q(q-2)+O(Q^2/(N\log Q)).
\]
Therefore
\[
 \langle f,Af\rangle=-\sum_q(q-2)+O_\psi(1/\log Q),
 \qquad
 \|A\|\ge(3/2+o(1))Q^2/\log Q.                         \tag{P7}
\]
A fixed profile is indispensable. No test here claims that either
arithmetic lane equals the constant vector.

The unabridged originating report also gives a finite-moment version
with an explicit fifth-moment tail and numerical diagnostics; the compact
support now recovered from the source makes that tail unnecessary here.

## P5. Normalized consequence and paid lane cost

Since \(A=D_G^{1/2}ZD_G^{1/2}\),
\[
 \|A\|/G_{\max}\le\|Z\|\le\|A\|/G_{\min}.
\]
Combining P4, P6, and P7 gives
\(c_\psi/H\le\|Z\|\le C_\psi\log Q/H\) eventually.
For any two vectors, the normalized norm-product bound is at least
\[
 \|Z\|\,\|D_G^{1/2}\beta\|\,\|D_G^{1/2}w\|
 \ge(G_{\min}/G_{\max})\|A\|\|\beta\|\|w\|.             \tag{P8}
\]
Thus row-energy normalization cannot remove the coefficient-blind
barrier proved with the literal lane norms in LANE_NORM_PROOF.md.

## Provenance and limitations

All identities above are explicit derivations from the locked V59 object.
The PNT input is the classical theorem, for example the original proof
in [Selberg, An elementary proof of the prime-number theorem (1949)](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf),
introductory statement (1.1); all weighted dyadic consequences here follow
by partial summation. The originating agent's DLMF link to 27.2.E3 is a
prime-counting definition, not an adequate PNT theorem pointer, and is
superseded by this source lock (also see DLMF 27.12.E5).

Finite floating-point positivity and matrix tests are diagnostics only.
The proof uses no global arithmetic conjecture. Round-1 independent operator
audit passed within this exact scope; its definition corrections are
implemented above. No novelty or numbered-paper readiness is asserted.
