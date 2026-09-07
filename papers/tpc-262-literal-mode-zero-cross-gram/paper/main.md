# A Literal Signed Reduced-Residue Operator and Phase-Character Firewall

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-261 identified a strict fixed-power gap of $1/400$ between the current V59 baseline and target, while TPC-260 identified a four-packet reassembly datum. We now freeze the literal reduced-residue signed operator at each additive phase. With the actual residue synthesis $S_{q,v}$, unit mask $P_q$, and outer prime weight retained, the operator is $J_{q,v}=S_{q,v}^{*}C_qS_{q,v}-(q-2)(q-1)^{-1}P_q$. We prove its exact quadratic remainder identity and the associated four-phase polarization. We also prove that aggregate packet mode zero and the nontrivial polarization characters are distinct. An exact finite operator-image certificate on $\{5,7,11,13\}$ gives identical diagonals with mode-zero energies $16\left\lVert Y\right\rVert^2$ and zero. This is a finite structural obstruction, not a growing-shell counterexample or an estimate for the source-frozen packets.

<!-- SOURCE_BODY_BEGIN -->

# Scope and motivation

The Route-B object is a signed coupling on one V59 clock. Earlier releases constructed the literal source operator, a four-block Haar frame, a source-frozen null direction, and an exact endpoint budget `\cite{tpc247,tpc260,tpc261}`. The remaining question is what exact quantity must be controlled before a packet diagonal estimate can be reassembled into the physical scalar?

The unit-class centering matrix is a constant-character fiber, not by itself the additive variable $v=0$ of the complete V59 integral. We retain this distinction throughout. The finite certificate audits $v=0$, while the operator identity is phase-by-phase and the growing integral remains open.

1.  identify the exact unit-class projection and signed remainder operator;

2.  prove the mode-zero/cross-Gram identity and phase-character separation;

3.  translate the signed expression into the strict $1/400$ criterion; and

4.  certify a literal finite operator-image adversary with rational arithmetic and an independent checker.

# The literal reduced-residue fiber

For an odd prime $q$, write $m_q=q-1$ and let ${\bf 1}_q\in{\mathbb R}^{m_q}$ be the all-ones vector. Define $$C_q=I_{m_q}-\frac{1}{m_q}{\bf 1}_q{\bf 1}_q^{\mathsf T}.
\label{eq:C}$$ The rows correspond to the nonzero residue classes; no ordinary residue class is inserted.

> **Lemma: unit-class projection** For every odd prime $q$, $C_q$ is symmetric and idempotent, is positive semidefinite, has rank $q-2$, and has kernel ${\mathbb R}{\bf 1}_q$.

> **Proof** Since ${\bf 1}_q^{\mathsf T}{\bf 1}_q=m_q$, direct multiplication gives $C_q^2=C_q$. For $v\in{\mathbb R}^{m_q}$, $$v^{\mathsf T}C_qv
> =\left\lVert v\right\rVert^2-\frac{|{\bf 1}_q^{\mathsf T}v|^2}{m_q}
> =\frac{1}{m_q}\sum_{r<s}(v_r-v_s)^2\geq0.
> \label{eq:psd}$$ The constant line is the kernel and its orthogonal complement is fixed, so the rank is $m_q-1=q-2$.

For a finite set $\mathcal Q$ of odd primes, a packet source is $a=(a_q)_{q\in\mathcal Q}$, $a_q\in{\mathbb R}^{m_q}$. Its zero-fiber output is $$Y(a)_q=C_qa_q,\qquad
\left\langle Y(a),Y(b)\right\rangle_{\mathcal Q}
:=\sum_{q\in\mathcal Q}q\,\left\langle C_qa_q,C_qb_q\right\rangle.
\label{eq:weighted}$$ The prime weight is inside the inner product, so no unrecorded normalization change is made.

## The signed remainder operator

