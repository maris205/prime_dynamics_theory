# A Source–Location Holdout for Signed Prime–Shell Spectral Profiles

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- Source date: 1 September 2026
- Source repository commit: `88c46824c79e9c202a698cf4db36fcaf98260537`
- Converter: `source-markdown-audit-v2`

## Abstract

We test whether the finite trace-normalized spectral-profile majorization pattern found in TPC-323 is tied to its source location. Keeping the deleted diagonal, height, prime-shell anchors, kernel exponents, and four sign laws fixed, we move the source coordinates to two pre-registered panels disjoint from the parent panel. The all-plus coherent profile majorizes the direct profile on all 48 holdout rows, with 24 out of 24 rows on each panel. The three alternative laws reproduce the parent census, with majorizing/mixed counts 34/14, 42/6, and 36/12 in aggregate. We prove the elementary conditional translation-covariance identity and verify that the selected offsets are not covered by it. The result is a finite, independently replayed source-location replication; it supplies no source-native arithmetic $L^2$ estimate, asymptotic power saving, or twin prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The preceding signed-projector audit separated coherent energy from spectral shape. On its training panel, the all-plus law had a strict trace-normalized profile-majorization label on every row, even though its unnormalized energy crossed the direct energy. A natural next question is whether this profile signal survives a change of source location. Such a test is useful because the literal blocks contain both difference kernels and absolute residue masks.

This paper makes one controlled intervention. The source cardinalities and all other parameters are unchanged; only the integer intervals are moved. The conclusion is deliberately finite. In particular, “replication” below means a frozen recomputation with an independent implementation, not an independence theorem for prime events.

# Literal block family

For a finite interval $I\subset\mathbb Z$, $p\in\mathcal P_Q$ and $s\in\{1,2\}$, we use the same block as the parent audit: $$B_{p,I}^{(s)}(u,t)=p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 1_{u\ne t}1_{p\nmid u}1_{p\nmid t}
 \left(1_{u\equiv t\pmod p}-\frac{1}{p-1}\right),
 \label{eq:block}$$ where $H=66$ and $$\mathcal P_Q=\{p: Q<p\leq 2Q,\ p\text{ prime}\},\qquad
 Q\in\{24,36,54,80\}.$$ The direct and coherent Gram matrices are $$G_0=\sum_{p\in\mathcal P_Q}B_p^*B_p,
 \qquad
 C_e=\sum_{p\in\mathcal P_Q}e_pB_p,
 \qquad G_e=C_e^*C_e,
 \label{eq:grams}$$ where $e_p\in\{+1,-1\}$. We compare the energy ratio $$\rho_e=\frac{\operatorname{tr}(G_e)}{\operatorname{tr}(G_0)}$$ with the normalized, descending spectral profile $$\pi(G)=\frac{(\lambda_1(G),\ldots,\lambda_n(G))}{\operatorname{tr}(G)}.$$ The label $G_e\succcurlyeq_\pi G_0$ means that every interior prefix of $\pi(G_e)-\pi(G_0)$ is nonnegative and at least one is positive; this is the usual finite majorization convention `\cite{marshall2011,bhatia1997}`.

# An exact covariance control

The source shift can sometimes be invisible to the literal block. We state the precise condition so that it is not confused with the numerical result.

> **Proposition: conditional translation covariance** Let $d$ be divisible by every prime in $\mathcal P_Q$, and let $T_d:\ell^2(I)\to\ell^2(I+d)$ relabel coordinates by $(T_df)(u+d)=f(u)$. Then $$B_{p,I+d}^{(s)}=T_dB_{p,I}^{(s)}T_d^{-1},\quad
>  G_0(I+d)=T_dG_0(I)T_d^{-1},\quad
>  G_e(I+d)=T_dG_e(I)T_d^{-1}.$$ Consequently $\rho_e$ and $\pi(G)$ are unchanged.

