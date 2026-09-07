# Fresh-Holdout Nuisance Orthogonalization\ A Control-Stability Obstruction for Masked Twin-Prime Responses

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `e848dbf1895cb067bad6665654a7c992406bcf65`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-340 supplied a sign-free Schur/Frobenius envelope, but broad-mask alignment remained unexplained. We test a more structural hypothesis on three fresh, non-overlapping source windows. The nine-control twin-prime mean is projected onto the span of the non-twin, prime-power, and zero-support means. This in-sample projection removes 74.3937–79.8911 percent of the twin-mean energy. A hostile leave-one-control-out test reverses the interpretation: training the nuisance span on eight controls and testing the omitted twin response leaves 44.3527–89.0447 percent of its energy in all 27 tests. The finite projection identity is exact, but mean-only nuisance removal is not control-stable on this panel and yields no arithmetic advance.

<!-- SOURCE_BODY_BEGIN -->

# Question and fresh finite panel

The preceding covariance and norm experiments suggest a tempting story: the twin-prime response might be mostly explained by directions shared with the other source classes, leaving a small arithmetic residual. Such a story is only useful if the nuisance directions transfer across controls. We ask: does a projection learned from a control ensemble also remove a twin response at a control that was left out of training?

We retain the parent-locked source construction and the all-plus deleted- diagonal shell operator $$A=\sum_{54<p\leq108}B_{p,54,1},\qquad Q=54,\quad H=66,$$ with kernel exponent one. The four source masks are twin prime ($T$), non-twin prime shift ($B$), prime-power shift ($P$), and zero support ($Z$). The nine controls are the identity, reversal, and the seven affine bijections used in TPC-338–TPC-340.

To obtain a genuinely new finite check, use the three origin/scale pairs $$(48097,1024),\qquad(48609,1024),\qquad(49217,1024).$$ Their source intervals are respectively $[48097,48608]$, $[48609,49120]$, and $[49217,49728]$. They do not overlap the current parent panel ending at 48096, and the shifted arguments remain below the parent finite cutoff 50,000. The prime-power mask is empty in the first two rows and contains $49727=223^2-2$ in the third. We retain this rank variation instead of padding it away.

# Projection and holdout statistic

For class $C$ and control $j$, write $$y_{C,j}=A P_j\beta_C.$$ Let $J$ be the nine-control set and form the nuisance mean matrix $$N_J=\left[\bar y_{B,J}\ \middle|\ \bar y_{P,J}\ \middle|\ \bar y_{Z,J}\right],
 \qquad
 \bar y_{C,J}=\frac1{|J|}\sum_{j\in J}y_{C,j}.$$ If $P_J$ denotes the Euclidean orthogonal projector onto $\operatorname{col}(N_J)$, define the in-sample residual fraction $$\rho_J=\frac{\|(I-P_J)\bar y_{T,J}\|_2^2}
                 {\|\bar y_{T,J}\|_2^2}.
 \label{eq:insample}$$

The hostile test omits one control $j$. For each nuisance class, replace its mean by the mean over $J\setminus\{j\}$, form the corresponding projector $P_{-j}$, and evaluate $$\rho^{\mathrm{LOO}}_j=
 \frac{\|(I-P_{-j})y_{T,j}\|_2^2}{\|y_{T,j}\|_2^2}.
 \label{eq:loo}$$ The omitted output is not used to construct $P_{-j}$. This is a deterministic leave-one-control-out diagnostic, not a claim of random sampling or statistical independence.

#### Finite identity.

For any finite matrix $N$ and vector $y$, the orthogonal projector satisfies $$\|y\|_2^2=\|P_Ny\|_2^2+\|(I-P_N)y\|_2^2.
 \label{eq:pythagorean}$$ Consequently $0\leq\rho_N(y)\leq1$ for nonzero $y$. The identity is the mathematical contribution that makes the residual statistic auditable; it does not say that the selected nuisance span has an arithmetic interpretation.

# Audit protocol

The producer builds four masks and nine controls for each of the three rows, giving $3\times9\times4=108$ raw records, of which 90 have nonzero source norm. It stores response energies and gains, mask counts, singular values and rank, the all-control projection, and all 27 leave-one-control-out records. The numerical rank counts singular values above $\max(\operatorname{shape})\,\epsilon\,\sigma_{\max}$. A reverse-shell independent checker reconstructs the source and operator from the TPC-340 independent engine under parent hash locks. Mutation stress changes row geometry, cutoff flags, both decision guards, rank metadata, and the claim firewall; every mutation must be rejected.

An exact three-dimensional anchor uses target $(1,1,1)$ and nuisance columns $(1,0,0)$ and $(0,1,0)$. Its target, projected, and residual energies are 3, 2, and 1, respectively, verifying [\[eq:pythagorean\]](main.tex#L98){reference-type="eqref" reference="eq:pythagorean"} exactly.

# Results

<div id="tab:results">

| quantity                                            |    finite range   |
|:----------------------------------------------------|:-----------------:|
| in-sample residual retention $\rho_J$               | 0.201089–0.256063 |
| in-sample energy removed                            | 0.743937–0.798911 |
| held-out residual retention $\rho^{\mathrm{LOO}}_j$ | 0.443527–0.890447 |
| held-out energy removed                             | 0.109553–0.556473 |
| nuisance rank                                       |       2 or 3      |
| rank/Pythagorean failures                           |         0         |

: Fresh-panel projection and hostile holdout readout.

</div>

The in-sample result satisfies the predeclared upper guard $\rho_J<0.30$ in all three rows. It might therefore be described informally as a strong nuisance removal. The leave-one-control-out result satisfies the opposing lower guard $\rho^{\mathrm{LOO}}_j>0.40$ in all 27 tests. Thus the small aggregate residual does not transfer to the individual control outputs.

The effective nuisance ranks are 2, 2, and 3. The largest in-sample condition number is 89.5591 and the largest holdout condition number is 92.7609. These values are finite diagnostics: they document the geometry and warn against calling the projection canonical. In particular, the empty prime-power mask in two rows is not evidence that the prime-power class is negligible in a growing model.

# Interpretation and claim firewall

The strongest positive result is methodological: a fresh, fully replayable panel distinguishes an aggregate mean fit from a held-out control test. The strongest obstruction is that the former can look favorable while the latter retains nearly half to nearly all of the omitted response energy. A raw twin-mean residual therefore cannot be promoted to a control-invariant arithmetic component on the basis of this projection.

The orthogonal decomposition is `PROVED_EXACT_FINITE_DECLARED_MODEL`. The raw replay, rank census, and 27 held-out calculations are `NUMERICALLY_CERTIFIED_FINITE`; the retention and conditioning ranges are finite numerical observations. The claim that mean-only nuisance removal is control-stable is `REFUTED_SCOPED`. The official Session Route-A and Route-B evaluator files are absent, so the local Bridge-B wrapper is fail-closed and does not assert an official route pass.

$$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$ There is no twin-prime theorem in this release. The nuisance span is a modeling choice, and the finite cutoff-safe holdout does not imply an asymptotic statement.

# Conclusion and next clue

The current route has now tested generic sign-free envelopes and a more structural projection on a fresh panel. The generic envelope is valid but loose; the mean-only projection is favorable in-sample but fails its hostile control holdout. The next responsible step is independent reproduction or a carefully justified replacement for the nuisance span, with no automatic arithmetic credit. This paper is the endpoint of the present five-paper batch; no new project is opened here.

<!-- SOURCE_BODY_END -->
