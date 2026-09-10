# Literal arithmetic lane norms and the norm-method budget

Date: 2026-09-09. Unnumbered proof; round-1 independent lane audit passed.
Precision corrections are implemented for bounded delta review.
Use exactly the definitions in DERIVATION_PACKAGE.md, including the original
hybrid \(b_x^{(z)}\), the physical shift 2, and
\(z=(\log x)^K\) for fixed \(K>0\).
No coefficient is replaced in the scalar. Envelopes below estimate norms only.
Throughout \(x\ge x_0(K)\), in particular \(z=(\log x)^K\ge2\).
The legacy clock is \(x=2X\); exact cardinality is
\(N=\lfloor x\rfloor-\lfloor x/2\rfloor\).

## L1. Hybrid second moment

For \(p>2\) let
\[
 a(p)=\left(\frac{p-1}{p-2}\right)^2-1>0,\qquad
 B_0=\prod_{p>2}(1+a(p)/p)<\infty .
\]
Convergence follows from \(a(p)=2/(p-2)+1/(p-2)^2=O(1/p)\);
the finite prime \(p=3\) causes no difficulty. Expand the nonnegative square:
\[
 \prod_{\substack{p\mid n\\p>z}}\left(\frac{p-1}{p-2}\right)^2
 =\sum_{\substack{d\mid n\\d\ \mathrm{squarefree}\\P^-(d)>z}}a(d),
 \quad a(d)=\prod_{p\mid d}a(p),\quad a(1)=1 .
\]
Since \(0<C_z\le1\) and the low-prime mask is at most 1, extending the
dyadic interval to \(1\le n\le x\), then interchanging nonnegative sums,
gives the rigorous bound
\[
 \|b_x^{(z)}\|_2^2
 \le W_z^2\sum_{d\le x}a(d)\lfloor x/d\rfloor
 \le xW_z^2\prod_{p>z}(1+a(p)/p)\le B_0xW_z^2.          \tag{L1}
\]
The unqualified \(d\)-sum in this display retains the squarefree and
least-prime-factor restrictions from the previous display. This bound is
valid for every \(z\ge2\); constants in \(B_0\) are absolute.

