# An Operator-Level Signed Projector Interface for Literal Prime–Shell Reassembly

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 1 September 2026
- Source repository commit: `88c46824c79e9c202a698cf4db36fcaf98260537`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding finite audits used a positive-semidefinite direct-sum Gram matrix for a deleted-diagonal, centered prime–shell operator. That construction records each prime block in an orthogonal output channel and therefore does not specify how cross-prime signs are to be reassembled. We introduce a finite operator-level interface: a sign-labelled isometric diagonal embedding and its orthogonal projector. If $B_p$ denotes the literal block and $C_e=\sum_p e_pB_p$, the projected Hilbert–Schmidt energy is exactly $m^{-1}\|C_e\|_F^2$, and the unnormalised ratio is a quadratic form of the Frobenius cross-block Gram. On the 24-row TPC-321 panel, exhaustive sign search finds a ratio below one and a ratio above one on every row. The all-plus law amplifies on 21 rows, whereas the prime-order alternating law contracts on 21 rows. The finite ratios range from $0.59905756561947343$ to $6.8711947177741193$. These results certify a precise signed interface and a finite sign-law obstruction; they do not provide a canonical arithmetic weight, a growing $L^2$ estimate, a power saving, or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

This paper remains in one dynamical-system family. TPC-321 found that the trace-normalised ordered spectrum of the positive Gram matrix is sensitive to the choice of prime shell. The next missing piece is not another scalar normalisation, but a typed answer to the following question:

> How can a direct-sum prime-shell output be projected back onto a coherent signed channel without silently discarding the cross-prime terms?

The answer below is finite and operator-level. It is deliberately agnostic about which sign vector would be supplied by an arithmetic theorem. This separation matters: a sign pattern that contracts one finite operator is not automatically a Mobius weight or a source-native cancellation estimate.

# Literal blocks and the direct-sum output

Let $I_X=(X/2,X]\cap\mathbb Z$, let $N=|I_X|$, and put $H=66$. For $\mathcal S_Q=\{p:Q<p\leq2Q,\ p\text{ prime}\}$ and $s\in\{1,2\}$, define $$B_p(u,t)=\mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}
 \frac{pH^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{u\equiv t\pmod p}-\frac{1}{p-1}\right).
 \label{eq:block}$$ The matrix $B_p$ has rows and columns indexed by $I_X$. With $m=|\mathcal S_Q|$, form the direct-sum map $$A_\oplus v=(B_pv)_{p\in\mathcal S_Q}:
 \mathbb R^N\longrightarrow\bigoplus_{p\in\mathcal S_Q}\mathbb R^N.
 \label{eq:direct}$$ The orthogonality of the output labels gives $$\|A_\oplus\|_{\operatorname{HS}}^2=D:=\sum_{p\in\mathcal S_Q}\|B_p\|_F^2.
 \label{eq:direct-energy}$$ The positive Gram construction $A_\oplus^{\mathsf T}A_\oplus$ contains only the diagonal terms in the prime label. It is therefore a useful envelope, but it is not itself a signed reassembly.

# Signed diagonal projection

For $e=(e_p)_p\in\{-1,+1\}^m$, define $$E_ev=m^{-1/2}(e_pv)_p,
 \qquad P_e=E_eE_e^{\mathsf T}.
 \label{eq:projector}$$ Since $E_e^{\mathsf T}E_e=I_N$, $P_e$ is the orthogonal projection onto a sign-labelled diagonal copy of $\mathbb R^N$. The coherent signed operator is $$C_e=\sum_{p\in\mathcal S_Q}e_pB_p.
 \label{eq:coherent}$$

> **Proposition: exact signed projector identity** For every finite block family and every sign vector $e$, $$P_eA_\oplus v=E_e(m^{-1/2}C_ev),
>  \qquad
>  \|P_eA_\oplus\|_{\operatorname{HS}}^2=\frac1m\|C_e\|_F^2.
>  \label{eq:identity}$$

> **Proof** The identity $E_e^{\mathsf T}E_e=I_N$ follows from $m^{-1}\sum_pe_p^2=1$. Applying $E_e^{\mathsf T}$ to $A_\oplus v$ gives $m^{-1/2}\sum_pe_pB_pv$. Applying $E_e$ again gives the first equality. The map $E_e$ is an isometry, so summing squared norms over the source basis gives the second equality.

Define the unnormalised reassembly ratio and the projected fraction by $$\rho_e=\frac{\|C_e\|_F^2}{D},
 \qquad \phi_e=\frac{\|P_eA_\oplus\|_{\operatorname{HS}}^2}{D}=\frac{\rho_e}{m}.
 \label{eq:ratios}$$ The distinction between the two quantities prevents a misleading interpretation of an amplified coherent sum: projection contraction applies to $\phi_e$, not to the unnormalised sum ratio $\rho_e$.

# Cross-block Gram and exact algebra

