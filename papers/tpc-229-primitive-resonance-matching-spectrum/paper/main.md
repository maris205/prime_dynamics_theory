# Matching and Sharp Block Spectrum of the\ Primitive 3–7 Resonance Graph

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

We prove that the primitive $3$–$7$ resonance graph arising at the first nontrivial shared-clock dilation is a matching at every scale. The resonance equation separates all low endpoints from all high endpoints and makes each counterpart unique. Hence the global collision operator is an orthogonal direct sum of two-coordinate swap blocks. Each block has spectrum $(-1,-1,+1,+1)$ and admits an exact symmetric/antisymmetric energy decomposition. The AP-to-diagonal ratio ranges sharply from zero to two, and a $\delta$-saving is equivalent to a precise antisymmetric-dominance inequality. The source-native bilinear block also satisfies a sharp half-mass bound. An exact replay of 4089 scales verifies maximum degree one throughout. The theorem removes graph complexity but supplies neither arithmetic antisymmetric dominance nor matched-mass density, so no Route-B level 2 claim is made.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

The first primitive shared-clock collisions are classified by $$7p+3r=16Q,\qquad p<r,
 \label{eq:resonance}$$ with two sign-symmetric shared coordinates `\cite{tpc226}`. A source-native polarization compiler subsequently identified the contribution of such a collision as a bilinear $\beta$–$w$ block `\cite{tpc228}`. The remaining finite geometry could in principle form a complicated graph, creating global spectral or combinatorial losses.

