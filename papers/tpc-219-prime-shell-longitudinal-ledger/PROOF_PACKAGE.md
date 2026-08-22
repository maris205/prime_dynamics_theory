# Proof Package

## Claim

Let `Q` be a nonempty finite set with `P=#Q`, let `V` be a Hilbert space, and let
`Z_q(n) in V` for `q in Q` and `n in I`, where `I` is finite. Define

```text
Zbar(n)=P^(-1) sum_q Z_q(n),  R_q(n)=Z_q(n)-Zbar(n),
E_shell=sum_n ||sum_q Z_q(n)||^2,
E_diag=sum_n sum_q ||Z_q(n)||^2,
E_perp=sum_n sum_q ||R_q(n)||^2.
```

Then

```text
E_shell=P(E_diag-E_perp),
0<=E_perp<=E_diag,
0<=E_shell<=P E_diag.
```

For `0<=eta<=1`, `E_shell<=eta P E_diag` holds if and only if
`E_perp>=(1-eta)E_diag`.

## Status

PROVABLE AS STATED

## Assumptions

- `P` is positive and finite;
- `V` has the Hilbert inner product;
- all sums are finite, so rearrangement is exact.

## Notation

The bar denotes the arithmetic mean over q. Norms are the Hilbert norm and all energies
are real nonnegative quantities.

## Proof Strategy

Expand `Z_q=Zbar+R_q`, use `sum_q R_q=0`, and sum the pointwise identity over `I`.

## Dependency Map

1. The mean-zero identity gives the diagonal Pythagorean decomposition.
2. The shell identity follows because `sum_q Z_q=P Zbar`.
3. Nonnegativity gives the endpoint inequalities.
4. Rearrangement gives the equivalence for `eta`.

## Proof

By definition,

```text
sum_q R_q = sum_q Z_q - P Zbar = 0.
```

Using sesquilinearity and the vanishing sum,

```text
sum_q ||Z_q||^2
 = sum_q ||Zbar+R_q||^2
 = P||Zbar||^2 + sum_q||R_q||^2.
```

Also `sum_q Z_q=P Zbar`, so

```text
||sum_q Z_q||^2=P^2||Zbar||^2
 = P sum_q||Z_q||^2-P sum_q||R_q||^2.
```

Summing this equality over `n in I` proves `E_shell=P(E_diag-E_perp)`. The displayed
Pythagorean identity and nonnegativity imply `E_perp<=E_diag`; hence the endpoint bounds.
Finally, subtracting the identity from `E_shell<=eta P E_diag` and dividing by positive
`P` gives exactly `E_perp>=(1-eta)E_diag`, and reversing the algebra proves the converse.
Thus every claim follows. ∎

## Corrections or Missing Assumptions

None.

## Open Risks

The theorem is abstractly exact. Applying it to TPC-218 only identifies the missing
transverse lower bound; it does not prove that bound for the literal source.
