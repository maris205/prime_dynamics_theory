# TPC-348 paper plan

## Question

Can the TPC-347 finite observation that the divisibility-mask defect is not
discardable be converted into a deterministic, position-aware lower witness
that does not use the defect's leading eigenvector or an unstructured spectral
proxy?

## Parent lock

The physical object, shell family, normalisation, and finite protocol are
inherited from TPC-347.  The producer and certificate hashes are locked in the
code and in the independent replay.  No new source vector, asymptotic regime,
or arithmetic estimate is introduced.

## Frozen protocol

Use origins `[40097,48097]`, source counts `[256,512,1024]`, shell anchors
`Q=[24,36,54,80]`, kernel exponents `[1,2]`, `H=66`, and the four declared
sign laws from TPC-347.  For each row define

```text
J_I = {t in I : p divides t for at least one active shell prime p}.
```

Store both the first-hit coordinate and the predeclared coordinate envelope

```text
W_I(D) = max_{t in J_I} ||D e_t||_2.
```

The selector is computed only from the declared interval, shell, and defect
matrix; the lower-bound theorem is checked separately from the producer.

## Decision rules

- The exact coordinate inequality is accepted only if
  `||D||_(2->2) >= W_I(D)`.
- A row is positive only when the selected mask-hit column has strictly positive
  norm and the two-sided projection formula is reproduced.
- Ratios to the ideal norm or to the defect norm are finite observations only;
  they do not receive asymptotic or arithmetic credit.
- A failed mask-term mutation must be rejected; a certificate mutation must not
  be silently accepted.

## Deliverables

- an exact finite coordinate lower-witness theorem and mask-hit column formula;
- a 192-row position audit with first-hit and best-hit readouts;
- an independent reverse-shell replay and hostile mutation stress suite;
- an exact rational six-point anchor for the witness column;
- proof package, theorem ledger, claim firewall, route evaluation, PDF, and
  local fail-closed Bridge-B audit;
- a narrowly scoped next clue: test prime-balanced defect witnesses before
  attempting a source-native arithmetic `L2` theorem.
