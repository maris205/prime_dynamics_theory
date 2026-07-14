# TPC-16: Square-root Type-II normal form

**Paper:** *Square-Root Normal Forms for a Fixed-Shift Type-II Gate:
Recentered Ramanujan Rows, a Near-11/21 Factorable Wedge, and a
Cross-Spectral Angular Criterion*

TPC-15 reduced the fixed-shift prime-pair error to one calibrated but broad
Vaughan hard packet. TPC-16 resolves four further layers without claiming a
twin-prime or parity breakthrough.

## Main results

- For every row modulus `m`, including `m > R`, the complete-period mean of
  the finite Ramanujan model is computed exactly. Its missing local-factor
  drift is

  ```text
  Delta_(h,R)(m) = sum_(q|m, q>R) mu(q)c_q(h)/phi(q).
  ```

- After subtracting this drift, maximal Bombieri--Vinogradov controls the
  full bounded Type-I row ball up to

  ```text
  M = X^(1/2) exp(-sqrt(log X)).
  ```

  Vaughan's identity with `U=M, V=1` gives

  ```text
  sum Lambda(n)Lambda(n+h)W(n/X)
    = singular_series(h) X I0(W)
      - sum_(ell>M,k>1) Lambda(ell)r_R(ell*k+h)W(ell*k/X)
      + O_A(X log^(-A) X).
  ```

  This closes the left unbalanced wing up to the classical square-root
  wall. The right wing remains.

- Opening the original coefficient `beta_V(k)` reveals the progression
  modulus `q=ell*d`. Every contribution with `ell*d <= R` is peeled off.
  Maynard's fixed-residue theorem then proves `o(X)` for one nonempty smooth
  three-scale subpacket approaching

  ```text
  D = X^(1/21), L = X^(10/21), K = X^(11/21).
  ```

  This controls one `D`-resolved factorable wedge, not the complete `(L,K)`
  block and not the whole Type-II packet.

- The Ramanujan residual satisfies the energy law

  ```text
  sum r_R(n)^2 F(n/X) = X log(X/R) I0(F) + O_delta(X).
  ```

  Hence it is not an `l2`-small error. The remaining hard packet is an exact
  translation matrix coefficient and a fixed Fourier coefficient of a
  cross-spectrum. Generic factor phases have power cancellation, but the
  required zero phase is not selected by the phase mean square.

The paper proves no fixed-shift prime-pair asymptotic, no twin-prime lower
bound, no new level of distribution, and no breach of sieve parity.

## Reproduction

From this directory:

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    python experiments/square_root_gate_certificate.py
    python -m unittest experiments.test_square_root_gate_certificate -v

The finite certificate checks algebraic identities, exponent ledgers, and
Fourier conventions only. It does not numerically certify any imported
analytic estimate or open fixed-shift assertion.

The canonical certificate payload SHA-256 is

```text
EE0CF6066CB2A091EBEFC7201C10D34B11CE7040519632EC55A5D33F12FE1A7E
```

The committed JSON file SHA-256 is

```text
20B7CF8A8D7827A23E6FD51A73B0972D611DA72411B4AC76D782E0E6EA7B1E06
```
