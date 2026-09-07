# Source Polarization and the Cross-Term Ledger\ in a Finite Twin-Prime Signed-Gram Model

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

TPC-332 moved a five-control signed-Gram decomposition to a disjoint two-origin, three-scale ensemble, but left the arithmetic source norm as the live gate. This paper removes the dense operator and isolates the source polarization identity $$\|\Lambda-b\|_2^2=\|\Lambda\|_2^2+\|b\|_2^2-2\langle\Lambda,b\rangle.$$ On the six parent-locked windows, the normalized cross-term coefficient $\kappa=2\langle\Lambda,b\rangle/(\|\Lambda\|_2^2+\|b\|_2^2)$ lies between $0.3548658992$ and $0.3625023538$. Thus the residual retains between $0.6374976462$ and $0.6451341008$ of the component-sum energy: the two components are neither nearly orthogonal nor nearly fully canceling on this finite panel. An independent reverse-factorization replay and mutation stress suite verify the ledger. This is a finite source diagnostic, not a source-uniform estimate, power saving, or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Motivation and claim boundary

The session’s dynamical twin-prime route uses a finite source vector of the form $\beta=\Lambda-b$ together with a signed prime-shell response. Earlier papers separated source norm from coordinate placement and then separated a control average from centered position response. The remaining arithmetic question is elementary in form but decisive in interpretation: how much of $\|\beta\|_2^2$ is explained by the cross term between the von Mangoldt-like component $\Lambda$ and the comparison component $b$?

We make one deliberately narrow contribution. We certify the four terms of the polarization identity on a new finite source ensemble and test two extreme readings of the cross term:

1.  “orthogonal”: the cross term is negligible;

2.  “complete cancellation”: the cross term nearly equals the sum of the two component energies.

The finite data reject both readings only for the declared windows and model; the underlying quadratic-form expansion is standard (see, e.g., `\cite{horn2013matrix}`). No statement below controls arbitrary origins, an unbounded cutoff, or the prime-pair counting function.

# Finite source model

For $o\in\{42001,44001\}$ and $N\in\{2048,4096,8192\}$, let $$I_{o,N}=\{o,o+1,\ldots,o+N/2-1\}.$$ The source is the parent-locked finite model $$\label{eq:source}
 \beta_o^{(2)}(t)=\Lambda(t+2)-b_o^{(2)}(t),\qquad
 b_o^{(2)}(t)=2C_2\,\mathbf 1_{2\nmid t}
 \prod_{\substack{p\mid t\\p>2}}\frac{p-1}{p-2}.$$ Here $\Lambda(p^k)=\log p$ and is zero away from prime powers. The finite Euler product defining $C_2$ is evaluated through the inherited cutoff $50000$, with the parent decimal midpoint and rational tail enclosure. All values $t+2$ in the six windows lie below this cutoff.

