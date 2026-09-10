# A Finite-Resonance Sieve Obstruction on Prime Shells

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology
- Source date: August 24, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

Let $\mathcal P_Q$ be the primes in $(Q,2Q)$ and let $E_{3,7}(Q)$ count primitive pairs $p<r$ in $\mathcal P_Q$ satisfying $7p+3r=16Q$. We compute the complete local root law for an exact two-linear-form parameterization and apply the Selberg upper-bound sieve to prove $$E_{3,7}(Q)\ll \frac{Q\log\log(3Q)}{(\log Q)^2},
 \qquad \frac{E_{3,7}(Q)}{|\mathcal P_Q|}\longrightarrow0.$$ The same conclusion holds for every fixed finite family of primitive nondegenerate linear resonances. Combined with an earlier sharp matched-mass ceiling, this proves that the literal aligned first-resonance mechanism cannot provide any fixed positive proportional energy saving at all sufficiently large scales, even under perfect edge anti-alignment. This is a scoped arithmetic obstruction, not a prime-pair lower bound or a cancellation theorem for the underlying physical source.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

The motivating prime-shell collision is $$7p+3r=16Q,\qquad Q<p<r<2Q,                         \label{eq:resonance}$$ with the primitive condition $(Q,21)=1$. Earlier exact work shows that these collisions form a matching and that a proportional energy saving cannot exceed the diagonal mass carried by its incident vertices. In the literal aligned row model, strict saving by $\delta$ therefore requires $$\frac{E_{3,7}(Q)}{|\mathcal P_Q|}\ge \frac{\delta}{8}.     \label{eq:toll}$$ For the program endpoint $\delta=1/400$, the toll is $1/3200$.

