# Derivation Package

## Target

Make the TPC-223 reassembly input literal: use one coefficient family indexed
by the same prime label `q`, packet label `j`, modulus `h`, residue `a`, and
atom `m`, then derive a common bound for the full reassembly from the two
marginal channel energies.

## Status

`COHERENT AFTER REFRAMING / EXTRA IDENTIFICATION STILL OPEN`.

The finite Hilbert interface is coherent and proved as stated. The paper does
not silently identify the abstract TPC-223 symbols `A_x` and `P_x` with new
asymptotic estimates; that identification remains an explicit downstream
obligation.

## Invariant Object

The invariant object is the common family of vectors

$$
  W_{q,j}=(C_h B_{h,q}^{(j)}(a))_{(h,a)\in\mathcal F}
  \in \ell^2(\mathcal F),
$$

where `q` and `j` are retained until all three energies have been formed. A
finite-window synthesis map can be applied to these vectors afterward; the
Hilbert inequalities are preserved by that map.

## Assumptions

- The label sets have finite cardinalities `P` and `J`.
- Every `W_(q,j)` belongs to one common complex Hilbert space.
- The same coefficient normalization, profile, clock, and support are used in
  all three channel definitions.
- For the literal audit, `B_(h,q)^(j)(a)` uses the TPC-220 residue rule and
  the same `m` cutoff for every channel.
- The finite scale relations are modeling choices for audit only; they are not
  an asymptotic prime-distribution theorem.

## Notation

- `P`: number of active prime labels.
- `J`: number of packet labels, fixed to four in the certificate.
- `E_AP = sum_j ||sum_q W_(q,j)||^2`.
- `E_pol = sum_q ||sum_j W_(q,j)||^2`.
- `E_all = ||sum_(q,j) W_(q,j)||^2`.
- `E_diag = sum_(q,j)||W_(q,j)||^2`.
- `C_(P,J)=PJ/(P+J)`.

## Derivation Strategy

First freeze the common vector family. Next define the two channel marginals
by summing along one label direction at a time. Apply Cauchy in the packet
direction and in the prime direction. Finally combine the two bounds with an
exact scalar min-to-sum inequality and test sharpness on aligned vectors.

## Derivation Map

1. The literal row formula defines one `W_(q,j)`, not two independent models.
2. Summing over `q` gives the AP marginal vectors; summing over `j` gives the
   polarized marginal vectors.
3. A second sum produces the full vector, so both marginal inequalities apply
   to the same target.
4. `min(J E_AP, P E_pol)` is converted to the sharp additive envelope.
5. The aligned family determines the optimal constant and refutes the unit
   constant when both label sets are nontrivial.

## Main Derivation

### Step 1: common literal rows (`IDENTITY`)

For each active `q,j`, define

$$
 B_{h,q}^{(j)}(a)=
 \sum_{0<|m|\le \lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m\bar q\equiv a\pmod h},
 \qquad
 W_{q,j}(h,a)=C_hB_{h,q}^{(j)}(a).
$$

No channel-specific copy of `B` is introduced.

### Step 2: marginal energies (`DEFINITION`)

Set `V_j=sum_q W_(q,j)`, `U_q=sum_j W_(q,j)`, and
`Z=sum_(q,j)W_(q,j)`. Then `Z=sum_j V_j=sum_q U_q`, and

$$
 E_{\rm AP}=\sum_j\|V_j\|^2,
 \qquad E_{\rm pol}=\sum_q\|U_q\|^2,
 \qquad E_{\rm all}=\|Z\|^2.
$$

### Step 3: directional Cauchy (`PROPOSITION`)

The two decompositions of `Z` give

$$
 E_{\rm all}\le J E_{\rm AP},
 \qquad E_{\rm all}\le P E_{\rm pol}.
$$

### Step 4: sharp scalar compiler (`IDENTITY + INEQUALITY`)

For nonnegative `a,b`,

$$
 \min(Ja,Pb)\le \frac{PJ}{P+J}(a+b).
$$

Taking `a=E_AP` and `b=E_pol` gives the common interface. The equality
family `W_(q,j)=u` shows that the coefficient cannot be reduced.

## Remarks and Interpretation

- With fixed `J=4`, `PJ/(P+J)<4`, so the structural factor is `O(1)` and
  contributes exponent loss zero. This is a structural improvement over
  treating reassembly as an unspecified power loss.
- The unit constant is still false: the congruence-aligned stress family has
  `W_(q,j)` identical across all labels and reaches the sharp constant.
- The theorem is stable under a common finite-window synthesis operator, but
  it does not supply either marginal arithmetic estimate.

## Boundaries and Non-Claims

- `source_surrogate` and `collision_stress` are distinct modeling choices and
  cannot be spliced into one growing theorem.
- Exact rational certificates do not prove a PNT, AP dispersion, or
  prime-shell cancellation estimate.
- The result does not create fixed-atom credit, `L2`, strict `1/400` payment,
  or a twin-prime conclusion.
- The natural Hilbert form of TPC-223's reassembly input is proved; matching
  every existing analytic notation to that form remains `OPEN`.

## Open Risks

- The source-clock surrogate must be replaced by a source-locked asymptotic
  theorem with the exact V46 parameter exponents.
- The AP and polarized marginal estimates must be proved simultaneously on
  the same literal coefficient family and physical normalization.
- Non-unit and zero-axis terms must be carried through any later synthesis
  theorem without using this finite audit as a shortcut.