> **Proof** Under $u\mapsto u+d$ and $t\mapsto t+d$, the difference $u-t$ and the deleted-diagonal indicator are unchanged. Divisibility of $d$ by $p$ gives $u+d\equiv u$ and $t+d\equiv t\pmod p$, so both residue indicators and both deleted divisibility masks are unchanged. Equation [\[eq:block\]](main.tex#L65){reference-type="eqref" reference="eq:block"} thus conjugates entry by entry. The Gram identities follow by summation, and unitary conjugation preserves eigenvalues and trace.

The holdout shifts are not common multiples of the complete active shells; the stress suite also exhibits changed residue masks. Thus Proposition 1 is an exact reusable control, not a reason to identify the two panels with the parent calculation.

# Frozen holdout protocol

TPC-323 used $[321,640]$, $[641,1280]$, and $[1281,2560]$. Before running the holdout computation we fixed the two source panels in Table [1](main.tex#L134){reference-type="ref" reference="tab:panels"}. The first is the natural continuation; the second inserts gaps. Their cardinalities are respectively $320$, $640$, and $1280$, and no source integer overlaps the parent union or the other holdout panel.

<div id="tab:panels">

| Panel        |    $n=320$    |    $n=640$    |    $n=1280$   |
|:-------------|:-------------:|:-------------:|:-------------:|
| continuation | $[2561,2880]$ | $[2881,3520]$ | $[3521,4800]$ |
| gap-offset   | $[5001,5320]$ | $[6001,6640]$ | $[8001,9280]$ |

: Frozen source-location panels.

</div>

For each of the $2\times3\times4\times2=48$ rows we retain forward matrix accumulation, reverse $\texttt{einsum}$ accumulation, and SciPy/NumPy profile paths. Scalar intervals expand path extrema by $10^{-12}$ and the majorization tolerance is $10^{-10}$. An independently written checker rebuilds the literal blocks in reverse order. It validates metrics and outward intervals rather than requiring last-bit equality of long floating profile digests across LAPACK builds.

# Results

Table [2](main.tex#L163){reference-type="ref" reference="tab:census"} gives the profile census. Each pair is “majorizing/mixed”; no reverse-only or unresolved row occurred. The per-panel counts are identical, so the aggregate is not produced by one exceptional source interval.

<div id="tab:census">

| Panel        | Rows | all-plus | alternating | mod-4 | half-split |
|:-------------|:----:|:--------:|:-----------:|:-----:|:----------:|
| continuation |  24  |   24/0   |     17/7    |  21/3 |    18/6    |
| gap-offset   |  24  |   24/0   |     17/7    |  21/3 |    18/6    |
| aggregate    |  48  |   48/0   |    34/14    |  42/6 |    36/12   |

: Finite profile census on the two holdouts.

</div>

The strict all-plus prefix lower endpoint over all rows is $$1.647473532339078\times 10^{-5}>0.$$ The all-plus energy ratio is below one on 6 rows and above one on 42 rows. Thus the holdout strengthens the amplitude–shape distinction: profile majorization is stable across the two source locations while the energy coordinate still crosses the direct baseline. The finite alternative-law census also matches the 24-row parent proportions exactly.

As an exact small anchor, the fresh interval $[4001,4016]$ with $Q=4$ and $s=1$ has positive direct and alternating signed rational energies. Their full SHA-256 digests are stored in the machine-readable certificate and are recomputed by the independent checker (prefixes `97225bdb` and `b475bf82`, respectively).

# Interpretation and firewall

The strongest positive statement is a two-panel, 48-row source-location replication of the all-plus normalized profile label, backed by an exact conditional covariance lemma and independent replay. The strongest obstruction is equally important: replication of a finite profile pattern does not provide a source-native arithmetic representation of the signs. The four laws are geometric probes, not Möbius or von Mangoldt weights.

Accordingly, the status of this paper is $$\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_SOURCE\_LOCATION\_HOLDOUT\_REPLICATION}.$$ It earns no fixed-power credit. A uniform scale theorem, canonical arithmetic sign law, source-native signed $L^2$ estimate, strict $1/400$ payment, and the twin-prime endpoint remain open. The Session-named `propose.md` and official Route-A/Route-B evaluator files are absent from this checkout; the included local Bridge-B checker is fail-closed.

# Conclusion and next route

The all-plus profile signal is not confined to the parent source interval: it survives both a natural continuation and a separated residue-sensitive holdout. The next economical test is a new scale ladder, followed by an attempt to express the signed profile in a source-native arithmetic $L^2$ interface. Until such a theorem exists, the result should be read as a map-level structural island rather than progress toward a twin-prime proof.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{marshall2011,
  author    = {Marshall, Albert W. and Olkin, Ingram and Arnold, Barry C.},
  title     = {Inequalities: Theory of Majorization and Its Applications},
  edition   = {2},
  publisher = {Springer},
  year      = {2011}
}

@book{bhatia1997,
  author    = {Bhatia, Rajendra},
  title     = {Matrix Analysis},
  publisher = {Springer},
  year      = {1997}
}
```

<!-- SOURCE_BODY_END -->