The purpose of this paper is to decide whether the left side of [\[eq:toll\]](sections/1_introduction.tex#L12){reference-type="eqref" reference="eq:toll"} can remain bounded below. The answer is no. The relevant arithmetic is an ordinary dimension-two upper-bound sieve, but its application requires keeping the moving determinant $16Q$ and its exceptional local factors. We use the classical Selberg sieve in the forms developed in `\cite{HalberstamRichert1974,IwaniecKowalski2004}`; the Goldbach and twin-prime derivations in `\cite{GreenAdditive,Rudnick2015}` provide close two-form templates.

Our second result isolates the real scope of the obstruction: any *fixed finite* set of nondegenerate linear resonance equations has zero edge density in the prime shell. A family whose depth grows with $Q$, or an arithmetic concentration of actual source mass on a sparse support, is not ruled out.

# Exact local arithmetic

Assume $(Q,21)=1$ and write $Q=3t+a$, where $a\in\{1,2\}$. Reducing [\[eq:resonance\]](sections/1_introduction.tex#L5){reference-type="eqref" reference="eq:resonance"} modulo three gives $p\equiv a\pmod 3$. Thus every solution has the unique parameterization $$L_1(k)=3k+a,\qquad L_2(k)=16t+3a-7k.               \label{eq:forms}$$ Its determinant is $$3(16t+3a)+7a=16Q.                                  \label{eq:determinant}$$ The shell inequalities imply $10Q/7<L_1(k)<8Q/5<L_2(k)<2Q$, so the parameter interval has length $2Q/35+O(1)$.

For a prime $\ell$, let $\nu_Q(\ell)$ be the number of residues $k\pmod\ell$ for which $L_1(k)L_2(k)\equiv0\pmod\ell$.

> **Lemma: local root law**<span id="lem:roots" label="lem:roots">\[lem:roots\]</span> For $(Q,21)=1$, $$\nu_Q(\ell)=
>  \begin{cases}
>  1,&\ell\in\{2,3,7\}\text{ or }\ell\mid Q,\\
>  2,&\text{otherwise}.
>  \end{cases}$$ In particular, the pair of forms is admissible.

> **Proof** Modulo two, both forms in [\[eq:forms\]](sections/2_local_arithmetic.tex#L7){reference-type="eqref" reference="eq:forms"} equal $k+a$. Modulo three, $L_1=a$ is nonzero and $L_2$ has one root. Modulo seven, $L_2$ is constant and nonzero: three times that constant is $2Q\pmod7$; meanwhile $L_1$ has one root. Outside $\{2,3,7\}$, both forms have one root, and the two roots coincide exactly when the determinant [\[eq:determinant\]](sections/2_local_arithmetic.tex#L11){reference-type="eqref" reference="eq:determinant"} vanishes modulo $\ell$.

Consequently the singular series has the exact shape $$\mathfrak S_{3,7}(Q)=C_{3,7}
 \prod_{\substack{\ell\mid Q\\ \ell\ge5}}
 \frac{\ell-1}{\ell-2},                              \label{eq:series}$$ where $C_{3,7}>0$ contains the fixed factors and the convergent generic Euler product.

# The sieve density theorem

> **Theorem**<span id="thm:3716" label="thm:3716">\[thm:3716\]</span> Uniformly for $Q\ge8$, $$E_{3,7}(Q)\ll \mathfrak S_{3,7}(Q)\frac{Q}{(\log Q)^2}
>  \ll \frac{Q\log\log(3Q)}{(\log Q)^2}.$$ Consequently $E_{3,7}(Q)/|\mathcal P_Q|\to0$.

> **Proof** If $(Q,21)>1$, the primitive edge set is empty. Otherwise, for squarefree $d$ the Chinese remainder theorem and interval counting give $$\#\{k\in I_Q:d\mid L_1(k)L_2(k)\}
>  =\frac{|I_Q|\nu_Q(d)}d+O(\nu_Q(d)).                 \tag{7}$$ Apply the standard Selberg upper-bound sieve of dimension two to (7), choosing a fixed small power of $Q$ as sieve level. The remainder is the standard $O(2^{\omega(d)})$ interval remainder, and Lemma [\[lem:roots\]](sections/2_local_arithmetic.tex#L20){reference-type="ref" reference="lem:roots"} gives [\[eq:series\]](sections/2_local_arithmetic.tex#L44){reference-type="eqref" reference="eq:series"}. This proves the first estimate.
>
> For each variable exceptional prime, $$\frac{\ell-1}{\ell-2}
>  =\frac{\ell}{\ell-1}
>   \left(1+\frac{1}{\ell(\ell-2)}\right).$$ The product of the second factors converges absolutely, while the first product is at most $Q/\varphi(Q)\ll\log\log(3Q)$. This proves the second estimate. Finally, the prime number theorem gives $|\mathcal P_Q|=\pi(2Q)-\pi(Q)\sim Q/\log Q$.

The theorem is one-sided. It neither predicts how often a resonance occurs nor supplies signed cancellation; it only proves that its maximum possible shell density tends to zero.

# Finite families and the matched-mass consequence

The determinant argument is not special to coefficients $3$ and $7$.

> **Theorem: fixed finite resonance families**<span id="thm:family" label="thm:family">\[thm:family\]</span> Fix a finite set $\mathcal R$ of triples $(a,b,c)$ with $a,b>0$, $(a,b)=1$, and $c\ne0$. The total number of prime-shell solutions to $$ap+br=cQ,\qquad p,r\in\mathcal P_Q,$$ over $(a,b,c)\in\mathcal R$ is $$O_{\mathcal R}\!\left(\frac{Q\log\log(3Q)}{(\log Q)^2}\right)
>  =o(|\mathcal P_Q|).$$ Hence the union of all incident prime rows has density $o(1)$.

> **Proof** For one triple, either there is no integral solution or all solutions have the form $p=p_0+bk$, $r=r_0-ak$. The determinant of these forms is $br_0+ap_0=cQ$. Away from the fixed primes dividing the coefficients, the two local roots coalesce only at primes dividing $cQ$. The proof of Theorem [\[thm:3716\]](sections/3_selberg_bound.tex#L3){reference-type="ref" reference="thm:3716"} therefore applies with a triple-dependent constant. A local inadmissibility yields no large prime pair. Sum the bounds over the fixed set $\mathcal R$; at most twice as many vertices as edges are incident.

For completeness, the support statement has a deterministic energy transfer. Suppose the collision energy is $$E_G=D+2\Re\sum_{\{p,r\}\in E(G_Q)}c_{p,r}\langle u_p,u_r\rangle,$$ where $|c_{p,r}|\le C$, the graph degree is at most $\Delta$, and positive row masses have ratio at most $\kappa$. If $M_{\rm inc}$ is the mass on incident rows, then Cauchy–Schwarz gives $$\frac{(D-E_G)_+}{D}
 \le C\Delta\frac{M_{\rm inc}}D
 \le 2C\Delta\kappa\frac{|E(G_Q)|}{|\mathcal P_Q|}.          \label{eq:graphtransfer}$$ Indeed, $2|\langle u_p,u_r\rangle|\le\|u_p\|^2+\|u_r\|^2$, and every incident mass is charged at most $\Delta$ times. Each fixed linear equation has degree at most two, so Theorem [\[thm:family\]](sections/4_finite_families.tex#L5){reference-type="ref" reference="thm:family"} makes [\[eq:graphtransfer\]](sections/4_finite_families.tex#L40){reference-type="eqref" reference="eq:graphtransfer"} tend to zero for a fixed finite family.

Let $D(Q)$ denote total literal aligned row mass and $M(Q)$ the mass on the first $3$–$7$ matching. The previous sharp mass theorem gives $$\frac{M(Q)}{D(Q)}\le 8\frac{E_{3,7}(Q)}{|\mathcal P_Q|}.$$

> **Corollary: fixed-saving obstruction** In the literal aligned first-resonance model, $M(Q)/D(Q)\to0$. Even if every edge is perfectly anti-aligned, the mechanism cannot produce any fixed positive proportional saving at all sufficiently large scales. In particular, strict $1/400$ is impossible on this scoped branch.

Theorem [\[thm:family\]](sections/4_finite_families.tex#L5){reference-type="ref" reference="thm:family"} also shows why merely adding a fixed number of similar resonance channels cannot repair the density deficit under comparable row masses. It does not address a number of channels growing with $Q$.

# Finite certification and adversarial controls

The executable certificate checks the determinant and local root law directly at multiple scales and primes. At $Q=25$, the determinant is $400$, the exceptional prime $5$ has one root rather than two, the singular correction is exactly $4/3$, and the unique edge is $(37,47)$.

A separate implementation scans every $8\le Q\le32768$. It reproduces 568,308 edges among 52,199,509 prime rows. Table [1](sections/5_certificate.tex#L28){reference-type="ref" reference="tab:scan"} records exact window statistics. They are diagnostics, not evidence for the asymptotic theorem.

<div id="tab:scan">

|      $Q$ window|    edges|        rows|  aggregate $E/P$|
|---------------:|--------:|-----------:|----------------:|
|        $8$–$31$|        3|         115|          $3/115$|
|      $32$–$127$|       32|       1,472|           $1/46$|
|     $128$–$511$|      338|      19,171|      $338/19171$|
|    $512$–$2047$|    3,681|     255,321|      $409/28369$|
|   $2048$–$8191$|   42,938|   3,482,706|  $21469/1741353$|
|  $8192$–$32768$|  521,316|  48,440,724|  $43443/4036727$|

: Exact finite reproduction scan.

</div>

The independent checker uses parameter-index enumeration rather than the producer’s prime-list enumeration. Adversarial tests perturb the determinant by one, replace an exceptional one-root prime by a generic two-root prime, and corrupt the Euler factor; all three mutations are detected. Normal and optimized Python modes are required to produce identical output.

# Conclusion and firewall

The first primitive resonance now has a complete progression from exact collision geometry to an asymptotic arithmetic obstruction: its graph is a matching, its saving capacity is at most its matched mass, and a Selberg sieve proves that this mass support has density zero in the literal aligned comparable-row model. The same support obstruction holds for every fixed finite family of linear resonances.

This result is deliberately scoped. It proves no twin-prime lower bound, no signed arithmetic cancellation, no identification of literal aligned rows with actual V59 source masses, and no statement about resonance depth growing with $Q$. Thus the first-resonance and fixed-finite-family branches are closed, while full Gate B and its strict $1/400$ endpoint remain open globally.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{HalberstamRichert1974,
  author    = {Halberstam, Heini and Richert, Hans-Egon},
  title     = {Sieve Methods},
  publisher = {Academic Press},
  year      = {1974}
}

@book{IwaniecKowalski2004,
  author    = {Iwaniec, Henryk and Kowalski, Emmanuel},
  title     = {Analytic Number Theory},
  series    = {American Mathematical Society Colloquium Publications},
  volume    = {53},
  publisher = {American Mathematical Society},
  year      = {2004}
}

@misc{GreenAdditive,
  author       = {Green, Ben},
  title        = {Additive Combinatorics},
  howpublished = {Course notes, Section 2.3},
  url          = {https://people.maths.ox.ac.uk/greenbj/papers/additive-combinatorics.pdf},
  note         = {Accessed 2026-08-24}
}

@misc{Rudnick2015,
  author       = {Rudnick, Zeev},
  title        = {Selberg's Sieve---Twin Primes},
  howpublished = {Course notes},
  year         = {2015},
  url          = {https://www.math.tau.ac.il/~rudnick/courses/sieves2015/selberg%20sieve%20twin%20primes.pdf}
}
```

<!-- SOURCE_BODY_END -->
