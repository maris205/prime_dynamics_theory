# Proof Package

## Claim

Let `\mathcal Q` be a finite label set of cardinality `P`, let
`j\in\{0,\ldots,J-1\}`, and let `W_(q,j)` be vectors in one complex Hilbert
space. Define

$$
 E_{\rm AP}=\sum_{j=0}^{J-1}\left\|\sum_{q\in\mathcal Q}W_{q,j}\right\|^2,
$$

$$
 E_{\rm pol}=\sum_{q\in\mathcal Q}\left\|\sum_{j=0}^{J-1}W_{q,j}\right\|^2,
 \qquad
 E_{\rm all}=\left\|\sum_{q\in\mathcal Q}\sum_{j=0}^{J-1}W_{q,j}\right\|^2.
$$

Then

$$
 E_{\rm all}\le J E_{\rm AP},
 \qquad
 E_{\rm all}\le P E_{\rm pol},
$$

and the sharp additive interface is

$$
 E_{\rm all}\le \frac{PJ}{P+J}
 \left(E_{\rm AP}+E_{\rm pol}\right).
 \tag{1}
$$

The factor `PJ/(P+J)` cannot be decreased uniformly. Consequently, the
unit-factor statement `E_all <= E_AP+E_pol` is false whenever `P,J>2`.

## Status

`PROVABLE AS STATED` for the finite common-Hilbert theorem. The application to
the TPC-223 asymptotic channel estimates remains an identification problem and
is not included in the theorem.

## Assumptions

- The vectors are in one common Hilbert space and use one common normalization.
- `P,J` are positive integers.
- All sums are finite, so rearrangement of the two label sums is exact.

## Notation

Set

$$
 V_j=\sum_qW_{q,j},\qquad U_q=\sum_jW_{q,j},qquad
 Z=\sum_{q,j}W_{q,j}.
$$

Then `Z=sum_j V_j=sum_q U_q`.

## Proof Strategy

Use Cauchy--Schwarz in the two label directions, then prove the scalar
min-to-sum inequality. For sharpness, use the rank-one aligned family
`W_(q,j)=u` with `u\ne0`.

## Dependency Map

1. `E_all <= J E_AP` depends only on `Z=sum_j V_j` and Cauchy--Schwarz.
2. `E_all <= P E_pol` depends only on `Z=sum_q U_q` and Cauchy--Schwarz.
3. The additive bound depends on the scalar inequality for nonnegative `a,b`.
4. Sharpness depends on the explicitly constructed aligned family.
5. The literal audit depends on substituting the TPC-220 row formula into the
   common vector definition; it does not add an asymptotic estimate.

## Proof

### Step 1: packet-direction bound

Because `Z=sum_j V_j`, Cauchy--Schwarz in the `J`-dimensional label space gives

$$
 \|Z\|^2=\left\|\sum_jV_j\right\|^2
 \le J\sum_j\|V_j\|^2=J E_{\rm AP}.
 \tag{2}
$$

### Step 2: prime-direction bound

Because `Z=sum_q U_q`, the same argument in the `P`-dimensional prime label
space gives

$$
 \|Z\|^2=\left\|\sum_qU_q\right\|^2
 \le P\sum_q\|U_q\|^2=P E_{\rm pol}.
 \tag{3}
$$

### Step 3: scalar min-to-sum inequality

For nonnegative `a,b`, set `r=Ja` and `s=Pb`. If `r\le s`, then

$$
 \min(r,s)=Ja
 \le \frac{PJ}{P+J}(a+b)
$$

because `Ja\le Pb` is equivalent to `a\le(P/J)b`. The other case is
symmetric. Thus

$$
 \min(Ja,Pb)\le\frac{PJ}{P+J}(a+b).
 \tag{4}
$$

Apply (4) with `a=E_AP` and `b=E_pol`, then combine (2) and (3), to obtain
(1).

### Step 4: sharpness

Choose a nonzero vector `u` and set `W_(q,j)=u` for every label. Then

$$
 E_{\rm AP}=J P^2\|u\|^2,
 \qquad
 E_{\rm pol}=P J^2\|u\|^2,
 \qquad
 E_{\rm all}=P^2J^2\|u\|^2.
$$

Therefore

$$
 \frac{E_{\rm all}}{E_{\rm AP}+E_{\rm pol}}
 =\frac{PJ}{P+J},
$$

so equality holds in (1). If `P,J>2`, this factor is greater than one;
therefore the unit-factor interface is false. The case `P=J=2` is the exact
boundary where the ratio equals one, and the one-label cases are also safe.

### Step 5: literal realization

For the TPC-220 row family define

$$
 W_{q,j}(h,a)=C_h
 \sum_{0<|m|\le\lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m\bar q\equiv a\pmod h}.
 \tag{5}
$$

The vector in (5) is formed once and then used in all three energies. If
`T_I` is any common finite-window synthesis map, replacing `W_(q,j)` by
`T_I W_(q,j)` leaves (2)--(4) valid because the proof uses only vector
addition and the Hilbert norm. This establishes the common literal structural
interface. It does not bound `E_AP` or `E_pol` by a power of `x`.

### Step 6: exact finite stress family

Take `h=5`, `H=5Q`, constant profiles, and primes `q` satisfying `q=1 mod 5`
in `(Q,2Q]`. The cutoff is one and `q^{-1}=1 mod 5`, so every primitive row
has the same two coordinates and the same value. Hence (5) realizes the
aligned family exactly, up to the common factor `C_h=1/h`. The resulting
unit-interface failure is literal within this finite stress scope.

Therefore the theorem and its sharpness claim follow. `\square`

## Corrections or Missing Assumptions

- No correction is needed for the finite Hilbert theorem.
- To turn it into a TPC-223 asymptotic input, one must prove that the existing
  AP and polarized estimates are estimates for exactly the two marginal
  quantities in (5), on one source-locked clock and normalization.

## Open Risks

- The stress clock is deliberately not the V46 asymptotic clock.
- The certificate is finite and exact; it contains no prime number theorem or
  cancellation input.
- Zero/nonunit and fixed-atom terms require a later source-locked transfer.
