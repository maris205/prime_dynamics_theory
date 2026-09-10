# A Conditional Signed-Reassembly Compiler\ for the Twin-Prime Bridge

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: August 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding prime-shell papers identify two different missing pieces: a prime-AP collision estimate and a phase-sensitive four-packet cross-correlation estimate. This paper isolates the exact exponent compiler that combines them. If the two channels provide savings $\delta_{\rm AP}$ and $\kappa_{\rm pol}$, and previously paid structural losses total $\lambda_{\rm struct}$, then the assembled exponent has effective saving $$\sigma=\min(\delta_{\rm AP},\kappa_{\rm pol})-\lambda_{\rm struct}.$$ Thus the strict endpoint margin is paid precisely when $\sigma>1/400$. The implication is proved algebraically and certified with exact rational ledgers, including strict, borderline, failed, missing-channel, and loss-dominated cases. The two analytic inputs and the literal reassembly interface remain conditional and open; no arithmetic $L^2$ advance or twin-prime result is claimed.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`CONDITIONAL_THEOREM / FULL_GATE_B_OPEN`.

# Why a compiler is the next bridge

TPC-220 wrote the $q$-transverse row family as a literal weighted prime-AP packet. Its Gram matrix retains the multiplicative collision condition $m q'=m' q\pmod h$, so an off-diagonal collision estimate is still needed. TPC-222 then showed that a four-packet signed quantity is not determined by its diagonal or trace: the exact polarization identity requires four phase-labelled energies. These are distinct interfaces. A bound on either one alone cannot pay a theorem about their reassembled object.

The purpose here is deliberately narrower than proving either estimate. We freeze a common exponent ledger and prove what follows if both estimates are available on the same literal shell, with the same normalization and clock. This makes the missing theorem explicit and prevents a marginal estimate from being silently promoted to a Gate-B result.

# The conditional two-channel interface

Let $E_0$ be a declared baseline exponent. Write $A_x$ for the prime-AP and collision channel, $P_x$ for the polarized four-packet cross-correlation channel, and $S_x$ for the target shell quantity. The input interface is

$$\begin{aligned}
 A_x &\ll x^{E_0-\delta_{\rm AP}+o(1)}, \label{eq:interface}\\
 P_x &\ll x^{E_0-\kappa_{\rm pol}+o(1)}, \\
 S_x &\ll x^{\lambda_{\rm struct}}(A_x+P_x).\end{aligned}$$

Here $\delta_{\rm AP},\kappa_{\rm pol},\lambda_{\rm struct}\geq 0$ are ledger parameters. The first line is the missing TPC-220-type dispersion input; the second is the missing TPC-222-type polarized input. The third line is a conditional identification and reassembly statement. None of these three lines is asserted as a new unconditional prime theorem in this paper.

> **Remark** The use of one common $x$ is essential. Bounds proved on different moduli, different packet profiles, or different averaged parameters cannot be inserted into [\[eq:interface\]](main.tex#L68){reference-type="eqref" reference="eq:interface"} without an additional identification theorem.

# Exact compiler theorem

> **Theorem: conditional signed-reassembly compiler** Assume [\[eq:interface\]](main.tex#L68){reference-type="eqref" reference="eq:interface"}. Define $$\sigma:=\min(\delta_{\rm AP},\kappa_{\rm pol})-\lambda_{\rm struct}.$$ Then $$S_x\ll x^{E_0-\sigma+o(1)}.
>  \label{eq:compiled}$$ If $\sigma>1/400$, then there is an $\varepsilon>0$ such that $$S_x\ll x^{E_0-1/400-\varepsilon+o(1)}.$$

> **Proof** The first two lines of the interface give $$A_x+P_x\ll
>  x^{\max(E_0-\delta_{\rm AP},E_0-\kappa_{\rm pol})+o(1)}.$$ The maximum is $E_0-\min(\delta_{\rm AP},\kappa_{\rm pol})$. Multiplication by the structural factor adds $\lambda_{\rm struct}$ to the exponent, which is exactly $E_0-\sigma$. If $\sigma>1/400$, choose $0<\varepsilon<\sigma-1/400$ and absorb the remaining constant and $x^{o(1)}$ factor into the displayed asymptotic bound.

The theorem is an exact compiler implication, not an estimate of $A_x$ or $P_x$. In particular, the minimum is unavoidable: the weaker channel controls the sum. This is the exponent analogue of the TPC-222 observation that one uncontrolled signed cross-term can destroy a diagonal-only conclusion.

# Rational certificate and adversarial boundaries

For the repository endpoint ledger we use $E_0=5/3$. The strict fixture is

$$\delta_{\rm AP}=\frac1{100},\qquad
 \kappa_{\rm pol}=\frac1{80},\qquad
 \lambda_{\rm struct}=\frac1{1200}.$$

The weakest channel saving is $1/100$, the effective saving is $11/1200$, and the margin over $1/400$ is $1/150$. The compiled exponent is $663/400$, while the strict target exponent is $$\frac53-\frac1{400}=\frac{1997}{1200}.$$

<div id="tab:certificate">

| case              | $\delta_{\rm AP}$ | $\kappa_{\rm pol}$ | $\lambda_{\rm struct}$ |    status   |
|:------------------|:-----------------:|:------------------:|:----------------------:|:-----------:|
| strict            |      $1/100$      |       $1/80$       |        $1/1200$        | strict pass |
| borderline        |      $1/400$      |       $1/400$      |           $0$          |  borderline |
| failed            |      $1/500$      |       $1/400$      |           $0$          |    reject   |
| missing polarized |      $1/100$      |         $0$        |        $1/1200$        |    reject   |
| loss dominated    |      $1/100$      |       $1/80$       |         $1/100$        |    reject   |

: Exact rational compiler boundaries. Equality at $1/400$ is not strict.

</div>

The independent checker recomputes every exponent from the three input fractions, rather than trusting the producer’s derived fields. A separate adversary checks that the borderline case, either zero channel, and a loss-dominated ledger are all rejected. These are finite arithmetic checks; they do not certify the existence of the corresponding prime-shell estimates.

# Route evaluation and claim firewall

The strongest positive result is the exact minimum-of-two-savings compiler. It turns the informal statement “both bridges must be strong enough” into the single strict inequality $$\min(\delta_{\rm AP},\kappa_{\rm pol})
   >\lambda_{\rm struct}+\frac1{400}.$$ The strongest obstruction is equally explicit: a zero channel or equality at the threshold cannot pass. The next open theorem is to establish the two conditional inputs on one literal prime shell, while retaining the finite-window, packet labels, signs, and physical normalization.

`TPC223_ARITHMETIC_ADVANCE=NO; L2=NONE; FULL_GATE_B=OPEN.`

# Conclusion

TPC-223 contributes a reusable conditional theorem and a fail-closed threshold certificate. It does not close a mathematical gate: the AP dispersion, polarized cross-correlation, and common literal reassembly interface remain open inputs. The result therefore belongs to `CONDITIONAL_THEOREM`, not `PROVED_ARITHMETIC`.

# References

9 TPC-220 repository proof record, “Prime-AP collision crosswalk,” 2026. Internal source lock; no external asymptotic estimate is invoked.

TPC-222 repository proof record, “Four-packet polarization and the PSD cross-term obstruction,” 2026. Internal source lock; the signed cross-term interface is exact but its literal arithmetic realization is open.

<!-- SOURCE_BODY_END -->
