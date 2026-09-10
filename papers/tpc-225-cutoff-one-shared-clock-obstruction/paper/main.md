# Cutoff-One Shared-Clock Obstruction\ Exact Prime-Row Orthogonality in a Literal Two-Channel Audit

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan, China
- Source date: August 22, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-224 showed that the prime-AP and polarized channels can be written on one common literal Hilbert family, but left open whether both marginals can save energy on one source clock. This paper audits the named finite clock $x=Q^3$, $H=4Q^2$, $h=4Q$, with primes $Q<q\leq 2Q$. Its literal cutoff is exactly one. We prove that the two residue coordinates of distinct prime rows are disjoint, for arbitrary packet profile values. Consequently $E_{\rm AP}=E_{\rm diag}$ and $E_{\rm all}=E_{\rm pol}$ exactly. Thus this clock cannot pay any positive prime-label AP saving; any cancellation is entirely packet-direction and profile-dependent. Nine exact-rational affine scales, aligned and balanced fixtures, and a complete $Q=3,\ldots,99$ boundary replay confirm the identities. The result is a structural, scoped obstruction, not an asymptotic arithmetic $L^2$ theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim ceiling

The previous compatibility audit `\cite{tpc224}` established that a common family $W_{q,j}$ supports three energies $$E_{\rm diag}=\sum_{q,j}\|W_{q,j}\|^2,\qquad
 E_{\rm AP}=\sum_j\left\|\sum_qW_{q,j}\right\|^2,
 \qquad
 E_{\rm pol}=\sum_q\left\|\sum_jW_{q,j}\right\|^2,
 \label{eq:energies}$$ and that $E_{\rm all}\leq PJ(E_{\rm AP}+E_{\rm pol})/(P+J)$. The next research question is narrower: does the source clock used for the finite audit actually create prime-label overlap on which an AP dispersion estimate could operate?

We answer this question exactly for the declared clock. Our claim is not that every possible V46 clock has the same geometry. The clock is a finite modeling choice inherited from the preceding audit, and no identification with the physical fixed atom is made. The principal result is therefore classified as `PROVED_STRUCTURAL_L1` with a scoped obstruction.

# The literal cutoff-one object

