# TPC-81: Fixed-shift arithmetic transfer gap

This paper identifies the exact bridge still missing between the
literal completion program and the distinguished zero-frequency
flatness condition.

For the actual fixed-shift determinant coefficient

```text
a_X = (A_{C_X}(n))_n
```

it separates

```text
Z_X = sum_n A_{C_X}(n)
D_X = sum_n |A_{C_X}(n)|^2
F_X = |Z_X|^2 / D_X.
```

The main exact results are:

- a missing-Gram Perron certificate for
  `B_X = A_X + M_X`;
- the coefficient-specific survival bound

  ```text
  (1 - sqrt(Xi_X(z)))_+^2
      <= ||B_X z||^2 / ||A_X z||^2
      <= (1 + sqrt(Xi_X(z)))^2;
  ```

- the conservative raw-normalized certificate

  ```text
  delta_reasm
    = [1 - 2 sqrt(kappa_hat chi) - kappa_hat chi - eta]_+;
  ```

- a determinant-binning/dictionary theorem

  ```text
  D_X >= (
      s_X sqrt(delta_reasm Gamma_pre)
      - ||r_X|| / sqrt(D_raw)
    )_+^2 D_raw;
  ```

- the exact high-row exponent transfer

  ```text
  F_X <= X^(1/400 + lambda_D - 2 eta_Z + o(1));
  ```

  hence the sharp condition for a deduction from these recorded
  bounds is

  ```text
  2 eta_Z >= lambda_D.
  ```

  This is not asserted to be necessary for the physical packet when
  the recorded exponents are nonoptimal.

With the current TPC-33 target `eta_Z = 0`, this transfer ledger
permits no positive certified energy loss; its sufficient natural
scale requirement is:

```text
D_X >= X^(-o(1)) Q_X^3 J_X^2.
```

The paper also proves two sharp no-go statements:

- identical unsigned support and energy can have zero modes `N` and
  `0`;
- raw atoms `+1` and `-1` in the same determinant bin have positive
  raw energy but zero determinant energy.

Therefore a completion census alone does not prove zero-frequency
flatness. A literal determinant map, a restricted lower modulus, a
small dictionary residual, a determinant-energy lower bound, and an
independent zero-mode estimate are all required.

Status: exact L0 algebra and a conditional L1 arithmetic interface.
The paper does **not** prove the physical energy lower bound, the
zero-mode estimate, an all-block cover, a fixed-shift
Hardy--Littlewood asymptotic, twin primes, or a breach of the parity
barrier.

Every physical specialization keeps one fixed nonzero `h0`, complete
native keys, literal coefficients, exact support, and one global raw
normalizer. The downstream fixed-power loss ledger continues only
while its total loss is strictly below `1/400`; equality or excess is
a stop condition.

Build with:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
