# Growing Prime Shells and the Scalar–Energy Firewall\ A Finite Gram and Full-Rank Obstruction

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 28 August 2026
- Source repository commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding finite prime-shell ledger found substantial cancellation after applying a four-block scalar attachment to a literal deleted-diagonal operator. A tempting next step is to treat that scalar cancellation as a proxy for an arithmetic $L^2$ saving. We test this implication on the same physical object. For each prime component we retain the full output vector, form its exact output Gram matrix, and audit the active aggregate operator. Finite regrouping, the Gram energy identity, and positive semidefiniteness are proved exactly. On a declared 34-row scale/shell/control grid whose largest shell contains 17 primes, every output Gram matrix has full rank; six selected aggregate physical matrices have full active rank. At the same time, 13 rows have an interval-certified scalar retention upper bound below $1/10$, while their exact vector output-energy ratio is greater than one. Thus scalar cancellation is a quotient-level phenomenon and cannot by itself be promoted to physical $L^2$ decay. The result is a finite obstruction and route marker: it supplies no growing-shell theorem, fixed-power credit, Gate-B proof, or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The active twin-prime route keeps a literal prime-shell operator, a fixed physical diagonal deletion, and a source profile inherited from the frozen TPC-268 engine. TPC-287 decomposed the physical output prime by prime and found mixed-sign scalar attachments on shells containing up to seven primes `\cite{tpc287}`. That observation is useful, but it leaves a dangerous identification gap. A scalar functional may cancel while the underlying output vectors remain aligned or even reinforce one another. The question of this paper is therefore:

> On the same literal operator, does finite shell growth turn scalar attachment cancellation into output-energy decay, or does the physical Gram object expose an obstruction?

We study this question without changing the source, normalization, or deleted-diagonal convention. The contributions are:

1.  an exact definition of the prime component matrices, output vectors, and their source-output Gram matrix;

2.  exact finite identities for shell regrouping, scalar attachment, Gram positivity, and vector energy;

3.  a two-axis finite probe: a scale/shell path reaching 17 prime components and an 18-row height/cutoff control grid;

4.  modular full-rank certificates for all 34 output Grams and six selected active aggregate physical matrices;

5.  a finite scalar–energy obstruction in 13 rows, with exact rational energy ratios and outward-interval scalar retention bounds.

The paper is deliberately classified as a finite Route-B structural audit. The words “full rank” and “positive spectrum” refer to the finite objects defined below; neither is an operator-norm saving.

# The literal physical components

Let $I=\{N/2+1,\ldots,N\}$, with $N$ even, and let $q$ be an odd prime. Put $$m_q(u)=\mathbf{1}_{q\nmid u},\qquad
 B_q(u,t)=m_q(u)m_q(t)
 \left(\mathbf{1}_{u\equiv t\pmod q}-\frac{1}{q-1}\right).
 \label{eq:B}$$ The physical matrix deletes the diagonal: $$D_q(u,t)=\mathbf{1}_{u\ne t}B_q(u,t).
 \label{eq:D}$$ For $H>0$ and $s\in\{1,2\}$, the kernel is $$K_{H,s}(h)=\frac{H^{2s}}{(H^2+h^2)^s}.
 \label{eq:K}$$ Given a finite shell $\mathcal S$, define the prime component matrix and its aggregate by $$A_q(u,t)=qK_{H,s}(u-t)D_q(u,t),
 \qquad A_{\mathcal S}=\sum_{q\in\mathcal S}A_q.
 \label{eq:A}$$ For the literal source vector $\beta$ supplied by the TPC-268 engine, write $$g_q=A_q\beta,\qquad
 g_{\mathcal S}=A_{\mathcal S}\beta.
 \label{eq:g}$$ The finite shell used in a row is $\mathcal S_Q=\{q:Q<q\leq2Q,\ q$ prime$\}$. The source weight $w$ is interval-valued because the comparison factor is outward rounded. Its four-block linear attachment is denoted by $$L_w(g)=\sum_{u\in I}w(u)g(u)
 -\sum_{r=1}^{3}\frac{W_r(w)G_r(g)}{d_r},
 \qquad C_q=L_w(g_q).
 \label{eq:L}$$ The three contrast vectors are $(1,1,-1,-1)$, $(1,-1,0,0)$, and $(0,0,1,-1)$, with $d_r=4b,2b,2b$ for block size $b$.

