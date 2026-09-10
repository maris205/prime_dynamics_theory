# A Subcritical Growing-Depth Obstruction\ for Prime-Shell Resonances

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

## Abstract

We determine a necessary growth rate for a prime-shell resonance mechanism to carry a fixed fraction of row energy. At depth $L$, the primitive shared-clock model uses modulus $4LQ$, prime rows $Q<q<2Q$, and multipliers $|m|\le \lfloor Lq/Q\rfloor$. We first prove that every collision in the short-multiplier regime has the one-wrap form $ar+bp=4LQ$, with $a,b<2L$, and that each channel creates exactly two sign-symmetric coordinates. A coefficient-uniform Selberg upper-bound sieve then gives $$C_L(Q)\ll_A LQ\log\log(3LQ)/(\log Q)^2$$ for $L\le(\log Q)^A$. Consequently $C_L(Q)/(\pi(2Q)-\pi(Q))\to0$ whenever $L=o(\log Q/\log\log Q)$. Under a fixed row-mass comparability constant, the incident energy fraction also tends to zero, so no fixed proportional saving can survive at subcritical depth. Two independent exact compilers agree on 19 finite scales; these records reproduce the collision geometry but are not used as asymptotic evidence. The result is a necessary-depth obstruction, not a lower bound at critical depth and not an identification with the actual arithmetic source.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

A fixed collection of two-prime resonance equations is too sparse to control a fixed fraction of a dyadic prime shell: a two-dimensional upper-bound sieve gives $O(Q\log\log Q/\log^2Q)$ edges, whereas the shell contains asymptotically $Q/\log Q$ primes. The natural escape is to let the number of resonance channels grow with the scale. The unresolved quantitative question is how quickly this depth must grow before the support obstruction disappears.

We answer the necessary half of that question for the primitive dilated-clock family. At depth $L$, row $q$ occupies residues $$S_{q,L}=\{mq^{-1}\pmod{4LQ}:0<|m|\le\lfloor Lq/Q\rfloor,
 (m,4LQ)=1\}.$$ This is an exact finite family, but the dilation parameter is a modeling choice. Our argument therefore separates the internal arithmetic theorem from any later source-identification claim.

The main contributions are:

1.  We classify every collision for $L<Q/4$ by one equation $ar+bp=4LQ$, and prove that no residue contains three prime rows.

2.  We retain the interval remainder in the Selberg sieve and obtain a bound uniform for all $L\le(\log Q)^A$, rather than summing a theorem whose implied constant was proved only for fixed coefficients.

3.  We show that the apparent $O(L^2)$ coefficient family has only $O(L)$ aggregate parameter length. This yields the threshold $L=o(\log Q/\log\log Q)$ below which normalized incidence vanishes.

4.  We transfer support sparsity to a fixed-saving obstruction under an explicit row-mass comparability hypothesis.

The analytic input is the classical Selberg upper-bound sieve `\cite{HalberstamRichert1974,IwaniecKowalski2004}`. The two-form mechanism and its determinant correction may also be compared with the expositions in `\cite{GreenAdditive,Rudnick2015}`. We derive all coefficient and clock dependence needed here.

# Growing-depth collision geometry

Let $\mathcal P_Q$ be the primes in $(Q,2Q)$, put $h=4LQ$, and assume $L<Q/4$. Every $q\in\mathcal P_Q$ is a unit modulo $h$, and every active multiplier has magnitude below $2L<q$. Thus each row is internally injective.

> **Lemma: One-wrap normal form** If distinct rows $q_1,q_2\in\mathcal P_Q$ share a residue, then their multipliers have opposite signs and, for positive $a,b<2L$, $$a q_2+b q_1=4LQ. \tag{1}$$ Moreover $(a,b)=1$, at most two rows occupy one residue, and every channel has exactly two residues related by global sign.

