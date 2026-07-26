# TPC-113: Canonical physical frame and reassembly

Paper title:

> *Canonical Physical Frame Conditioning and Reassembly Audit: Exact Quotient
> Singular Values, a Sharp Coherence Obstruction, and the Strict
> Endpoint Gate*

## Core result

For the declared literal synthesis map `S_X` and its declared Hilbert
source norm, the exact quotient condition number is

```text
kappa_q(S_X)
  = sigma_max(S_X) / sigma_min^+(S_X)
  = sqrt(lambda_max^+(S_X^* S_X) / lambda_min^+(S_X^* S_X)).
```

The source is first quotiented by `ker S_X`; kernel zero-directions are
not infinite-conditioning obstructions.  The quotient condition
number is not invariant under arbitrary redundant reparameterization
and is not automatically the H9 forward synthesis cost.  Its exact
operator meaning is

```text
sup_{||Q|| <= 1} ||S_X Q S_X^dagger|| = kappa_q(S_X).
```

This is a sharp uniform upper envelope over intervening operators,
not an inevitable loss: `S_X S_X^dagger` is the identity on the
physical range and has norm one. The H9 ledger must use the actual
literal composite/norm.

For two literal physical columns with norms `alpha,beta` and
normalized coherence `rho`, the two-column Gram eigenvalues satisfy

```text
lambda_+/- =
  (alpha^2 + beta^2
   +/- sqrt((alpha^2-beta^2)^2 + 4 alpha^2 beta^2 rho^2)) / 2,

kappa_q_pair^2 = lambda_+ / lambda_-
             >= (1 + rho) / (1 - rho).
```

Equality in the lower bound occurs for equal norms. This transfers to
the complete frame only if the pair is a reducing Gram block or a
separate full-Gram certificate proves the inheritance. Under that
hypothesis, `1-rho <= X^(-2 chi+o(1))` forces quotient conditioning at
least `X^(chi+o(1))`.  This alone does not stop the endpoint. A stop
requires a separate lower bound for the actual unavoidable H9
composite or a forced-extremal-direction certificate.

## Claim level

- The quotient/SVD identities and sharp two-column example are L0.
- Attaching this quotient condition number to H9 is only a conditional
  L1 bridge requiring the actual operator chain and norm conversion.
- No growing physical Gram lower bound or actual polynomial
  obstruction is proved. There is no L2 arithmetic saving, parity
  breakthrough, or prime-pair theorem.

## Reproduce

```powershell
python experiments/tpc113_frame_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`canonical-physical-frame-reassembly.pdf`

SHA-256: `6f6b8916190859710c836b234a93a2a1f2d103b43bbe1ee50932eed454efee93`
