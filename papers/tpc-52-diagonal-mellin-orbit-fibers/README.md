# TPC-52 — Diagonal Mellin Reassembly on Actual Orbit Fibers

This directory contains the paper

> **Diagonal Mellin Reassembly on Actual Orbit Fibers: Scalar Saturation, Profile Overlap, and an Interior TPC Bridge**

TPC-51 isolated a gap between stable fixed scalar Mellin families and the actual growing row-dependent orbit-translate family. TPC-52 gives a conditional interior bridge by separating two operators that had been conflated and by isolating the remaining actual-profile dictionary as an explicit checkable hypothesis.

- If the orbit label is forgotten, nearby normalized scalar translates have a Gram eigenvalue

  $$
  \lambda_{\min}\ll_r J^{-2r}.
  $$

  On a translate-independent interior window, preserving the energy of every vector in the exact span requires rank of order $J$; a fixed or polylogarithmic scalar bank cannot do this.

- The physical coefficientwise space retains $(m,r,j,\gamma)$ as orthogonal labels. For the provenance-fixed direction, a $q$-factor diagonal Mellin identity gives

  $$
  \frac{\mathcal E_B(\mathbf W;c)^2}
       {\|\mathcal S_{\mathbf W}c\|_2^2}
  =\frac{A_B(\mathbf W)^2}{\Theta(\mathbf W;c)}.
  $$

  Thus the scale-dependent condition number is exactly the reciprocal of a nonnegative physical profile-overlap ratio; no lower frame for arbitrary signed Mellin densities is needed.

- On a compact **uniformly active** direct cell, the new explicit hypothesis

  $$
  \rho_*=\inf_{\beta}
  \frac{\int |F_\beta|^2 e^{x+y}\,dx\,dy\,dt}
       {\int |B_\beta|^2 e^{x+y}\,dx\,dy\,dt}>0
  $$

  together with the exact coordinatewise actual-profile dictionary, one complete nondegenerate row cell, prime–squarefree row sampling, orbit Riemann sampling, and literal-mask deletion gives $\Theta_X^{\rm act}\ge \rho_*/2$. Consequently the declared coefficientwise pre-terminal direction has $O(1)$ canonical condition number, uniformly under arbitrary source concentration and arbitrary finite retained cofactor support. The paper does not verify the dictionary or uniform overlap for every inherited packet.

- A tensor row-log cosine bank has total approximation-and-calibration ledger

  $$
  O\!\left(K_{\rm F}^{-2}+\Delta_X^{\rm mom}K_{\rm F}^{C_0}
  +\epsilon_X(K_{\rm F}+1)^2\right),
  \qquad
  \Delta_X^{\rm mom}=e^{-c\sqrt{\log L}}+D^{-1/2+\delta}.
  $$

  For $K_{\rm F}=(\log X)^A$ this is $o(1)$ under the stated endpoint hypotheses. The actual-field normalization is proved under the same exact-dictionary and nondegeneracy hypotheses, and the projection leaves the full orbit fiber untouched.

- The overlap assumption is sharp. Two fixed flat bumps with scaled supports approaching a common endpoint make $\Theta_X^{\rm act}$ smaller than every power of $X$; on a sufficiently fine grazing sequence the sampled physical output is exactly zero while the carrier envelope is positive.

This is a conditional L1 coefficient-interface result on a declared exact-dictionary, complete-row, uniformly active packet. It does **not** verify those conditions for every inherited packet or control coherent prime summation, grouping by $s=d(m)r$, localization from frozen shifts to $h_0$, the native physical Gram, the full signed TPC-48 profile, or any fixed-shift prime-pair correlation. It proves no parity-barrier breach and no twin-prime statement.

## Files

- `main.tex` — paper driver
- `sections/` — theorem, proof, endpoint, and certificate sections
- `references.bib` — bibliography
- `experiments/tpc52_certificate.py` — deterministic exact-rational regression certificate
- `experiments/tpc52_certificate_output.txt` — committed certificate output
- `diagonal-mellin-orbit-fibers.pdf` — release PDF

## Build

From this directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Exact certificate

Run:

```powershell
python experiments/tpc52_certificate.py --output experiments/tpc52_certificate_output.txt
```

The current certificate performs **4,372 exact assertions** using only the Python standard library.

- normalized source SHA-256: `3d6244dd53736436539c4842b732731919539164d001d1f41e8f886d80702ee4`
- semantic SHA-256: `0fc0c178543beddd5ba86120d235fd28cd135ffdd84893cdda12cd296ca54bf9`
- certificate-core SHA-256: `2e136caf81b9ce92f8dccd55d834c78cf4eeedc5c559d283f483e5d333177065`

The certificate checks finite algebraic identities. It does not certify the exact actual-profile dictionary, prime asymptotics, profile nondegeneracy, coherent prime cancellation, or any parity-sensitive conclusion.

## Dependency position

```text
TPC-50: fixed direct cells survive the literal static mask
    |
    v
TPC-51: fixed-family quotient frames + sampled row-log banks
        + actual growing translate family identified as the next gap
    |
    v
TPC-52: conditional coefficientwise diagonal Mellin bridge
        on exact-dictionary, uniformly active retained-label orbit fibers
        + sharp grazing obstruction
    |
    v
Next open gate: coherent-prime lower square on the retained labels
```
