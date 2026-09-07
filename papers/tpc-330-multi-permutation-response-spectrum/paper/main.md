# A Multi-Permutation Response Spectrum for the\ Twin-Prime Signed-Gram Diagnostic

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`
- Converter: `source-markdown-audit-v2`

## Abstract

A preceding finite audit found that a single source-coordinate permutation could reverse the sign readout of a signed Gram diagnostic while preserving the source multiset and its Euclidean norm. We test whether that effect is tied to one chosen permutation. Holding the literal deleted-diagonal prime-shell operator and the finite V59 source model fixed, we evaluate five predeclared bijections on two held-out origins, two scales, four shell anchors, two kernel exponents, and four sign laws. This gives 640 guarded law/control observations. Each of three odd-affine controls is positive for the all-plus off-diagonal readout on all 32 rows, whereas identity and reversal retain the actual $31$ negative/$1$ positive classification census. The all-plus five-control spectrum is mixed on 31 rows and unanimously positive on one. The exact finite Gram decomposition and norm invariance are proved; the numerical spectrum is independently replayed and stress-tested. The result is a finite position-sensitivity obstruction and a rejection of both source-norm-only and single-affine-accident explanations on this panel. It does not provide a growing arithmetic estimate, fixed-power credit, a Route-B gate payment, or a twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Question and contribution

The twin-prime route studied here uses a literal centered prime-shell operator acting on a source vector. A sign observed in one coordinate arrangement can be caused by the interaction between the source coordinates and the physical matrix rather than by the source norm or its coordinate multiset. The previous audit used one affine placement null. The present paper asks the smallest follow-up question: *does the response persist across a predeclared affine family, and how does it compare with identity and reversal?*

The contribution is a finite response spectrum. We keep the source, origins, scales, shells, kernel, and sign laws unchanged, and replace one control by the following five-map menu: $$\pi_0(i)=i,\quad
 \pi_{3,11}(i)=(3i+11)\bmod M,\quad
 \pi_{5,17}(i)=(5i+17)\bmod M,$$ $$\pi_{7,29}(i)=(7i+29)\bmod M,\qquad
 \pi_{\rm rev}(i)=M-1-i,\qquad M=N/2.$$ The maps are frozen before reading the certificate. Three affine maps replicate the earlier sign reversal; reversal does not. This is a position-aware finite obstruction, not an asymptotic claim.

# The finite object

For an origin $o$ and even scale $N$, let $$I_{o,N}=\{o,o+1,\ldots,o+N/2-1\}.$$ We use $$o\in\{28001,36001\},\quad N\in\{4096,8192\},\quad
 H=66,\quad Q\in\{24,36,54,80\},\quad s\in\{1,2\}.$$ For a prime $p\in(Q,2Q]$, define the literal block $$\label{eq:block}
 B_{p,Q,s}(u,t)=
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac{1}{p-1}\right).$$ For a fixed sign law $e=(e_p)$ on the shell, put $$C_e=\sum_{p\in(Q,2Q]}e_pB_{p,Q,s}.$$ The four laws are all-plus, alternating index, the sign of $p$ modulo $4$, and a half split in increasing prime order.

For a finite vector $v=(v_t)_{t\in I_{o,N}}$, define $$\begin{aligned}
 E_e(v)&=\|C_ev\|_2^2,\\
 D_e(v)&=\sum_t v_t^2\|C_ee_t\|_2^2,\\
 O_e(v)&=E_e(v)-D_e(v),\qquad
 R_e(v)=\frac{E_e(v)}{D_e(v)}.\end{aligned}$$ All recorded rows have $E_e(v)>0$ and $D_e(v)>0$. Thus $R_e<1$ and $R_e>1$ are exactly negative and positive off-diagonal Gram mass.

# Source model and control orbit

The finite source model inherited from V59 is $$\Lambda(m)=
 \begin{cases}
  \log p,&m=p^k,\\
  0,&\text{otherwise},
 \end{cases}$$ and $$\label{eq:source}
 b^{(2)}(t)=2C_2\,\mathbf 1_{2\nmid t}
 \prod_{\substack{p\mid t\\p>2}}\frac{p-1}{p-2},\qquad
 \beta_o^{(2)}(t)=\Lambda(t+2)-b^{(2)}(t).$$ The Euler product is cut off at $50000$ with the inherited positive tail enclosure. Logarithms use 100-digit Decimal midpoint intervals and a rational $10^{-70}$ guard; matrix readouts use float64 and an outward ratio guard $5\cdot10^{-8}$.

Let $P_j$ be the permutation matrix associated with one of the five maps. Because $M$ is either $2048$ or $4096$, the multipliers $1,3,5,7$ are units modulo $M$. Hence $$P_j^{T}P_j=I,\qquad
 \|P_jv\|_2=\|v\|_2,\qquad
 \operatorname{multiset}(P_jv)=\operatorname{multiset}(v).$$ This is an exact finite statement. It does not imply that the physical operator commutes with $P_j$: $$E_e(P_jv)=v^TP_j^TC_e^TC_eP_jv.$$ The five-control response vector $$\left(R_e(P_0v),R_e(P_{3,11}v),R_e(P_{5,17}v),
       R_e(P_{7,29}v),R_e(P_{\rm rev}v)\right)$$ is therefore a deterministic diagnostic of coordinate placement, not a probability distribution over permutations.

# Exact identities and certificate protocol

#### Finite Gram identity.

Since $C_ev=\sum_t v_tC_ee_t$, finite bilinearity gives $$E_e(v)=\sum_{t,t'}v_tv_{t'}
       \langle C_ee_t,C_ee_{t'}\rangle.$$ The diagonal terms are $D_e(v)$ and the remaining terms are $$O_e(v)=\sum_{t\ne t'}v_tv_{t'}
       \langle C_ee_t,C_ee_{t'}\rangle.$$ Consequently $E_e(v)=D_e(v)+O_e(v)$ exactly for every finite vector. No limit or arithmetic estimate is used; this is the usual finite Gram expansion `\cite{horn2013matrix}`.

#### Five-map invariance.

The modular-unit argument proves the five bijections and their norm and multiset preservation. It does not prove $P_j^TC_e^TC_eP_j=C_e^TC_e$. Any response difference is therefore compatible with exact norm invariance and reflects the interaction with the literal coordinate-dependent block.

The producer writes canonical JSON for all 32 rows. Each row contains geometry, shell, source enclosure, the four actual metrics, and four metrics for each of the five controls. The independent checker reconstructs the source with separate factorization code, accumulates shell blocks in reverse order, and recomputes every metric, classification, response signature, control census, and pairwise summary without importing the producer. A separate stress checker tests mutations, exact rational Gram algebra, provenance locks, and fail-closed claim labels.

# Finite response spectrum

Table [1](main.tex#L190){reference-type="ref" reference="tab:census"} reports negative/positive counts. There are no unresolved rows.

<div id="tab:census">

| control         |  all-plus|  alternating|  mod-$4$|  half split|
|:----------------|---------:|------------:|--------:|-----------:|
| identity        |      31/1|         25/7|     32/0|        32/0|
| affine $(3,11)$ |      0/32|        20/12|     27/5|        31/1|
| affine $(5,17)$ |      0/32|         30/2|     32/0|        28/4|
| affine $(7,29)$ |      0/32|        21/11|     32/0|        29/3|
| reversal        |      31/1|         25/7|     32/0|        32/0|

: Five-control classification census over 32 rows.

</div>

The three affine controls are positive for all-plus in $32/32$ rows. Relative to identity, each changes $31/32$ all-plus classifications. Their all-plus ratio ranges are $$\begin{array}{c|c}
\text{control} & \text{ratio range}\\ \hline
(3,11)&[1.1086266653921864,\;5.8662166822283597]\\
(5,17)&[1.0796604870824567,\;3.7402812188967256]\\
(7,29)&[1.0729497333260283,\;2.7548351258227446].
\end{array}$$ The all-plus five-control signatures are $$\underbrace{(-,+,+,+,-)}_{31\ {\rm rows}},\qquad
 \underbrace{(+,+,+,+,+)}_{1\ {\rm row}}.$$ For the other laws, the numbers of unanimous-negative, unanimous-positive, and mixed rows are respectively $$\begin{array}{c|rrr}
 & \text{unanimous negative}&\text{unanimous positive}&\text{mixed}\\ \hline
\text{alternating}&17&0&15\\
\text{mod-4}&27&0&5\\
\text{half split}&25&0&7.
\end{array}$$ The certificate records 640 law/control observations and all ten pairwise control summaries. Identity and reversal have equal classifications in all 32 rows for all-plus (and, in fact, for all four laws), but their ratios are not identical: the largest all-plus ratio difference is $0.022723042898999735$. We therefore do not state an exact reflection symmetry.

## Inherited scale audit

The same certificate retains the two-scale comparison at fixed origin, shell, and exponent. It contains 64 law-level pairs from $4096$ to $8192$. For all-plus, 15 of 16 pairs preserve the classification and one crosses. The energy growth factor and base-2 slope lie in $$1.9663131482417533\leq E_{8192}/E_{4096}
 \leq2.14326466572482,$$ $$0.97549309860589706\leq
 \log_2(E_{8192}/E_{4096})
 \leq1.0998100153677246.$$ The analogous sign-persistence counts for alternating, mod-$4$, and half split are $15/16$, $16/16$, and $16/16$. These are finite observations and not estimates uniform in the source or in scale.

## Component controls

The positive von-Mangoldt component and the positive comparison component remain positive under the all-plus readout on all 32 rows. Their minimum ratios are, respectively, $$\min R_+(\Lambda(\cdot+2))=1.3668932693626414,\qquad
 \min R_+(b^{(2)})=3.0441001012913311.$$ This rules out a zero-energy component in this finite computation, but does not establish cancellation for the difference in [\[eq:source\]](main.tex#L118){reference-type="eqref" reference="eq:source"}.

# Exact anchor

At $I=[36001,36016]$, $Q=4$, and $s=1$, the shell is $\{5,7\}$. With the rational vector $$v_t=\mathbf 1_{t+2\ {\rm prime}}-\mathbf 1_{t\ {\rm odd}},$$ the exact Fraction calculation gives $$E=306.7544239093389,\qquad
 D=332.4445614235858,\qquad
 O=-25.69013751424689,$$ and verifies $E=D+O$ before decimal display. SHA-256 digests of the reduced numerator/denominator forms for all three values are stored in the certificate and replayed independently. This anchor is a finite arithmetic sanity check only.

# Interpretation and claim boundary

The strongest finite positive result is a three-control affine consensus: the earlier $(5,17)$ response is reproduced by $(3,11)$ and $(7,29)$ on the entire all-plus panel. The strongest obstruction is that identical source multisets and norms produce different physical readouts: identity/reversal remain $31/1$, while every nontrivial affine control is $0/32$.

The following labels are the release ceiling:

-   `PROVED_EXACT_FINITE`: matrix formula, Gram split, five bijections, norm/multiset invariance, and exact anchor identity;

-   `NUMERICALLY_CERTIFIED_FINITE`: 32 rows, 640 response observations, 10 pairwise summaries, and 64 scale pairs;

-   `REFUTED_SCOPED`: source-norm-only sign determination and uniqueness of the $(5,17)$ affine response on this panel;

-   `OPEN`: position-aware structural bound, growing source-native $L^2$, canonical sign law, strict $1/400$ payment, full Gate B, and the twin-prime endpoint.

Thus $$\texttt{ARITHMETIC\_ADVANCE=NO},\quad
 \texttt{FIXED\_POWER\_CREDIT=0},\quad
 \texttt{FULL\_GATE\_B=OPEN},\quad
 \texttt{TWIN\_PRIME\_RESULT=NONE}.$$ The Session-named Route-A and Route-B evaluator files are absent from this checkout. The local Bridge-B checker is a fail-closed fallback and is not an official evaluator pass.

# Reproducibility

The auditable package contains the source producer, canonical certificate, independent checker, stress checker, derivation and proof packages, and route ledger. Reproduction commands and the exact parent locks are listed in the project README. The machine-readable result is `results/tpc330_certificate.json`; the compiled manuscript is `paper/paper.pdf`.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{horn2013matrix,
  author    = {Roger A. Horn and Charles R. Johnson},
  title     = {Matrix Analysis},
  edition   = {2},
  publisher = {Cambridge University Press},
  year      = {2013}
}
```

<!-- SOURCE_BODY_END -->
