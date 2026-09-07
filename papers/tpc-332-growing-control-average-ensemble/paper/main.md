# A Growing Control Ensemble for a Finite Signed-Gram Diagnostic

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

We study the finite signed-Gram diagnostic used in this session’s twin-prime dynamical bridge. The preceding control-orbit identity was tested on a small held-out panel. Here the same five multiset-preserving controls are moved to two disjoint origins and three nested source scales, giving 48 rows and 192 law-level decompositions. Finite quadratic algebra proves an exact split of the control-average response into a coherent mean and a centered-position response. An independently replayed source polarization identity is recorded at the same six windows. The all-plus control-average and centered components are positive on all 48 rows, while the coherent component is positive on 47. In contrast, the unpermuted source-native residual has 27 negative and 21 positive rows. This is a stable finite localization, not an arithmetic estimate: source growth, a canonical sign, the strict power payment, the official route gates, and the twin-prime endpoint remain open. The algebra is the standard finite quadratic-form expansion `\cite{horn2013matrix}`; all conclusions are scoped to the declared model and replay protocol.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The signed-Gram object combines a literal prime-shell matrix with a finite arithmetic source vector. Coordinate permutations preserve the source multiset and its Euclidean norm, but need not preserve the matrix response. TPC-331 showed that five controls admit an exact mean–centered decomposition on a two-origin, two-scale panel. The present hostile replication asks:

> Does the decomposition survive a disjoint growing source ensemble, and does its sign pattern survive with it?

The algebraic split and the positive all-plus control-average/centered readouts replicate. The canonical unpermuted residual sign does not.

# Declared finite model

For an origin $o$ and even scale $N$, set $$I_{o,N}=\{o,o+1,\ldots,o+N/2-1\}.$$ The new panel is $$o\in\{42001,44001\},\qquad N\in\{2048,4096,8192\},$$ with source counts $1024,2048,4096$. For $p\in(Q,2Q]$ define $$\label{eq:block}
 B_{p,Q,s}(u,t)=\mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right),$$ where $H=66$, $Q\in\{24,36,54,80\}$, and $s\in\{1,2\}$. The four shell laws are all-plus, alternating index, the sign of $p$ modulo $4$, and the half split in increasing prime order; $C_e=\sum_p e_pB_{p,Q,s}$.

The arithmetic vector is the finite V59 model $$\label{eq:source}
 v(t)=\beta_o^{(2)}(t)=\Lambda(t+2)-b^{(2)}(t),\qquad
 b^{(2)}(t)=2C_2\mathbf 1_{2\nmid t}
 \prod_{\substack{p\mid t\\p>2}}\frac{p-1}{p-2}.$$ The Euler product is evaluated through the fixed cutoff $50000$, with the inherited decimal midpoint and rational tail guard. Every $t+2$ remains below that cutoff, so “growing ensemble” names a finite nested panel only. For a vector $x$ define $$\begin{aligned}
 E_e(x)&=\|C_ex\|_2^2, &D_e(x)&=\sum_t x_t^2\sum_u C_e(u,t)^2,\\
 O_e(x)&=E_e(x)-D_e(x), &R_e(x)&=E_e(x)/D_e(x).
\label{eq:metrics}\end{aligned}$$ The guarded sign of $O_e$ is read from $R_e-1$; a ratio within $5\cdot10^{-8}$ of one is unresolved.

# Five controls and exact identities

Let $M=N/2$ and use $$\pi_0(i)=i,\quad \pi_{3,11}(i)=3i+11\pmod M,\quad
 \pi_{5,17}(i)=5i+17\pmod M,$$ $$\pi_{7,29}(i)=7i+29\pmod M,\qquad \pi_{\rm rev}(i)=M-1-i.$$ The odd multipliers are units modulo $M$, hence each map is a permutation. Writing $P_j$ for its permutation matrix, put $$w_j=P_jv,\qquad \bar v=\frac15\sum_{j=1}^5w_j,
 \qquad z_j=w_j-\bar v.$$ Then $\sum_jz_j=0$. For any real matrix $A$, finite bilinearity gives $$\label{eq:quad}
 \frac15\sum_{j=1}^5\|Aw_j\|_2^2
 =\|A\bar v\|_2^2+\frac15\sum_{j=1}^5\|Az_j\|_2^2.$$ Expanding $Aw_j=A\bar v+Az_j$ cancels the cross terms, so this is an exact finite identity with no limiting or arithmetic input. If $$\Delta_e=\operatorname{diag}\left(\sum_uC_e(u,t)^2\right)_t,
 \qquad D_e(x)=x^T\Delta_ex,$$ the same expansion for $C_e$ and $\Delta_e^{1/2}$ gives $$\begin{aligned}
 \overline E_e&=E_e(\bar v)+E_e^{\rm cen},
 &\overline D_e&=D_e(\bar v)+D_e^{\rm cen},\\
 \overline O_e&=O_e(\bar v)+O_e^{\rm cen}.
 \label{eq:three}\end{aligned}$$ These are identities for quadratic values, not ratios. Independently, the source layer obeys the exact finite polarization identity $$\label{eq:polar}
 \|\Lambda-b\|_2^2=\|\Lambda\|_2^2+\|b\|_2^2-2\langle\Lambda,b\rangle.$$ The largest recorded replay error in this identity is $1.4551915228366852\cdot10^{-11}$.

