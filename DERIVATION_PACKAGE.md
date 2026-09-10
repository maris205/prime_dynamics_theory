# TPC working derivation: the long-window congruence terms

Research reconnaissance, 2026-09-09. This is an unnumbered working document,
not a paper release, a route authorization, or a claim that a physical gate is paid.

## Target

Derive the exact full-kernel row energy when the window is no longer shorter
than every selected prime, then test a uniform locally normalized operator bound.
The target is an identity followed by a model proposition, not an arithmetic
cancellation theorem. An independent scoped proof/source audit has now passed.

## Status

COHERENT AS STATED for the explicitly defined model below.
The bound has an independently audited parent proof in [PROOF_PACKAGE.md](PROOF_PACKAGE.md).
Identification with the physical TPC scalar is NOT established.

## Invariant Object

Use the full masked, diagonal-deleted C1 kernel already printed in
[TPC401, exact production-domain identity](papers/tpc-401-c1-diagonal-deletion-decomposition/paper/main.tex).
Do not extend its short-window simplification by dropping congruence terms.
For a finite nonempty set of odd primes $\mathcal P$, let

$$
I_o=\{o,\ldots,o+N-1\},\qquad
T_{uv}=\frac{H^2}{H^2+(u-v)^2},
$$

$$
K_p(u,v)=a_pT_{uv}
\big((p-1)\mathbf1_{p\mid u-v}-1\big)
\mathbf1_{u\ne v}\mathbf1_{p\nmid u}\mathbf1_{p\nmid v}.
$$

The C1 shell specialization is $a_p=p^3/[Q_p^2(p-1)]$, where $Q_p<p\le2Q_p$.
For the algebra, any $a_p>0$ is allowed and must stay in the final bound.

## Assumptions and Notation

- $H$ is a positive integer, $N=4H$, and $o\in\mathbb Z$ is arbitrary.
- The proposed long-window bound additionally requires $p\le H$ for every $p\in\mathcal P$.
- $\varepsilon_p\in[-1,1]$ are arbitrary real model coefficients, not identified arithmetic signs.
- $M=\sum_p\varepsilon_pK_p$ and $G(u)=\sum_p\sum_vK_p(u,v)^2$.
- $D=\operatorname{diag}(G(u))$. Define $D^{-1/2}(u,u)=0$ when $G(u)=0$;
  otherwise it is $G(u)^{-1/2}$. Put $Z=D^{-1/2}MD^{-1/2}$.
- $\mu=\min_{p\in\mathcal P}a_pp>0$.

This is full-kernel row-energy normalization. On the short-window domain it
reduces to the geometry formula used by TPC401; it is not asserted to equal
the physical normalization of the original number-theoretic endpoint.

## Derivation Strategy and Map

1. **Identity:** retain the off-diagonal same-residue matrix instead of setting it to zero.
2. **Identity:** square the literal entry to derive the missing congruence contribution to $G$.
3. **Proposition:** in the long-window domain, same-residue neighbors give a uniform row-energy lower bound.
4. **Proposition:** compare each absolute row sum to its own energy, then use a weighted Schur estimate.
5. **Interpretation only:** compare parameter ranges with the TPC route; no physical saving follows without an identification and loss theorem.

## Main Derivation

Let $U_p=\operatorname{diag}(\mathbf1_{p\nmid u})$ and
$R_p(u,v)=\mathbf1_{p\mid u-v}$. Entrywise, for every window length,

$$
K_p=a_p\left[(p-1)U_p(T\circ R_p)U_p-U_pTU_p-(p-2)U_p\right].
$$

Here $\circ$ is entrywise multiplication. The last term deletes the diagonal;
its coefficient must remain $p-2$. If $N<p$, the off-diagonal part of $R_p$
vanishes, recovering $K_p=-a_p(U_pTU_p-U_p)$.

For an active row $p\nmid u$, define

$$
S_{p,u}=\sum_{\substack{v\in I_o\\v\ne u,\ p\nmid v}}T_{uv}^2,
\qquad
C_{p,u}=\sum_{\substack{v\in I_o\\v\ne u,\ p\mid u-v}}T_{uv}^2.
$$

The entries on the same nonzero residue class have multiplier $p-2$;
the remaining unit entries have multiplier $-1$. Therefore the exact identity is

$$
G(u)=\sum_{p\nmid u}a_p^2
\left[S_{p,u}+(p-1)(p-3)C_{p,u}\right].
$$

For $N<p$, $C_{p,u}=0$ and each prime deletes at most one window coordinate.
That recovers the earlier short-window geometry. For $H\ge p$, at least
$\lfloor H/p\rfloor$ same-residue neighbors are within distance $H$ on one
side of every active row. For $p>3$ their extra energy contribution cannot
be dropped. At $p=3$ the coefficient $(p-1)(p-3)$ is zero: these neighbors
are already counted in $S_{p,u}$, although their kernel signs still differ.

The proof document establishes the candidate estimate

$$
\boxed{\|Z\|_2\le\frac{144\pi}{\mu}<\frac{576}{\mu}.}
$$

In particular, for a shell $Q<p\le2Q$, $H\ge2Q$, and
$a_p=p^3/[Q^2(p-1)]>1$, it gives $\|Z\|_2<576/Q$.
The estimate is uniform in $o$, the number of primes, and all the declared model signs.
Its gain comes from the full row-energy denominator, not from arithmetic sign cancellation.

## Diagnostics

A parent in-memory check used $H\in\{3,5,7,11\}$ with four declared prime/weight
families and four origins each, always respecting $p\le H$. It checked 860 active
prime-row geometry identities and 416 combined row inequalities using exact rational
arithmetic. Eighty-eight sign/operator cases were also evaluated with floating-point
eigenvalues. All probes passed; the largest observed $\mu\|Z\|_2$ was approximately
$5.2959001214$. These are debugging observations, not interval certificates or a proof.
No existing producer or expected artifact was changed by these probes.

## Remarks and Interpretation

The route's historical scales $H\asymp X^{21/32}$ and $Q\asymp X^{1/3}$
eventually lie on the long-window side, unlike the TPC417/418 short-window CRT
simplification. Matching those two exponents is only a domain check: the actual
coefficients, outer weights, readout, and physical losses are separate obligations.

## Boundaries and Non-Claims

- No fixed physical $h_0=2$, actual Möbius signs, packet coverage, or natural outer normalization has been identified.
- No estimate for $|\mathfrak C_X|$ or fixed-power arithmetic credit is asserted.
- A uniform model norm bound does not supply the weighted norms of physical input/output vectors.
- The statement does not cover arbitrary short principal subwindows with newly recomputed energies.
- This does not change a handoff verdict or authorize a new numbered paper.

## Open Risks

The [independent proof/source audit](research/tpc-big-road/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon-longwindow-proof-audit.md)
passed; its minor boundary qualifications are incorporated above and in the proof.
The bounded existing-work comparison identifies the mechanism as an elementary
weighted Schur argument, without establishing publication novelty. No new
physical consequence has been proved. That limitation must survive any later summary.