We show that this concern disappears completely. Equation [\[eq:resonance\]](sections/1_introduction.tex#L6){reference-type="eqref" reference="eq:resonance"} separates its two endpoint types at $8Q/5$, and each endpoint determines its unique partner. The resonance graph is therefore a matching for every $Q$. Its spectrum and all symmetric-source energy questions reduce to independent two-prime blocks.

This yields a sharp local saving criterion. It also exposes the next obstruction: geometry does not tell us how much physical source mass lies on matched vertices, nor whether that mass favors antisymmetric modes. Those are arithmetic questions rather than graph-theoretic ones.

# The resonance graph is a matching

Let $G_Q$ have as vertices the primes in $(Q,2Q)$, with an edge $p<r$ when [\[eq:resonance\]](sections/1_introduction.tex#L6){reference-type="eqref" reference="eq:resonance"} holds and the primitive multiplier conditions from TPC-226 are satisfied.

> **Theorem: Endpoint separation and matching** <span id="thm:matching" label="thm:matching">\[thm:matching\]</span> Every edge of $G_Q$ satisfies $$\frac{10Q}{7}<p<\frac{8Q}{5}<r<2Q.
>  \label{eq:ranges}$$ Moreover, every vertex has degree at most one.

> **Proof** The shell inequality $r<2Q$ and [\[eq:resonance\]](sections/1_introduction.tex#L6){reference-type="eqref" reference="eq:resonance"} imply $7p=16Q-3r>10Q$. Since $p<r$, we also have $10p<7p+3r=16Q<7r+3r$, which gives $p<8Q/5<r$. This proves [\[eq:ranges\]](sections/2_matching.tex#L12){reference-type="eqref" reference="eq:ranges"}.
>
> The low and high endpoint intervals in [\[eq:ranges\]](sections/2_matching.tex#L12){reference-type="eqref" reference="eq:ranges"} are disjoint. A low endpoint $p$ determines $r=(16Q-7p)/3$, and a high endpoint $r$ determines $p=(16Q-3r)/7$. Thus no vertex belongs to two edges.

> **Corollary** Collision coordinates from different resonance edges have disjoint prime-row support. Consequently every collision quadratic or bilinear form is a direct sum over edges.

# Sharp two-coordinate spectrum

Order the two shared coordinates on one edge and write its two row vectors as $u,v\in\mathbb R^2$. The collision adjacency on their direct sum is $$J=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix}.
 \label{eq:swap}$$ Its symmetric and antisymmetric subspaces have eigenvalues $+1$ and $-1$, each twice.

Put $s=(u+v)/\sqrt2$ and $d=(u-v)/\sqrt2$. Then $$\begin{aligned}
 E_{\rm diag}&=\|s\|^2+\|d\|^2,\\
 E_{\rm collision}&=2\langle u,v\rangle=\|s\|^2-\|d\|^2,\\
 E_{\rm AP}&=\|u+v\|^2=2\|s\|^2.
 \label{eq:energies}\end{aligned}$$ It follows immediately that $$0\le \frac{E_{\rm AP}}{E_{\rm diag}}\le2,
 \label{eq:ratio}$$ with equality at $v=-u$ and $v=u$ respectively.

> **Theorem: Exact saving criterion** For $0\le\delta<1$, $$E_{\rm AP}\le(1-\delta)E_{\rm diag}
>  \quad\Longleftrightarrow\quad
>  (1+\delta)\|s\|^2\le(1-\delta)\|d\|^2.
>  \label{eq:criterion}$$ The same equivalence holds globally after summing symmetric and antisymmetric energies over the matching blocks.

> **Proof** Substitute [\[eq:energies\]](sections/3_spectrum.tex#L16){reference-type="eqref" reference="eq:energies"} and rearrange. Orthogonality between matching blocks permits summation without cross terms.

# Sharp source-bilinear block bound

TPC-228 gives on one edge $$B_e=\langle\beta_p,w_r\rangle+\langle\beta_r,w_p\rangle.$$ By the elementary Hilbert inequality $2|\langle x,y\rangle|\le
\|x\|^2+\|y\|^2$, $$|B_e|\le\frac12\left(
 \|\beta_p\|^2+\|\beta_r\|^2+\|w_p\|^2+\|w_r\|^2
 \right).
 \label{eq:bilinear-bound}$$ The constant is sharp: choose $w_r=\beta_p$ and $w_p=\beta_r$.

Matching means that summing [\[eq:bilinear-bound\]](sections/4_source_block.tex#L13){reference-type="eqref" reference="eq:bilinear-bound"} introduces no graph-degree loss. This is stronger than a general Schur envelope, but it remains an absolute bound. A negative arithmetic contribution requires signed information about the exchanged source pairs.

# Exact certification

The all-scale proof above is symbolic. The certificate independently replays the literal prime-shell equation for every $8\le Q\le4096$. Across 4089 scales it finds 2268 edge-bearing scales and 13,754 edges. The largest count is 18, first at $Q=3440$; the maximum vertex degree is one throughout.

Four exact-rational spectral fixtures attain AP ratios $2,0,1,$ and $2/3$, covering aligned, anti-aligned, orthogonal and partially negative blocks. A source-bilinear fixture attains equality in [\[eq:bilinear-bound\]](sections/4_source_block.tex#L13){reference-type="eqref" reference="eq:bilinear-bound"}. A separate checker rederives the spectrum and fixture ratios, with byte-identical normal and optimized output. Seven semantic mutations are rejected.

The scan is a regression for the implementation, not the reason the matching theorem is true. It contains no estimate for resonance density or source amplitudes.

# Conclusion

The primitive $3$–$7$ collision geometry has no large connected components: it is a matching at every scale. The collision operator is therefore exactly solvable, and a fixed AP saving is equivalent to antisymmetric-mode dominance in independent edge blocks. This removes a combinatorial obstruction but reveals a quantitative one. The next step must determine how much total source mass can occupy matched resonance vertices; without that mass, even perfect cancellation on every edge cannot yield a fixed proportional global saving.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc226,author={Liang Wang},title={First Primitive-Collision Transition in Dilated Shared Clocks},year={2026},note={TPC-226 repository proof record}}
@misc{tpc228,author={Liang Wang},title={A Source-Native Polarized Collision Compiler},year={2026},note={TPC-228 repository proof record}}
```

<!-- SOURCE_BODY_END -->
