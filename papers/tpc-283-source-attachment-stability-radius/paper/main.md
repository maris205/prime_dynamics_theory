# How Stable Is a Literal Twin-Prime Source Attachment?

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding source-lock stage found a nonzero scalar attachment for the literal V59 prime-shell operator on twelve finite rows. We prove an exact Hilbert-space stability formula: for nonzero $S$, $C=\langle w,S\rangle$, $W=\|w\|^2$, and $Y=\|S\|^2$, the squared relative distance from $w$ to the zero-attachment hyperplane is $|C|^2/(WY)$. The unique closest zeroing source is $w-(C/Y)S$. Transferring the TPC-282 intervals shows that every registered row can be zeroed by an information-model perturbation of relative norm less than $3/10$, and six of twelve by one less than $1/10$. This is a precise obstruction to inferring robust arithmetic nondegeneracy from a finite table. The zeroing direction is not claimed to preserve the literal prime source class; admissible source stability remains open.

<!-- SOURCE_BODY_BEGIN -->

# Motivation

Let $P_3$ be the three-contrast block projection. The literal output and source readout are $$S=(I-P_3)A\beta,\qquad w_\perp=(I-P_3)w,\qquad
 C=\langle w_\perp,S\rangle .$$ TPC-282 evaluated this quantity on the frozen V59 operator and found a sign-separated value on all twelve registered rows, but with a small normalized coefficient on the weakest row. We now ask for the distance to a source readout with zero attachment. The vectors below are the projected vectors; the common projection is suppressed from the notation.

# Exact zeroing-radius theorem

> **Theorem: distance to the zero-attachment hyperplane** Let $S$ be nonzero in a real or complex Hilbert space and let $w$ satisfy $$C=\langle w,S\rangle,\qquad W=\|w\|^2>0,\qquad Y=\|S\|^2.$$ For $\mathcal Z_S=\{u:\langle u,S\rangle=0\}$, the unique closest point of $\mathcal Z_S$ to $w$ is $$w_*=w-\frac{C}{Y}S,$$ and $$\operatorname{dist}(w,\mathcal Z_S)^2=\frac{|C|^2}{Y},
>  \qquad
>  \frac{\operatorname{dist}(w,\mathcal Z_S)^2}{W}
>  =\frac{|C|^2}{WY}.
>  \label{eq:radius}$$

> **Proof** $w_*$ is in $\mathcal Z_S$. For any $u\in\mathcal Z_S$, $$w-u=\frac{C}{Y}S+(w_*-u),$$ and the summands are orthogonal. Therefore $\|w-u\|^2=|C|^2/Y+\|w_*-u\|^2$, with equality only at $w_*$.

> **Remark** This is an information-model theorem. The zeroing direction need not arise from changing a cutoff, clock, prime shell, or Möbius coefficient.

The normalized coefficient in [\[eq:radius\]](main.tex#L57){reference-type="eqref" reference="eq:radius"} is exactly the quantity reported by TPC-282; no numerical surrogate is introduced.

# Finite transfer

The registered triples $(X,H,Q)$ are $$(64,15,4),(96,20,5),(128,24,5),(192,32,6),(256,38,6),(384,50,7),$$ with $s=1,2$. The TPC-282 certificate supplies outward intervals for $\rho^2=|C|^2/(WY)$. Every upper endpoint is below $9/100$, and six are below $1/100$. Hence the nearest zeroing perturbation has relative norm below $3/10$ on all rows and below $1/10$ on six rows.

|  $X$|  $H$|  $Q$|  $s$|            |
|----:|----:|----:|----:|:----------:|
|   64|   15|    4|    1|  0.074822  |
|   64|   15|    4|    2|  0.061464  |
|   96|   20|    5|    1|  0.089816  |
|   96|   20|    5|    2|  0.083341  |
|  128|   24|    5|    1|  0.015583  |
|  128|   24|    5|    2|  0.025142  |
|  192|   32|    6|    1| 0.00005284 |
|  192|   32|    6|    2|  0.001541  |
|  256|   38|    6|    1|  0.001145  |
|  256|   38|    6|    2| 0.00003372 |
|  384|   50|    7|    1|  0.0009667 |
|  384|   50|    7|    2|  0.0002706 |

: Upper endpoints for the squared relative zeroing radius.

The smallest lower endpoint is at $(256,38,6,2)$ and is about $3.36\times10^{-5}$. Thus the finite source is genuinely nonzero while its unrestricted information distance to failure is small. These statements are compatible and should not be reduced to a binary attached/unattached label.

# Interpretation for Gate B

The typed $L^2$ interface requires both an operator upper bound and a source identification statement. The theorem shows that the latter must specify an admissible source class. If the whole projected Hilbert space is admissible, the explicit zeroing direction is inexpensive on every registered row. If only literal sources are admissible, the relevant distance is to the intersection of that source class with $\mathcal Z_S$, which is not characterized here. Consequently no arithmetic exponent or fixed-power credit is paid, and full Gate B remains open.

# Verification and claim firewall

The producer hash-locks TPC-282 code and result. Four exact rational fixtures verify the minimizer and zeroing identity; the independent checker transfers all twelve parent rows without importing the producer; a hostile checker rejects mutations of the theorem, thresholds, budget, provenance, fixtures, and census. Normal and optimized runs have empty standard error and identical output. The adversary is explicitly information-model only, not a physical counterexample inside the prime/Möbius source family.

# Conclusion

The exact distance formula turns the weak TPC-282 coefficient into a stability radius. Every registered row lies within $30\%$ of a zero-attachment source in the unrestricted projected space, and half lie within $10\%$. The next natural bridge is an admissible-literal-source control theorem, not an unsupported asymptotic lower bound.

# References

9 Liang Wang, *Literal Source Attachment in the Four-Packet TPC Interface*, TPC-282 in-repository artifact, 2026.

<!-- SOURCE_BODY_END -->
