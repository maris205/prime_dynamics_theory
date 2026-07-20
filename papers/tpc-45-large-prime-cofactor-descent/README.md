# TPC-45: Large-prime cofactor descent

> **Large-Prime Cofactor Descent for a Four-Möbius Walsh Energy**

TPC-45 returns from the abstract Walsh corner of TPC-43/44 to the
actual equality coefficients

```text
u_(alpha,j) = d_alpha (ell_alpha d_alpha j + h).
```

The paper proves a genuine partial physical de-randomization, together
with the exact boundary of the method. It does not claim a parity
breakthrough, a prime-pair asymptotic, or a twin-prime theorem.

## Main unconditional results

### 1. Exact global large-prime descent

For

```text
P_R = {p prime : sqrt(N_+) < p <= N_-/R},
```

every occurrence `n = p r` has `r >= R`, the prime `p` is unique, and

```text
u = p (d r),
mu(u) = -mu(d r).
```

Thus every sign in `P_R` can be set globally to its physical value
`-1`, while the label descends exactly from `u` to `d r`.

### 2. Sharp fiber compression

At a fixed Hilbert coordinate, equal descended labels have multiplicity

```text
rho_R <= X^o(1) (1 + L_0/R)
      = X^((lambda_L-theta)_+ + o(1)),
lambda_L = 99979/210000,
R = X^(theta+o(1)).
```

The squared operator norm of the grouping map is exactly the maximal
fiber size. This proves both the positive compression theorem and the
sharp support-only boundary.

### 3. Band/cutoff tradeoff

After the physical band is frozen, every prime sign below
`z=(log X)^A` may still be overwritten simultaneously for a
density-one set of the remaining environments whenever

```text
(lambda_L-theta)_+
  + (62549/52500)(1-1/A) < 1/400.
```

Two explicit points are proved:

- Keeping the TPC-44 cutoff `A=501/500` and taking
  `R=ell_+ X^(-1/10000)` freezes the whole band through exponent
  `55021/105000 = 0.5240095238...`. The exact unused margin is
  `577/26302500 > 0`.
- Taking `A=1001/1000` and `R=ell_+ X^(-1/1000)` reaches band exponent
  `110231/210000 = 0.5249095238...`.

For the touched component alone, the residual label exponent drops to

```text
lambda_1 = 36299/52500,
```

which permits the stronger cutoff `(log X)^(1003/1000)`. This stronger
cutoff is not asserted for the full packet.

### 4. Very-high-prime affine collapse

At `y=X^(267/400+eta)`, every label has at most one prime above `y`,
and fixed `(j,p)` meets at most one source row in each source system.
Two different exact Gram forms result:

```text
Z_0(-1_(<=y), epsilon_(>y))
  = ||v_0 + sum_(p>y) epsilon_p v_p||^2,
```

and, after averaging the lower signs,

```text
E_(<=y) Z_0(epsilon_(<=y), -1_(>y))
  = D_0 - D_H + ||sum_(p>y) x_p||^2.
```

The first retains all output-coordinate cross terms; the second retains
only exact residual-label matches. Their norms agree prime by prime,
but their cross inner products are generally different.

### 5. Exact remaining arithmetic gate

The residual collisions lie on the fixed-determinant ladders

```text
r p - d j ell = h,
p   = p_0   + (d j/g)t,
ell = ell_0 + (r/g)t,
g = gcd(r,dj) | h.
```

When `r << L_0`, the ambient fiber has size
`X^o(1)(1+L_0/r)`. All atoms in one residual fiber have the same
physical Möbius sign, so cancellation must come from the actual complex
source/mask coefficients or from different residual labels.

The cited Bettin–Chandee fixed-determinant corollary permits two
arbitrary arithmetic coefficient slots; this packet has three nonsmooth slots.
That is the paper's precise “third-coefficient barrier.” The cited 2026
Dong–Robles–Zeindler preprint is explicitly recorded as withdrawn; its
announced improved bound is not used.

## Reproducibility

Prerequisites are Python 3, `pdflatex`, and `bibtex`.  Run the commands
below from this manuscript directory.  The certificate uses only the
Python standard library.

Run the exact finite certificate:

```powershell
python experiments/tpc45_certificate.py
```

Expected stdout begins with
`TPC-45 certificate: 32894 exact checks passed`.  The expected canonical
JSON payload SHA-256 is
`e9c3bdf309863cf560fd31e5253e1429236281069101df26c7fe689d6faa438e`.

Archival status: July 2026 repository preprint; no external DOI or
arXiv identifier has yet been assigned to this version.

The current certificate performs 32,894 exact checks and writes
`experiments/tpc45_certificate.json`. It verifies finite character
descent, grouped energies, affine and low-averaged Gram identities,
determinant ladders, sharp finite fiber norms, and all rational exponent
ledgers. It does not test asymptotic Möbius cancellation.

Build the paper with:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Files

- `main.tex` — manuscript entry point.
- `sections/` — theorem, proof, boundary, and literature sections.
- `references.bib` — bibliography, including current withdrawal status.
- `experiments/tpc45_certificate.py` — standard-library exact checker.
- `experiments/tpc45_certificate.json` — generated certificate report.
- `main.pdf` — compiled manuscript.

## Claim boundary

The paper proves exact descent, a polynomial-width physical prime-band
freezing theorem, a quantitative band/cutoff frontier, and exact Gram
normal forms. It does **not** prove the remaining fixed-determinant
Bessel estimate, the complete deterministic TPC equality bound, Chowla
at a fixed shift, Hardy–Littlewood for prime pairs, a breach of the
sieve parity barrier, or the twin-prime conjecture.
