# Derivation Package

## Target

Derive the exact relation between the q-labelled diagonal energy, the q-transverse
variance, and the scalar prime-shell energy in the TPC-218 packet object.

## Status

COHERENT AS STATED

## Invariant Object

For each interval index `n`, the invariant object is the tuple of packet vectors
`(Z_q(n))_(q in Q_x)` in the direct-sum Hilbert space `V^P`, where `V=C^J`.

## Assumptions and notation

- `Q_x` is a nonempty finite prime-label set and `P=#Q_x`.
- `V` is a finite-dimensional complex Hilbert space.
- `Z_q(n)` is any V-valued family; no independence or arithmetic cancellation is assumed.
- `Zbar=P^(-1)sum_q Z_q` and `R_q=Z_q-Zbar`.

## Derivation Strategy

Use the orthogonal decomposition of `V^P` into the constant q-direction and its
orthogonal complement, then expand the two squared norms. This is an identity, not an
estimate and not a model replacement.

## Derivation Map

1. The mean-zero relation `sum_q R_q=0` removes the cross term.
2. The shell is `P Zbar`.
3. Summing over `n` gives the integrated ledger.
4. Rearranging gives the necessary and sufficient transverse lower bound for any claimed
   improvement over the factor `P`.

## Main Derivation

For each `n`, write `Z_q=Zbar+R_q`. Then

```text
sum_q ||Z_q||^2 = P||Zbar||^2 + sum_q||R_q||^2,
||sum_q Z_q||^2 = P^2||Zbar||^2.
```

Eliminating `P^2||Zbar||^2` gives

```text
||sum_q Z_q||^2
 = P sum_q||Z_q||^2 - P sum_q||R_q||^2.
```

Summation over `n` produces `E_shell=P(E_diag-E_perp)`. Since `E_perp` is between zero
and `E_diag`, the sharp interval is `0<=E_shell<=P E_diag`. For `0<=eta<=1`,
`E_shell<=eta P E_diag` is equivalent to `E_perp>=(1-eta)E_diag`.

## Remarks and Interpretation

The exact hard part is now a lower bound on q-transverse energy for the literal source;
an upper bound on diagonal energy, even a Hilbert-valued one, cannot supply it.

## Boundaries and Non-Claims

- The identity does not prove that the literal prime shell is transverse.
- The aligned endpoint is a finite structural adversary, not an asymptotic prime family.
- No Möbius, prime, four-packet, or twin-prime cancellation is inferred.

## Open Risks

The next bridge must express `E_perp` in the actual congruence data rather than introduce
an abstract vector family unrelated to the common-source kernel.
