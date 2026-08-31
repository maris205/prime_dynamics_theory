# TPC-318 derivation package

## 1. Frozen literal operator

Let `I_X={X/2+1,...,X}`, `S_Q={p prime: Q<p<=2Q}`, and `H=66`.  For
`u,t in I_X`, define

```text
K_(p,u,t) = 1_(u!=t, p does not divide ut) *
            p H^(2s)/(H^2+(u-t)^2)^s *
            (1_(u=t mod p)-1/(p-1)).
```

The source-to-output matrix is `A_(Q,s,X)=(K_(p,u,t))`, and
`G_(Q,s,X)=A^*A`.  All finite entries are rational and `G` is positive
semidefinite.

## 2. Exact spectral inequalities

If the eigenvalues of `G` are `lambda_1 >= ... >= lambda_N >= 0`, then

```text
lambda_1 <= sqrt(sum_i lambda_i^2) = sqrt(trace(G^2)) <= trace(G).
```

TPC-317 certified the middle trace-power envelope.  TPC-318 computes a finite
numerical readout of `lambda_1` itself and retains the middle envelope as a
reference quantity.

## 3. Finite perturbation model

Let `Ghat` be a floating-point reconstruction and suppose
`||G-Ghat||_2 <= epsilon`.  Weyl's inequality gives

```text
|lambda_max(G)-lambda_max(Ghat)| <= epsilon.
```

The implementation uses the safe entry bound `|K|<=160`, the elementary
`||E||_2 <= ||E||_F <= N max|E_ij|` conversion, dual forward/reverse shell
accumulation, two symmetric eigensolver paths, and the returned residual.  The
resulting interval is explicitly a finite numerical certificate under this
model; it is not a proof that the hardware error model covers every future
implementation.

## 4. Normalization and obstruction diagnostics

The reported quantity is `lambda_1(G)/N`, where `N=|I_X|`.  A decrease of this
normalized value has finite log-base-two slopes in the declared range
`[-0.9972378,-0.4238528]`.  The corresponding unnormalized slopes are shifted
by `+1`, so the finite data alone do not pay a source-to-output power budget.

The second eigenvalue is recorded as a stability diagnostic.  Ten of the 24
rows have relative top gap below `0.01`, and the minimum observed gap is about
`0.001704`.  Thus a top-eigenvector argument would need a clustered-subspace
analysis before it could be used for arithmetic reassembly.
