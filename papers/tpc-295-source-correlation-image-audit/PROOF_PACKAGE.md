# TPC-295 proof package

## Theorem 1 — Gram full rank implies source-correlation surjectivity

Let $A\in\mathbb Q^{n\times m}$ and $G=A^{\mathsf T}A$.  If $G$ is
nonsingular, then the map $A^{\mathsf T}:\mathbb Q^n\to\mathbb Q^m$ is
surjective.  For every $b\in\mathbb Q^m$, one exact preimage is
$h=A G^{-1}b$.

**Proof.** Nonsingularity of $G$ implies that $G^{-1}$ exists over
$\mathbb Q$.  Set $h=A G^{-1}b$.  Then
$A^{\mathsf T}h=A^{\mathsf T}A G^{-1}b=GG^{-1}b=b$. ∎

## Lemma 2 — modular nonzero determinant certifies rational nonsingularity

Let $G$ have rational entries and let $p$ avoid all entry denominators.  If
the entrywise reduction $G_p$ has nonzero determinant in $\mathbb F_p$, then
$\det G\ne0$ over $\mathbb Q$.

**Proof.** Clear denominators using a common denominator $D$ with
$p\nmid D$.  The reduction of $D^m\det G$ is the nonzero value
$\det G_p$.  Therefore the integer numerator $D^m\det G$ is nonzero, hence
$\det G\ne0$. ∎

## Corollary — finite feasibility of TPC-294 targets

If the modular rank test is full on a row, the all-positive vector, the
TPC-293 max-cut vector, and the TPC-294 weighted minimizer all have exact
finite rational source preimages under $A^{\mathsf T}$.  The certificate finds
full rank at both moduli on all 18 rows, so this corollary holds for all 18.

This corollary is not a native-profile theorem: it uses the explicitly broad
source space $\mathbb Q^I$.

## Finite certificate consequence

```text
mod 1000000007 full rank = 18 / 18
mod 998244353 full rank = 18 / 18
unrestricted source-correlation surjectivity = 18 / 18
weighted minimizer target feasibility = 18 / 18
```
