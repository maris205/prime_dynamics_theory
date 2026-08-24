# TPC-232 proof package

## Claim

Fix \(A>0\).  Let \(C_L(Q)\) count primitive collision channels in the
TPC-226 dilated-clock family at \(h=4LQ\), with primes in \((Q,2Q)\), modulo
the two global-sign coordinates.  Uniformly for

\[
1\le L\le(\log Q)^A,
\]

one has

\[
C_L(Q)\ll_A
\frac{LQ\log\log(3LQ)}{(\log Q)^2}. \tag{1}
\]

Consequently, if \(L=o(\log Q/\log\log Q)\), then

\[
\frac{C_L(Q)}{\pi(2Q)-\pi(Q)}\longrightarrow0. \tag{2}
\]

For fixed-comparability row masses, no collision mechanism supported only on
these channels can yield a fixed positive proportional saving in this range.

## Status

`PROVABLE AS STATED` for the declared dilated-clock model.

## Assumptions

- \(Q\) tends to infinity through integers.
- \(L\) is integral and \(1\le L\le(\log Q)^A\).
- Multipliers satisfy the literal cutoff and are primitive modulo \(4LQ\).
- The last assertion assumes a \(Q\)-independent row-mass ratio \(\kappa\).

## Proof strategy

Use an exact collision classification, a coefficient-uniform Selberg sieve
with an explicit interval remainder, and a weighted coefficient count.

## Dependency map

1. Lemma 1 reduces support intersections to \(ar+bp=4LQ\).
2. Lemma 2 bounds one coefficient channel.
3. Lemma 3 sums \(1/\max(a,b)\).
4. PNT proves normalized sparsity.
5. TPC-230's unmatched-mass floor proves the energy corollary.

## Proof

### Lemma 1: growing-depth collision normal form

For all sufficiently large \(Q\), polylogarithmic \(L\) satisfies \(L<Q/4\).
Every active prime is then invertible modulo \(h=4LQ\), and every active
multiplier has magnitude below \(2L<q\).  If two rows collide, then

\[
m_1q_2-m_2q_1\equiv0\pmod h. \tag{3}
\]

For equal signs, the left side has magnitude below \(h\).  It cannot vanish,
because distinct primes and \(|m_i|<q_i\) would force a prime to divide a
nonzero shorter multiplier.  Hence the signs are opposite.  Their absolute
sum is positive and below \(2h\), so (3) becomes

\[
a q_2+b q_1=h,\qquad 1\le a,b<2L. \tag{4}
\]

Both coefficients are coprime to \(h\).  If \(d=(a,b)\), then (4) gives
\(d\mid h\), while \((d,h)=1\); therefore \(d=1\).  Three rows cannot meet
one residue, since two associated multipliers would share a sign and violate
the equal-sign exclusion.  Changing both signs supplies the second and only
other residue in a channel.  This proves the normal form.

### Lemma 2: one-channel uniform upper bound

Fix \(a,b\).  If (4) has an integer solution, coprimality parameterizes every
solution by

\[
q_1=p_0+ak,\qquad q_2=r_0-bk. \tag{5}
\]

The two shell restrictions cut out an interval of length
\[
K\ll Q/\max(a,b)+1. \tag{6}
\]
The determinant of the affine forms is \(ar_0+bp_0=h\).

Let \(\nu(\ell)\) count roots of their product modulo a prime \(\ell\).
If \(\ell\nmid abh\), then \(\nu(\ell)=2\).  If \(\ell\mid h\), the two
roots coalesce.  If \(\ell\mid a\) or \(\ell\mid b\), one affine form is a
nonzero constant and the other has one root.  The exceptional correction is
therefore at most
\[
\prod_{\ell\mid abh,\,\ell\ge3}\frac{\ell-1}{\ell-2}
\ll\log\log(3LQ). \tag{7}
\]
The last estimate follows by comparison with the product over the smallest
primes; \(ab h\ll L^3Q\).

For squarefree \(d\), the Chinese remainder theorem and interval counting give
\[
A_d=K\frac{\nu(d)}d+O(\nu(d)). \tag{8}
\]
If \(K<Q^{1/2}\), the trivial bound for the channel is \(O(Q^{1/2})\).
Otherwise apply the classical Selberg upper-bound sieve to (8), choosing
\(z=K^{1/10}\).  The main term is bounded by the right side of (6), divided
by \((\log z)^2\), times (7).  The Selberg double-divisor remainder uses
moduli below \(z^2\); since \(\nu(d)\le2^{\omega(d)}\), its total is
\(O(z^2(\log z)^C)\) for an absolute \(C\).  In the second branch
\(\log z\asymp\log Q\), and this remainder is \(O_A(Q^{1/2})\).  Combining
the two branches gives
\[
C_{a,b}(Q)\ll_A
\left(\frac{Q}{\max(a,b)}+1\right)
\frac{\log\log(3LQ)}{(\log Q)^2}
+O_A(Q^{1/2}). \tag{9}
\]
This is the required coefficient-uniform form.

### Lemma 3: aggregate coefficient length

For \(M=2L-1\), grouping pairs by \(m=\max(a,b)\) yields
\[
\sum_{a,b\le M}\frac1{\max(a,b)}
=\sum_{m\le M}\frac{2m-1}{m}<2M<4L. \tag{10}
\]

### Completion of the count

Sum (9) over all \(a,b<2L\).  Equation (10) bounds the leading lengths.
The \(O(L^2)\) constant terms and the summed sieve remainders are
\(o_A(LQ/\log^2Q)\), since \(L\) is polylogarithmic.  This proves (1).
The prime number theorem gives
\(\pi(2Q)-\pi(Q)\sim Q/\log Q\), so (2) follows under
\(L=o(\log Q/\log\log Q)\).

### Energy corollary

Let \(I_L(Q)\) be the number of incident rows.  Lemma 1 gives
\(I_L(Q)\le2C_L(Q)\).  If the maximum row mass is at most \(\kappa\) times
the minimum, the incident mass fraction is at most
\[
2\kappa\frac{C_L(Q)}{\pi(2Q)-\pi(Q)}=o(1). \tag{11}
\]
Rows outside the incident set remain orthogonal to every other row, so their
diagonal mass survives in the AP norm.  Equivalently, the TPC-230
unmatched-mass floor bounds any saving by (11).  No fixed positive saving,
including \(1/400\), can persist in the subcritical range. \(\square\)

## Corrections or missing assumptions

- The theorem is uniform only in the stated polylogarithmic range.
- Comparable row mass is used only for the energy transfer.
- The dilated clock is not identified with the actual V59 source.

## Open risks

The proof gives no lower bound at critical depth.  It also leaves open whether
the literal V59 source carries any non-negligible mass on these modeled rows.