> **Proof** A shared residue gives $$m_1q_2-m_2q_1\equiv0\pmod h. \tag{2}$$ For equal signs, the magnitude in (2) is below $h$. Equality to zero would force an active prime to divide a nonzero multiplier shorter than that prime. Hence the signs are opposite. The resulting positive sum is below $2h$, so its only possible positive multiple of $h$ is $h$, proving (1).
>
> Primitivity gives $(a,h)=(b,h)=1$. A common divisor of $a,b$ would divide the right side of (1), and is therefore one. If three rows occupied a residue, two multipliers would have the same sign, contradicting the first part. Finally, changing both multiplier signs gives a second residue. The two cannot coincide because that would make $h$ divide a nonzero integer of magnitude below $4L$. No third residue is possible by the same classification.

This lemma upgrades the first $3$–$7$ collision into a complete growing-depth channel compiler. It does not assert that any particular channel contains prime solutions.

# A coefficient-uniform upper-bound sieve

Fix a coefficient pair $a,b$. If (1) is soluble, $(a,b)=1$ and all integer solutions have the form $$q_1=p_0+ak,\qquad q_2=r_0-bk. \tag{3}$$ The two shell conditions restrict $k$ to an interval $I_{a,b}$ of length $$K_{a,b}\ll Q/\max(a,b)+1. \tag{4}$$ The determinant of the forms in (3) is $$ar_0+bp_0=4LQ. \tag{5}$$

Let $\nu(\ell)$ count the roots of their product modulo a prime $\ell$. There are two roots when $\ell\nmid ab(4LQ)$. At an exceptional prime the two roots coalesce, or one form becomes a nonzero constant, so there is at most one root. The resulting correction is bounded by $$\prod_{\substack{\ell\mid ab(4LQ)\\\ell\ge3}}
 \frac{\ell-1}{\ell-2}
 \ll \log\log(3LQ). \tag{6}$$ The final estimate follows by comparing with the product over the smallest primes and using $ab(4LQ)\ll L^3Q$.

For squarefree $d$, the Chinese remainder theorem gives the explicit remainder formula $$\#\{k\in I_{a,b}:d\mid(p_0+ak)(r_0-bk)\}
 =K_{a,b}\frac{\nu(d)}d+O(\nu(d)). \tag{7}$$ This formula controls the uniformity in $a,b$. Apply Selberg weights with $z=K_{a,b}^{1/10}$. The main term is (4) times (6), divided by $\log^2z$. The double-divisor remainder has moduli below $z^2$; using $\nu(d)\le2^{\omega(d)}$, it is $O(z^2(\log z)^C)$ for an absolute $C$.

There is one short-interval boundary. If $K_{a,b}<Q^{1/2}$, trivial counting gives $O(Q^{1/2})$. Otherwise $\log z\asymp\log Q$, and the sieve remainder is also $O_A(Q^{1/2})$. Thus, for $L\le(\log Q)^A$, the two branches give $$\begin{split}
 C_{a,b}(Q)\ll_A&
 \left(\frac{Q}{\max(a,b)}+1\right)
 \frac{\log\log(3LQ)}{(\log Q)^2}\\
 &+O_A\!\left(Q^{1/2}\right).
\end{split}
\tag{8}$$ Thus (8) is a genuinely uniform growing-coefficient estimate, not a formal sum of fixed-form asymptotics.

# The subcritical depth threshold

The coefficient family has $O(L^2)$ members, but its total parameter length is only linear in $L$.

> **Lemma** For $M=2L-1$, $$\sum_{1\le a,b\le M}\frac1{\max(a,b)}
>  =\sum_{m\le M}\frac{2m-1}{m}<4L. \tag{9}$$

> **Proof** Exactly $2m-1$ ordered pairs have maximum $m$. Summing their weights gives $2M-\sum_{m\le M}1/m<2M<4L$.

> **Theorem: Growing-depth incidence bound** For fixed $A>0$, uniformly over $1\le L\le(\log Q)^A$, $$C_L(Q)\ll_A
>  \frac{LQ\log\log(3LQ)}{(\log Q)^2}. \tag{10}$$

> **Proof** Sum (8) over $a,b<2L$ and apply (9). The summed constant and remainder terms are $o_A(LQ/\log^2Q)$, because $L$ is polylogarithmic.

