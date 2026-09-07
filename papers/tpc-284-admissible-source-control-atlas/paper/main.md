# A Finite Control Atlas for Literal Twin-Prime Source Attachment

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding TPC-283 stage showed that an unrestricted projected-space source can lie close to a zero-attachment hyperplane. We now impose a small, explicit family of controls inherited from the literal finite operator: change the clock height by $\pm2$, the comparison cutoff by $\pm1$, or the lower endpoint of the prime shell by $\pm1$. On six registered scales and two kernel exponents this produces a 72-row finite control atlas. Outward interval replay certifies that every controlled source attachment is separated from zero: 60 rows are negative and 12 positive. Nevertheless, eight rows flip sign relative to the baseline. The weakest controlled normalized attachment has lower endpoint about $1.4118\times10^{-5}$, while the largest upper endpoint is about $0.1539$. Thus the finite literal source remains nonzero under the declared controls, but finite non-vanishing does not imply sign stability. The six controls are not claimed to exhaust the admissible source class; asymptotic stability, arithmetic $L^2$, and Gate B remain open.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The source-identification gap in the typed Gate-B interface is not resolved by an arbitrary dual functional. For the frozen literal operator $A$, source profile $\beta$, and three-contrast block projection $P_3$, the actual objects are $$S=(I-P_3)A\beta,\qquad w_\perp=(I-P_3)w,
 \qquad C=\langle w_\perp,S\rangle .
 \label{eq:attachment}$$ TPC-282 locked this scalar on twelve baseline rows. TPC-283 proved that an arbitrary projected-space perturbation can zero it at a small relative distance. The present paper takes the next narrower step: test named local controls of the literal schedule itself `\cite{tpc283,tpc268}`.

The word “control” is intentional. We do not assert that changing $H$, $z$, or $Q$ is a physically complete model of every source perturbation. We declare a finite control set, replay it, and report exactly what that set does. This makes the result useful as a boundary test without silently promoting a finite table to a growing theorem.

# Frozen operator and control map

For distinct indices $u,t$ in the registered interval, the literal matrix has the form $$A(u,t)=\sum_{q\in\mathcal Q(Q)}qK_H(u-t)
 {\bf 1}_{q\nmid u}{\bf 1}_{q\nmid t}
 \left({\bf 1}_{u\equiv t\pmod q}-\frac{1}{q-1}\right),
 \label{eq:operator}$$ where $$K_H(h)=\frac{H^{2s}}{(H^2+h^2)^s},
 \qquad \mathcal Q(Q)=\{q:q\text{ prime},\ Q<q\leq 2Q\}.
 \label{eq:kernel}$$ The source coordinates are the frozen prime-power weight minus the comparison profile at cutoff $z$. The projection divides the interval into four equal blocks and uses the three orthogonal contrasts $$(1,1,-1,-1),\qquad(1,-1,0,0),\qquad(0,0,1,-1),
 \label{eq:contrasts}$$ with denominators $4b,2b,2b$ for block size $b$.

The six baseline triples $(X,H,Q,z)$ are $$(64,15,4,4),\ (96,20,5,4),\ (128,24,5,4),\
 (192,32,6,5),\ (256,38,6,5),\ (384,50,7,5),
 \label{eq:baseline}$$ and $s\in\{1,2\}$. Around each baseline we declare $$\begin{array}{lll}
 H-2,&H+2,\\[-2pt]
 z-1,&z+1,\\[-2pt]
 Q-1,&Q+1.
 \end{array}
 \label{eq:controls}$$ Thus $6\cdot2\cdot6=72$ controlled rows. The baseline sign is the sign certified in the TPC-283 result; a flip means that the controlled sign differs from it.

# Interval-sign certification

All rational source and operator calculations are performed in the frozen TPC-268 implementation. Logarithmic prime weights are represented by outward intervals on a fixed rational grid. If an operation receives intervals $[a_-,a_+]$ and $[b_-,b_+]$, its result is rounded down at the lower endpoint and up at the upper endpoint. Exact rational output entries are used for the projected output energy $Y=\|S\|^2$; the source scalar and source norm are retained as outward intervals.

The normalized attachment is $$\rho^2=\frac{C^2}{WY},\qquad
 W=\|w_\perp\|^2,\quad Y=\|S\|^2.
 \label{eq:rho}$$ The elementary interval predicate used below is the following.

> **Proposition: finite sign predicate** If the replayed interval for $C$ is $[c_-,c_+]$ with $c_+<0$, then the controlled attachment is certified negative; if $c_->0$, it is certified positive. If the lower endpoint of the replayed interval for $\rho^2$ is positive, the normalized attachment is certified nonzero.

> **Proof** Every represented real value lies in its enclosing interval. The two strict endpoint inequalities put the interval wholly on one side of zero. The normalized assertion is the same observation applied to $\rho^2$.

# Finite control atlas