Let $H^{\rm blk}$ be the $m\times m$ Frobenius Gram $$H^{\rm blk}_{p,q}=\langle B_p,B_q\rangle_F.
 \label{eq:blockgram}$$ It is positive semidefinite, and $D=\operatorname{tr}(H^{\rm blk})$. Expanding [\[eq:coherent\]](main.tex#L99){reference-type="eqref" reference="eq:coherent"} yields the exact quadratic form $$\rho_e=\frac{e^{\mathsf T}H^{\rm blk}e}{\operatorname{tr}(H^{\rm blk})}
 =1+\frac{2\sum_{p<q}e_pe_qH^{\rm blk}_{p,q}}{D}.
 \label{eq:quadratic}$$ This is the first point at which signed cross-prime information appears. Also, $C_{-e}=-C_e$, so $\rho_{-e}=\rho_e$; fixing one sign to $+1$ merely removes a global gauge duplication.

# Finite protocol

The declared panel is $$X\in\{640,1280,2560\},\qquad Q\in\{24,36,54,80\},\qquad s\in\{1,2\}.$$ It contains 24 literal matrices. Four named sign laws are tested: all-plus; alternating signs in increasing prime order; the sign $+1$ for $p\equiv1\pmod4$ and $-1$ for $p\equiv3\pmod4$; and a half split in prime order. In addition, all $2^{m-1}$ sign vectors with the first sign fixed are enumerated. The largest shell has $m=15$, so the largest search has 16,384 vectors.

The producer computes the block Gram by explicit elementwise Frobenius sums in forward and reverse shell order. Each ratio is enclosed by an outward guard of $10^{-12}$. The independent checker rebuilds the blocks in reverse order and uses ‘einsum‘ for each block inner product; it does not import the producer. A small $16\times16$ rational anchor with shell $\{5,7\}$ checks the exact quadratic identity independently of the large floating-point panel.

# Results

Table [1](main.tex#L178){reference-type="ref" reference="tab:atlas"} reports the finite sign-law census. “Below” and “above” refer to $\rho_e$ relative to the direct-sum energy $D$; they do not refer to the projected fraction $\phi_e$.

<div id="tab:atlas">

| Sign law or search         | $\rho<1$ | $\rho>1$ |
|:---------------------------|:--------:|:--------:|
| All-plus                   |     3    |    21    |
| Index-alternating          |    21    |     3    |
| Mod-4 character            |    19    |     5    |
| Half split                 |    21    |     3    |
| Exhaustive minimum/maximum |    24    |    24    |

: Finite operator-level reassembly census on 24 rows.

</div>

The exhaustive minimum ratio lies in the finite range $$0.59905756561947343\leq\rho_{\min}\leq0.98033069254228578,$$ while the maximum lies in $$1.0122088324409428\leq\rho_{\max}\leq6.8711947177741193.$$ The endpoints include the declared two-path outward guard. In every row, therefore, the sign-labelled coherent channel can be made smaller than the direct-sum diagonal energy and can also be made larger. The named laws do not agree: the all-plus choice mostly reinforces the blocks, whereas the index-alternating choice mostly cancels them, with three finite reversals in each direction.

The exact anchor uses $I=\{17,\ldots,32\}$, $Q=4$, $s=1$, and shell $\{5,7\}$. Its direct energy is approximately $1476.201999985143$ and the $(+,-)$ coherent energy is approximately $1613.337756768249$. The producer and independent checker compare exact rational digests for both quantities; the decimal values are only a readable view.

# Interpretation and route status

The positive result is a typed finite interface: the previously implicit “signed reassembly” is an orthogonal projection followed by a coherent operator, with all cross-block terms visible in one PSD Gram. This interface is reusable for the next spectral-profile audit.

The obstruction is equally important. A finite sign vector exists in both directions on every row, and two simple named laws have opposite dominant behaviour. Consequently the current data do not select a canonical sign law. The result is not a contradiction: $\phi_e=\rho_e/m\leq1$ always, and $\rho_e>1$ only says that coherent addition can exceed the sum of diagonal block energies before the $m^{-1}$ projector factor.

No arithmetic advance is claimed. The signs were selected by finite operator geometry, not supplied by a source theorem for the prime weights. There is no growing source-image estimate, no signed arithmetic $L^2$ bound, no fixed-power credit, and no Route-B Gate-B closure. The official Session-named evaluator files are absent from this checkout; the local bridge is a fail-closed reproducibility record only.

# Statements

#### Data availability.

All finite inputs, source code, certificate, and replay commands are included in this project directory.

#### Ethics declaration.

This work uses no human participants, personal data, or biological materials.

#### Author contributions.

Liang Wang: conceptualisation, formal analysis, software, validation, and writing.

#### Conflict of interest.

The author declares no conflict of interest.

#### Funding.

No external funding is claimed for this finite audit.

#### AI-use disclosure.

An AI assistant was used for bounded code and document assistance; all mathematical claims, scope labels, and release decisions were checked against the local source and executable certificate.

# Conclusion

TPC-322 connects the PSD direct-sum surrogate to a precise signed projector without hiding the cross-prime terms. Its 24-row atlas establishes finite sign flexibility and rejects two simple universal sign laws on the declared panel. The next necessary question is whether any canonical sign law survives at the ordered spectral-profile level and, separately, whether a source-native arithmetic theorem can pay for it. Neither conclusion follows from the present finite ratios.

<!-- SOURCE_BODY_END -->