Mertens' product theorem gives \(W_z\ll\log z\) for \(z\ge2\).
For fixed \(K>0\), therefore,
\[
 \|b_x^{((\log x)^K)}\|_2=O_K(\sqrt x\log\log x)
                 =o(\sqrt{x\log x}).                 \tag{L2}
\]
Only this unconditional classical product theorem is used, not an RH
statement about its error. A primary research source explicitly stating
the baseline theorem is [Lamzouri, A bias in Mertens' product formula, opening paragraph of Section 1](https://arxiv.org/html/1410.3777v2#S1).

## L2. Size of the literal shifted-von-Mangoldt lane

PNT and partial summation imply
\(\sum_{p\le y}(\log p)^2\sim y\log y\). Prime powers of exponent
at least 2 contribute \(O(\sqrt y\log^3 y)=o(y\log y)\) to
\(\sum_{n\le y}\Lambda(n)^2\). Hence
\[
 \sum_{u\in I_x}\Lambda(u+2)^2\sim(x/2)\log x.
\]
The shift by 2 changes at most finitely many boundary integers and is
retained throughout; it does not change this leading asymptotic.
The two-sided norm comparison
\[
 \big|\|w\|_2-\|\Lambda(\cdot+2)\|_2\big|\le\|b_x^{(z)}\|_2
\]
and L2 now give
\[
 \boxed{\|w\|_2^2\sim(x/2)\log x.}                     \tag{L3}
\]
No unproved orthogonality between \(b\) and \(\Lambda(\cdot+2)\) is needed.
In particular this is a norm statement, not a signed mixed-scalar bound.

## L3. A semiprime source of order x/log x for the beta norm

Let \(p,r\) be primes satisfying
\[
 x^{2/5}<p\le x^{9/20},\qquad x/(2p)<r\le x/p.
\]
For sufficiently large \(x\), one has \(p<r\), \(p>U=x^{133/400}\),
and \(r>U\). Thus \(n=pr\in I_x\) has only the divisor \(1\) below
\(U\), is not a prime power, and its literal coefficient is
\(\beta(n)=0-\mu(1)=-1\).
The smaller prime \(p\) is unique, so no products are counted twice.

Let \(M_x\) be the number of these products. Write \(y=x/p\).
Uniformly for this prime range, \(y\ge x^{11/20}\), and the definition
of the PNT limit yields
\[
 \pi(y)-\pi(y/2)=(1+o(1))\,y/(2\log y).
\]
The relative error is uniform because the smallest \(y/2\) tends to
infinity. All summands are nonnegative. Therefore
\[
 M_x=(1+o(1))\frac{x}{2}
       \sum_{x^{2/5}<p\le x^{9/20}}\frac1{p\log(x/p)} .
\]
Apply Stieltjes partial summation with
\(f(t)=1/(t\log(x/t))\).
On this range \(f'<0\), \(|f'|\ll1/(t^2\log x)\);
the uniform error \(\pi(t)-\operatorname{li}(t)=o(t/\log t)\)
contributes \(o(1/\log x)\) after the endpoints and the integral.
The main term is exactly
\[
 \int_{x^{2/5}}^{x^{9/20}}\frac{dt}{t\log t\log(x/t)}
 =\frac1{\log x}\int_{2/5}^{9/20}\frac{da}{a(1-a)}
 =\frac{\log(27/22)}{\log x}.
\]
(The endpoint ratio is \((9/11)/(2/3)=27/22\).)
It follows that
\[
 M_x=(\tfrac12\log(27/22)+o(1))x/\log x,\qquad
 \boxed{\|\beta\|_2^2\ge
        (\tfrac12\log(27/22)+o(1))x/\log x.}            \tag{L4}
\]
The PNT source and its unconditional scope are recorded in PROOF_PACKAGE.md.
No PNT in a moving arithmetic progression or a short interval is used:
the intervals for \(r\) are ordinary dyadic intervals.

For completeness, \(|\beta(n)|\le1+\tau(n)\le2\tau(n)\).
For each exponent \(e\ge0\),
\((e+1)^2\le\binom{e+3}{3}\), since the difference after division
by \(e+1\) is \(e(e-1)/6\ge0\). Consequently
\(\tau(n)^2\le\tau_4(n)\), and
\[
 \|\beta\|_2^2\le4\sum_{n\le x}\tau_4(n)
 \le4x(1+\log x)^3.                                   \tag{L5}
\]
The last inequality counts four factors and bounds the three resulting
harmonic sums separately. This upper estimate is deliberately crude.

## L4. Coefficient-blind and row-normalized norm barrier

Combining L3 and L4,
\[
 \liminf_{x\to\infty}\frac{\|\beta\|_2\|w\|_2}{x}
 \ge\tfrac12\sqrt{\log(27/22)}.
\]
Together with the actual-operator lower bound P7,
\[
 \boxed{\liminf_{x\to\infty}
  \frac{\log Q}{xQ^2}\|A\|\,\|\beta\|_2\,\|w\|_2
 \ge\tfrac34\sqrt{\log(27/22)}>0.}                     \tag{L6}
\]
Therefore every coefficient-blind norm certificate \(B_x\ge\|A\|\)
has a norm-product right-hand side bounded below at this scale.
Such a right-hand side is not \(O(xQ^2x^{-\delta+o(1)})\) for any
fixed \(\delta>0\); it cannot by itself prove the requested estimate
with \(\delta>1/400\).

For the particular full-row normalization \(Z\), P8 and P6 imply the
same barrier up to fixed profile constants. This is not a statement
about every possible preconditioner or every coefficient-sensitive
estimate, and does not forbid using genuine cancellation between the
two specified lanes.

Most importantly, a lower bound on an upper-bound expression is not a
lower bound for \(|\langle w,A\beta\rangle|\). That scalar remains
unestimated at the needed power scale. No arithmetic gate is closed.
