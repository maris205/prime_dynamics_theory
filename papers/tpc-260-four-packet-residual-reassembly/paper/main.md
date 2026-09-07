# A Null-Compatible Four-Packet Completion Obstruction\ for the Literal V59 Interface

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding same-clock analysis suppresses one source-frozen rank-one channel of the signed V59 coupling, but leaves an orthogonal residual. We give an exact finite audit of whether four packet marginals and the existing Haar information can control that residual. First, a polygon-completion theorem gives the sharp range of the full residual for fixed packet norms. Second, a four-point discrete Fourier transform (DFT) identifies the missing datum: packet diagonal energy fixes the sum of all mode energies, whereas the full reassembly is precisely mode zero. In the equal-norm case, two packet families have identical norms, vanish on every Haar contrast and on the TPC-259 null channel, yet have full residual energies $16$ and $0$. The result is a structural obstruction, not a prime-shell counterexample. It converts the next arithmetic task into a precise one: prove a common-clock mode-zero or cross-Gram estimate while retaining the hard window, deleted diagonal, unit masks, and the physical residual.

<!-- SOURCE_BODY_BEGIN -->

# Scope and motivation

The V59 Route-B object is a signed coupling on a fixed real clock. Recent work constructed a four-block Haar frame and then chose a source-frozen transverse vector that cancels the known diagonal asymptotic. Coupling that vector to the literal hybrid sequence gives an exact split $$\left\langle w,A_x\beta\right\rangle
 =\overline{\left\langle z_{\rm null},w\right\rangle}\,\left\langle z_{\rm null},A_x\beta\right\rangle
   +\left\langle w_\perp,A_x\beta\right\rangle,
 \qquad
 w_\perp=w-\left\langle z_{\rm null},w\right\rangle z_{\rm null}.
 \label{eq:tpc259-split}$$ The first term is source-backed and arbitrarily small in fixed logarithmic powers; the second term is not estimated. This paper asks a deliberately narrower question: can the residual be recovered from packet norms and the finite Haar projections already present in the interface?

The answer is no at the level of finite Hilbert-space algebra. The obstruction is useful because it does not merely repeat a generic Gram example. It keeps the specific source-frozen null direction, embeds it in the four-block Haar complement, and gives a sharp continuum of compatible residual sizes. Thus it tells us exactly which information a future literal theorem must add.

Our contributions are:

1.  an exact weighted four-block Haar complement containing the TPC-258 null direction;

2.  a sharp polygon interval for the residual under fixed packet marginals and a zero null channel;

3.  a four-packet DFT ledger showing that the unresolved quantity is mode zero, not the total diagonal energy; and

4.  an exact plus/alternating witness, checked over varied block sizes, that refutes uniform promotion from these marginals to full reassembly.

All statements below are finite and structural. In particular, no finite record is used as evidence for a growing prime-distribution estimate.

# The four-block interface