# Certificate and exact anchor

The machine-readable certificate contains $2\times3\times4\times2=48$ unique rows and $48\times4=192$ law-level decompositions. It stores all three components in [\[eq:three\]](main.tex#L116){reference-type="eqref" reference="eq:three"}, source norms, the source cross term, scale-pair ratios, and guarded classifications. The producer is locked to TPC-331. An independent checker reverses shell accumulation and uses an independent factorization path. A stress suite mutates row geometry, an exact digest, a component census, a protocol field, and the claim firewall; all five mutations are rejected. The local Bridge-B wrapper repeats normal and optimized runs with empty stderr and byte-identical output.

For an exact small anchor, take $I=[44001,44016]$, $Q=4$, shell $\{5,7\}$, $s=1$, and $v(t)=\mathbf 1_{t+2\ {\rm prime}}-\mathbf 1_{t\ {\rm odd}}$. Reduced rational arithmetic verifies all three identities. The decimal projection is:

| component         |         $E$|         $D$|           $O$|
|:------------------|-----------:|-----------:|-------------:|
| identity          |  457.396492|  556.296899|  $-98.900407$|
| control average   |  500.483940|  561.517841|  $-61.033900$|
| coherent mean     |  326.601333|  356.782477|  $-30.181145$|
| centered position |  173.882608|  204.735363|  $-30.852755$|

The reduced-fraction digests, rather than these decimals, are the stored anchor object.

# Finite results

Table [1](main.tex#L160){reference-type="ref" reference="tab:census"} gives negative/positive/unresolved counts over the 48 rows.

<div id="tab:census">

| law               | control average | coherent mean | centered position |
|:------------------|:---------------:|:-------------:|:-----------------:|
| all-plus          |      0/48/0     |     1/47/0    |       0/48/0      |
| alternating index |     31/17/0     |    38/10/0    |      29/19/0      |
| mod-$4$ character |      48/0/0     |     44/4/0    |       47/1/0      |
| half split        |      48/0/0     |     39/9/0    |       48/0/0      |

: Guarded off-diagonal census.

</div>

For the unpermuted all-plus residual, the sign census is 27 negative and 21 positive, with guarded ratio range $$[0.44646203339149909,\;1.1102919670326215].$$ The all-plus coherent energy fraction lies in $[0.12487732823422547,0.244815364950286]$, while the centered fraction lies in $[0.755184635049714,0.87512267176577452]$. Thus the centered response is not negligible. The four adjacent-scale residual-energy growth factors are $$1.8736551016394614,\quad1.9695310092544431,\quad
1.9140068638900343,\quad2.037675446375288,$$ with base-2 slopes $$0.90585540926787733,\quad0.97785213162340834,\quad
0.93659600353467931,\quad1.0269242825184262.$$ These finite descriptors are not a source-uniform asymptotic law.

# Interpretation and claim firewall

The strongest positive result is structural: the exact mean–centered split survives a new two-origin, three-scale panel, and the all-plus average and centered terms remain positive on every row. The source polarization ledger is reproduced to replay precision. The strongest obstruction is the mixed canonical sign and the large centered energy share: control averaging does not remove the position-aware part.

The status labels are:

-   `PROVED_EXACT_FINITE`: equations [\[eq:quad\]](main.tex#L101){reference-type="eqref" reference="eq:quad"}–[\[eq:polar\]](main.tex#L120){reference-type="eqref" reference="eq:polar"}, permutation bijectivity, and the rational anchor;

-   `NUMERICALLY_CERTIFIED_FINITE`: the 48-row decomposition, six source windows, independent replay, and mutation stress;

-   `NUMERICAL_OBSERVATION`: sign ranges, energy fractions, and scale descriptors;

-   `OPEN`: source-uniform $L^2$, a position-response theorem, canonical arithmetic sign, strict $1/400$ payment, full Gate B, and the twin-prime endpoint.

Consequently, $$\texttt{ARITHMETIC\_ADVANCE=NO},\quad\texttt{FIXED\_POWER\_CREDIT=0},\quad
 \texttt{FULL\_GATE\_B=OPEN},\quad\texttt{TWIN\_PRIME\_RESULT=NONE}.$$ The Session-named Route-A and Route-B evaluator files are absent. The local Bridge-B result is a fail-closed repository check, not an official route pass.

# Reproducibility and next question

The project contains the producer, canonical JSON certificate, independent checker, stress suite, derivation and proof packages, route notes, and PDF; the README lists all commands. The next minimal question is to isolate the source cross term $\langle\Lambda,b\rangle$ and classify its support: does it track actual twin-prime pairs, or mostly the odd composite background?

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
