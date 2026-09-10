# A Matched-Resonance Mass Ceiling for Global AP Saving

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

> Source-format notice: the originals contain CR separators. Only reader line endings are normalized; suspected TeX typos are not repaired. See the [separator ledger](../CONVERSION_RECORD.md#original-crcrlf-separator-ledger) and bounded source audit before interpreting affected formulas.

## Abstract

The primitive $3$–$7$ resonance graph is a matching, so collision can alter only the diagonal mass carried by matched vertices. We formalize this as a sharp global ceiling. If $D$ is total diagonal mass and $M$ is matched mass, then $E_{\rm AP}\ge D-M$ and the possible saving is at most $M$; perfect anti-alignment on every edge attains equality. Thus a fixed $\delta$-saving requires $M/D\ge\delta$. Under row-mass comparability with ratio $\kappa$, this becomes the necessary edge-density toll $E/P\ge\delta/(2\kappa)$. Literal aligned dilation-four rows satisfy $\kappa\le4$, so the strict $1/400$ target requires $E/P\ge1/3200$. Exact finite certificates validate the ceiling and row-weight ledger. Asymptotic resonance density and physical source comparability remain open.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

TPC-229 proves that the first primitive $3$–$7$ resonance graph is a matching and diagonalizes every edge into symmetric and antisymmetric modes `\cite{tpc229}`. This removes graph-degree losses, but it also shows that unmatched rows are spectrally isolated. Even ideal cancellation on every existing edge cannot change their energy.

The present paper quantifies this limitation. The maximum possible saving equals at most the fraction of diagonal mass on matched vertices. The statement is deterministic, sharp, and independent of the signs on the edges. It converts a desired global saving into a necessary resonance-density condition whenever row masses are comparable.

For the literal aligned rows of the finite dilation-four model `\cite{tpc226}`, elementary primitive-multiplier counting gives a uniform comparability constant four. The strict $1/400$ endpoint therefore has an explicit, previously hidden toll: at least one resonance edge per 3200 prime rows in the normalized sense $E/P$.

# The sharp matched-mass ceiling

Let $G$ be a matching on a finite set of Hilbert vectors $u_q$. Write $$D=\sum_q\|u_q\|^2,
 \qquad M=\sum_{q\ {
m matched}}\|u_q\|^2,
 \qquad U=D-M.$$

> **Theorem: Matched-mass ceiling** <span id="thm:ceiling" label="thm:ceiling">\[thm:ceiling\]</span> The corresponding AP energy satisfies $$E_{\rm AP}\ge D-M,
>  \qquad D-E_{\rm AP}\le M.
>  \label{eq:ceiling}$$ Both inequalities are sharp. In particular, $$E_{\rm AP}\le(1-\delta)D\quad\Longrightarrow\quad \frac MD\ge\delta.
>  \label{eq:necessary-mass}$$

> **Proof** Matching gives the orthogonal decomposition $$E_{\rm AP}=\sum_{q\ {
> m unmatched}}\|u_q\|^2
>  +\sum_{(p,r)\in E(G)}\|u_p+u_r\|^2.$$ The first sum is $D-M$ and the second is nonnegative, proving [\[eq:ceiling\]](sections/2_mass_ceiling.tex#L16){reference-type="eqref" reference="eq:ceiling"}. Choosing $u_r=-u_p$ on every edge makes the second sum vanish, so the bound is sharp. Combining the first inequality with the hypothesis in [\[eq:necessary-mass\]](sections/2_mass_ceiling.tex#L21){reference-type="eqref" reference="eq:necessary-mass"} proves the implication.

The theorem is a ceiling even under perfect arithmetic signs. No local estimate can compensate for insufficient matched mass.

# From matched mass to edge density

Suppose every row mass lies in $[d_{\min},d_{\max}]$ and put $\kappa=d_{\max}/d_{\min}$. If $P$ is the number of rows and $E$ the number of matching edges, then $$M\le2E d_{\max},\qquad D\ge P d_{\min}.$$ Therefore $$\frac MD\le2\kappa\frac EP.
 \label{eq:density-bound}$$

> **Corollary: Necessary density toll** Under the preceding comparability hypothesis, a $\delta$-saving requires $$\frac EP\ge\frac{\delta}{2\kappa}.
>  \label{eq:density-toll}$$

For equal row mass, $M/D=2E/P$ exactly. The loss in [\[eq:density-bound\]](sections/3_density_toll.tex#L12){reference-type="eqref" reference="eq:density-bound"} records only possible concentration within the declared comparability class.

# Literal aligned row weights

At dilation four, $\lfloor4q/Q\rfloor\in\{4,5,6,7\}$. A primitive row contains some of the signed odd multipliers $$\pm1,\ \pm3,\ \pm5,\ \pm7.$$ The pair $\pm1$ always survives, while at most all eight values survive. With aligned equal-amplitude atoms, row mass is proportional to the surviving atom count. Hence $$2\le d_q\le8,\qquad \kappa\le4.
 \label{eq:kappa}$$

Substituting $\delta=1/400$ and [\[eq:kappa\]](sections/4_literal_rows.tex#L12){reference-type="eqref" reference="eq:kappa"} into [\[eq:density-toll\]](sections/3_density_toll.tex#L19){reference-type="eqref" reference="eq:density-toll"} yields $$\frac EP\ge\frac1{3200}.
 \label{eq:endpoint-toll}$$ This is necessary, not sufficient: the matched blocks must additionally occupy the correct antisymmetric modes.

The comparison is scoped to literal aligned finite-model rows. Actual V59 source amplitudes may have a different and presently unproved mass distribution.

# Exact certification

A five-row fixture with two anti-aligned edges and one unmatched row has $D=45$, $M=20$, and $E_{\rm AP}=25=D-M$, attaining the ceiling. A second fixture checks a nonextremal block. The literal census over $8\le Q\le4096$ verifies row atom counts between two and eight and the comparability bound at every scale.

At $Q=25$, six prime rows contain one edge. Uniform mass gives $M/D=1/3$; literal aligned atom mass gives $10/26=5/13$. Across the finite scan, 2268 scales contain at least one edge and 1821 contain none. These counts are regression facts only; they do not establish an asymptotic edge density.

The independent checker rederives the sharp fixture and the $1/3200$ toll in normal and optimized modes. Seven semantic mutations are rejected.

# Conclusion

The first-resonance mechanism now has a sharp global capacity bound. Perfect signed cancellation can remove no more than the mass already placed on matched vertices. For comparable literal rows, a fixed endpoint saving therefore demands a positive edge density. The next natural question is arithmetic: apply a two-linear-form upper-bound sieve to the exact equation $7p+3r=16Q$ and determine whether this density toll can persist asymptotically.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc226,author={Liang Wang},title={First Primitive-Collision Transition in Dilated Shared Clocks},year={2026},note={TPC-226 repository proof record}}
@misc{tpc229,author={Liang Wang},title={Matching and Sharp Block Spectrum of the Primitive 3--7 Resonance Graph},year={2026},note={TPC-229 repository proof record}}
```

<!-- SOURCE_BODY_END -->