The complete certificate contains the 72 controlled intervals. Its census is $$\#\{C<0\}=60,\qquad \#\{C>0\}=12,
 \qquad \#\{C\text{ crosses }0\}=0.
 \label{eq:census}$$ The smallest lower endpoint of $\rho^2$ is attained at the controlled row $(X,s,\text{control})=(192,1,H+2)$: $$\rho^2\ \geq\frac{70591945087}{5000000000000000}
 =1.41183890174\times10^{-5}.
 \label{eq:weakest}$$ The largest upper endpoint is attained at $(64,2,z+1)$ and is less than $0.153899$. Both values are finite extrema over the declared atlas, not uniform constants.

The sign changes are more informative than the raw nonzero census. Table [1](main.tex#L165){reference-type="ref" reference="tab:flips"} lists all eight. The displayed $\rho^2$ intervals are short decimal renderings; the released JSON retains exact rational encodings of the same outward endpoints.

<div id="tab:flips">

|  $X$|  $s$|  $H$|  $Q$| control | baseline | controlled |
|----:|----:|----:|----:|:--------|:--------:|:----------:|
|  128|    1|   24|    5| $Q+1$   |    $-$   |     $+$    |
|  128|    2|   24|    5| $Q+1$   |    $-$   |     $+$    |
|  192|    1|   32|    6| $z-1$   |    $-$   |     $+$    |
|  192|    1|   32|    6| $Q-1$   |    $-$   |     $+$    |
|  192|    2|   32|    6| $Q-1$   |    $-$   |     $+$    |
|  256|    1|   38|    6| $z-1$   |    $-$   |     $+$    |
|  256|    1|   38|    6| $Q-1$   |    $-$   |     $+$    |
|  256|    2|   38|    6| $Q+1$   |    $+$   |     $-$    |

: All sign flips relative to the TPC-283 baseline.

</div>

For example, the $(128,1,Q+1)$ interval for $C$ is approximately $[13.3823,13.3889]$, whereas its baseline is negative. The $(192,1,z-1)$ row has $C$ approximately in $[12.1115,12.1223]$. These are not numerical near-zero ambiguities: all 72 intervals are separated from zero. The flips therefore certify orientation sensitivity of the finite source readout under the named controls.

# What the atlas proves, and what it cannot prove

> **Theorem: declared finite control atlas** For the baseline schedule in [\[eq:baseline\]](main.tex#L91){reference-type="eqref" reference="eq:baseline"}, exponents $s=1,2$, and the six controls in [\[eq:controls\]](main.tex#L100){reference-type="eqref" reference="eq:controls"}, the hash-locked literal replay certifies 72 sign-separated nonzero source attachments. The census is $(60,12,0)$ for (negative, positive, crossing), and exactly eight rows flip relative to the baseline.

> **Proof** The producer enumerates the Cartesian product in the stated order and stores the outward intervals for $C$ and $\rho^2$. The independent checker loads only the frozen TPC-268 engine, reconstructs each controlled parameter tuple, and compares both intervals as exact rational strings. The strict endpoint predicate proves the sign and nonzero assertions row by row. Counting the certified signs and comparing with the hash-locked TPC-283 baseline gives [\[eq:census\]](main.tex#L143){reference-type="eqref" reference="eq:census"} and the eight keys in Table [1](main.tex#L165){reference-type="ref" reference="tab:flips"}.

> **Remark: finite versus asymptotic** The theorem quantifies only a finite declared set. It does not say that a continuous change in $H$, a different cutoff rule, another prime shell, or a Möbius/source perturbation has been tested. In particular, the eight flips do not refute a possible restricted asymptotic theorem; they show that such a theorem must state its control class and margin explicitly.

# Route-B consequence

The literal source interface now has two separate finite facts. Under the unrestricted projected-space model, TPC-283 gives a small distance to zero attachment. Under the six declared schedule controls, every tested row stays nonzero, but the orientation can change. These facts are compatible: a finite control path can avoid zero while crossing from one side of the hyperplane to the other between sampled parameter values, and a finite nonzero table gives no lower bound along a growing family.

Consequently the next useful theorem is not a generic “stability” slogan. It is a source-class statement: specify which prime-shell, cutoff, and clock changes are admissible, prove a quantitative margin for that class, and then establish the arithmetic $L^2$ estimate needed by Gate B. The present paper contributes the finite control atlas and identifies the sign-stability obstruction. It pays no fixed-power credit and proves no twin-prime result.

# Verification and conclusion

The release includes a canonical JSON certificate, an independent replay, a hostile mutation audit, and a fail-closed Bridge-B checker. Normal and optimized executions have empty standard error and identical output. The producer binds TPC-283 and the frozen TPC-268 engine by SHA-256 hashes, so a silent change in the parent source or operator invalidates the certificate.

The main conclusion is deliberately narrow: the declared finite controls preserve nonzero attachment on 72 rows but produce eight sign flips. This is a real source-level diagnostic and a reusable next-step interface, not an asymptotic theorem. The corresponding open problem is to characterize a growing admissible literal-source class and prove its attachment margin.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc283,
  author = {Liang Wang},
  title = {Source-Attachment Stability Radius and Adversarial Zeroing},
  note = {TPC-283 in-repository research artifact, 2026}
}

@misc{tpc268,
  author = {Liang Wang},
  title = {Finite Cutoff Sensitivity Obstruction for the Literal Operator},
  note = {TPC-268 in-repository research artifact, 2026}
}
```

<!-- SOURCE_BODY_END -->
