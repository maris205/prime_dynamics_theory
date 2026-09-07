# A Finite Literal V59 Residual-Radius and Signed-Phase Census

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 26 August 2026
- Source repository commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`
- Converter: `source-markdown-audit-v2`

## Abstract

The current Bridge-B obstruction for the twin-prime program is an exact orthogonal residual left after a source-backed rank-three channel. We give the first finite replay in which the residual is formed from the physical prime shell, both unit masks, the deleted diagonal, the source coefficient $\beta$, and the shifted-prime comparison $w=\Lambda(\cdot+2)-b^{(2)}$. For twelve natural finite representatives of the V59 clock and two explicit nonnegative Fourier profiles, rational interval arithmetic certifies the identity $C=C_3+C_\perp$, positivity of the residual radius, and $\lvert C_\perp\rvert/R<1/4$. The largest certified upper endpoint is $0.2320126753$. This is a finite signed-phase observation, not an asymptotic power-saving theorem: the radius itself, its growing-parameter phase, arithmetic $L^2$, and the twin-prime conclusion remain open.

<!-- SOURCE_BODY_BEGIN -->

# Position and claim firewall

TPC-266 composed three previous interfaces without allowing a fixed-log center to become a power bound or allowing the orthogonal residual to be deleted. Its remaining input is a literal V59 radius or signed-phase estimate with effective saving strictly larger than $1/400$. The present paper takes a deliberately finite step toward that input. It does not pretend that a finite table is an asymptotic theorem.

Our status is therefore

`FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS`\
*numerically certified finite result*.

The exact operator and projection algebra are proved finite identities. The real-number evaluations use outward intervals and are reported as numerical certificates. The two kernel profiles and rounded finite clocks are explicit modeling choices, so no uniform smooth-profile assertion is made.

# The finite physical object

Let $N$ be even and put $$I_N=\{N/2+1,\ldots,N\},\qquad
 \mathcal Q_Q=\{q:q\text{ prime},\ Q<q\leq 2Q\}.$$ For $s\in\{1,2\}$, we use $$K_{H,s}(h)=\left(1+(h/H)^2\right)^{-s}.                 \tag{1}$$ These kernels are Fourier transforms of explicit normalized nonnegative profiles. For example, for $s=1$, one may take $\psi_1(v)=\pi e^{-2\pi\lvert v\rvert}$; for $s=2$, take $\psi_2(v)=\frac\pi2(1+2\pi\lvert v\rvert)e^{-2\pi\lvert v\rvert}$. The profiles are used only to define a finite audit kernel.

The source coefficient is $$\beta_N(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d^{400}\leq N^{133}}}\mu(d).       \tag{2}$$ The first term is rational on every finite input: it equals $1/k$ when $t=p^k$, and is zero otherwise. We use the coarse shifted-prime comparison $$b^{(2)}(u)=2C_2\,1_{2\nmid u}
       \prod_{\substack{p\mid u\\p>2}}\frac{p-1}{p-2},qquad
 C_2=\prod_{p>2}\left(1-\frac1{(p-1)^2}\right),                 \tag{3}$$ and $w_N(u)=\Lambda(u+2)-b^{(2)}(u)$.

The finite matrix is $$A(u,t)=1_{u\ne t}\sum_{q\in\mathcal Q_Q}qK_{H,s}(u-t)1_{q\nmid ut}
 \left(1_{u\equiv t\pmod q}-\frac1{q-1}\right).             \tag{4}$$ Thus the diagonal is deleted before any absolute value, and the outer prime weight is retained. Set $g=A\beta_N$ and $$C=\sum_{u\in I_N}w_N(u)g(u).                                \tag{5}$$

# The rank-three residual

Split $I_N$ into four equal consecutive blocks of size $B=|I_N|/4$. Use the base contrasts $$c_0=(1,1,-1,-1),\qquad c_1=(1,-1,0,0),\qquad
 c_2=(0,0,1,-1).                                               \tag{6}$$ They are pairwise orthogonal as vectors on $I_N$, with squared norms $4B,2B,2B$. If $W_j$ and $G_j$ denote their block contrast sums against $w_N$ and $g$, respectively, define $$C_3=\frac{W_0G_0}{4B}+\frac{W_1G_1}{2B}+\frac{W_2G_2}{2B},
 \qquad C_\perp=C-C_3.                                        \tag{7}$$

> **Proposition: finite projection identity** For every finite row, (7) is the cross-Gram of the orthogonal projection onto the span of the three contrasts, and $$C_\perp=\langle (I-P_3)w_N,(I-P_3)g\rangle.                 \tag{8}$$ Moreover, with $$R^2=\left\lVert (I-P_3)w_N\right\rVert^2\left\lVert (I-P_3)g\right\rVert^2,                   \tag{9}$$ we have $R^2>0$ on every certified row.

> **Proof** The three vectors in (6) have disjoint or cancelling block sums, so their pairwise inner products vanish. The orthogonal projection formula for a non-normalized orthogonal vector $c_j$ is $P_3f=\sum_j\langle c_j,f\rangle c_j/\left\lVert c_j\right\rVert^2$. Taking the cross-Gram of the two projected vectors gives (7), and subtracting it from (5) gives (8). Applying the same formula to the two squared norms gives (9). The strict positivity is checked by the rational interval certificate described next.

# Certified intervals

The only infinite object in (3) is $C_2$. Let $P=50000$ and multiply the factors through $P$. Since $0\leq a_i<1$, $$\prod_i(1-a_i)\geq1-\sum_i a_i,$$ and $$\sum_{p>P}\frac1{(p-1)^2}
 \leq\sum_{m=P}^{\infty}\frac1{m^2}<\frac1{P-1}.             \tag{10}$$ This gives a rational lower and upper endpoint for $C_2$. Every logarithm in $\Lambda(u+2)$ is enclosed by a 100-digit decimal evaluation with a $10^{-25}$ guard, then rounded outward to a rational grid of width $10^{-30}$. All later interval operations are exact rational operations.

The certificate does not take a square root to decide the phase contraction. It computes the interval quotient $$\rho^2=\frac{|C_\perp|^2}{R^2}                           \tag{11}$$ and verifies $\sup\rho^2<1/16$. This is both numerically stable and faithful to the Schur radius interface from TPC-264 and TPC-265.

> **Theorem: twelve finite contractions** For the twelve rows $$\begin{split}
>  &(N,H,Q,s)=(64,15,4,1),(64,15,4,2),\\
>  &(96,20,5,1),(96,20,5,2),(128,24,5,1),(128,24,5,2),\\
>  &(192,32,6,1),(192,32,6,2),(256,38,6,1),(256,38,6,2),\\
>  &(384,50,7,1),(384,50,7,2),
> \end{split}$$ the interval computation gives $R^2>0$ and $$\sup \rho^2<\frac1{16},\qquad\text{hence}\qquad
>  \frac{|C_\perp|}{R}<\frac14.                               \tag{12}$$ The largest stored upper endpoint for $|C_\perp|/R$ is $0.2320126753$. The residual interval is negative on the real axis in ten rows and positive in two rows.

> **Proof** The producer enumerates the finite prime shell, evaluates (2) exactly, forms (4) with rational kernel entries, and applies the projection formula (7). The interval endpoints for the shifted logarithms and (3) are propagated by exact rational interval addition, multiplication, squaring, and division. The twelve stored upper endpoints of (11) are all below $1/16$; the independent replay recomputes the corresponding floating-point ratios and finds all twelve below $1/4$. The complete values and interval endpoints are included in `results/tpc267_certificate.json`.

|    N|    H|    Q|    s|  $\#\mathcal Q_Q$|  upper $\rho$| phase    |
|----:|----:|----:|----:|-----------------:|-------------:|:---------|
|   64|   15|    4|    1|                 2|  0.2320126753| negative |
|   64|   15|    4|    2|                 2|  0.1739441111| negative |
|   96|   20|    5|    1|                 1|  0.2138888503| negative |
|   96|   20|    5|    2|                 1|  0.1908411939| negative |
|  128|   24|    5|    1|                 1|  0.1267919366| negative |
|  128|   24|    5|    2|                 1|  0.1512378362| negative |
|  192|   32|    6|    1|                 2|  0.0066519390| negative |
|  192|   32|    6|    2|                 2|  0.0204279911| negative |
|  256|   38|    6|    1|                 2|  0.0093009287| positive |
|  256|   38|    6|    2|                 2|  0.0410812441| positive |
|  384|   50|    7|    1|                 2|  0.0631257787| negative |
|  384|   50|    7|    2|                 2|  0.0484836866| negative |

: Selected finite residual phase bounds. The displayed value is an upper endpoint; the full rational intervals are stored in the certificate.

# What the census does and does not say

The result is stronger than an abstract Schur witness in one precise sense: the vectors entering the finite residual are generated by the physical prime shell and source-shaped coefficients. It is weaker than the open theorem in three equally precise senses.

First, the radius $R$, not just the correlation ratio, is large enough that no exponent can be inferred from the table. Second, the phase sign changes between rows, so the data do not support a universal fixed ray. Third, the finite kernel and comparison cutoff are declared choices. Replacing them by the growing $z=(\log x)^K$ comparator and a source-specified smooth profile requires a new uniform theorem.

In particular, (12) is not a payment of the endpoint budget. TPC-266 requires a power or signed-phase saving with effective size strictly greater than $1/400$ on the common asymptotic clock. A finite ratio bounded away from one is neither of those. We therefore record $$\texttt{FIXED\_POWER\_CREDIT=0},\quad
 \texttt{ARITHMETIC\_ADVANCE=NO},\quad
 \texttt{FULL\_GATE\_B=OPEN}.$$

# Conclusion and next experiment

TPC-267 establishes a reproducible physical finite interface for the object that TPC-266 left open. The reusable construction is $$\text{literal }A\ \longrightarrow\ P_3\text{ split}\ \longrightarrow\
 R^2\text{ interval}\ \longrightarrow\text{signed phase ratio}.$$ The next minimal question is adversarial stability: vary the rounded clock, the local cutoff, and a genuinely smooth profile. If the contraction breaks, that failure is a useful obstruction; if it survives, it supplies evidence for a source-level sector lemma. Neither outcome alone is an asymptotic arithmetic theorem.

# References

9 L. Wang, “Typed end-to-end claim firewall,” TPC-266 project, 2026. L. Wang, “Schur radius to endpoint-budget compiler,” TPC-265 project, 2026. L. Wang, “Four-block Haar transverse norm floor,” TPC-257 project, 2026. L. Wang, “Polarized local BDH scalar compiler,” Bridge-B V59 source note, 2026.

<!-- SOURCE_BODY_END -->