> **Remark** All factors in [\[eq:A\]](main.tex#L110){reference-type="eqref" reference="eq:A"} are retained: the prime label, residue centering, active masks, and deleted diagonal. In particular, $A_q$ is not the lower-rank centered block from the pre-deletion analysis `\cite{tpc285}`.

# Exact identities and the spectral object

> **Theorem: finite shell and attachment additivity** For every finite shell $\mathcal S$ and source vector $\beta$, $$A_{\mathcal S}=\sum_{q\in\mathcal S}A_q,
>  \qquad g_{\mathcal S}=\sum_{q\in\mathcal S}g_q,
>  \qquad C_{\mathcal S}=\sum_{q\in\mathcal S}C_q.
>  \label{eq:add}$$

> **Proof** The first identity is the definition of the finite aggregate. Multiplying it by $\beta$ gives the second identity coordinate by coordinate. The functional in [\[eq:L\]](main.tex#L125){reference-type="eqref" reference="eq:L"} is a sum of terms linear in $g$, so applying it to the second identity gives the third. No limiting or infinite rearrangement is used.

For the shell output vectors define the $|\mathcal S|\times|\mathcal S|$ Gram matrix $$G_{q,r}=\langle g_q,g_r\rangle_I
 =\sum_{u\in I}g_q(u)g_r(u).
 \label{eq:gram}$$

> **Lemma: Gram positivity and energy decomposition** The matrix $G$ is real symmetric positive semidefinite. If $\mathbf{1}_{\mathcal S}$ is the all-ones vector, then $$\operatorname{tr}G=\sum_{q\in\mathcal S}\|g_q\|_2^2=:E_{\mathrm{diag}},
>  \qquad
>  \mathbf{1}_{\mathcal S}^{\mathsf T}G\mathbf{1}_{\mathcal S}
>  =\|g_{\mathcal S}\|_2^2=:E_{\mathrm{shell}}.
>  \label{eq:energy}$$

> **Proof** For any real vector $a=(a_q)$, $$a^{\mathsf T}Ga
>  =\sum_{u\in I}\left|\sum_{q\in\mathcal S}a_qg_q(u)\right|^2\geq0.$$ This proves positive semidefiniteness and symmetry. The trace is the sum of the diagonal inner products. Expanding the all-ones quadratic form and using the second identity in [\[eq:add\]](main.tex#L145){reference-type="eqref" reference="eq:add"} gives the second equality in [\[eq:energy\]](main.tex#L172){reference-type="eqref" reference="eq:energy"}.

We compare two intentionally different ratios: $$R_C=\frac{|C_{\mathcal S}|}{\sum_{q\in\mathcal S}|C_q|},
 \qquad
 R_E=\frac{E_{\mathrm{shell}}}{E_{\mathrm{diag}}}.
 \label{eq:ratios}$$ The first is a quotient after applying $L_w$; the second is a quadratic quantity before that quotient. Equation [\[eq:energy\]](main.tex#L172){reference-type="eqref" reference="eq:energy"} shows that $R_E$ contains all cross terms of the output Gram matrix.

> **Proposition: finite modular spectral witness** Let $M$ be a rational square matrix whose entry denominators are units modulo a prime $p$. If its reduction has full rank over $\mathbb F_p$, then $M$ is nonsingular over $\mathbb Q$. Consequently, if a rational Gram matrix is positive semidefinite and has full modular rank, all of its real eigenvalues are strictly positive.

> **Proof** Full modular rank makes the reduced determinant nonzero. The rational determinant therefore has a numerator not divisible by $p$ and is nonzero. A full-rank real positive semidefinite matrix has no zero eigenvalue, so all its eigenvalues are positive.

For the aggregate physical matrix, define the active set $$I_{\mathrm{act}}=\{u\in I:q\nmid u\text{ for every }q\in\mathcal S\}.
 \label{eq:active}$$ Rows and columns outside this set vanish for every component. A full-rank modular witness for $A_{\mathcal S}|_{I_{\mathrm{act}}}$ therefore certifies a full-rank physical block on its actual nonzero coordinates.

# Finite growth and control design

The eight growth-path anchors are shown in Table [1](main.tex#L234){reference-type="ref" reference="tab:path"}. The first four enlarge both $N$ and $Q$; the final points hold $N=512$ while increasing the shell endpoint. This separation prevents a shell effect from being mistaken for a scale effect.

<div id="tab:path">

|  $N$|  $H$|  $Q$|  $|\mathcal S_Q|$|  $|I_{\mathrm{act}}|$|  $R_C^+(s=1)$|  $R_E(s=1),R_E(s=2)$|
|----:|----:|----:|-----------------:|---------------------:|-------------:|--------------------:|
|  128|   24|    9|                 3|                    49|      0.160590|       1.9553, 2.1249|
|  192|   32|   16|                 5|                    75|      0.956258|       3.0370, 3.4437|
|  256|   38|   27|                 7|                   106|      1.000268|       2.1666, 2.6226|
|  384|   50|   40|                10|                   158|      0.080212|       4.5574, 7.1066|
|  512|   58|   50|                10|                   219|      0.072951|       4.7417, 7.5286|
|  512|   58|   60|                13|                   217|      0.361521|      6.9169, 10.9927|
|  512|   58|   70|                15|                   217|      0.246425|      8.9010, 13.5583|
|  512|   58|   90|                17|                   222|      0.135277|     12.3630, 16.4393|

: Growth-path rows. Each anchor is evaluated at $s=1,2$.

</div>

The $R_C^+$ column is an interval upper bound, not a floating-point estimate of the exact ratio. The control grid fixes $(N,Q)=(384,70)$ and varies $H\in\{48,50,52\}$, $z\in\{3,5,7\}$, and $s\in\{1,2\}$. It contains 18 rows. The comparison cutoff $z$ changes the literal source weight; the height changes the kernel. The complete grid consequently has $16+18=34$ rows.

# Certificate construction

Every source coefficient, residue factor, and kernel value is represented as an exact rational number. The comparison weights use the outward interval implementation inherited from TPC-268. For a component interval $J_q=[\ell_q,u_q]$, define $$\begin{aligned}
 a_q^-&=\begin{cases}0,&0\in J_q,\\
 \min(|\ell_q|,|u_q|),&0\notin J_q,\end{cases}&
 a_q^+&=\max(|\ell_q|,|u_q|).
 \label{eq:absinterval}\end{aligned}$$ With $J_{\mathcal S}$ the independently computed shell interval, set $$m^- =\sum_q a_q^-,\quad
 m^+=\sum_q a_q^+,quad
 R_C^- =\frac{a_{\mathcal S}^-}{m^+},\quad
 R_C^+ =\frac{a_{\mathcal S}^+}{m^-}.
 \label{eq:ret}$$ When $m^->0$, interval inclusion gives $$R_C\leq R_C^+.
 \label{eq:retupper}$$ Thus $R_C^+<1/10$ is a finite certified cancellation event.

The output energy is computed before decimal serialization: $$E_{\mathrm{diag}}=\sum_{q,u}g_q(u)^2,qquad
 E_{\mathrm{shell}}=\sum_u\left(\sum_qg_q(u)\right)^2.
 \label{eq:exactenergy}$$ The ratio $R_E$ is therefore exact rational data. The output Gram is reduced modulo $p=1\,000\,000\,007$ and row-reduced. On the finite grid all denominators are units modulo $p$; in particular, the largest kernel denominator before powers is below $p$. Six declared rows additionally reduce the aggregate physical matrix restricted to $I_{\mathrm{act}}$.

# Results

The full finite audit is summarized in Table [2](main.tex#L305){reference-type="ref" reference="tab:summary"}.

<div id="tab:summary">

| Quantity                                       |  Count|         Total|
|:-----------------------------------------------|------:|-------------:|
| Rows                                           |     34|            34|
| Full-rank output Grams                         |     34|            34|
| Strictly positive finite Gram spectra          |     34|            34|
| Full active aggregate physical rank (selected) |      6|             6|
| Energy-amplified rows ($R_E>1$)                |     34|            34|
| Scalar retention upper $R_C^+<1/10$            |     13|            34|
| Scalar–energy mismatch rows                    |     13|            34|
| Component interval crossings                   |      0|  34-row total|
| Maximum shell cardinality                      |     17|             –|

: TPC-288 finite certificate summary.

</div>

The strongest individual mismatch occurs on the control grid at $(N,H,Q,z,s)=(384,52,70,5,2)$: $$R_C^+\approx0.00395715,
 \qquad R_E\approx14.10725.$$ Both values are retained as exact rational strings in the certificate; the displayed decimals are only for orientation. The same control family gives the following pattern:

<div id="tab:controls">

|  $H$|  $z$|  $R_C^+(s=1)$|  $R_E(s=1)$|  $R_C^+(s=2)$|  $R_E(s=2)$|
|----:|----:|-------------:|-----------:|-------------:|-----------:|
|   48|    3|      0.106440|     10.5722|      0.013005|     14.3229|
|   48|    5|      0.044143|     10.5722|      0.005786|     14.3229|
|   48|    7|      0.440945|     10.5722|      0.804599|     14.3229|
|   50|    3|      0.108556|     10.3029|      0.010528|     14.2207|
|   50|    5|      0.045148|     10.3029|      0.005556|     14.2207|
|   50|    7|      0.421984|     10.3029|      0.781372|     14.2207|
|   52|    3|      0.110703|     10.0392|      0.006542|     14.1072|
|   52|    5|      0.046166|     10.0392|      0.003957|     14.1072|
|   52|    7|      0.404106|     10.0392|      0.759009|     14.1072|

: Selected source-control values at $N=384$, $Q=70$.

</div>

The table makes two points. First, the vector energy is amplified on every registered row, including rows with a small scalar retention upper bound. Second, changing the source cutoff can move the scalar quotient across the one-tenth threshold while leaving the vector energy unchanged at fixed $(N,H,Q,s)$. This is exactly the behavior expected when a linear readout forgets directions of the physical output.

## What full rank does and does not say

The modular witnesses show that all 34 finite output Grams have rational rank equal to their shell cardinality. Lemma 3 then gives a strictly positive finite Gram spectrum. The six aggregate matrix witnesses show the analogous absence of a null direction on the actual active coordinates for those rows. These are useful structural facts because they rule out a low-rank or zero-output explanation for the observed scalar cancellation.

They do not imply a lower bound uniform in $N$ or $Q$, and they do not imply that the smallest eigenvalue is bounded below on a growing family. A full rank matrix can be arbitrarily ill-conditioned, and positive semidefiniteness is compatible with large positive cross terms. The exact identity $$R_E=1+\frac{2\sum_{q<r}\langle g_q,g_r\rangle}{
                    \sum_q\|g_q\|_2^2}$$ shows why a scalar sign cancellation is insufficient: it controls one functional of the sum, not the cross-prime Gram form.

# The obstruction and the route consequence

The finite result can be stated as a precise implication failure: $$R_C^+<\frac{1}{10}\quad\not\Longrightarrow\quad R_E<1
 \label{eq:firewall}$$ on the literal finite grid. In fact, the left event and $R_E>1$ coexist in 13 rows. This does not refute a future theorem that estimates the full cross-prime Gram form directly. It refutes only the shortcut that would replace that theorem by a scalar attachment cancellation statement.

The reusable route segment is now

|                                            |
|:------------------------------------------:|
|          literal prime components          |
|                $\downarrow$                |
|   output Gram and active physical matrix   |
|                $\downarrow$                |
| direct collective estimate (still missing) |

The obstruction also clarifies how the next estimate must be typed. It must act on the source-native cross-prime Gram or on a genuinely equivalent operator-valued object. A bound on $L_w(g_{\mathcal S})$ alone cannot pay the physical $L^2$ gate. The literal arithmetic source, the fixed $1/400$ endpoint budget, and Gate B remain untouched.

# Verification and claim firewall

The release contains a producer, an independent replay, a hostile mutation test, and a fail-closed Bridge-B checker. The producer locks the TPC-287 source/result and the frozen TPC-268 engine by normalized-LF SHA-256 hashes. The independent replay does not import the producer. It reconstructs every row, every interval record, every exact energy ratio, every Gram rank, and the six selected operator ranks. Ordinary and optimized executions are required to have empty standard error and byte-identical pass output.

The claim firewall is:

| Claim                                                                              | Status             |
|:-----------------------------------------------------------------------------------|:-------------------|
| $A_{\mathcal S}=\sum_qA_q$, $g_{\mathcal S}=\sum_qg_q$, $C_{\mathcal S}=\sum_qC_q$ | EXACT              |
| Gram PSD and energy identity                                                       | EXACT              |
| /34 Gram full rank and positive finite spectrum                                    | FINITE CERTIFICATE |
| /6 selected active aggregate ranks                                                 | FINITE CERTIFICATE |
| scalar–energy mismatch rows                                                        | FINITE OBSTRUCTION |
| Uniform growing-shell Gram bound                                                   | OPEN               |
| Literal arithmetic $L^2$ estimate                                                  | OPEN               |
| Fixed-power credit / Gate B                                                        | 0 / OPEN           |
| Twin-prime conclusion                                                              | NONE               |

The Session-named Route-A and Route-B evaluator files are absent from this checkout. The local proof package, certificate, independent replay, stress audit, and Bridge-B wrapper therefore record a scoped fallback and do not claim an official evaluator pass.

# Conclusion

TPC-288 follows the cancellation clue from TPC-287 into the physical output space. The exact Gram identity and finite modular witnesses show that the relevant multi-prime object is neither a hidden zero mode nor a low-rank centered shortcut on the audited rows. More decisively, 13 literal rows have strong scalar cancellation while their vector energy is amplified. The scalar readout and the physical $L^2$ problem are therefore separated by a real firewall.

The map position is consequently sharper: the next live bridge is a source-native cross-prime Gram estimate, not another scalar sign census. No asymptotic promotion is made, and all arithmetic and twin-prime gates remain open.

# Reproduction record

From the project directory:

    export PYTHONDONTWRITEBYTECODE=1
    P=code/tpc288_growing_shell_gram_certificate.py
    I=experiments/tpc288_independent_checker.py
    S=experiments/tpc288_gram_stress.py
    python -B "$P" --write
    python -B "$P" --check
    python -O -B "$P" --check
    python -B "$I"
    python -O -B "$I"
    python -B "$S"

The JSON certificate is canonical. Exact rational strings are retained for the scalar masses and energies, while decimal fields are deterministic presentations generated by the frozen engine. The modular prime is $p=1\,000\,000\,007$; all denominators used on this finite grid are checked to be invertible modulo $p$.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc287,
  author = {Liang Wang},
  title = {Prime-Shell Cancellation Depth},
  note = {TPC-287 in-repository research artifact, 2026}
}

@misc{tpc285,
  author = {Liang Wang},
  title = {Prime-Shell Residue Factorization and the Deleted-Diagonal Rank Obstruction},
  note = {TPC-285 in-repository research artifact, 2026}
}

@misc{tpc268,
  author = {Liang Wang},
  title = {Finite Cutoff Sensitivity Obstruction for the Literal Operator},
  note = {TPC-268 in-repository research artifact, 2026}
}
```

<!-- SOURCE_BODY_END -->