The symbols in [\[eq:source\]](main.tex#L71){reference-type="eqref" reference="eq:source"} are therefore a declared finite numerical model, not an assertion that a truncated comparison is an exact global identity. The parent TPC-332 producer and certificate are locked by normalized SHA-256 in the machine-readable result.

# Polarization ledger

For finite real vectors $a,b$, symmetry and bilinearity of the Euclidean inner product give $$\label{eq:polarization}
 \|a-b\|_2^2=\langle a-b,a-b\rangle
 =\|a\|_2^2+\|b\|_2^2-2\langle a,b\rangle.$$ Applying this to $a=\Lambda$ and $b=b_o^{(2)}$ gives the source identity. Let $$S=\|\Lambda\|_2^2+\|b\|_2^2>0,qquad
 \kappa=\frac{2\langle\Lambda,b\rangle}{S},qquad
 \rho=\frac{\|\Lambda-b\|_2^2}{S}.$$ Then, exactly, $$\label{eq:complement}
 \rho=1-\kappa,qquad
 \operatorname{corr}(\Lambda,b)=
 \frac{\langle\Lambda,b\rangle}{\|\Lambda\|_2\|b\|_2}.$$ The coefficient $\kappa$ is a dimensionless diagnostic. It is not a positive-definite correlation coefficient and need not lie in $[0,1]$ in an arbitrary model; the interval observed here is a finite result.

# Protocol and exact anchor

The producer evaluates the source arrays for the six pairs $(o,N)$, records the four terms in [\[eq:polarization\]](main.tex#L90){reference-type="eqref" reference="eq:polarization"}, and compares the two nested scales at each origin. It also stores nonzero-coordinate and coordinate-sign counts, so that a later support audit can use the same rows. The independent checker uses its own trial sieve, reverse distinct-factorization pass, and reverse order for the finite tail product. It does not import the producer’s source routine. The stress program mutates the row count, a cross-term entry, the interval census, the firewall, and the exact anchor; every mutation is rejected.

The exact algebra anchor uses rational vectors $$\Lambda=(3,-2,5,1),\qquad b=(1,1,-1,2),
 \qquad \Lambda-b=(2,-3,6,-1).$$ It gives $$\|\Lambda\|^2=39,\quad \|b\|^2=7,\quad
 \langle\Lambda,b\rangle=-2,\quad
 \|\Lambda-b\|^2=50=39+7-2(-2).$$ Reduced-fraction digests of these values are stored in the certificate. The anchor proves the finite algebra and does not pretend to be a prime-density experiment.

# Results

Table [1](main.tex#L144){reference-type="ref" reference="tab:range"} summarizes the six source windows. Every row falls in the predeclared diagnostic interval $(0.35,0.37)$.

<div id="tab:range">

| quantity                            |       minimum       |       maximum       |
|:------------------------------------|:-------------------:|:-------------------:|
| $\kappa=2\langle\Lambda,b\rangle/S$ | 0.35486589921455675 | 0.36250235375855522 |
| $\rho=\|\Lambda-b\|^2/S$            | 0.63749764624144467 | 0.64513410078544309 |
| normalized cross-correlation        | 0.46455337638475735 | 0.48443427505641973 |

: Ranges over the six source windows.

</div>

The largest recorded floating-point identity error is $1.4551915228366852\times10^{-11}$. The four adjacent-scale residual-energy growth factors, in origin order and scale order, are $$1.8736551016394614,\quad 1.9695310092544431,\quad
 1.9140068638900343,\quad 2.037675446375288.$$ The corresponding changes in $\kappa$ are $$-0.0047693401,\quad 0.0029351603,\quad
 -0.0016238452,\quad -0.0044484720.$$ These numbers describe finite-dimensional inclusions, not a convergence claim. In particular, the source cutoff is fixed while the vector dimension changes.

The observed coefficient has a useful interpretation. The cross term removes roughly 35–36 percent of the sum of component energies, leaving roughly 64 percent in the residual. This is enough to rule out a narrative in which the comparison term is irrelevant on this panel, but far from enough to establish a cancellation mechanism that could pay a power-saving gate.

# What the ledger does and does not prove

The strongest positive result is a clean source-level interface: the four terms, dimensionless coefficient, and nested-scale comparisons are all recomputed independently on six disjoint-from-parent windows. The strongest obstruction is equally clear: finite source polarization is in a mixed regime, so neither near orthogonality nor near total cancellation is a safe replacement for a future uniform estimate.

The release labels are:

-   `PROVED_EXACT_FINITE`: [\[eq:polarization\]](main.tex#L90){reference-type="eqref" reference="eq:polarization"} and [\[eq:complement\]](main.tex#L101){reference-type="eqref" reference="eq:complement"};

-   `NUMERICALLY_CERTIFIED_FINITE`: six rows, four scale pairs, independent replay, and five mutation rejections;

-   `REFUTED_SCOPED`: the two extreme cross-term readings on this finite panel;

-   `OPEN`: a source-uniform arithmetic $L^2$ bound, support attribution, strict $1/400$ payment, Route-B Gate B, and a twin-prime conclusion.

Thus $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN},\qquad
 \texttt{TWIN\_PRIME\_RESULT=NONE}.$$ The Session-named Route-A and Route-B evaluator files are not present in this checkout. The local Bridge-B check is consequently a fail-closed repository test, not an official evaluator pass.

# Next question

The cross term is substantial, but its numerical value alone does not say which arithmetic coordinates create it. The next natural paper will split $\langle\Lambda,b\rangle$ into actual twin-prime coordinates, prime-power coordinates, and the odd composite background. That support ledger is the smallest test of whether the source polarization has any twin-prime-specific content.

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
