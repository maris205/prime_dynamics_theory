# TPC-51 — Canonical Mellin Quotient Frames

This directory contains the paper

> **Canonical Mellin Quotient Frames: Finite-Sampling Kernels, Interior Stability, and the Boundary of Signed TPC Reassembly**

The paper analyzes the next gap isolated by TPC-50. Its answer has a negative half, an abstract positive half, and an explicit unverified bridge to the actual provenance:

- A lower frame on **all arbitrary continuous signed Mellin densities is impossible** at every finite scale. The synthesis maps an infinite-dimensional coefficient space into a finite-dimensional physical space and has a nonzero smooth kernel. For finite phase samples the kernel is explicit.
- For one fixed scalar shape, exact Mellin inversion reconstructs its sampled values. A uniform coordinatewise condition bound requires the explicit hypothesis $\inf_n|W(x_n)|\geq\eta>0$; near-zero coordinates give a worst-direction obstruction.
- For a **fixed finite scalar shape family**, exact redundancies are removed by a quotient. Its condition number is bounded in terms of the least positive eigenvalue of a normalized sampled Gram matrix, with constants depending on the family and its normalizations.
- On the fixed-modulus prime–squarefree dyadic row universe, the logarithmic empirical measure converges to

  $$
  e^{x+y}\,dx\,dy,\qquad (x,y)\in[0,\log 2]^2.
  $$

  Fixed limiting-independent scalar families therefore have an $O(1)$ quotient condition number.
- A two-dimensional log-Fourier bank of degree $K\leq(\log X)^A$ has uniform sampled Riesz bounds. The literal TPC static mask changes the lower bound by only

  $$
  O\!\left(\varepsilon_X(2K+1)^2\right),
  $$

  which is $o(1)$ at the inherited endpoint.

These theorems give zero polynomial sampling-and-mask cost for the declared fixed scalar families and retained finite banks. They do **not** yet close the actual row-labelled, coefficientwise pre-terminal provenance gate. The genuine factors $W(mj/X)$ and $\Psi(dj/K)$ form an $X$-dependent Hilbert-valued orbit-translate family. TPC-51 proves that distinct nonzero compactly supported log translates are linearly independent, so this family cannot generically be replaced by a fixed-rank scalar family merely by relabelling.

The paper therefore states an explicit **Actual-provenance bridge criterion**. A future transfer must prove either a uniform normalized Gram for that Hilbert-valued family or a uniform relative Fourier-tail estimate, and must also compare the actual weighted continuous Mellin envelope with the resulting Hilbert energy. None of those bridge hypotheses is verified here. This bridge is the next open gate, before the coherent prime square, residual grouping, frozen-to-physical localization, native-Gram identification, and the nonlinear full TPC-48 projective profile. The paper proves no fixed-shift prime-pair estimate, parity breach, or twin-prime statement.

## Files

- `main.tex` — paper driver
- `sections/` — theorem, proof, endpoint, and certificate sections
- `references.bib` — bibliography
- `experiments/tpc51_certificate.py` — deterministic exact-rational regression certificate
- `experiments/tpc51_certificate_output.txt` — committed certificate output
- `canonical-mellin-quotient-frames.pdf` — release PDF

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
python experiments/tpc51_certificate.py --output experiments/tpc51_certificate_output.txt
```

The current certificate performs **18,498 exact assertions** using only the Python standard library.

- normalized source SHA-256: `6c8fac5abc221e00bd885ac59159b08d3a644a39426ff23910a883172d86c78c`
- semantic SHA-256: `c64511069ce4e590eec2ac973663446bb3a8f6e16f93543daaf5e2334979a332`
- certificate-core SHA-256: `c0be9331cddaec485b3ec560e0368cee89c30f0df3bf42b384c3dd427c09cfe8`

The certificate checks finite algebraic identities and perturbation bounds. It does not certify prime asymptotics or any parity-sensitive conclusion.

## Dependency position

```text
TPC-50: fixed canonical cells survive the static mask
    |
    v
TPC-51: continuous lower-frame no-go
        + fixed scalar-family quotient Gram stability
        + prime-squarefree sampled log-frame
        + O(epsilon_X K^2) literal-mask perturbation
        + translate-independence obstruction
    |
    v
Next open gate: actual Hilbert-valued orbit-translate provenance bridge
    |
    v
Later gate: coherent-prime square on the retained labels
```