Let $Q\geq 3$ be an integer and let $\mathcal Q_Q=\{q: q\text{ prime},\ Q<q\leq 2Q\}$. Set $$x=Q^3,\qquad H=4Q^2,\qquad h=4Q,
 \qquad C_h=\frac1h.
 \label{eq:clock}$$ For a packet profile $\psi_j$, define the literal residue vector $$W_{q,j}(a)=C_h\sum_{0<|m|\leq\lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod h}.
 \label{eq:row}$$ The inverse exists because an active prime is odd and larger than every prime factor of $Q$. The vector space is the Euclidean space indexed by residues modulo $h$. All four energies in [\[eq:energies\]](main.tex#L47){reference-type="eqref" reference="eq:energies"}, and $E_{\rm all}=\|\sum_{q,j}W_{q,j}\|^2$, use exactly this vector and this normalization.

The clock has a decisive feature: $$\left\lfloor\frac{hq}{H}\right\rfloor
 =\left\lfloor\frac qQ\right\rfloor=1.
 \label{eq:cutoff}$$ The endpoint $q=2Q$ is not prime for $Q\geq3$, so no exceptional endpoint is hidden in [\[eq:cutoff\]](main.tex#L86){reference-type="eqref" reference="eq:cutoff"}. Writing $r_q=q^{-1}\pmod{4Q}$, every row has the form $$W_{q,j}=u_{q,j}e_{r_q}+v_{q,j}e_{-r_q},\qquad
 u_{q,j}=C_h\psi_j(Q/q),\quad v_{q,j}=C_h\psi_j(-Q/q).
 \label{eq:twopoint}$$

> **Lemma: disjoint inverse-residue supports** For distinct $q_1,q_2\in\mathcal Q_Q$, $\{r_{q_1},-r_{q_1}\}\cap\{r_{q_2},-r_{q_2}\}=\varnothing$.

> **Proof** An intersection would give $q_1^{-1}\equiv\varepsilon q_2^{-1}\pmod{4Q}$ for $\varepsilon\in\{1,-1\}$. Multiplication by the units $q_1q_2$ gives $q_2\equiv\varepsilon q_1\pmod{4Q}$. For $\varepsilon=1$, the absolute difference is smaller than $Q<4Q$, hence the primes are equal. For $\varepsilon=-1$, divisibility by $4Q$ and $2Q<q_1+q_2\leq4Q$ force $q_1+q_2=4Q$. The upper bounds then force both primes to equal $2Q$, which is not prime. Both alternatives are contradictions.

# Exact marginal identities

> **Theorem: cutoff-one shared-clock obstruction** For every finite collection of real packet profiles on the clock [\[eq:clock\]](main.tex#L67){reference-type="eqref" reference="eq:clock"}, the energies satisfy $$E_{\rm AP}=E_{\rm diag},\qquad E_{\rm all}=E_{\rm pol}.
>  \label{eq:main}$$ In particular, if $E_{\rm diag}>0$, then no $\delta>0$ can satisfy $E_{\rm AP}\leq(1-\delta)E_{\rm diag}$ uniformly on this clock.

> **Proof** The lemma makes the rows from distinct prime labels orthogonal, including their supports across all packet labels. For fixed $j$, Pythagoras gives $$\left\|\sum_{q\in\mathcal Q_Q}W_{q,j}\right\|^2
>  =\sum_{q\in\mathcal Q_Q}\|W_{q,j}\|^2.$$ Summing this equality over $j$ proves the first identity. For the second, let $Y_q=\sum_jW_{q,j}$. Each $Y_q$ is supported on the two-point set of its prime label, so the $Y_q$ are pairwise orthogonal. Therefore $$\left\|\sum_qY_q\right\|^2=\sum_q\|Y_q\|^2,$$ which is exactly $E_{\rm all}=E_{\rm pol}$. The final statement follows from the first identity when the diagonal energy is nonzero.

The theorem is stronger than a numerical observation: no choice of finite profile values can create prime-label cancellation before a nontrivial cutoff or a different, source-identified transform is introduced. It also separates the two channel roles. The AP marginal is rigidly diagonal, while the polarized marginal may vary from complete packet cancellation to maximal packet alignment.

# Affine profiles and exact closed forms

For the affine profiles used in TPC-224, write $\psi_j(t)=1+s_jt$, $t_q=Q/q$, and set $S_1=\sum_js_j$, $S_2=\sum_js_j^2$. Directly from [\[eq:twopoint\]](main.tex#L94){reference-type="eqref" reference="eq:twopoint"}, $$\begin{aligned}
 E_{\rm diag}=E_{\rm AP}
  &=2C_h^2\sum_{q\in\mathcal Q_Q}(J+S_2t_q^2),
 \label{eq:affined}\\
 E_{\rm pol}=E_{\rm all}
  &=2C_h^2\sum_{q\in\mathcal Q_Q}(J^2+S_1^2t_q^2).
 \label{eq:affinep}\end{aligned}$$ For $J=4$ and $s=(0,1,-1,2)/10$, $S_1=1/5$, $S_2=3/50$, so the summands are $$C_h^2\left(8+\frac{3}{25}t_q^2\right),\qquad
 C_h^2\left(32+\frac{2}{25}t_q^2\right).
 \label{eq:special}$$ The second summand is near four times the first on the source shell. This is packet alignment, not an AP saving.

<div id="tab:affine">

|  $Q$|  $\#\mathcal Q_Q$|  $E_{\rm AP}/E_{\rm diag}$|  $E_{\rm all}/E_{\rm pol}$|  $E_{\rm pol}/E_{\rm diag}$|
|----:|-----------------:|--------------------------:|--------------------------:|---------------------------:|
|   11|                 3|                          1|                          1|                    3.975681|
|   17|                 4|                          1|                          1|                    3.975294|
|   29|                 6|                          1|                          1|                    3.974163|
|   43|                 9|                          1|                          1|                    3.976754|
|   61|                12|                          1|                          1|                    3.975547|
|   89|                16|                          1|                          1|                    3.975183|
|  127|                23|                          1|                          1|                    3.975056|
|  181|                30|                          1|                          1|                    3.975418|
|  257|                42|                          1|                          1|                    3.975244|

: Exact-rational affine source-clock replay. The two identity columns are exactly one at every scale; the final column is shown to six decimals only for readability and is not used as evidence.

</div>

# Adversarial profile controls

The exact obstruction does not depend on the affine choice. For an aligned profile, all four plus and minus values are one. Each prime row then has $E_{\rm pol}/E_{\rm diag}=4$, and $E_{\rm all}=E_{\rm pol}$. For a balanced profile, choose plus values $(1,-1,0,0)$ and minus values $(0,0,1,-1)$. The packet sums vanish at every prime, so $$E_{\rm pol}=E_{\rm all}=0,\qquad E_{\rm AP}=E_{\rm diag}>0.
 \label{eq:balanced}$$ These fixtures bracket the packet direction while leaving the AP identity unchanged. A complete boundary replay for $3\leq Q\leq99$ found no support collision and verified [\[eq:main\]](main.tex#L120){reference-type="eqref" reference="eq:main"} with exact integers and rationals.

# Block decomposition and certification protocol

The support lemma has a useful operator interpretation. Let $${\cal R}_q=\operatorname{span}\{e_{r_q},e_{-r_q}\}
 \quad\text{and}\quad
 {\cal H}_Q=\mathbb R^{4Q}.$$ For the named clock, the active part of the Hilbert space is the orthogonal direct sum $$\bigoplus_{q\in{\cal Q}_Q}{\cal R}_q\ \subseteq\ {\cal H}_Q .
\label{eq:block}$$ Thus the source object is not merely a collection of rows with small support: it is a block-diagonal embedding of the prime label into residue space. Any linear operation that sums over $q$ while retaining the literal coordinates acts independently on these blocks. The AP marginal therefore has no cross-block terms to estimate, and the full sum has no cross-block terms after packet aggregation either. This is the reusable structure extracted from the obstruction.

The finite replay was designed to distinguish an identity from a floating point coincidence. The producer constructs all coefficients as rational numbers, forms the four energies by exact inner products, and serializes a canonical JSON certificate. The independent checker has its own prime enumerator and row constructor; it does not import the producer. It checks the cutoff, the residue support, all energy identities, and the profile fixtures before comparing the certificate. Running the independent checker with and without Python optimization produced byte-identical output.

<div id="tab:audits">

| Audit layer         | Input scales                                                                                                                                                                                                                                 | Checked statement                                                                                                |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| Affine source clock |                                                                                                                                                                                                                                              |                                                                                                                  |
| 127,181,257         | $E_{\rm AP}=E_{\rm diag}$, $E_{\rm all}=E_{\rm pol}$, and the closed forms in [\[eq:affined\]](main.tex#L158){reference-type="eqref" reference="eq:affined"}–[\[eq:affinep\]](main.tex#L161){reference-type="eqref" reference="eq:affinep"}. |                                                                                                                  |
| Boundary profiles   | $Q=3,5,7,13,31,47,73$                                                                                                                                                                                                                        | Aligned and balanced packet directions retain the two exact identities; the balanced diagonal energy is nonzero. |
| Boundary geometry   | Every integer $3\leq Q\leq99$                                                                                                                                                                                                                | The cutoff is one and all active prime supports are pairwise disjoint.                                           |

: Exact replay layers and their claim ceilings.

</div>

The replay has a deliberately narrow interpretation. It certifies the literal finite object and its exact theorem; it does not estimate how often primes occur in a longer interval, and it does not replace a source-lock argument for a physical V46 transform. In particular, changing $H/h$ so that a second $m$-layer enters changes the collision graph and invalidates the block decomposition [\[eq:block\]](main.tex#L225){reference-type="eqref" reference="eq:block"} as a proof shortcut. That is why the next candidate is a nontrivial-cutoff audit rather than an immediate claim of arithmetic dispersion.

# Route consequence

The shared-clock question from TPC-224 therefore splits into two logically different tasks. On the cutoff-one clock, the AP task is stopped: the literal prime rows are already orthogonal, so a prime-label dispersion saving cannot come from summing these rows. The polarized task remains profile-dependent, and the exact V46 transfer is still open. A productive AP route must either use a source-locked clock with $\lfloor hq/H\rfloor\geq2$, where distinct prime rows can have genuine multiplicative collisions, or prove a different physical synthesis map that creates legitimate overlap. Neither option is asserted here.

    TPC225_CUTOFF_ONE = PROVED_EXACT
    TPC225_SUPPORT_DISJOINTNESS = PROVED_EXACT
    TPC225_AP_EQUALS_DIAGONAL = PROVED_EXACT
    TPC225_ALL_EQUALS_POLARIZED = PROVED_EXACT
    E_AP = E_diag
    E_all = E_pol
    TPC225_AP_SAVING_ON_NAMED_CLOCK = REFUTED_SCOPED
    TPC225_ARITHMETIC_ADVANCE = NO
    TPC225_L2 = NONE
    TPC225_FULL_GATE_B = OPEN

# Conclusion

TPC-225 supplies a concrete obstruction immediately downstream of the common Hilbert interface. In the named cutoff-one source clock, the AP marginal is exactly the diagonal energy and the full energy is exactly the polarized marginal. Thus the next bridge cannot be crossed by simply declaring a shared clock; it must expose nontrivial cutoff support or a separately proved source-identified overlap mechanism. The result is structural L1 only: there is no arithmetic $L^2$ advance, fixed-atom credit, strict $1/400$ payment, or twin-prime conclusion.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc224,
  author       = {Liang Wang},
  title        = {Literal Two-Channel Compatibility Audit},
  year         = {2026},
  note         = {TPC-224 internal source record, prime dynamics theory session}
}

@misc{tpc220,
  author       = {Liang Wang},
  title        = {Prime-AP Collision Crosswalk for the Literal Shell},
  year         = {2026},
  note         = {TPC-220 internal source record, prime dynamics theory session}
}
```

<!-- SOURCE_BODY_END -->