Let $I$ be a finite interval and $v\in\mathbb R$. For a coefficient vector $a\in\mathbb C^I$, define the physical residue synthesis $$(S_{q,v}a)_r=\sum_{\substack{n\in I\\n\equiv r\pmod q}}
a_n e(vn/H),\qquad r\in\mathbb F_q^\times.
\label{eq:synthesis}$$ Let $P_q$ be the diagonal projection onto $q$-units. The signed reduced-residue remainder is represented exactly by $$J_{q,v}=S_{q,v}^{*}C_qS_{q,v}
-\frac{q-2}{q-1}P_q.
\label{eq:J}$$ The first term is positive semidefinite, but $J_{q,v}$ is a signed Hermitian operator. Direct expansion gives $$V_q^\times(a;v)-D_q^\times(a;v)
=\left\langle a,J_{q,v}a\right\rangle,\quad
V_q^\times(a;v)=\left\lVert C_qS_{q,v}a\right\rVert^2,\quad
D_q^\times(a;v)=\frac{q-2}{q-1}\left\lVert P_qa\right\rVert^2.
\label{eq:remainder}$$ Consequently the common-clock operator $$\mathcal J_x=\int_{\mathbb R}\psi_+(v)
\sum_{q\in\mathcal Q_x}qJ_{q,v}\,dv
\label{eq:Jglobal}$$ satisfies the exact V59 polarization identity $$\mathfrak C_x=\frac14\sum_{j=0}^3\mathrm i^j
\left\langle a^{(j)},\mathcal J_xa^{(j)}\right\rangle,
\qquad a^{(j)}=\beta+\mathrm i^jw.
\label{eq:polarizedJ}$$ This is an exact factorization, not an estimate.

# Mode zero is a signed cross-Gram

