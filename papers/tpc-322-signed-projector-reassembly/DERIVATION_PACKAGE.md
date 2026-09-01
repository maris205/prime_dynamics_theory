# TPC-322 derivation package

## 1. Literal block operator

Let (I_X=(X/2,X]capmathbb Z), (N=|I_X|), (H=66), and
(mathcal S_Q={p:Q<pleq2Q, p {m prime}}).  For (sin{1,2}), define

\[
 B_p(u,t)=\mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}
 \frac{pH^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{u\equiv t\pmod p}-\frac1{p-1}\right).
\]

Here (B_p) is an (N\times N) matrix.  The direct-sum operator is

\[
 A_\oplus v=(B_pv)_{p\in\mathcal S_Q}
 :\mathbb R^N\longrightarrow\bigoplus_{p\in\mathcal S_Q}\mathbb R^N.
\]

Its Hilbert--Schmidt energy is

\[
 D=\|A_\oplus\|_{\rm HS}^2=\sum_p\|B_p\|_F^2.
\]

This is the same literal finite formula as TPC-321; only the output-space
map changes.

## 2. Sign-labelled diagonal projector

Put (m=|\mathcal S_Q|) and (e=(e_p)_p\in\{-1,+1\}^m).  Define

\[
 E_e v=m^{-1/2}(e_pv)_p,
 \qquad P_e=E_eE_e^*.
\]

Since (E_e^*E_e=I_N), (P_e) is an orthogonal projection onto a coherent
diagonal copy of (mathbb R^N).  Define the aligned signed reassembly

\[
 C_e=\sum_{p\in\mathcal S_Q}e_pB_p.
\]

Direct substitution gives

\[
 P_eA_\oplus v=E_e(m^{-1/2}C_ev),
 \qquad
 \|P_eA_\oplus\|_{\rm HS}^2=m^{-1}\|C_e\|_F^2.
\]

The unnormalised reassembly ratio and coherent projected fraction are

\[
 \rho_e=\frac{\|C_e\|_F^2}{D},\qquad
 \phi_e=\frac{\|P_eA_\oplus\|_{\rm HS}^2}{D}=\frac{\rho_e}{m}.
\]

## 3. Cross-block Gram reduction

Let (H_{pq}=\langle B_p,B_q\rangle_F).  Then (H) is PSD as the Gram
matrix of the matrices (B_p), (D=\operatorname{tr}H>0), and

\[
 \rho_e=\frac{e^{\mathsf T}He}{\operatorname{tr}H}.
\]

This is the finite signed cross-block interface.  It retains the cross terms

\[
 e^{\mathsf T}He=D+2\sum_{p<q}e_pe_qH_{pq},
\]

which the direct-sum Gram (A_\oplus^*A_\oplus) discards.

## 4. Declared finite panel

The panel is (X\in\{640,1280,2560\}), (Q\in\{24,36,54,80\}), and
(s\in\{1,2\}), giving 24 rows.  The named laws are all-plus,
index-alternating, the mod-4 quadratic residue sign, and a half split in
prime order.  Exhaustive search fixes (e_1=+1), because (ho_e=ho_{-e}).

The producer uses forward and reverse prime order.  All stored ratios receive
an outward guard (10^{-12}).  The independent checker uses reverse order and
`einsum` accumulation.