> **Corollary: Subcritical obstruction** If $L=o(\log Q/\log\log Q)$, then $$\frac{C_L(Q)}{|\mathcal P_Q|}\longrightarrow0. \tag{11}$$ If positive row masses have a fixed maximum-to-minimum ratio $\kappa$, the maximum saving supported only on these collisions is also $o(1)$.

> **Proof** The prime number theorem gives $|\mathcal P_Q|\sim Q/\log Q$, which proves (11). At most $2C_L(Q)$ rows are incident to a collision, so their mass fraction is at most $2\kappa C_L(Q)/|\mathcal P_Q|$. All nonincident rows remain orthogonal to every other row and retain their diagonal energy. Hence the possible saving is bounded by the incident mass fraction.

In particular, no fixed $\delta>0$, including $\delta=1/400$, can be paid at subcritical depth. The corollary is only a necessary condition: $L\asymp\log Q/\log\log Q$ is not proved sufficient.

# Finite reproduction and adversarial checks

The certificate evaluates 19 pairs $(Q,L)$, from the anchor $(25,4)$ through $(3203,512)$. One implementation constructs every primitive row support and intersects residue buckets. A separate implementation starts from (1), solves for the second coefficient, and never uses modular support intersections. The implementations agree on every channel count and unique edge count in normal and optimized Python modes.

At $(25,4)$, both recover the single $3$–$7$ channel and its two coordinates. At $(3203,512)$, the scan contains 381 prime rows, 291934 primitive atoms, 1623 channel occurrences, 338 incident rows, and maximum simple-graph degree 28. These larger finite densities illustrate why a growing-depth theorem is distinct from a fixed-family theorem; they do not establish a limiting density.

The adversarial suite rejects Boolean values as integers, unsafe depths, and the nonprimitive multiplier $m=4$. It verifies the exact identity behind (9) for $1\le L\le79$. The complete scan digest is

`fd4023281dc31c15c23d15ad66e49629565a9918ea36962a7705492bcff8dd5c`.

All finite records are reproducibility checks. The asymptotic conclusion comes only from the sieve proof.

# Conclusion

Allowing resonance depth to grow does not immediately remove the support obstruction. The exact collision compiler and a coefficient-uniform Selberg sieve show that every $L=o(\log Q/\log\log Q)$ still reaches only a vanishing fraction of prime rows. This supplies a quantitative lower order of growth that any fixed saving mechanism must overcome.

Two boundaries remain decisive. First, the theorem is an upper bound and does not prove enough resonances at critical depth. Second, the dilated clock is a modeled family, not the actual source object. The next step is therefore to audit critical-depth row mass and degree, and then test whether the resulting clock can be attached to the physical source without changing coefficients, profiles, signs, or normalization.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{HalberstamRichert1974,
  author    = {Halberstam, Heini and Richert, Hans-Egon},
  title     = {Sieve Methods},
  publisher = {Academic Press},
  year      = {1974}
}

@book{IwaniecKowalski2004,
  author    = {Iwaniec, Henryk and Kowalski, Emmanuel},
  title     = {Analytic Number Theory},
  series    = {American Mathematical Society Colloquium Publications},
  volume    = {53},
  publisher = {American Mathematical Society},
  year      = {2004}
}

@misc{GreenAdditive,
  author       = {Green, Ben},
  title        = {Additive Combinatorics},
  howpublished = {Course notes, Section 2.3},
  url          = {https://people.maths.ox.ac.uk/greenbj/papers/additive-combinatorics.pdf},
  note         = {Accessed 2026-08-24}
}

@misc{Rudnick2015,
  author       = {Rudnick, Zeev},
  title        = {Selberg's Sieve---Twin Primes},
  howpublished = {Course notes},
  year         = {2015},
  url          = {https://www.math.tau.ac.il/~rudnick/courses/sieves2015/selberg\%20sieve\%20twin\%20primes.pdf}
}
```

<!-- SOURCE_BODY_END -->
