# TPC-232 derivation package

## Target

Quantify the smallest possible growing resonance depth that is not already
eliminated by support density in the TPC-226 dilated-clock family.

## Status

`COHERENT AS STATED / PROVED_ARITHMETIC_OBSTRUCTION_L1`.

## Invariant object

For primes \(Q<q<2Q\), an integer depth \(L<Q/4\), and clock \(h=4LQ\), retain

\[
S_{q,L}=\{m q^{-1}\pmod h:0<|m|\le\lfloor Lq/Q\rfloor,\ (m,h)=1\}.
\]

Let \(C_L(Q)\) count collision channels modulo global sign: a channel is a tuple
\((p,r,a,b)\), with \(p<r\) in the prime shell, that produces the two coordinates
with multipliers \((a,-b)\) and \((-a,b)\).

## Assumptions

- \(Q\ge8\), \(1\le L<Q/4\), and eventually \(L\le(\log Q)^A\) for fixed \(A\).
- Every multiplier is primitive modulo \(4LQ\).
- Row masses are comparable only in the final energy corollary.
- The dilated clock remains the TPC-226 `MODELING_CHOICE`; no V59 identification is assumed.

## Derivation strategy

Reduce every support collision to one positive linear equation, apply a uniform
two-dimensional Selberg upper-bound sieve to each coefficient channel, and sum
the channel lengths with the exact weight \(1/\max(a,b)\).

## Derivation map

1. Short multipliers force opposite signs and one wrap.
2. A channel has equation \(ar+bp=4LQ\), with \(a,b<2L\) and \((a,b)=1\).
3. For fixed \(a,b\), the prime pair is parameterized by two affine forms on an
   interval of length \(O(Q/\max(a,b)+1)\).
4. Exceptional local primes divide \(ab(4LQ)\), giving at most a
   \(\log\log(3LQ)\) singular correction.
5. The coefficient identity
   \[
   \sum_{a,b<2L}\frac1{\max(a,b)}\le4L
   \]
   converts \(O(L^2)\) formal channels into an \(O(L)\) aggregate length.
6. PNT and the unmatched-mass floor transfer zero incidence density to zero
   fixed-saving capacity.

## Main derivation

### Exact geometry

Since \(L<Q/4\), every cutoff satisfies \(|m|<2L<q\), every prime row is a unit
modulo \(h\), and each row is internally injective.  A shared coordinate obeys

\[
m_1q_2-m_2q_1\equiv0\pmod h.
\]

Same-sign multipliers give a left side of magnitude below \(h\); equality to
zero would force one active prime to divide a shorter nonzero multiplier.
Thus signs are opposite.  Their positive sum is below \(2h\), hence it equals
exactly one wrap:

\[
a q_2+b q_1=4LQ. \tag{D1}
\]

Three rows cannot share one coordinate, because two of their multipliers would
have the same sign.  Global sign creates exactly two coordinates for each
channel.

### One-channel sieve

For a nonempty coefficient channel, primitivity and (D1) imply \((a,b)=1\).
All integer solutions are

\[
p=p_0+ak,\qquad r=r_0-bk, \tag{D2}
\]

on an interval \(I_{a,b}\) of length

\[
K_{a,b}\ll \frac{Q}{\max(a,b)}+1. \tag{D3}
\]

The determinant of the two forms in (D2) is

\[
a r_0+b p_0=4LQ. \tag{D4}
\]

Outside primes dividing \(ab(4LQ)\), the forms have two distinct roots.
At an exceptional prime they have at most one root; therefore the local
correction is bounded by

\[
\prod_{\ell\mid ab(4LQ),\,\ell\ge3}\frac{\ell-1}{\ell-2}
\ll\log\log(3LQ). \tag{D5}
\]

For squarefree \(d\), interval counting gives

\[
\#\{k\in I_{a,b}:d\mid(p_0+ak)(r_0-bk)\}
=K_{a,b}\frac{\nu(d)}d+O(\nu(d)). \tag{D6}
\]

Applying Selberg weights up to \(z=K_{a,b}^{1/10}\) gives, uniformly for
\(L\le(\log Q)^A\) and \(K_{a,b}\ge Q^{1/2}\),

\[
C_{a,b}(Q)
\ll_A
\left(\frac{Q}{\max(a,b)}+1\right)
\frac{\log\log(3LQ)}{(\log Q)^2}
+O_A(Q^{1/2}). \tag{D7}
\]

If \(K_{a,b}<Q^{1/2}\), the trivial channel count is already \(O(Q^{1/2})\).
Thus (D7) holds for every channel.  The displayed error records both the
short-interval branch and the complete sieve remainder rather than silently
importing a fixed-coefficient constant.

### Sum over growing coefficients

For \(M=2L-1\),

\[
\sum_{1\le a,b\le M}\frac1{\max(a,b)}
=\sum_{m=1}^M\frac{2m-1}{m}
=2M-\sum_{m=1}^M\frac1m
<4L. \tag{D8}
\]

Summing (D7), the \(O(L^2)\) constant and sieve-remainder terms are absorbed
for polylogarithmic \(L\), and

\[
C_L(Q)\ll_A
\frac{LQ\log\log(3LQ)}{(\log Q)^2}. \tag{D9}
\]

With \(P(Q)=\pi(2Q)-\pi(Q)\sim Q/\log Q\),

\[
\frac{C_L(Q)}{P(Q)}
\ll_A\frac{L\log\log(3LQ)}{\log Q}. \tag{D10}
\]

Thus \(L=o(\log Q/\log\log Q)\) implies \(C_L(Q)/P(Q)\to0\).

### Energy transfer

At most \(2C_L(Q)\) prime rows are incident to a collision.  If row masses
have fixed ratio at most \(\kappa\), their mass fraction is at most
\(2\kappa C_L(Q)/P(Q)\).  The TPC-230 unmatched-mass floor then shows that
the maximum proportional saving is \(o(1)\) throughout the subcritical range.

## Remarks and interpretation

- Growing depth removes the fixed-family hypothesis of TPC-231, but not the
  density obstruction until approximately logarithmic depth.
- The result is a necessary-depth theorem, not a resonance lower bound.
- The clock is algebraically consistent throughout the declared range, but
  physical V59 attachment remains a separate source theorem.

## Boundaries and non-claims

- No claim is made at \(L\asymp\log Q/\log\log Q\) or above.
- An upper bound does not show that enough resonances exist at critical depth.
- The finite scan is not asymptotic evidence.
- No actual source mass, sign, \(L^2\), strict \(1/400\), full Gate B, or
  twin-prime theorem is proved.

## Open risks

The next minimal question is whether critical depth remains a legitimate
well-conditioned row family and whether its actual incident mass can approach
a fixed proportion before attempting any V59 attachment.