Let $B_0,B_1,B_2,B_3$ be consecutive nonempty blocks with lengths $s_0,s_1,s_2,s_3$ and $N=s_0+s_1+s_2+s_3$. On blockwise-constant vectors use the weighted inner product $$\left\langle u,v\right\rangle_s=\sum_{j=0}^3s_j\,\overline{u_j}v_j.$$ Write $\ell=s_0+s_1$ and $r=s_2+s_3$. The three contrasts used in the recent V59 construction are $$\begin{aligned}
 z_0&=\rho_0\left(\frac1\ell,\frac1\ell,-\frac1r,-\frac1r\right),
 &\rho_0^2&=\frac{\ell r}{N},\\
 z_1&=\rho_1\left(\frac1{s_0},-\frac1{s_1},0,0\right),
 &\rho_1^2&=\frac{s_0s_1}{\ell},\\
 z_2&=\rho_2\left(0,0,\frac1{s_2},-\frac1{s_3}\right),
 &\rho_2^2&=\frac{s_2s_3}{r}.\end{aligned}$$ Direct counting gives $$\left\langle z_a,z_b\right\rangle_s=\delta_{ab},\qquad
 \left\langle \boldsymbol 1,z_a\right\rangle_s=0 \quad (0\leq a,b\leq2).
 \label{eq:haar}$$ The normalized scaling direction is $e_{\rm sc}=\boldsymbol 1/\sqrt N$. Consequently, $z_0,z_1,z_2,e_{\rm sc}$ form an orthonormal basis of the four-dimensional block space. In particular, the source-frozen vector $$z_{\rm null}=\frac{L_2z_1-L_1z_2}{\sqrt{L_1^2+L_2^2}},\qquad
 L_1=\log\frac{3456}{3125},\quad
 L_2=\log\frac{884736}{823543},
 \label{eq:null}$$ is orthogonal to $e_{\rm sc}$. Notice that this conclusion uses only the exact zero weighted sums in [\[eq:haar\]](main.tex#L111){reference-type="eqref" reference="eq:haar"}; it does not use numerical values for the logarithms.

For comparison, the prior four-packet polarization result established that a general packet Gram matrix is positive semidefinite and that diagonal/trace data do not determine signed cross terms. Here we specialize the obstruction to the new same-clock residual: the packets will lie in the scaling complement of the Haar contrasts, so all three contrast measurements are fixed at zero.

# A sharp null-compatible completion theorem

Let $z,w$ be orthonormal vectors in a complex Hilbert space $\mathcal H$. We regard $z$ as the source-frozen null direction and $w$ as a possible residual direction. A four-packet family is $V_0,V_1,V_2,V_3\in\mathcal H$ and its full output is $G=\sum_jV_j$.

> **Theorem: polygon completion** Fix nonnegative packet lengths $d_0,d_1,d_2,d_3$. Among the families $$V_j=d_j e^{\mathrm i\theta_j}w,
>  \qquad \theta_j\in\mathbb R,$$ the null condition $\left\langle z,G\right\rangle=0$ holds identically. If $$D=\sum_{j=0}^3d_j,\qquad d_{\max}=\max_jd_j,$$ then the possible residual moduli $$R=\left\langle w,G\right\rangle$$ are exactly $$\max\{2d_{\max}-D,0\}\leq |R|\leq D.
>  \label{eq:polygon}$$ Every modulus in this interval and every argument is attained.

> **Proof** The scalar $R=\sum_jd_je^{\mathrm i\theta_j}$ is the sum of four planar vectors with prescribed lengths. The triangle inequality gives the upper endpoint. If one side is longer than the other three combined, reversing the shorter sides gives the lower endpoint $d_{\max}-(D-d_{\max})$. Otherwise the four sides close to a polygon, so the lower endpoint is zero. Rotating one side continuously fills the interval between the two endpoints; a common rotation supplies any argument. Since $z\perp w$, every member of the family has $\left\langle z,G\right\rangle=0$. The same two triangle inequalities apply to every choice of phases, proving sharpness.

For equal packet lengths $d_j=1$, the interval is $[0,4]$, and the squared residual can range over $[0,16]$. This is a completion statement, not merely two isolated examples.

> **Corollary: Haar-complement realization** In the four-block space above, take $z=z_{\rm null}$ and $w=e_{\rm sc}$. The families in the theorem have zero projection on $z_0,z_1,z_2$, zero TPC-259 rank-one coefficient $\left\langle z,w\right\rangle$, and residual range [\[eq:polygon\]](main.tex#L156){reference-type="eqref" reference="eq:polygon"}.

> **Proof** Equation [\[eq:haar\]](main.tex#L111){reference-type="eqref" reference="eq:haar"} makes $e_{\rm sc}$ orthogonal to each contrast, and [\[eq:null\]](main.tex#L120){reference-type="eqref" reference="eq:null"} makes it orthogonal to $z_{\rm null}$. Substitute these vectors into the theorem.

The corollary is the key distinction from a purely abstract diagonal counterexample: the same finite Haar geometry used to select the null direction supplies a concrete orthogonal completion direction. It also makes clear why suppressing the first term in [\[eq:tpc259-split\]](main.tex#L61){reference-type="eqref" reference="eq:tpc259-split"} says nothing by itself about the second.

# The missing DFT mode

The polygon theorem describes the size ambiguity. The following identity locates its information-theoretic source. Define the four-point packet DFT by $$\widehat V_k=\frac12\sum_{j=0}^3\mathrm i^{-jk}V_j,
 \qquad 0\leq k\leq3.
 \label{eq:dft}$$

> **Theorem: mode ledger** For arbitrary packets in a complex Hilbert space, $$\begin{aligned}
>  \sum_{k=0}^3\left\lVert \widehat V_k\right\rVert^2&=\sum_{j=0}^3\left\lVert V_j\right\rVert^2, \label{eq:parseval}\\
>  G=\sum_{j=0}^3V_j&=2\widehat V_0, \label{eq:inverse}\\
>  \left\lVert G\right\rVert^2&=4\left\lVert \widehat V_0\right\rVert^2. \label{eq:modezero}\end{aligned}$$ Thus packet diagonal energy determines the sum of mode energies, while full reassembly asks for the individual mode-zero energy.

> **Proof** The matrix $(2^{-1}\mathrm i^{-jk})_{k,j}$ is unitary, which gives [\[eq:parseval\]](main.tex#L206){reference-type="eqref" reference="eq:parseval"}. Fourier inversion at index zero gives [\[eq:inverse\]](main.tex#L207){reference-type="eqref" reference="eq:inverse"}, and taking norms gives [\[eq:modezero\]](main.tex#L208){reference-type="eqref" reference="eq:modezero"}.

The distinction is exact in the two families $$\begin{aligned}
 V_j^+&=w, & (j=0,1,2,3),\\
 V_j^-&=(-1)^jw, & (j=0,1,2,3).\end{aligned}$$ Both have packet diagonal $(1,1,1,1)$, total packet energy $4$, zero projection on every Haar contrast, and zero null channel. Yet $$\bigl(\left\lVert \widehat V_k^+\right\rVert^2\bigr)_{k=0}^3=(4,0,0,0),
 \qquad
 \bigl(\left\lVert \widehat V_k^-\right\rVert^2\bigr)_{k=0}^3=(0,0,4,0),$$ so their full residual energies are $16$ and $0$. The alternating family has simply moved all energy from mode zero to mode two. A fourth-root rotating family similarly moves it to mode one.

The full energy can also be written directly as $$\left\lVert G\right\rVert^2=\sum_j\left\lVert V_j\right\rVert^2
  +2\operatorname{Re}\sum_{0\leq j<\ell\leq3}\left\langle V_j,V_\ell\right\rangle.
 \label{eq:crossgram}$$ Therefore a literal proof must estimate a phase-sensitive cross-Gram sum (or an equivalent mode-zero quantity). A bound on the diagonal sum alone cannot do so.

# Finite audit and route consequence

The release certificate reconstructs 128 varied positive four-block families. For each family it checks all three exact Haar norms, all three pairwise orthogonalities, all three scaling complements, and the null/scaling complement. It then checks the plus, alternating, and fourth-root phase patterns using exact Gaussian rational arithmetic. The resulting counts are shown in Table [1](main.tex#L257){reference-type="ref" reference="tab:checks"}.

<div id="tab:checks">

| Quantity                         |   Count|
|:---------------------------------|-------:|
| Four-block families              |     128|
| Haar norm identities             |     384|
| Haar orthogonality identities    |     384|
| Scaling-complement identities    |     384|
| Null/scaling complements         |     128|
| Phase families                   |       3|
| Exact endpoint residual energies |  $0,16$|

: Finite exact audit counts. These are reproducibility checks, not asymptotic evidence.

</div>

The producer, independent checker, and stress checker all pass in both ordinary and optimized Python modes. The PDF and certificate are frozen by the accompanying bridge checker. These checks establish the algebra and guard against accidental promotion of a finite witness to a prime theorem; they do not estimate the literal V59 mode-zero output.

The resulting claim firewall is:

| Item                                         | Status                |
|:---------------------------------------------|:----------------------|
| Haar complement and polygon completion       | PROVED\_EXACT\_FINITE |
| Four-packet DFT ledger                       | PROVED\_EXACT         |
| Null-compatible residual non-identifiability | REFUTED\_SCOPED       |
| Literal prime-shell counterexample           | NONE                  |
| Arithmetic $L^2$ and full Gate B             | NONE / OPEN           |
| Strict global $1/400$ and fixed atom         | UNPAID / ZERO         |
| Twin-prime conclusion                        | NONE                  |

This is a scoped Route-B advance: it removes a tempting but invalid promotion rule and leaves a sharply stated positive target. The next theorem should control $$\left|\left\langle w_\perp,\sum_{j=0}^3V_j\right\rangle\right|
 \quad\text{or equivalently the mode-zero/cross-Gram quantity in
 \eqref{eq:modezero}--\eqref{eq:crossgram},}$$ for the common literal V59 packet output. It must retain the hard window, deleted diagonal, unit masks, and both boundary lanes. The finite completion result gives no license to drop any of them.

# Conclusion

TPC-259’s source-backed null-channel suppression is a genuine projected result, but the orthogonal residual is an independent degree of freedom. TPC-260 makes this statement exact: fixed packet marginals and all existing four-block contrast data allow a sharp polygon range, including residual energies zero and sixteen. A DFT rephrasing shows that the missing arithmetic information is mode selection, or the equivalent signed cross-Gram correlation.

The result is intentionally modest. It neither proves nor disproves a cancellation in the growing prime shell, and it pays no arithmetic $L^2$ or endpoint credit. Its value is diagnostic: the next useful paper must attack a common-clock mode-zero estimate directly. The local Route-A/Route-B evaluator files named in the Session plan are absent from this checkout; the proof package, theorem ledger, certificate, bridge checker, and repository policy are the fail-closed evaluation record.

# References

9 L. Wang. Four-packet polarization and the PSD cross-term obstruction. Session report TPC-222, 2026.

L. Wang. Four-block Haar lifts and a transverse norm floor for the literal V59 adjoint. Session report TPC-257, 2026.

L. Wang. A source-frozen transverse null direction for the literal V59 adjoint. Session report TPC-258, 2026.

L. Wang. A same-clock null-channel decomposition for the literal V59 signed coupling. Session report TPC-259, 2026.

<!-- SOURCE_BODY_END -->
