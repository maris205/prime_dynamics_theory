# TPC-46: Shift-spectral gaps and tensor-normalization barriers

> **Mesoscopic Shift-Spectral Gaps and Tensor-Normalization Barriers for Three-Coefficient Determinant Packets**

TPC-46 studies the next analytic door left by TPC-45 for the
large-prime determinant packet

```text
p r - m j = h.
```

It asks whether averaging the determinant shift and exploiting the
smooth orbit variable `j` can release the missing third arithmetic
coefficient. The answer has a rigorous positive part and an equally
important transfer boundary: a genuine mesoscopic spectral gap exists
for the completed/frozen packet, but this alone does not give the
atomic-normalized physical column at one fixed shift.

The actual orbit profile also contains a fixed residue-class selector.
The paper retains it exactly and proves the corresponding arithmetic-
progression Poisson formula; it changes constants, not the endpoint
gap exponents.

## Main results

### 1. Exact fixed-shift tensor closure

Multiplicative synthesis gives

```text
T_h = sum_n A(n) C(n-h),
```

and hence

```text
|T_h|^2 <= rho_pr rho_mj D_tensor.
```

In the large-prime TPC range, `rho_pr = 1` and `rho_mj = X^o(1)`.
A finite Fourier-Bohr lift gives the analogous closure after retaining
the residual label `s = d(m) r`.

The normalization is crucial:

```text
D_tensor = sum_h Delta_h,
```

not the atomic diagonal `Delta_h0` at the physical shift. Flat boxes
and a prescribed-shift coherent construction show a polynomial gap can
occur between these two scales.

### 2. A genuine mesoscopic shift-spectral gap

For a completed Hilbert-valued packet whose vector coefficient is
independent of `j`, Poisson summation gives

```text
K_m(alpha) = J sum_k w_hat(J(k - m alpha)).
```

If `w_hat` is supported in `[-sigma,sigma]`, the packet vanishes on

```text
sigma/(M_- J) < ||alpha|| < (1 - sigma/J)/M_+.
```

At the TPC endpoint this becomes

```text
X^(-1+o(1)) < ||alpha|| < X^(-267/400+o(1)).
```

Band-pass shift averages supported in that gap vanish exactly.
Low-pass averages have an exact zero-Poisson-mode formula. For ordinary
compactly supported smooth profiles, the Fourier gap becomes rapid
decay on a fixed power-shrunken band, while the low-pass identity
becomes a Poisson approximation with a power-saving remainder.

### 3. Exact averaged-diagonal formula

The paper separately computes the averaged atomic diagonal. It does
not identify this diagonal with the averaged squared synthesis: equal-
determinant cross terms remain. A signed vanishing average cannot be
squared and reinterpreted as a positive energy estimate.

### 4. Sharp transfer boundaries

- Weighted averaging leaves the exact support-only grouping norm equal
  to the largest realized fiber when numerator and diagonal use the
  same weights.
- The inherited TPC alias progression folds the full shift spectrum
  into `M_al` branches.
- Collision-free equality labels in the common zero-extended geometry
  are presently proved only up to
  `X^(29629/210000-epsilon)`.
- Resolving the first Poisson alias requires a dense shift window at
  least `X^(267/400+o(1))`, so these ranges do not overlap.
- Positivity alone pays the full effective number of shifts when an
  averaged quantity is localized back to one prescribed shift.

### 5. Exact next gate

The route now splits into four independently testable doors:

1. prove orbit-frequency regularity for an actual projected dual field;
2. obtain atomic normalization on one additional cofactor block;
3. prove anti-alias or maximal-in-shift control; or
4. construct actual-mask coefficients saturating one of the remaining
   frontiers, giving a sharp negative result for that route.

## Reproducibility

Prerequisites are Python 3, `pdflatex`, and `bibtex`. Run from this
manuscript directory.

Exact finite certificate:

```powershell
python experiments/tpc46_certificate.py
```

Expected output begins with:

```text
TPC-46 certificate: 122232 checks passed
```

Expected canonical payload SHA-256:

```text
38287f0cbee8060ebfb73407f6a4cd0255490e64effefea4481ee67ec1adb4ea
```

The certificate uses only the Python standard library. It verifies
finite algebraic identities, exact operator norms, squarefree residual
collision/Walsh identities, discrete spectral support and alias
analogues, the sharp localization spike, and the principal rational
exponent ledgers. It does not
certify asymptotic Fourier decay or Mobius cancellation.

Build the paper:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Files

- `main.tex` - manuscript entry point.
- `sections/` - coefficient interface, theorems, proofs, boundaries,
  literature audit, next gate, and claim ledger.
- `references.bib` - primary literature and stable TPC predecessors.
- `experiments/tpc46_certificate.py` - exact standard-library checker.
- `experiments/tpc46_certificate.json` - generated certificate report.
- `main.pdf` - compiled manuscript.

## Claim boundary

TPC-46 proves a deterministic shift-spectral theorem and exact tensor,
Bohr, Poisson, folding, and normalization results for their stated
models. It does **not** prove that the actual TPC dual output is orbit-
band-limited, a fixed-shift atomic Bessel bound, Chowla at a fixed
shift, a Hardy-Littlewood prime-pair asymptotic, a breach of the sieve
parity barrier, or the twin-prime conjecture.
