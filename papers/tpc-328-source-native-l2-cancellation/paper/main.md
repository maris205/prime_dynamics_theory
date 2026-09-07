# Source-Native Arithmetic $L^2$ Cancellation and the Finite Signed-Gram Obstruction

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 1, 2026
- Source repository commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`
- Converter: `source-markdown-audit-v2`

## Abstract

The finite prime-shell experiments in the preceding releases compared signed and direct operators without attaching the arithmetic source vector itself to the coherent reassembly. We make that attachment explicit. On three disjoint origins and four nested scales, we apply the literal deleted-diagonal centered prime-shell matrix to the finite V59 comparison residual $\beta_o^{(2)}(t)=\Lambda(t+2)-b^{(2)}(t)$. An exact finite Gram expansion separates the output energy into a coordinate-diagonal term $D$ and an off-diagonal term $O$. Across $96$ rows and four predeclared sign laws, the all-plus residual has $O<0$ on $81$ rows and $O>0$ on $15$ rows, with no guard-unresolved row. The two positive component controls are $O>0$ on all $96$ rows. A rational anchor records the same identity on a local prime-indicator-minus-odd vector. Independent reverse-order reconstruction, mutation stress, and normal/optimized replay pass. The contribution is a finite source-native $L^2$ cancellation atlas and a scoped obstruction to a uniform contraction for the four declared laws. It supplies no growing arithmetic estimate, fixed-power credit, Route-B gate payment, or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Question and contribution

The current twin-prime route uses a literal centered prime-shell operator. A recurring risk is that a stable-looking finite spectral readout may describe only the operator geometry, while the arithmetic source is never actually inserted. The minimal next test is therefore to use the source-native residual, retain the physical masks, and inspect the cross-coordinate Gram term directly.

The paper makes four finite contributions:

1.  it fixes the source vector before measuring any signed energy;

2.  it proves the exact identity $E=D+O$ for the source-coordinate Gram decomposition;

3.  it gives a guarded $96$-row replay over three origins, four scales, four shell anchors, two exponents, and four sign laws; and

4.  it records a non-vacuous finite obstruction: every declared sign law has positive off-diagonal rows, while the all-plus law also has cancellation rows.

All claims below are finite. In particular, a row count is not a uniformity quantifier and a ratio is not an asymptotic exponent.

# The literal finite object

For an origin $o$ and an even scale $N$, set $$I_{o,N}=\{o,o+1,\ldots,o+N/2-1\}.$$ The experiment uses $$o\in\{12001,16001,20001\},\quad
 N\in\{320,640,1280,2560\},\quad H=66,$$ and $Q\in\{24,36,54,80\}$ with $s\in\{1,2\}$. For a prime $p\in(Q,2Q]$, define the real matrix $$\label{eq:block}
 B_{p,Q,s}(u,t)=
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}\,
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right).$$ The diagonal is deleted before the centered residue factor is applied. For a sign law $e=(e_p)_{p\in(Q,2Q]}$, put $$C_e=\sum_{p\in(Q,2Q]}e_pB_{p,Q,s}.$$ The four frozen laws are all-plus, index-alternating, the sign of $p$ modulo $4$, and a half split of the shell in increasing prime order.

For a finite real vector $v=(v_t)_{t\in I_{o,N}}$, define $$\begin{aligned}
 E_e(v)&=\|C_ev\|_2^2,\\
 D_e(v)&=\sum_{t\in I_{o,N}}v_t^2\|C_ee_t\|_2^2,\\
 O_e(v)&=E_e(v)-D_e(v).\end{aligned}$$ Whenever $D_e(v)>0$, the diagnostic ratio is $$R_e(v)=\frac{E_e(v)}{D_e(v)}.$$ Thus $R_e<1$ and $R_e>1$ have an unambiguous finite meaning: negative and positive off-diagonal Gram mass, respectively.

# The source-native model

The arithmetic vector is the finite V59 comparison model, with $$\Lambda(m)=
 \begin{cases}
   \log p,&m=p^k,\ k\geq1,\\
   0,&\text{otherwise},
 \end{cases}$$ and $$\label{eq:comparison}
 b^{(2)}(t)=2C_2\,\mathbf 1_{2\nmid t}
 \prod_{\substack{p\mid t\\p>2}}\frac{p-1}{p-2},\qquad
 C_2=\prod_{p>2}\left(1-\frac1{(p-1)^2}\right).$$ The source vector is $$\beta_o^{(2)}(t)=\Lambda(t+2)-b^{(2)}(t),
 \qquad t\in I_{o,N}.$$ The product in the executable certificate is evaluated through $50000$ and paired with the declared lower multiplier $1-1/(50000-1)$. Logarithms are evaluated at $100$-digit Decimal precision with a rational $10^{-70}$ guard; midpoint values are then passed to the float64 matrix replay. This is a declared finite model and numerical protocol. It is not an identification theorem for an asymptotic twin-prime count.

# Exact Gram decomposition

#### Proposition.

For every finite interval, every finite family of matrices in ([\[eq:block\]](main.tex#L78){reference-type="ref" reference="eq:block"}), every fixed sign law $e$, and every vector $v$, $$\label{eq:gram}
 E_e(v)=D_e(v)+
 \sum_{t\ne t'}v_tv_{t'}
 \langle C_ee_t,C_ee_{t'}\rangle.$$

#### Proof.

The finite matrix product is $C_ev=\sum_t v_tC_ee_t$. Bilinearity of the Euclidean inner product gives $$\|C_ev\|_2^2
 =\sum_{t,t'}v_tv_{t'}
   \langle C_ee_t,C_ee_{t'}\rangle.$$ The terms with $t=t'$ are exactly $D_e(v)$, and the remaining finite terms are the second summand in ([\[eq:gram\]](main.tex#L139){reference-type="ref" reference="eq:gram"}). No limiting interchange or arithmetic estimate is used. $\square$

The proposition is the invariant object of this release. The positivity and finite trace bookkeeping are standard finite-dimensional matrix facts `\cite{horn2013matrix}`. It prevents a small output energy from being silently attributed to diagonal mass alone, and it makes the sign of the cross-coordinate contribution auditable.

# Protocol and certificate

The producer writes a canonical JSON certificate containing every row, including source interval, shell, matrix dimensions, component controls, $E,D,O,R$, the ratio guard, and the classification. A row is labelled `NEGATIVE_OFF_DIAGONAL` when $R+5\cdot10^{-8}<1$, and `POSITIVE_OFF_DIAGONAL` when $R-5\cdot10^{-8}>1$; otherwise it is unresolved. The certificate requires no unresolved residual row and positive component controls.

The independent checker does not import the producer. It constructs the source values with separate factorization code, accumulates the shell in reverse order, recomputes all four coherent matrices, and checks the stored metrics. The stress suite checks the finite identity with exact rational arithmetic, the deleted diagonal, source/sign mutations, shell geometry, provenance locks, and the claim firewall. Normal and optimized executions are required to have empty standard error and identical output.

# Finite results

The full Cartesian panel has $3\times4\times4\times2=96$ rows. Table [1](main.tex#L189){reference-type="ref" reference="tab:census"} gives the off-diagonal census.

<div id="tab:census">

| sign law          |  $O<0$|  $O>0$|  unresolved|
|:------------------|------:|------:|-----------:|
| all-plus          |     81|     15|           0|
| alternating index |     73|     23|           0|
| mod-$4$ character |     74|     22|           0|
| half split        |     61|     35|           0|

: Guarded finite off-diagonal census.

</div>

For all-plus and the residual vector, the ratio range over all rows is $$0.15702348685234854\ \leq R_{+}(\beta_o^{(2)})
 \leq 1.4021661919173145.$$ The all-plus ratio for the positive von-Mangoldt component is above one on all $96$ rows. Its minimum and the corresponding minimum for the comparison component are $$\min R_+(\Lambda(\mathord{\cdot}+2))=1.4345187728485156,
 \qquad
 \min R_+(b^{(2)})=3.1071920015130248.$$ Consequently, the residual split is not a zero-energy or unresolved-component artifact.

The row-level finite conclusion is deliberately narrow:

> None of the four declared sign laws supplies the contraction $E_e(\beta_o^{(2)})\leq D_e(\beta_o^{(2)})$ uniformly on the released panel.

The all-plus law nevertheless exhibits cancellation on a substantial finite subpanel, so the experiment records both behaviors rather than selecting a favorable subset.

# Exact local anchor

At $I=[20001,20016]$, $Q=4$, and $s=1$, the shell is $\{5,7\}$. We use the exact rational vector $$v_t=\mathbf 1_{t+2\text{ is prime}}-\mathbf 1_{t\text{ is odd}}.$$ For this vector, the exact Fraction calculation gives $$E=673.6882555385803,\qquad
 D=576.5224534951882,\qquad
 O=97.16580204339213,$$ and verifies $E=D+O$ before decimal display. The certificate stores SHA-256 digests of the reduced numerator/denominator strings:

    energy       34a3720cc5edefae7d277fc91ac90846886a54860e76653f57ad5d7ea08241a1
    diagonal     471ba6760b9567f1619c5e1a785c47b727c4b0a78488f9e9337085bbab33b262
    off-diagonal cc7a9f5f61dea745d57fb30e041decb28a79afac5c383d87838b4d1f57738074

The prime indicator records the local pair at $t=20009$ because $20011$ is prime. This is an exact finite anchor, not a statement about the density of twin primes.

# Interpretation and claim boundary

The strongest positive result is the exact source-coordinate decomposition combined with an independently replayed source-native finite atlas. The strongest obstruction is the sign change of $O$ under every predeclared law; in particular, the all-plus law has $15$ positive rows. This refutes a uniform contraction only on the declared finite panel.

The following consequences remain open or unpaid:

-   a growing, source-uniform arithmetic $L^2$ estimate;

-   a canonical arithmetic sign law and a proof of its reassembly bound;

-   an operator-norm estimate with the required physical normalization;

-   the strict $1/400$ endpoint loss, Route-B Gate B, and any twin-prime conclusion.

Accordingly, the release records $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN},\qquad
 \texttt{TWIN\_PRIME\_RESULT=NONE}.$$ The Session-named Route-A and Route-B evaluator files are absent from this checkout; the local Bridge-B checker is a fail-closed fallback and is not an official evaluator pass.

# Reproducibility

The source code, canonical certificate, independent checker, stress suite, proof package, and route ledger are in the project directory `papers/tpc-328-source-native-l2-cancellation`. From the repository root, run:

    python -B papers/tpc-328-source-native-l2-cancellation/code/
      tpc328_source_native_l2_cancellation.py --check
    python -B papers/tpc-328-source-native-l2-cancellation/experiments/
      tpc328_independent_checker.py --check
    python -B papers/tpc-328-source-native-l2-cancellation/experiments/
      tpc328_source_native_l2_stress.py --check

The local Bridge-B checker repeats the required normal/optimized equality and provenance cascade. The next natural question is whether the source-native atlas survives a genuinely held-out growing origin, or whether the finite off-diagonal obstruction can first be upgraded to a structural signed-Gram bound.

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