Let $Y_0,Y_1,Y_2,Y_3$ be four vectors in [\[eq:weighted\]](main.tex#L87){reference-type="eqref" reference="eq:weighted"}. Put $$\Gamma_{jk}=\left\langle Y_j,Y_k\right\rangle_{\mathcal Q},\qquad
D=\sum_{j=0}^3\Gamma_{jj},\qquad
R=\sum_{0\leq j<k\leq3}\operatorname{Re}\Gamma_{jk}.
\label{eq:gram}$$

> **Theorem: literal cross-Gram mode-zero identity** With $$\widehat Y_k=\frac12\sum_{j=0}^3\mathrm i^{-jk}Y_j,\qquad 0\leq k\leq3,
> \label{eq:dft}$$ one has $$\begin{aligned}
> \left\lVert Y_0+Y_1+Y_2+Y_3\right\rVert_{\mathcal Q}^2&=D+2R,\label{eq:modegram}\\
> \sum_{k=0}^3\left\lVert \widehat Y_k\right\rVert_{\mathcal Q}^2&=D,\label{eq:parseval}\\
> \left\lVert Y_0+Y_1+Y_2+Y_3\right\rVert_{\mathcal Q}^2
> &=4\left\lVert \widehat Y_0\right\rVert_{\mathcal Q}^2.\label{eq:modezero}\end{aligned}$$ Thus diagonal mass alone does not determine mode zero.

> **Proof** Expanding the first left side gives the diagonal terms and each off-diagonal term with its conjugate, hence $D+2R$. Orthogonality of the four roots of unity gives Parseval for [\[eq:dft\]](main.tex#L144){reference-type="eqref" reference="eq:dft"}; setting $k=0$ gives the last identity.

## The phase-character firewall

The packet index has its own Fourier characters. For two vectors $X,Y$ write $$E_j=\left\lVert X+\mathrm i^jY\right\rVert^2,\qquad
F_k=\frac14\sum_{j=0}^3\mathrm i^{kj}E_j.
\label{eq:phase}$$ With the conjugate-linear-first-slot convention, direct expansion yields $$F_0=\left\lVert X\right\rVert^2+\left\lVert Y\right\rVert^2,\qquad
F_1=\left\langle Y,X\right\rangle,\qquad
F_2=0,\qquad
F_3=\left\langle X,Y\right\rangle.
\label{eq:phasechars}$$ Thus aggregate packet mode zero and the nontrivial character selected by the V59 polarized scalar are different observables. A theorem must name the character it estimates; a mode-zero bound cannot be silently substituted for the $F_1$ or $F_3$ coupling.

The identity is compatible with the V59 four-packet construction: whenever the packet outputs are produced by one literal linear map, every $\Gamma_{jk}$ is a sum over the same primes and reduced-residue unit masks. The theorem does not replace the smooth kernel or prove a favorable sign.

> **Corollary: endpoint translation** The current V59 ledger is $$E_0=\frac53=\frac{2000}{1200},\qquad
> E_*=\frac{1997}{1200},\qquad E_0-E_*=\frac1{400}.
> \label{eq:gap}$$ If $D+2R$ has effective fixed-power saving $\sigma$ after all paid losses, the finite-lane endpoint compiler closes when $\sigma>1/400$.

> **Proof** This is the exact exponent substitution into TPC-261’s strict finite-lane compiler; strictness absorbs the arbitrary $x^\varepsilon$ loss.

# A finite literal operator-image adversary

Take the actual finite prime shell $$\mathcal Q=\{5,7,11,13\}.
\label{eq:shell}$$ Let $e$ be the first coordinate in the $q=5$ fiber and zero elsewhere, and let $Y=Y(e)$. Equation [\[eq:psd\]](main.tex#L75){reference-type="eqref" reference="eq:psd"} gives $Y\neq0$, and $$\left\lVert Y\right\rVert_{\mathcal Q}^2
=5\left(\left(\frac34\right)^2+3\left(\frac14\right)^2\right)
=\frac{15}{4}.
\label{eq:probe}$$ Define two families in the same literal operator image: $$Y_j^+=Y,\qquad Y_j^-=(-1)^jY.
\label{eq:adversary}$$ Every packet in both families has diagonal $15/4$, and both have total packet energy $15$, but $$\left\lVert \sum_jY_j^+\right\rVert^2=60,\qquad
\left\lVert \sum_jY_j^-\right\rVert^2=0.
\label{eq:endpoints}$$ The corresponding $R$’s are $45/2$ and $-15/2$. The difference is entirely in the signed cross-Gram, not in the diagonal.

This is a finite structural adversary. Its source probes are freely chosen and are not identified with $\beta+\mathrm i^jw$ on the growing V59 interval. It refutes only the shortcut that literal diagonal and PSD information imply mode-zero saving. It does not refute a future theorem using the arithmetic of the actual source packets.

| Family            | diagonal per packet |   $R$   | mode-zero energy |
|:------------------|:-------------------:|:-------:|:----------------:|
| Aligned           |        $15/4$       |  $45/2$ |       $60$       |
| Alternating       |        $15/4$       | $-15/2$ |        $0$       |
| Mixed $(+,+,-,-)$ |        $15/4$       | $-15/2$ |        $0$       |

: Exact four-packet fiber audit.

# Route status and conclusion

TPC-262 pays one structural interface: the literal signed reduced-residue operator, its deleted diagonal, and its packet-index phase typing are now written exactly on one common finite object. It also identifies the exact failure mode of a diagonal-only argument after actual prime unit matrices are retained. The aggregate mode-zero identity is useful, but it is not silently identified with the nontrivial V59 polarization character.

The next experiment is a census of cross-Gram entries on a growing prime shell, restoring the smooth kernel, deleted diagonal, unit masks, and the source-frozen $\beta,w$ inputs. A positive result must prove negative signed cross-Gram cancellation with effective credit strictly larger than $1/400$. A finite census may instead reveal another obstruction; neither outcome is an asymptotic theorem by itself.

| Item                                                | Status                                     |
|:----------------------------------------------------|:-------------------------------------------|
| Unit-class projection and signed remainder operator | proved exactly                             |
| Mode-zero DFT and cross-Gram ledger                 | proved exactly                             |
| Phase-character separation                          | proved exactly                             |
| Endpoint threshold                                  | proved exactly, conditional on lane bounds |
| Finite operator-image witness                       | numerically certified structural           |
| Growing $\beta,w$ cross-Gram estimate               | open                                       |
| Arithmetic $L^2$, full Gate B, twin primes          | none / open                                |

: Claim firewall.

The named Session Route-A/Route-B evaluator files are absent from this checkout. The proof package, theorem ledger, exact certificate, bridge checker, and `AGENTS.md` are the available fail-closed authority.

# References

9 L. Wang, "Literal V59 source-operator attachment," TPC-247 project artifact, 2026. L. Wang, "Null-compatible four-packet residual reassembly," TPC-260 project artifact, 2026. L. Wang, "A strict endpoint-budget compiler," TPC-261 project artifact, 2026.

<!-- SOURCE_BODY_END -->
