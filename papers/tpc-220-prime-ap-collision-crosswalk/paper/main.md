# Prime-AP Collision Crosswalk for the Literal Prime Shell

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: August 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding longitudinal/transverse ledger identifies the missing quantity in a sub-$P$ prime-shell estimate, but it does not yet express that quantity in arithmetic coordinates. This paper performs that crosswalk for the literal TPC rows. Multiplying the row congruence by the prime label converts reassembly into weighted prime sums in arithmetic progressions. Expanding two rows gives an exact multiplicative collision Gram with congruence $m q'=m' q\pmod h$. The diagonal reduces to the usual fixed-$q$ atom energy under the inherited cutoff injectivity, whereas every off-diagonal contribution is retained as a collision edge. Exact rational certificates verify constant and affine profiles. No estimate for primes in progressions and no arithmetic $L^2$ advance is claimed.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1 / EXACT_PRIME_AP_MULTIPLICATIVE_CROSSWALK`.

# From the transverse ledger to arithmetic coordinates

TPC-219 proved that the scalar shell energy satisfies $$E_{\mathrm{shell}}=P(E_{\mathrm{diag}}-E_{\perp}),$$ so a genuine improvement requires a lower bound on q-transverse energy. A lower bound cannot be formulated honestly until the residual is written using the original rows. This paper makes that translation without changing the source object.

Fix an active denominator $h$, a prime $q\in\mathcal Q_x$ with $(q,h)=1$, and write $$L_{h,q}=\left\lfloor\frac{hq}{H}\right\rfloor,
 \qquad
 \mathcal M_{h,q}^{*}=\{m\in\mathbb Z:0<|m|\leq L_{h,q},\ (m,h)=1\}.$$ For a packet profile $\psi_j$, put $$w_{h,m,q}^{(j)}=\psi_j\!\left(\frac{Hm}{hq}\right).$$ On a primitive residue $a\pmod h$, the literal row is $$B_{h,q}^{(j)}(a)=
 \sum_{m\in\mathcal M_{h,q}^{*}}w_{h,m,q}^{(j)}
 \mathbf 1_{m q^{-1}\equiv a\ (h)}. \tag{1}$$ The restriction to $\mathcal M_{h,q}^{*}$ is harmless for primitive $a$: a nonunit $m$ cannot occupy a primitive residue. It makes the collision formula transparent.

# Exact weighted prime-AP crosswalk

> **Theorem: Prime-AP crosswalk** For complex weights $(\lambda_q)_{q\in\mathcal Q_x}$ and primitive $a\pmod h$, define $$\Pi_{h,m}^{(j)}(r;\lambda)=
>  \sum_{\substack{q\in\mathcal Q_x, q\equiv r\ (h)\\ |m|\leq L_{h,q}}}
>  \lambda_q w_{h,m,q}^{(j)}.$$ Then $$\sum_{q\in\mathcal Q_x}\lambda_q B_{h,q}^{(j)}(a)
>  =\sum_{m\neq0}\Pi_{h,m}^{(j)}(a^{-1}m;\lambda). \tag{2}$$ The $m$ sum may be restricted to $0<|m|\leq\lfloor 2hQ/H\rfloor$.

> **Proof** Because $a$ and $q$ are units modulo $h$, $$m q^{-1}\equiv a\pmod h
>  \Longleftrightarrow m\equiv aq\pmod h
>  \Longleftrightarrow q\equiv a^{-1}m\pmod h.$$ Insert this equivalence into (1), multiply by $\lambda_q$, and interchange the finite sums over $q$ and $m$. The cutoff is exactly the one displayed in the definition of $\Pi$, so no boundary term is introduced. Since $q\leq2Q$, the stated global $m$ range contains every term. This proves (2).

Equation (2) is not an average-prime approximation. It is a weighted AP incidence operator whose q-dependent profile and cutoff remain visible.

# The multiplicative collision Gram

Define the primitive row Gram for two packet coordinates by $$\Gamma_h^{(j,\ell)}(q,q')=
 \sum_{\substack{a\pmod h\\(a,h)=1}}
 B_{h,q}^{(j)}(a)\overline{B_{h,q'}^{(\ell)}(a)}.$$ We refer to this matrix as the *Gamma* matrix below.

> **Theorem: Collision formula** The Gram entry equals $$\begin{aligned}
>  \Gamma_h^{(j,\ell)}(q,q')
>   ={}&\sum_{m\in\mathcal M_{h,q}^{*}}
>        \sum_{m'\in\mathcal M_{h,q'}^{*}}
>        w_{h,m,q}^{(j)}\overline{w_{h,m',q'}^{(\ell)}}\\
>      &\hspace{25mm}\times
>        \mathbf 1_{m q'\equiv m'q\ (h)}. \tag{3}\end{aligned}$$ If $2L_{h,q}<h$, then $$\Gamma_h^{(j,j)}(q,q)=
>  \sum_{m\in\mathcal M_{h,q}^{*}}|w_{h,m,q}^{(j)}|^2. \tag{4}$$

> **Proof** Expand both rows. A common primitive residue exists exactly when both atoms are units modulo $h$ and $$m q^{-1}\equiv m'(q')^{-1}\pmod h.$$ Multiplication by $qq'$ gives the congruence in (3), and the common primitive residue is then unique. For $q=q'$, the congruence is $m\equiv m'\pmod h$. Since  $|m-m'|\leq2L_{h,q}<h$, it forces $m=m'$, which gives (4).

The diagonal is therefore the fixed-q row energy already controlled by the structural large-sieve lift. The off-diagonal is not a formal error: it is the explicit graph of solutions to $m q'\equiv m'q\pmod h$.

# Finite collision audit

The release certificate uses $H=500$, $h\in\{17,19,23\}$, and $q\in\{101,103,107,109\}$. It checks (2), (3), and (4) exactly for a constant profile and a rational affine profile. All residuals are zero, while off-diagonal collision entries are nonempty. This separates an identity check from an arithmetic estimate: the existence of collision edges is certified, but their growing-scale aggregate is not bounded here.

| object             | finite scope                                 | status   |
|:-------------------|:---------------------------------------------|:---------|
| AP crosswalk       | 3 moduli, 4 primes, 2 profiles               | exact    |
| Gram crosswalk     | 6 profile/modulus records                    | exact    |
| diagonal reduction | $2L_{h,q}<h$                                 | exact    |
| off-diagonal graph | at least one edge in every tested row family | observed |

: TPC-220 certificate scope and claim boundary.

# Route position

Route A is not applicable. Route-B structural threshold A passes because (2)–(4) act on the literal rows and retain the physical labels. The claim ceiling is `PROVED_STRUCTURAL_L1`; $$\texttt{ARITHMETIC\_ADVANCE}=\texttt{NO},\qquad
 \texttt{L2}=\texttt{NONE},\qquad
 \texttt{FULL\_GATE\_B}=\texttt{OPEN}.$$ The next theorem must quantify the off-diagonal collision graph beyond an absolute Schur bound. That is a separate question from proving the crosswalk itself.

# Conclusion

TPC-220 identifies the exact arithmetic carrier of the TPC-219 transverse term: weighted prime sums in progressions and a multiplicative collision Gram. The diagonal is paid by the inherited cutoff lemma; every possible saving must control the off-diagonal graph. The paper advances the route by fixing the object of the next estimate, while making no arithmetic or twin-prime claim.

# References

1 TPC-218 repository proof record, “Prime-shell Hilbert lift and the sharp collapse barrier,” 2026. This is an internal source lock, not an external theorem citation.

<!-- SOURCE_BODY_END -->
